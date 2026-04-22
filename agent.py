import json
import logging
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from time import sleep
from typing import Any, Callable

import httpx
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape

from common import StepResult
from ghl import GHLClient
from telegram_bot import TelegramNotifier

load_dotenv()

LOGGER = logging.getLogger("roberts_sdr.agent")
LOGGER.setLevel(logging.INFO)

ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "logs"
LOG_PATH = LOG_DIR / "pipeline.jsonl"
EMAIL_DISPATCH_LOG_PATH = LOG_DIR / "email_dispatch.jsonl"
PROMPT_PATH = ROOT / "prompts" / "sdr_system.txt"
EMAIL_TEMPLATE_DIR = ROOT / "email_templates"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514").strip() or "claude-sonnet-4-20250514"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
DRY_RUN = os.getenv("DRY_RUN", "false").strip().lower() in {"1", "true", "yes", "on"}
DAILY_EMAIL_LIMIT = int(os.getenv("DAILY_EMAIL_LIMIT", "100") or "100")
PROSPECT_EMAIL_SUBJECT = (
    os.getenv("PROSPECT_EMAIL_SUBJECT", "Planning outdoor improvements this season?")
    .strip()
    or "Planning outdoor improvements this season?"
)
ROBERTS_FROM_EMAIL = os.getenv("ROBERTS_FROM_EMAIL", "contact@roberts-landscape.com")
ROBERTS_REPLY_TO_EMAIL = os.getenv("ROBERTS_REPLY_TO_EMAIL", ROBERTS_FROM_EMAIL).strip() or ROBERTS_FROM_EMAIL
ROBERTS_CTA_URL = os.getenv(
    "ROBERTS_CTA_URL",
    "https://robertslandscapecod.com/contact",
)
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY", "").strip()
COMPOSIO_BASE_URL = os.getenv("COMPOSIO_BASE_URL", "https://backend.composio.dev/api/v3")
COMPOSIO_ENTITY_ID = os.getenv("COMPOSIO_ENTITY_ID", "default").strip() or "default"
COMPOSIO_GMAIL_ACCOUNT = os.getenv("COMPOSIO_GMAIL_ACCOUNT", "").strip()
COMPOSIO_GCAL_ACCOUNT = os.getenv("COMPOSIO_GCAL_ACCOUNT", "").strip()
COMPOSIO_NOTION_ACCOUNT = os.getenv("COMPOSIO_NOTION_ACCOUNT", "").strip()
COMPOSIO_NOTION_DATABASE_ID = os.getenv("COMPOSIO_NOTION_DATABASE_ID", "").strip()

jinja = Environment(
    loader=FileSystemLoader(EMAIL_TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


def _read_prompt() -> str:
    try:
        return PROMPT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _mask_email(email: str) -> str:
    if "@" not in email:
        return email
    local, domain = email.split("@", 1)
    prefix = local[:1] if local else "*"
    return f"{prefix}***@{domain}"


def _ensure_log_dir() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def _log_pipeline(payload: dict[str, Any]) -> None:
    _ensure_log_dir()
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _normalize_email(email: str | None) -> str:
    return (email or "").strip().lower()


def _iter_email_dispatch_records() -> list[dict[str, Any]]:
    if not EMAIL_DISPATCH_LOG_PATH.exists():
        return []
    records: list[dict[str, Any]] = []
    for line in EMAIL_DISPATCH_LOG_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def _emails_sent_today(now: datetime) -> int:
    target_date = now.date().isoformat()
    return sum(
        1
        for record in _iter_email_dispatch_records()
        if record.get("status") == "success" and str(record.get("sent_at", "")).startswith(target_date)
    )


def _email_already_sent(email: str) -> bool:
    normalized_email = _normalize_email(email)
    return any(
        record.get("status") == "success" and _normalize_email(record.get("recipient_email")) == normalized_email
        for record in _iter_email_dispatch_records()
    )


def _record_email_dispatch(
    recipient_email: str,
    status: str,
    detail: str,
    lead: dict[str, Any],
) -> None:
    _ensure_log_dir()
    payload = {
        "sent_at": datetime.now(UTC).isoformat(),
        "recipient_email": _normalize_email(recipient_email),
        "status": status,
        "detail": detail,
        "lead_name": " ".join(filter(None, [lead.get("first_name"), lead.get("last_name")])),
        "source": lead.get("source"),
    }
    with EMAIL_DISPATCH_LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _parse_budget_amount(budget: str | None) -> float | None:
    if not budget:
        return None
    normalized = "".join(char for char in budget if char.isdigit() or char == ".")
    if not normalized:
        return None
    try:
        return float(normalized)
    except ValueError:
        return None


def _budget_score(budget: str | None) -> int:
    if not budget:
        return 5
    digits = "".join(char for char in budget if char.isdigit())
    if not digits:
        return 5
    amount = int(digits)
    if amount >= 50000:
        return 9
    if amount >= 30000:
        return 8
    if amount >= 15000:
        return 7
    if amount >= 8000:
        return 6
    return 5


def _interest_score(interest: str | None) -> int:
    if not interest:
        return 5
    normalized = interest.lower()
    premium_keywords = ("outdoor kitchen", "patio", "hardscape", "design-build")
    mid_keywords = ("landscape", "lighting", "stone", "walkway", "fire pit")
    if any(keyword in normalized for keyword in premium_keywords):
        return 9
    if any(keyword in normalized for keyword in mid_keywords):
        return 7
    return 6


def _default_analysis(lead: dict[str, Any]) -> dict[str, Any]:
    heuristic_score = round((_budget_score(lead.get("budget")) + _interest_score(lead.get("interest"))) / 2)
    summary = (
        f"{lead.get('first_name', 'Lead')} is interested in "
        f"{lead.get('interest') or 'landscaping services'}"
    )
    priority = "high" if heuristic_score >= 8 else "medium" if heuristic_score >= 6 else "low"
    notes = [
        "Prioritize a warm first response under 10 minutes.",
        "Reference Cape Cod outdoor living and consultation availability.",
    ]
    return {
        "score": heuristic_score,
        "priority": priority,
        "summary": summary,
        "notes": notes,
        "recommended_next_step": "Send a warm intro email and invite the lead to schedule a consultation.",
        "source": "heuristic",
    }


def _strip_json_fence(raw_content: str) -> str:
    content = raw_content.strip()
    if content.startswith("```"):
        lines = content.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return content


def _normalize_analysis(parsed: dict[str, Any], fallback: dict[str, Any], source: str) -> dict[str, Any]:
    score = parsed.get("score", fallback["score"])
    try:
        normalized_score = max(1, min(10, int(score)))
    except (TypeError, ValueError):
        normalized_score = fallback["score"]

    priority = str(parsed.get("priority") or fallback["priority"]).lower()
    if priority not in {"low", "medium", "high"}:
        priority = "high" if normalized_score >= 8 else "medium" if normalized_score >= 6 else "low"

    notes = parsed.get("notes", fallback["notes"])
    if isinstance(notes, str):
        notes = [notes]
    elif isinstance(notes, list):
        notes = [str(note) for note in notes if str(note).strip()]
    else:
        notes = fallback["notes"]

    return {
        "score": normalized_score,
        "priority": priority,
        "summary": str(parsed.get("summary") or fallback["summary"]),
        "notes": notes or fallback["notes"],
        "recommended_next_step": str(parsed.get("recommended_next_step") or fallback["recommended_next_step"]),
        "source": source,
    }


def _analyze_with_anthropic(lead: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    from anthropic import Anthropic

    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=600,
        temperature=0.2,
        system=_read_prompt() or "Analyze the lead and return JSON.",
        messages=[
            {
                "role": "user",
                "content": (
                    "Return valid JSON only.\n"
                    f"Lead payload:\n{json.dumps(lead)}"
                ),
            }
        ],
    )
    raw_content = "\n".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    )
    parsed = json.loads(_strip_json_fence(raw_content or "{}"))
    return _normalize_analysis(parsed=parsed, fallback=fallback, source="anthropic")


def _analyze_with_deepseek(lead: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    from openai import OpenAI

    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": _read_prompt() or "Analyze the lead and return JSON."},
            {"role": "user", "content": json.dumps(lead)},
        ],
    )
    raw_content = response.choices[0].message.content or "{}"
    parsed = json.loads(raw_content)
    return _normalize_analysis(parsed=parsed, fallback=fallback, source="deepseek")


def analyze_lead(lead: dict[str, Any]) -> dict[str, Any]:
    fallback = _default_analysis(lead)

    if ANTHROPIC_API_KEY:
        try:
            return _analyze_with_anthropic(lead=lead, fallback=fallback)
        except Exception as exc:  # pragma: no cover - external dependency path
            LOGGER.warning("Anthropic analysis failed: %s", exc)

    if DEEPSEEK_API_KEY:
        try:
            return _analyze_with_deepseek(lead=lead, fallback=fallback)
        except Exception as exc:  # pragma: no cover - external dependency path
            LOGGER.warning("DeepSeek analysis failed: %s", exc)

    if ANTHROPIC_API_KEY or DEEPSEEK_API_KEY:
        fallback["notes"] = fallback["notes"] + ["AI enrichment failed; heuristic score used."]
        fallback["source"] = "heuristic-fallback"

    return fallback


def render_email_template(lead: dict[str, Any], analysis: dict[str, Any]) -> str:
    template = jinja.get_template("welcome.html")
    return template.render(
        first_name=lead.get("first_name") or "there",
        interest=lead.get("interest") or "your outdoor project",
        message=lead.get("message"),
        phone=lead.get("phone"),
        reply_email=ROBERTS_REPLY_TO_EMAIL,
        sender_email=ROBERTS_FROM_EMAIL,
        score=analysis.get("score"),
        cta_url=ROBERTS_CTA_URL,
        submitted_at=datetime.now(UTC).strftime("%B %d, %Y"),
    )


def render_prospecting_template(contact: dict[str, Any]) -> str:
    template = jinja.get_template("prospecting.html")
    return template.render(
        first_name=contact.get("first_name") or "there",
        phone=contact.get("phone"),
        reply_email=ROBERTS_REPLY_TO_EMAIL,
        sender_email=ROBERTS_FROM_EMAIL,
        cta_url=ROBERTS_CTA_URL,
    )


def _retry_step(step_name: str, callback: Callable[[], StepResult], attempts: int = 3) -> StepResult:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return callback()
        except Exception as exc:  # pragma: no cover - retry wrapper
            last_error = exc
            sleep(2 ** (attempt - 1))
    return StepResult(step=step_name, status="failed", detail=str(last_error or "Unknown error"))


def _dry_run_step(step: str, detail: str) -> StepResult:
    return StepResult(step=step, status="skipped", detail=f"DRY_RUN enabled; {detail}")


def _should_halt_outreach(email_step: StepResult) -> bool:
    if email_step.status != "skipped":
        return False
    detail = email_step.detail.lower()
    return "duplicate outreach prevented" in detail or "daily email limit reached" in detail


def _execute_composio_tool(
    step: str,
    tool_slug: str,
    connected_account_id: str | None,
    arguments: dict[str, Any],
) -> StepResult:
    if DRY_RUN:
        return _dry_run_step(step=step, detail=f"{tool_slug} was not executed")
    if not COMPOSIO_API_KEY:
        return StepResult(step=step, status="skipped", detail="COMPOSIO_API_KEY is not configured")
    if not connected_account_id:
        return StepResult(step=step, status="skipped", detail=f"{step} connected account is not configured")

    payload = {
        "connected_account_id": connected_account_id,
        "entity_id": COMPOSIO_ENTITY_ID,
        "arguments": arguments,
    }
    headers = {
        "x-api-key": COMPOSIO_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        with httpx.Client(timeout=45.0) as client:
            response = client.post(
                f"{COMPOSIO_BASE_URL}/tools/execute/{tool_slug}",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
    except Exception as exc:  # pragma: no cover - external dependency path
        return StepResult(step=step, status="failed", detail=str(exc))

    if not data.get("successful", False):
        return StepResult(
            step=step,
            status="failed",
            detail=str(data.get("error") or "Composio execution failed"),
            data=data,
        )

    return StepResult(step=step, status="success", detail=f"{tool_slug} executed", data=data.get("data") or data)


def _send_gmail_message(
    lead: dict[str, Any],
    subject: str,
    html_body: str,
    step_name: str = "gmail_send_email",
    apply_local_guards: bool = True,
) -> StepResult:
    recipient_email = _normalize_email(lead.get("email"))
    if not recipient_email:
        return StepResult(step=step_name, status="skipped", detail="Lead email is not configured")

    now = datetime.now(UTC)
    if apply_local_guards and _email_already_sent(recipient_email):
        detail = "Email already sent to this contact; duplicate outreach prevented"
        _record_email_dispatch(recipient_email=recipient_email, status="skipped_duplicate", detail=detail, lead=lead)
        return StepResult(step=step_name, status="skipped", detail=detail)

    sent_today = _emails_sent_today(now)
    if apply_local_guards and sent_today >= DAILY_EMAIL_LIMIT:
        detail = f"Daily email limit reached ({DAILY_EMAIL_LIMIT})"
        _record_email_dispatch(recipient_email=recipient_email, status="skipped_limit", detail=detail, lead=lead)
        return StepResult(step=step_name, status="skipped", detail=detail)

    arguments = {
        "recipient_email": recipient_email,
        "subject": subject,
        "body": html_body,
        "is_html": True,
        "user_id": "me",
    }
    result = _execute_composio_tool(
        step=step_name,
        tool_slug="GMAIL_SEND_EMAIL",
        connected_account_id=COMPOSIO_GMAIL_ACCOUNT,
        arguments=arguments,
    )
    _record_email_dispatch(recipient_email=recipient_email, status=result.status, detail=result.detail, lead=lead)
    return result


def _send_email(lead: dict[str, Any], analysis: dict[str, Any]) -> StepResult:
    html_body = render_email_template(lead, analysis)
    subject = f"Welcome to Roberts Landscape, {lead.get('first_name', 'there')}! Let's Build Something Beautiful"
    return _send_gmail_message(lead=lead, subject=subject, html_body=html_body, step_name="gmail_send_email")


def send_prospecting_email(contact: dict[str, Any], apply_local_guards: bool = True) -> StepResult:
    html_body = render_prospecting_template(contact)
    return _send_gmail_message(
        lead=contact,
        subject=PROSPECT_EMAIL_SUBJECT,
        html_body=html_body,
        step_name="gmail_send_prospecting_email",
        apply_local_guards=apply_local_guards,
    )


def _schedule_follow_up(lead: dict[str, Any], analysis: dict[str, Any]) -> StepResult:
    if DRY_RUN:
        return _dry_run_step(step="googlecalendar_create_event", detail="GOOGLECALENDAR_CREATE_EVENT was not executed")
    if not COMPOSIO_API_KEY:
        return StepResult(step="googlecalendar_create_event", status="skipped", detail="COMPOSIO_API_KEY is not configured")

    from composio import ComposioToolSet, Action

    start = datetime.now(UTC) + timedelta(hours=24)
    try:
        ts = ComposioToolSet(api_key=COMPOSIO_API_KEY, entity_id=COMPOSIO_ENTITY_ID)
        result = ts.execute_action(
            action=Action.GOOGLECALENDAR_CREATE_EVENT,
            params={
                "summary": f"Follow-up - {lead.get('first_name', 'Lead')} | {lead.get('interest') or 'Landscape Inquiry'}",
                "description": json.dumps(
                    {
                        "lead": lead,
                        "analysis": analysis,
                        "checklist": [
                            "Confirm project scope",
                            "Confirm timeline and budget",
                            "Invite to schedule a consultation",
                        ],
                    }
                ),
                "start_datetime": start.strftime("%Y-%m-%dT%H:%M:%S"),
                "event_duration_minutes": 30,
                "calendar_id": "primary",
                "timezone": "America/New_York",
            },
            entity_id=COMPOSIO_ENTITY_ID,
        )
    except Exception as exc:
        return StepResult(step="googlecalendar_create_event", status="failed", detail=str(exc))

    if not result.get("successful"):
        return StepResult(
            step="googlecalendar_create_event",
            status="failed",
            detail=str(result.get("error") or "Composio GCal execution failed"),
            data=result,
        )
    return StepResult(
        step="googlecalendar_create_event",
        status="success",
        detail="GOOGLECALENDAR_CREATE_EVENT executed",
        data=result.get("data") or result,
    )


def _build_notion_properties(lead: dict[str, Any], analysis: dict[str, Any]) -> list[dict[str, str]]:
    full_name = " ".join(filter(None, [lead.get("first_name"), lead.get("last_name")])) or "Unknown Lead"
    source = lead.get("source")
    budget_amount = _parse_budget_amount(lead.get("budget"))
    properties: list[dict[str, str]] = [
        {"name": "Nome do Cliente", "type": "title", "value": full_name},
        {"name": "Data de Entrada", "type": "date", "value": datetime.now(UTC).isoformat()},
        {"name": "Status", "type": "status", "value": "Novo"},
        {
            "name": "Nível de Interesse",
            "type": "select",
            "value": "Alto" if analysis.get("priority") == "high" else "Médio" if analysis.get("priority") == "medium" else "Baixo",
        },
    ]

    if lead.get("email"):
        properties.append({"name": "E-mail", "type": "email", "value": str(lead["email"])})
    if lead.get("phone"):
        properties.append({"name": "Telefone", "type": "phone_number", "value": str(lead["phone"])})
    if lead.get("interest"):
        properties.append({"name": "Serviço de Interesse", "type": "rich_text", "value": str(lead["interest"])})
    if budget_amount is not None:
        properties.append({"name": "Valor Estimado ($)", "type": "number", "value": str(budget_amount)})
    if lead.get("budget"):
        properties.append({"name": "Descrição do Orçamento", "type": "rich_text", "value": str(lead["budget"])})
    if source in {"Google Ads", "sms-leads"}:
        properties.append({"name": "Fonte de Contato", "type": "select", "value": str(source)})

    internal_notes = [
        analysis.get("summary") or "",
        lead.get("message") or "",
        f"Score: {analysis.get('score', 'n/a')}/10",
    ]
    properties.append(
        {
            "name": "Observações Internas",
            "type": "rich_text",
            "value": " | ".join(part for part in internal_notes if part)[:1900],
        }
    )
    return properties


def _create_notion_record(lead: dict[str, Any], analysis: dict[str, Any]) -> StepResult:
    if not COMPOSIO_NOTION_DATABASE_ID:
        return StepResult(step="notion_create_page", status="skipped", detail="COMPOSIO_NOTION_DATABASE_ID is not configured")

    arguments = {
        "database_id": COMPOSIO_NOTION_DATABASE_ID,
        "properties": _build_notion_properties(lead, analysis),
    }
    return _execute_composio_tool(
        step="notion_create_page",
        tool_slug="NOTION_INSERT_ROW_DATABASE",
        connected_account_id=COMPOSIO_NOTION_ACCOUNT,
        arguments=arguments,
    )


def _sync_ghl(lead: dict[str, Any], analysis: dict[str, Any]) -> list[StepResult]:
    if DRY_RUN:
        return [StepResult(step="ghl_sync", status="skipped", detail="DRY_RUN enabled; GoHighLevel sync was not executed")]

    client = GHLClient.from_env()
    if not client.is_configured:
        return [StepResult(step="ghl_sync", status="skipped", detail="GHL credentials are not configured")]

    contact_result = client.create_contact(lead, analysis)
    opportunity_result = client.create_opportunity(lead, analysis, contact_result.data or {})
    return [contact_result, opportunity_result]


def run_pipeline(lead: dict[str, Any]) -> dict[str, Any]:
    received_at = datetime.now(UTC).isoformat()
    analysis = analyze_lead(lead)
    step_results: list[StepResult] = []

    email_step = _retry_step("gmail_send_email", lambda: _send_email(lead, analysis))
    step_results.append(email_step)

    if _should_halt_outreach(email_step):
        halt_detail = f"Outbound workflow halted: {email_step.detail}"
        step_results.append(StepResult(step="googlecalendar_create_event", status="skipped", detail=halt_detail))
        step_results.append(StepResult(step="notion_create_page", status="skipped", detail=halt_detail))
        step_results.append(StepResult(step="ghl_sync", status="skipped", detail=halt_detail))
        step_results.append(StepResult(step="telegram_notify", status="skipped", detail=halt_detail))
    else:
        step_results.append(_retry_step("googlecalendar_create_event", lambda: _schedule_follow_up(lead, analysis)))
        step_results.append(_retry_step("notion_create_page", lambda: _create_notion_record(lead, analysis)))
        step_results.extend(_sync_ghl(lead, analysis))

        if DRY_RUN:
            step_results.append(_dry_run_step(step="telegram_notify", detail="Telegram notification was not sent"))
        else:
            notifier = TelegramNotifier.from_env()
            step_results.append(notifier.send_lead_notification(lead=lead, analysis=analysis, steps=step_results))

    payload = {
        "timestamp": received_at,
        "dry_run": DRY_RUN,
        "lead": {
            "name": " ".join(filter(None, [lead.get("first_name"), lead.get("last_name")])),
            "email": _mask_email(str(lead.get("email", ""))),
            "interest": lead.get("interest"),
            "source": lead.get("source"),
        },
        "analysis": analysis,
        "steps": [step.as_dict() for step in step_results],
    }
    _log_pipeline(payload)
    return payload


if __name__ == "__main__":  # pragma: no cover - manual smoke path
    sample_lead = {
        "first_name": "John",
        "last_name": "Mitchell",
        "email": "john@example.com",
        "phone": "(508) 555-0123",
        "interest": "Patio & Outdoor Kitchen",
        "message": "Looking for a premium backyard renovation.",
        "source": "Google Ads",
        "budget": "$45,000",
    }
    print(json.dumps(run_pipeline(sample_lead), indent=2))

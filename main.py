import os
import threading
import time
from hashlib import sha256
from hmac import compare_digest
from typing import Any

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from agent import run_pipeline
from telegram_bot import start_bot

load_dotenv()

APP_STARTED_AT = time.time()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").strip()
PORT = int(os.getenv("PORT", "8000"))
DRY_RUN = os.getenv("DRY_RUN", "false").strip().lower() in {"1", "true", "yes", "on"}

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Roberts Landscape SDR Agent", version="0.1.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class Lead(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True, str_strip_whitespace=True)

    first_name: str = Field(min_length=1)
    last_name: str | None = None
    email: str = Field(min_length=3)
    phone: str | None = None
    interest: str | None = None
    message: str | None = None
    source: str | None = None
    budget: str | None = None
    company: str | None = None


def _split_name(full_name: str | None) -> tuple[str, str | None]:
    if not full_name:
        return "Lead", None
    parts = [part for part in full_name.strip().split(" ") if part]
    if not parts:
        return "Lead", None
    if len(parts) == 1:
        return parts[0], None
    return parts[0], " ".join(parts[1:])


def _normalize_payload(payload: dict[str, Any]) -> Lead:
    first_name = payload.get("first_name") or payload.get("firstName")
    last_name = payload.get("last_name") or payload.get("lastName")

    if not first_name:
        first_name, inferred_last_name = _split_name(
            payload.get("full_name")
            or payload.get("fullName")
            or payload.get("name")
            or payload.get("contact_name")
        )
        last_name = last_name or inferred_last_name

    custom_data = payload.get("customData") if isinstance(payload.get("customData"), dict) else {}
    email = payload.get("email") or payload.get("contact_email") or payload.get("Email")
    phone = payload.get("phone") or payload.get("contact_phone") or payload.get("Phone")
    interest = (
        payload.get("interest")
        or payload.get("service")
        or payload.get("service_interest")
        or custom_data.get("interest")
    )
    source = payload.get("source") or payload.get("lead_source") or payload.get("utm_source")
    budget = payload.get("budget") or payload.get("estimated_budget") or custom_data.get("budget")
    message = payload.get("message") or payload.get("notes") or payload.get("description")
    normalized_keys = {
        "first_name",
        "firstName",
        "last_name",
        "lastName",
        "full_name",
        "fullName",
        "name",
        "contact_name",
        "email",
        "contact_email",
        "Email",
        "phone",
        "contact_phone",
        "Phone",
        "interest",
        "service",
        "service_interest",
        "source",
        "lead_source",
        "utm_source",
        "budget",
        "estimated_budget",
        "message",
        "notes",
        "description",
        "company",
        "customData",
    }
    extra_payload = {key: value for key, value in payload.items() if key not in normalized_keys}

    return Lead(
        first_name=first_name or "Lead",
        last_name=last_name,
        email=email or "",
        phone=phone,
        interest=interest,
        message=message,
        source=source,
        budget=budget,
        company=payload.get("company"),
        **extra_payload,
    )


def _validate_signature(signature: str | None, query_secret: str | None, raw_body: bytes) -> bool:
    if not WEBHOOK_SECRET:
        return True
    if query_secret and compare_digest(query_secret.strip(), WEBHOOK_SECRET):
        return True
    if not signature:
        return False

    normalized = signature.strip()
    if compare_digest(normalized, WEBHOOK_SECRET):
        return True

    digest = sha256(raw_body + WEBHOOK_SECRET.encode("utf-8")).hexdigest()
    return compare_digest(normalized, digest)


@app.on_event("startup")
async def startup_event() -> None:
    thread = threading.Thread(target=start_bot, daemon=True, name="telegram-bot")
    thread.start()


@app.get("/health")
async def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "roberts-sdr-agent",
        "uptime_seconds": round(time.time() - APP_STARTED_AT, 2),
        "port": PORT,
        "dry_run": DRY_RUN,
    }


@app.post("/webhook/lead")
@limiter.limit("20/minute")
async def receive_lead(request: Request, background_tasks: BackgroundTasks) -> dict[str, Any]:
    raw_body = await request.body()
    signature = request.headers.get("X-GHL-Signature")
    query_secret = request.query_params.get("secret")

    if not _validate_signature(signature, query_secret, raw_body):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    payload = await request.json()
    lead = _normalize_payload(payload)
    background_tasks.add_task(run_pipeline, lead.model_dump(mode="json"))

    return {
        "accepted": True,
        "email": lead.email,
        "first_name": lead.first_name,
    }

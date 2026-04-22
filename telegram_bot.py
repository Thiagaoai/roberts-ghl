import asyncio
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from common import StepResult

load_dotenv()

ROOT = Path(__file__).resolve().parent
LOG_PATH = ROOT / "logs" / "pipeline.jsonl"


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str) -> None:
        self.token = token
        self.chat_id = chat_id

    @property
    def is_configured(self) -> bool:
        return bool(self.token and self.chat_id)

    @classmethod
    def from_env(cls) -> "TelegramNotifier":
        return cls(
            token=os.getenv("TELEGRAM_BOT_TOKEN", "").strip(),
            chat_id=os.getenv("TELEGRAM_CHAT_ID", "").strip(),
        )

    def send_lead_notification(
        self,
        lead: dict[str, Any],
        analysis: dict[str, Any],
        steps: list[StepResult],
    ) -> StepResult:
        if not self.is_configured:
            return StepResult(step="telegram_notify", status="skipped", detail="Telegram credentials are not configured")

        message = self._build_message(lead, analysis, steps)

        try:
            import httpx

            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            with httpx.Client(timeout=15.0) as client:
                resp = client.post(url, json={"chat_id": self.chat_id, "text": message})
                resp.raise_for_status()
            return StepResult(step="telegram_notify", status="success", detail="Telegram notification sent")
        except Exception as exc:  # pragma: no cover - external dependency path
            return StepResult(step="telegram_notify", status="failed", detail=str(exc))

    def _build_message(
        self,
        lead: dict[str, Any],
        analysis: dict[str, Any],
        steps: list[StepResult],
    ) -> str:
        lines = [
            "NEW LEAD - Roberts Landscape",
            "",
            f"Name: {' '.join(filter(None, [lead.get('first_name'), lead.get('last_name')]))}",
            f"Email: {lead.get('email')}",
            f"Phone: {lead.get('phone') or 'n/a'}",
            f"Interest: {lead.get('interest') or 'n/a'}",
            f"Budget: {lead.get('budget') or 'n/a'}",
            f"Source: {lead.get('source') or 'n/a'}",
            f"Score: {analysis.get('score', 'n/a')}/10",
            "",
            "Pipeline:",
        ]
        for step in steps:
            lines.append(f"- {step.step}: {step.status} ({step.detail})")
        return "\n".join(lines)


def start_bot() -> None:
    notifier = TelegramNotifier.from_env()
    if not notifier.is_configured:
        return

    try:
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes

        async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            if str(update.effective_chat.id) != notifier.chat_id:
                return
            await update.message.reply_text("Roberts SDR agent is online.")

        async def leads_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            if str(update.effective_chat.id) != notifier.chat_id:
                return
            if not LOG_PATH.exists():
                await update.message.reply_text("No pipeline runs logged yet.")
                return
            lines = LOG_PATH.read_text(encoding="utf-8").splitlines()[-10:]
            await update.message.reply_text("\n".join(lines)[:4000] or "No leads logged yet.")

        application = Application.builder().token(notifier.token).build()
        application.add_handler(CommandHandler("status", status_command))
        application.add_handler(CommandHandler("leads", leads_command))
        application.run_polling(drop_pending_updates=True)
    except Exception:
        return

import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from time import sleep
from typing import Any

import httpx
from dotenv import load_dotenv

from common import StepResult

load_dotenv()


@dataclass
class GHLRequestError(RuntimeError):
    status_code: int
    message: str
    payload: dict[str, Any] | None = None

    def __str__(self) -> str:
        if self.payload:
            return f"GHL request failed ({self.status_code}): {self.message} | payload={self.payload}"
        return f"GHL request failed ({self.status_code}): {self.message}"


@dataclass
class GHLClient:
    api_key: str
    location_id: str
    pipeline_id: str | None = None
    stage_id: str | None = None
    base_url: str = "https://services.leadconnectorhq.com"

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.location_id)

    @classmethod
    def from_env(cls) -> "GHLClient":
        return cls(
            api_key=os.getenv("GHL_ROBERTS_API_KEY", "").strip(),
            location_id=os.getenv("GHL_ROBERTS_LOCATION_ID", "").strip(),
            pipeline_id=os.getenv("GHL_ROBERTS_PIPELINE_ID", "").strip() or None,
            stage_id=os.getenv("GHL_ROBERTS_STAGE_ID", "").strip() or None,
        )

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Version": "2021-07-28",
        }

    def _normalize_phone(self, phone: str | None) -> str | None:
        if not phone:
            return None
        digits = re.sub(r"\D", "", phone)
        if not digits:
            return None
        if len(digits) == 10:
            return f"+1{digits}"
        if len(digits) == 11 and digits.startswith("1"):
            return f"+{digits}"
        if phone.startswith("+"):
            return phone
        return f"+{digits}"

    def _request(self, method: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.is_configured:
            raise RuntimeError("GHL client is not configured")

        url = f"{self.base_url}{path}"
        last_error: Exception | None = None
        for attempt in range(1, 4):
            try:
                with httpx.Client(timeout=20.0) as client:
                    response = client.request(method, url, headers=self._headers(), json=payload)
                    response.raise_for_status()
                    return response.json() if response.content else {}
            except httpx.HTTPStatusError as exc:  # pragma: no cover - external API path
                response_payload: dict[str, Any] | None = None
                try:
                    response_payload = exc.response.json()
                except ValueError:
                    response_payload = None
                message = (
                    str(response_payload.get("message"))
                    if isinstance(response_payload, dict) and response_payload.get("message")
                    else exc.response.text
                )
                last_error = GHLRequestError(
                    status_code=exc.response.status_code,
                    message=message,
                    payload=response_payload,
                )
            except Exception as exc:  # pragma: no cover - external API path
                last_error = exc
            sleep(2 ** (attempt - 1))
        if isinstance(last_error, Exception):
            raise last_error
        raise RuntimeError("GHL request failed")

    def create_contact(self, lead: dict[str, Any], analysis: dict[str, Any]) -> StepResult:
        if not self.is_configured:
            return StepResult(step="ghl_create_contact", status="skipped", detail="GHL credentials are not configured")

        payload = {
            "locationId": self.location_id,
            "firstName": lead.get("first_name"),
            "lastName": lead.get("last_name"),
            "name": " ".join(filter(None, [lead.get("first_name"), lead.get("last_name")])),
            "email": lead.get("email"),
            "phone": self._normalize_phone(lead.get("phone")),
            "source": lead.get("source"),
            "tags": ["sdr-agent", "roberts-landscape", "auto"],
        }

        try:
            response = self._request("POST", "/contacts/", payload)
            return StepResult(
                step="ghl_create_contact",
                status="success",
                detail="Contact sent to GoHighLevel",
                data={"contact": response},
            )
        except GHLRequestError as exc:
            if exc.status_code == 400 and exc.payload:
                meta = exc.payload.get("meta") if isinstance(exc.payload, dict) else None
                contact_id = meta.get("contactId") if isinstance(meta, dict) else None
                if contact_id and "duplicated contacts" in exc.message.lower():
                    return StepResult(
                        step="ghl_create_contact",
                        status="success",
                        detail="Existing GoHighLevel contact reused",
                        data={
                            "contact": {
                                "id": contact_id,
                                "name": meta.get("contactName"),
                            },
                            "duplicate": True,
                        },
                    )
            return StepResult(step="ghl_create_contact", status="failed", detail=str(exc))
        except Exception as exc:
            return StepResult(step="ghl_create_contact", status="failed", detail=str(exc))

    def search_contacts(
        self,
        page_limit: int = 100,
        search_after: list[Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "locationId": self.location_id,
            "pageLimit": page_limit,
        }
        if search_after:
            payload["searchAfter"] = search_after
        return self._request("POST", "/contacts/search", payload)

    def list_contacts(
        self,
        max_contacts: int = 100,
        page_limit: int = 100,
    ) -> list[dict[str, Any]]:
        contacts: list[dict[str, Any]] = []
        cursor: list[Any] | None = None

        while len(contacts) < max_contacts:
            response = self.search_contacts(page_limit=min(page_limit, max_contacts - len(contacts)), search_after=cursor)
            batch = response.get("contacts") or []
            if not isinstance(batch, list) or not batch:
                break
            contacts.extend(batch)
            last_cursor = batch[-1].get("searchAfter")
            if not last_cursor:
                break
            cursor = last_cursor

        return contacts[:max_contacts]

    def is_contact_older_than(self, contact: dict[str, Any], min_age_days: int) -> bool:
        date_added = contact.get("dateAdded")
        if not date_added:
            return False
        try:
            created_at = datetime.fromisoformat(str(date_added).replace("Z", "+00:00"))
        except ValueError:
            return False
        age = datetime.now(UTC) - created_at.astimezone(UTC)
        return age.days >= min_age_days

    def create_opportunity(
        self,
        lead: dict[str, Any],
        analysis: dict[str, Any],
        contact_result: dict[str, Any],
    ) -> StepResult:
        if not self.is_configured:
            return StepResult(step="ghl_create_opportunity", status="skipped", detail="GHL credentials are not configured")
        if not self.pipeline_id:
            return StepResult(step="ghl_create_opportunity", status="skipped", detail="Pipeline ID is not configured")

        contact = contact_result.get("contact") or {}
        contact_id = contact.get("id") or contact.get("contact", {}).get("id")
        if not contact_id:
            return StepResult(step="ghl_create_opportunity", status="skipped", detail="No GoHighLevel contact ID available")
        payload = {
            "locationId": self.location_id,
            "pipelineId": self.pipeline_id,
            "pipelineStageId": self.stage_id,
            "contactId": contact_id,
            "name": f"{lead.get('first_name', 'Lead')} - {lead.get('interest') or 'Landscape Inquiry'}",
            "status": "open",
            "monetaryValue": analysis.get("score", 0) * 1000,
            "source": lead.get("source"),
        }

        try:
            response = self._request("POST", "/opportunities/", payload)
            return StepResult(
                step="ghl_create_opportunity",
                status="success",
                detail="Opportunity created in GoHighLevel",
                data={"opportunity": response},
            )
        except Exception as exc:
            return StepResult(step="ghl_create_opportunity", status="failed", detail=str(exc))

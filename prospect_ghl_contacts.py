import argparse
import json
from collections import Counter
from datetime import UTC, datetime
from typing import Any

from agent import send_prospecting_email
from ghl import GHLClient


def _normalize_contact(contact: dict[str, Any]) -> dict[str, Any]:
    return {
        "first_name": contact.get("firstName") or contact.get("contactName") or "there",
        "last_name": contact.get("lastName"),
        "email": contact.get("email"),
        "phone": contact.get("phone"),
        "source": contact.get("source"),
        "contact_id": contact.get("id"),
        "tags": contact.get("tags") or [],
        "date_added": contact.get("dateAdded"),
    }


def _is_internal_contact(contact: dict[str, Any]) -> bool:
    source = str(contact.get("source") or "").lower()
    tags = {str(tag).lower() for tag in contact.get("tags") or []}
    email = str(contact.get("email") or "").lower()
    return (
        source.startswith("internal")
        or "sdr-agent" in tags
        or "do-not-prospect" in tags
        or "+pipeline" in email
        or "+test" in email
    )


def _has_active_opportunity(contact: dict[str, Any]) -> bool:
    opportunities = contact.get("opportunities") or []
    return any(str(item.get("status") or "").lower() == "open" for item in opportunities)


def _is_eligible(contact: dict[str, Any], ghl: GHLClient, min_age_days: int) -> tuple[bool, str]:
    if not contact.get("email"):
        return False, "missing_email"
    if contact.get("dnd") or contact.get("unsubscribeEmail") or contact.get("bounceEmail"):
        return False, "suppressed"
    if _is_internal_contact(contact):
        return False, "internal"
    if _has_active_opportunity(contact):
        return False, "active_opportunity"
    if min_age_days > 0 and not ghl.is_contact_older_than(contact, min_age_days=min_age_days):
        return False, "too_recent"
    return True, "eligible"


def main() -> None:
    parser = argparse.ArgumentParser(description="Prospect Roberts Landscape contacts from GoHighLevel.")
    parser.add_argument("--limit", type=int, default=25, help="Maximum contacts to process.")
    parser.add_argument("--fetch", type=int, default=100, help="Maximum contacts to fetch from GHL.")
    parser.add_argument("--page-limit", type=int, default=100, help="GHL page size.")
    parser.add_argument("--min-age-days", type=int, default=30, help="Skip contacts newer than this many days.")
    parser.add_argument("--send", action="store_true", help="Actually send emails. Default is preview only.")
    args = parser.parse_args()

    ghl = GHLClient.from_env()
    contacts = ghl.list_contacts(max_contacts=args.fetch, page_limit=args.page_limit)

    reasons = Counter()
    eligible_contacts: list[dict[str, Any]] = []
    for contact in contacts:
        eligible, reason = _is_eligible(contact, ghl=ghl, min_age_days=args.min_age_days)
        reasons[reason] += 1
        if eligible:
            eligible_contacts.append(contact)
        if len(eligible_contacts) >= args.limit:
            break

    results: list[dict[str, Any]] = []
    for contact in eligible_contacts:
        normalized = _normalize_contact(contact)
        if args.send:
            step = send_prospecting_email(normalized)
            results.append(
                {
                    "contact_id": contact.get("id"),
                    "email": contact.get("email"),
                    "name": contact.get("contactName"),
                    "result": step.as_dict(),
                }
            )
        else:
            results.append(
                {
                    "contact_id": contact.get("id"),
                    "email": contact.get("email"),
                    "name": contact.get("contactName"),
                    "date_added": contact.get("dateAdded"),
                    "source": contact.get("source"),
                }
            )

    payload = {
        "timestamp": datetime.now(UTC).isoformat(),
        "mode": "send" if args.send else "preview",
        "fetched_contacts": len(contacts),
        "eligible_contacts": len(eligible_contacts),
        "reason_counts": dict(reasons),
        "results": results,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

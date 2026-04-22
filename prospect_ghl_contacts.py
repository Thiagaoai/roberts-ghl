import argparse
import json

from prospecting_service import DEFAULT_CAMPAIGN_NAME, ProspectingService


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Legacy wrapper: sync GHL contacts to Supabase, then preview or send a prospecting batch."
    )
    parser.add_argument("--campaign", default=DEFAULT_CAMPAIGN_NAME, help="Campaign name.")
    parser.add_argument("--limit", type=int, default=25, help="Maximum prospects to preview or send.")
    parser.add_argument("--fetch", type=int, default=500, help="Maximum contacts to fetch from GHL for sync.")
    parser.add_argument("--page-limit", type=int, default=100, help="GHL page size for sync.")
    parser.add_argument("--min-age-days", type=int, default=30, help="Skip contacts newer than this many days.")
    parser.add_argument("--send", action="store_true", help="Actually send emails. Default is preview only.")
    args = parser.parse_args()

    service = ProspectingService()
    sync_payload = service.sync_contacts(
        campaign_name=args.campaign,
        fetch=args.fetch,
        page_limit=args.page_limit,
        min_age_days=args.min_age_days,
    )
    batch_payload = (
        service.send_batch(campaign_name=args.campaign, limit=args.limit, min_age_days=args.min_age_days)
        if args.send
        else service.preview_batch(campaign_name=args.campaign, limit=args.limit, min_age_days=args.min_age_days)
    )

    payload = {
        "timestamp": batch_payload["timestamp"],
        "campaign": args.campaign,
        "sync": sync_payload,
        "batch": batch_payload,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

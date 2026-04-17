# Roberts SDR Agent

FastAPI service scaffold for the Roberts Landscape SDR automation pipeline.

## What is implemented

- `POST /webhook/lead` with payload normalization, secret validation, and background execution
- `GET /health` uptime/status endpoint
- Lead analysis and scoring with Anthropic-first enrichment, then DeepSeek, then heuristic fallback
- `DRY_RUN` mode to validate the pipeline without triggering external integrations
- Daily email cap and duplicate-send prevention for outbound outreach
- Email template rendering with Jinja2
- GHL client foundation with retry/backoff
- Telegram notifier foundation
- JSONL pipeline logging
- GHL batch prospecting script with preview mode and safe filtering

## Local run

1. Create a virtualenv and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   `agent.py` prioritizes `ANTHROPIC_API_KEY` with `ANTHROPIC_MODEL`, then falls back to DeepSeek, then heuristic scoring. The project still calls the Composio API directly with `httpx`, but also includes the official `composio`, `composio-anthropic`, and `anthropic` packages for the Anthropic provider flow. Set `COMPOSIO_CACHE_DIR` to a writable folder such as `./.composio-cache`. `httpx` is pinned to `0.25.2` to match `python-telegram-bot==20.7`.

2. Copy `.env.example` to `.env` and fill the credentials you have. Keep `DRY_RUN=true` while validating the flow safely.

   `DAILY_EMAIL_LIMIT` defaults to `100`, and successful sends are tracked in `logs/email_dispatch.jsonl` so the same email address is not contacted twice.

3. Start the API:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. Check health:

   ```bash
   curl http://localhost:8000/health
   ```

## Example webhook

```bash
curl -X POST http://localhost:8000/webhook/lead \
  -H "Content-Type: application/json" \
  -H "X-GHL-Signature: your-secret" \
  -d '{
    "first_name": "John",
    "last_name": "Mitchell",
    "email": "john@example.com",
    "phone": "(508) 555-0123",
    "interest": "Patio & Outdoor Kitchen",
    "message": "We want a full backyard redesign.",
    "source": "Google Ads",
    "budget": "$45,000"
  }'
```

PowerShell example:

```powershell
$headers = @{
  "Content-Type" = "application/json"
  "X-GHL-Signature" = "your-secret"
}

$body = @{
  first_name = "John"
  last_name = "Mitchell"
  email = "john@example.com"
  phone = "(508) 555-0123"
  interest = "Patio & Outdoor Kitchen"
  message = "We want a full backyard redesign."
  source = "Google Ads"
  budget = '$45,000'
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/webhook/lead" -Method Post -Headers $headers -Body $body
```

## Notes

- Without external credentials, the pipeline still runs and logs each step as `skipped` instead of crashing.
- With `DRY_RUN=true`, the app still performs lead analysis and logging but skips Gmail, Calendar, Notion, GHL, and Telegram side effects.
- Outbound email dedupe is based on successful sends recorded in `logs/email_dispatch.jsonl`.
- Railway should point at this `roberts-sdr/` directory as the service root.

## Batch Prospecting

Preview eligible GHL contacts without sending:

```bash
py -3.14 prospect_ghl_contacts.py --limit 25 --fetch 100
```

Send to eligible contacts:

```bash
py -3.14 prospect_ghl_contacts.py --send --limit 25 --fetch 100
```

Default safeguards:
- skips contacts without email
- skips internal/test contacts
- skips contacts with active open opportunities
- skips contacts newer than 30 days
- respects `DAILY_EMAIL_LIMIT`
- blocks duplicate sends using `logs/email_dispatch.jsonl`

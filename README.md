# fraud-rules-engine
A small, data-driven rules engine and REST API for scoring account events (SIM swap, new device, OTP abuse) into `APPROVE / STEP_UP_AUTH / DECLINE`.

**Architecture notes**
- Rules are plain data (`Rule` dataclass), so they can later be loaded from a config store or hot-reloaded without redeploying.
- Stateless scoring, so it scales horizontally behind a gateway.
- Natural next steps: Kafka consumer for streaming events, rule versioning, shadow-mode evaluation, ML score blending.

```bash
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
curl -X POST localhost:8000/v1/score -H 'content-type: application/json' \
  -d '{"account_id":"A1","hours_since_sim_swap":2,"new_country":true}'
```
*Synthetic, generic design. No employer IP.*

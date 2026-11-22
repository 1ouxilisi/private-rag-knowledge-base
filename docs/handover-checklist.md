# Handover Checklist

Tick each item before project sign-off. Keep a copy with the delivered package.

## Code & configuration
- [ ] Source code delivered and runs from a clean checkout
- [ ] `.env` created from `.env.example`; secrets not committed to version control
- [ ] `requirements.txt` installs cleanly in a fresh virtual environment
- [ ] Deployment scripts run on the target OS (Linux / Windows)

## Models & data
- [ ] Required models pulled: chat model, embedding model
- [ ] `data/chunks.json` built from the client's documents
- [ ] Backup copy of `inputs/` and `chunks.json` provided
- [ ] Document formats and any unsupported files listed

## Verification
- [ ] `scripts/healthcheck.sh` (or Windows equivalent) passes
- [ ] Agreed acceptance questions answered correctly with citations
- [ ] Unsupported questions are declined, not hallucinated
- [ ] Performance baseline recorded (model, VRAM, tokens/s, hardware)

## Documentation
- [ ] `DEPLOYMENT.md` reviewed against the actual target environment
- [ ] Start/stop/backup/update steps confirmed with the client's admin
- [ ] Access details, ports, and service accounts documented securely

## Knowledge transfer
- [ ] Walkthrough session held with the client's team
- [ ] Client admin can restart the service and re-ingest new documents
- [ ] Support contact and retainer terms agreed (if applicable)

## Security
- [ ] NDA on file (where required)
- [ ] No client-confidential data retained on the developer's machine
- [ ] Access restricted to internal network / VPN / SSO as agreed

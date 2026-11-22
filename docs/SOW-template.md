# Statement of Work (Template) — Private RAG / LLM Deployment

> Fill bracketed fields per client. This is a template, not a legal contract;
> have it reviewed before signing.

## 1. Project
- **Client:** [Client name]
- **Prepared by:** [Freelancer / company]
- **Date:** [YYYY-MM-DD] · **Version:** [1.0]

## 2. Objective
Deploy a private, on-premise or private-cloud AI system that answers questions
from the client's own documents, with model and data staying inside the client's
infrastructure.

## 3. In scope
- Model selection and quantization for the target hardware ([model]).
- Local/private deployment of the LLM and embedding model via Ollama/vLLM.
- Document ingestion pipeline for [PDF / DOCX / MD / HTML / CSV].
- Private RAG knowledge base with retrieval and source citations.
- Web interface or API endpoint for internal users.
- Setup scripts, source code, configuration, and handover documentation.
- [N] rounds of revision within the listed scope.

## 4. Out of scope
- Public cloud hosted-model API calls for client data.
- Model pre-training or large-scale custom fine-tuning (unless added as a change order).
- Integration with systems not listed in Section 3.
- Ongoing 24/7 support, hosting, or hardware procurement (unless covered by a separate retainer).
- Data entry, document cleanup, or content authoring by the developer.

## 5. Deliverables
- [ ] Deployed system on the agreed environment
- [ ] Source code and configuration (`.env` template)
- [ ] Ingested vector store from provided documents
- [ ] Deployment manual (`DEPLOYMENT.md`)
- [ ] Handover checklist and short walkthrough
- [ ] Test results for the agreed acceptance questions

## 6. Milestones & payment
| Milestone | Deliverable | Payment | Due |
|---|---|---|---|
| M1 — Kickoff & discovery | Requirements, hardware, data sources confirmed | [30–50%] deposit | [date] |
| M2 — Deployment & RAG | System deployed, knowledge base ingested, demo | [40–50%] | [date] |
| M3 — Acceptance & handover | Sign-off, docs, walkthrough | [remaining] | [date] |

## 7. Client responsibilities
- Provide documents, access credentials, and environment in time for each milestone.
- Assign a point of contact for questions and acceptance testing.
- Approve scope changes in writing; out-of-scope work is a change order.

## 8. Acceptance criteria
- [ ] System runs in the client's own environment; no client document is sent to a public LLM API.
- [ ] Agreed acceptance questions return answers with correct source citations.
- [ ] Questions unsupported by the documents are declined rather than hallucinated.
- [ ] Handover documentation and source code are delivered and reviewed.

## 9. Revisions & changes
- Included revisions: [N] rounds within Section 3 scope.
- Additional scope, integrations, or fine-tuning are quoted separately.

## 10. Assumptions & constraints
- Client provides compatible hardware or a prepared cloud VM with GPU drivers.
- Documents are provided in supported formats and reasonably structured.
- Timeline assumes timely client feedback at each milestone.
- [Add client-specific compliance constraints: GDPR / HIPAA / internal policy.]

## 11. Commercials
- Fixed project fee: [amount] [currency]
- Optional monthly retainer (hosting updates, new documents, monitoring): [amount]/mo
- Payment terms: [deposit / milestone / net-__]

# MasterThesis
This repository contains the codebase for the master's thesis:
"Investigating the Role of Pre-trained LLMs in Automated Penetration Testing" conducted by me (Julie Lervåg Breivik), NTNU, June 2025.

## Investigating the Role of Pre‑Trained LLMs in Automated Penetration Testing
A proof‑of‑concept security assessment system leveraging pre‑trained large language models (LLMs) to detect and analyze Broken Access Control vulnerabilities.

### Structure
├── app.py              # Flask application: routes and dashboard rendering
├── scanner.py          # Core logic: role login, endpoint scanning, LLM invocation
├── cve.py              # Fetches relevant CVE for Broken Access Control CWEs via the NVD API
├── config.py           # Configuration: URLs to check, roles, HTTP methods, API endpoints- to LM studio conection
├── analyzer.py         # Three analysis strategies- only the generall is here (general, challenge-driven & hint-augumented)
├── utils.py            # Helper functions
├── templates/
│   └── dashboard.html  # Frontend UI for entering target URL and viewing results
└── README.md           # This file



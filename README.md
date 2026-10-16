# Certificate generator (LangGraph)

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows   (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env          # Mac/Linux: cp .env.example .env   -> add your API key
```

## Run
```bash
python main.py "Issue a certificate to Rahul Verma, 16 October 2026, 2:15 PM"
```
If something is missing or ambiguous, the pipeline asks you in the terminal.
PDFs are saved in `output/`; every issued certificate is logged in `output/audit_log.jsonl`.

## Change the course / instructor
Edit `config.yaml`. Change the design in `templates/certificate.html`.

## Windows note
WeasyPrint needs GTK libraries on Windows. If you see a "libgobject" error, install the
GTK runtime (see the WeasyPrint docs) or switch `render.py` to Playwright.

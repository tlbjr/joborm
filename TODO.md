DO:

PUNT:
Use BaseSettings for env overrides.
Proper persistent datastore.
    Sqlite to start or straight to postgres? Or keyval store?
Frontend.
Multiuser.
    API_KEY, oauth, or both?
(Some) shared data models.
    Who's allowed to edit and add companies and opportunities?
    Maybe the user "requests" a new record and puts in details + a URL.
Data scraper(s).
    Company info
        Official
        Crunchbase
        Glassdoor
        LinkedIn
    Position info
        Official JD
        LinkedIn, etc. links
Async tasks (long running)
docker-compose
Create pytest tests.
Use testcontainers.
Service stack as VS code tasks.

DONE:
Basic README.
Basic data model.
Basic REST API.
Basic tests: type + bash.
Basic guardrails black, mypy, ruff.
Basic Dockerfile.
Basic tmux devloop boot stript.
Basic mono repo stub.
Move to public GH repo.

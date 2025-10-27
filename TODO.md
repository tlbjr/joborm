## DO ##
1. Proper persistent datastore
    * Postgres? Or keyval / document store?

## PUNT ##
1. Frontend
2. Multiuser
    * API_KEY, oauth, or both?
3. (Some) shared data models
    * Who's allowed to edit and add companies and opportunities?
    * Maybe the user "requests" a new record and puts in details + a URL.
4. Data scraper(s)
    * Company info
        * Official
        * Crunchbase
        * Glassdoor
        * LinkedIn
    * Position info
        * Official JD
        * LinkedIn, etc. links
5. Async tasks (long running); rq? celery? argo workflow?
6. docker-compose
7. Create pytest tests
8. Use testcontainers
9. Service stack as VS code tasks

## DONE ##
* Basic README.
* Basic data model.
* Basic REST API.
* Basic tests: type + bash.
* Basic guardrails black, mypy, ruff.
* Basic Dockerfile.
* Basic tmux devloop boot stript.
* Basic mono repo stub.
* Basic BaseSettings for env overrides
* Move to public GH repo.

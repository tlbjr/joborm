## DO ##
1. Proper persistent datastore
    * Sqlite to start or straight to postgres? Or keyval store?

## PUNT ##
1. Use BaseSettings for env overrides
2. Frontend
3. Multiuser
    * API_KEY, oauth, or both?
4. (Some) shared data models
    * Who's allowed to edit and add companies and opportunities?
    * Maybe the user "requests" a new record and puts in details + a URL.
5. Data scraper(s)
    * Company info
        * Official
        * Crunchbase
        * Glassdoor
        * LinkedIn
    * Position info
        * Official JD
        * LinkedIn, etc. links
6. Async tasks (long running)
7. docker-compose
8. Create pytest tests
9. Use testcontainers
10. Service stack as VS code tasks

## DONE ##
* Basic README.
* Basic data model.
* Basic REST API.
* Basic tests: type + bash.
* Basic guardrails black, mypy, ruff.
* Basic Dockerfile.
* Basic tmux devloop boot stript.
* Basic mono repo stub.
* Move to public GH repo.

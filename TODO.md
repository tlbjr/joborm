## DO ##

## PUNT ##
1. Frontend: Auto-gen'd python and typescript clients
2. Auth'd user: API_KEY, oauth, or both?
3. (Some) shared data models
    * Who's allowed to edit and add companies and opportunities? Just me to start?
    * Maybe the user "requests" a new record and puts in details + a URL and the system snarfs.
4. Data scraper(s)
    * Company info
        * Official site
        * Crunchbase
        * Glassdoor
        * LinkedIn
    * Position info
        * Official JD
        * LinkedIn, etc. links
5. Create pytest tests
6. Use testcontainers
7. Basic hosting

## ICE ##
1. (Need?) docker-compose
2. (Need?) Async tasks (long running); rq? celery (beat)? argo workflow? APScheduler?
3. Service stack as VS code tasks
4. Dev CLI

## DONE ##
* Basic README.
* Basic data model.
* Basic REST API.
* Basic tests: type + bash.
* Basic guardrails black, mypy, ruff.
* Basic Dockerfile.
* Basic tmux devloop boot stript.
* Basic mono repo stub.
* Basic BaseSettings for env overrides.
* Basic persistent datastore.
* Move to public GH repo.


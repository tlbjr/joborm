## DO ##
1. Auth'd user: API_KEY, oauth, or both?
2. Use testcontainers

## PUNT ##
1. (Some?) shared data models
    * Who's allowed to edit and add companies and opportunities? Just me to start?
    * Maybe the user "requests" a new record and puts in details + a URL and the system snarfs.
2. Drive by (anonymous?) moderation
    1. Prompt for the correctness of scraped data
        If more than one user (try 3+?) say it's wrong, add it to a deny list and include that list in the search terms.
    2. Prompt for the correct data directly
    3. Control how often the prompts go out
    4. Capture moderation success and failure rates
3. Implement an audit / history table
4. Implement OSS observability solutions
5. Basic hosting
    single inet host + let's encrypt?
    AWS and zappa (serverless)?
    AWS CDK / ECS?
    k3s on that single inet host?
    talos on-prem?
6. Add test coverage tracking to pytests

## ICE BOX ##
1. (Scaffold use cases first) Frontend: Auto-gen'd python and typescript clients
    Remember to use subpath hosting instead of subdomain hosting for easier deployment
2. (Need?) docker-compose
3. (Need?) AWS CDK, ECS, and Fargate?
4. (Need?) AKS w/control plane on tailscale?
5. (Need?) Async tasks (long running); rq? celery (beat)? argo workflow? APScheduler?
6. Service stack as VS code tasks
7. Dev CLI
8. Richer models
    * team size, HRM contact, recruiting contact, WLB fields, etc.
9. More data scraper(s) / integrations
    * Company info
        * Number of employees
        * Incorporation type and fundraising stage
    * Position info
        * LinkedIn, etc. links

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
* Basic data scraper POC.
    * Company info
        * Official site
        * Crunchbase
        * Glassdoor
        * LinkedIn
    * A JD link (not necessary official)
* Move to public GH repo.
* Basic resource routers.
* Basic pytest test.


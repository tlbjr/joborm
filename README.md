# Job Opporunity Relationship Manager #

Like a reverse ATS/CRM for job hunters.

## OS set up ##

Ubuntu or WSL:

```
sudo apt install python3-venv libpq-dev jq
```

You probably want this in your tmux.conf file if it's not there already.
```
echo "set -g mouse on" >> .tmux.conf
```


## Dev environment set up ##

Bootstrap a virtual environment and activate it.

```
source ./bin/setup.sh
```

## Usage ##

Setup a 4 pane dev loop with tmux.
Note: The API server is slow to come up for some reason!

```
./bin/tmux.sh
```

## Contributing ##

```
git clone ...
./bin/setup.sh
./bin/tmux.sh  # Setup a 4 pane tight dev loop with tmux.
# Create and fix all the things here.
# Try the quality and change control guardrails.
./bin/fmt.sh
./bin/lint.sh
./bin/type_check.sh
./bin/tests.sh
# Submit a pull request.
```

## Design ##

Not much here yet. See `sample_data.py` for the data model and browse to `/docs`. 

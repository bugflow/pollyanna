# pollyanna

report the plan as it really is

You may be familiar with the famous and most excellent "Kanned Bananas",
which draws data from GitHub (using it's GraphQL API)
and ZehHub (using it's REST API),
and produces reports of **what actually happened**
as well as **what work is currently in progress**.
If not, you should check it out and probably start using it.

Pollyanna is similar, in that it draws data from GitHub GraphQL API and ZenHub REST API,
but different in that it documents **what the plan says is going to happen**.

See, similar but different. Maybe you need both?

## Install

Do this:
```
virtualenv -p python3.8 .venv
. .venv/bin/activate
pip install -r requirements.txt
./post_pip_install.sh  # because we want bleeding edge of gql
pytest
```

The last thing you shouls see should look something like that:
```
=================================== test session starts ====================================
platform linux -- Python 3.8.0, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /home/chris/src/supman/supman/docs/jupyter_mashup, configfile: pytest.ini
plugins: mock-3.3.1
collected 11 items                                                                         

test_fs_cache.py .......                                                             [ 63%]
test_repos.py ...                                                                    [ 90%]
test_utils.py .                                                                      [100%]

==================================== 11 passed in 0.14s ====================================
```
But hopefully with more tests being run :)

Then copy `local_settings.py.sample` to `local_settings.py` and edit it.

Then do `python run.py` or, if you are lucky just `run.py` should work for you.

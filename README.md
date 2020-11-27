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
Kanned Banannas answers the question "between these dates, what happened?".
Pollyanna answers the question "based on everything we know up until now,
what are we saying we are going to do?".

See, similar but different. Maybe you need both?

Pollyanna generates a diffable output.
This means that when the tickets change,
and you keep clobbering you old planning documents with new ones,
the only difference will be the things that changed.
So you can put your generated documents under version control
and use `git diff` to see how the plan changed over time.
This is because the the plan is an important artefact.
It needs to be distributed among tickets so that you can do it,
but it also needs to be consolidated in one place
so that you can present it to people who need to know what the plan is
(more than just the people who need to do it).
You need to be able to discuss how the plan has changed,
why the plan changed, and when.

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

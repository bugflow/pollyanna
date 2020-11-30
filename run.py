#!/usr/bin/env python
"""
This script re-generates the project plan RST
with current data (from GitHub/ZenHub).
It should run as a cron job that clobbers
the documentation in a local git repository.
And then commits the changes,
with a suitable summary message.
"""
from local_settings import *  # NOQA
from repositories import (
    MockGHGraphQLRepo,
    RSTPlanRepo,
    ZenHubRestRepo
)
from usecases import GenerateThePlanUseCase


# TODO: maybe make this a click CLI?
if __name__ == "__main__":
    gh_repo = MockGHGraphQLRepo(
        api_token=github_api_token,
        repo_name=github_repo_name,
        repo_owner=github_repo_owner
    ) # replace this with a real one later
    # maybe this could be a CLI switch (dry-run etc)

    print("INSTANTIATING ZH_REPO")  # DEBUG
    zh_repo = ZenHubRestRepo(
        repo_id=zenhub_repo_id,
        api_token=zenhub_token,
        cache_dir=zenhub_cache_dir
    )

    print("INSTANTIATING WRITER_REPO")  # DEBUG
    writer_repo = RSTPlanRepo(
        template_dir=report_template_dir,
        output_dir=output_dir
    )

    print("INSTANTIATING UC")  # DEBUG
    uc = GenerateThePlanUseCase(
        github_repo=gh_repo,
        zenhub_repo=zh_repo,
        output_repo=writer_repo
    )

    print("EXECUTING UC")  # DEBUG
    print(uc.execute())

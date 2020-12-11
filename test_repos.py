from repositories import ZenHubRestRepo
from pytest_mock import MockerFixture
import run  # KLUDGE. A bad one
# FIXME - should be able to run the test suite without a local_settings.py


def test_zhrr_int(mocker: MockerFixture) -> None:
    mocker.patch("repositories.ZenHubRestRepo._get_fresh_epic_list", return_value=[])
    repo = ZenHubRestRepo(
        repo_id=run.zenhub_repo_id,
        api_token=run.zenhub_token,
        cache_dir="./delme"
    )
    assert type(repo) == ZenHubRestRepo


def test_zhrr_get_fresh_epic_list_makes_request(mocker: MockerFixture) -> None:
    class FakeResponse:
        def __init__(self):
            self.ok = True

        def json(self):
            return {"epic_issues": []}

    mocker.patch("requests.get", return_value=FakeResponse())
    repo = ZenHubRestRepo(
        repo_id=run.zenhub_repo_id,
        api_token=run.zenhub_token,
        cache_dir="./delme"
    )
    assert type(repo) == ZenHubRestRepo


def test_zhrr_get_and_process_epics(mocker: MockerFixture) -> None:
    fake_epic_list = [{"issue_number": 123}, ]
    fake_epic_detail = {
        "issue_number": 123,
        "repo_id": 123,
        "pipelines": [],
        "total_epic_estimates": [],
        "issues": []
    }

    mocker.patch(
        "repositories.ZenHubRestRepo._get_fresh_epic_list",
        return_value=fake_epic_list
    )
    mocker.patch(
        "repositories.ZenHubRestRepo._get_fresh_epic_detail",
        return_value=fake_epic_detail
    )
    repo = ZenHubRestRepo(
        repo_id=123,
        api_token="secret ;)",
        cache_dir="./delme"
    )
    epics = repo._get_and_process_epics()
    assert len(epics) == 1

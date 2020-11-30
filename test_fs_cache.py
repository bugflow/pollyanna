from datetime import (
    datetime,
    timedelta
)
import os.path
from pytest_mock import MockerFixture
from repositories import FSCache


# repo_exists
#
def test_repo_exists_true(mocker: MockerFixture) -> None:
    mocker.patch("repositories.FSCache._dir_exists", return_value=True)
    mocker.patch("repositories.FSCache._repo_path", return_value='/some-repo-path')
    c = FSCache()
    assert c.repo_exists('foo_repo')

def test_repo_exists_false(mocker: MockerFixture) -> None:
    mocker.patch("repositories.FSCache._dir_exists", return_value=False)
    mocker.patch("repositories.FSCache._repo_path", return_value='/some-repo-path')
    c = FSCache()
    assert not c.repo_exists('foo_repo')

# issue_exists
#
def test_issue_exists_false_if_no_repo(mocker: MockerFixture) -> None:
    mocker.patch("repositories.FSCache.repo_exists", return_value=False)
    mocker.patch("repositories.FSCache.update_epic_list")
    c = FSCache()
    assert not c.issue_exists("foo-repo", 123)


def test_issue_exists_false_if_repo_but_no_issue(mocker: MockerFixture) -> None:
    mocker.patch("repositories.FSCache.repo_exists", return_value=True)
    mocker.patch("repositories.FSCache._file_exists", return_value=False)
    c = FSCache(cache_dir='.pollyanna_cache')
    assert not c.issue_exists("foo-repo", 123)


def test_issue_exists_true_if_repo_and_issue_exist(mocker: MockerFixture) -> None:
    mocker.patch("repositories.FSCache.repo_exists", return_value=True)
    mocker.patch("repositories.FSCache._file_exists", return_value=True)
    c = FSCache(cache_dir='.pollyanna_cache')
    assert c.issue_exists("foo-repo", 123)

# _dir_exists
#
def test_dir_exists_true(mocker: MockerFixture) -> None:
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.path.isdir", return_value=True)
    c = FSCache()
    assert c._dir_exists('/some-dir')


def test_dir_exists_false(mocker: MockerFixture) -> None:
    mocker.patch("os.path.exists", return_value=False)
    c = FSCache()
    assert not c._dir_exists('/some-dir')

# _file_exists
#
def test_file_exists_true(mocker: MockerFixture) -> None:
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.path.isfile", return_value=True)
    c = FSCache()
    assert c._file_exists('/some-dir')

def test_file_exists_false(mocker: MockerFixture) -> None:
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.path.isfile", return_value=False)
    c = FSCache()
    assert not c._file_exists('/some-dir')

def test_file_exists_false_missing_dir(mocker: MockerFixture) -> None:
    mocker.patch("os.path.exists", return_value=False)
    c = FSCache()
    assert not c._file_exists('/some-dir')

# _repo_path
# _zenhub_repo_path
# _issue_path
# _epic_list_path
# _file_date

# epic_list_stale
#
def test_epic_list_stale(mocker: MockerFixture) -> None:
    mocker.patch("repositories.FSCache.repo_exists", return_value=True)
    mocker.patch("repositories.FSCache._file_exists", return_value=True)
    now = datetime.now() # freeze time here
    mocker.patch("repositories.FSCache._now", return_value=now)
    threshold = 600
    sub_unity_values = (0.999999, 0.9, 0.1, 0.00001)
    super_unity_values = (1.000001, 1.9, 2, 3, 99999999)
    for x in sub_unity_values:
        offset = threshold * x
        tstamp = now - timedelta(seconds=offset)
        mocker.patch("repositories.FSCache._file_date", return_value=tstamp)
        c = FSCache(cache_dir=".pollyanna_cache")
        assert not c.epic_list_stale('some-repo', threshold)
    for x in super_unity_values:
        offset = threshold * x
        tstamp = now - timedelta(seconds=offset)
        mocker.patch("repositories.FSCache._file_date", return_value=tstamp)
        c = FSCache(cache_dir=".pollyanna_cache")
        assert c.epic_list_stale('some-repo', threshold)
    # expired exactly now == expired
    tstamp = now - timedelta(seconds=threshold)
    mocker.patch("repositories.FSCache._file_date", return_value=tstamp)
    c = FSCache(cache_dir=".pollyanna_cache")
    assert c.epic_list_stale('some-repo', threshold)

# epic_list
#
def test_epic_list(mocker: MockerFixture) -> None:
    mocker.patch("repositories.FSCache._epic_list_path", return_value="/tmp")
    # cache miss
    mocker.patch("repositories.FSCache._file_exists", return_value=False)
    c = FSCache(cache_dir=".pollyanna_cache")
    assert not c.epic_list(123534)
    # cache hit
    mocker.patch("repositories.FSCache._file_exists", return_value=True)
    dumb_data = {"foo": 123, "bar": []}
    mocker.patch("repositories.FSCache._read_json", return_value=dumb_data)
    c = FSCache(cache_dir=".pollyanna_cache")
    assert c.epic_list("9876tfg") == dumb_data

    
# update_epic_list
def test_update_epic_list(mocker: MockerFixture) -> None:
    fake_path = "/tmp/foo"
    dumb_data = {"foo": 123, "bar": []}
    mocker.patch("repositories.FSCache._epic_list_path", return_value=fake_path)
    mocker.patch("repositories.FSCache._file_exists", return_value=True)
    mock_write = mocker.patch("repositories.FSCache._write_json", return_value=True)
    c = FSCache(cache_dir=".pollyanna_cache")
    c.update_epic_list("9876tfg", dumb_data)
    mock_write.assert_called_with(fake_path, dumb_data)

# _read_json
# _write_json

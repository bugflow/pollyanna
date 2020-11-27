from repositories import FSCache
#from pytest_mock import MockerFixture


def test_dir_exists_true():
    # assert that FSCache._dir_exists(path) -> True
    # if the given path exists
    # and the given path is a directory
    pass

def test_dir_exists_false():
    # FSCache._dir_exists(path) -> False
    # if the given path does not exist
    pass

def test_dir_exists_error():
    # FSCache._dir_exists(path) raises an error
    # if the path exists
    # but it is not a directory
    pass

def test_repo_exists():
    # FSCache.repo_exists(repo_name) returns True
    # if the directory exists with the appropriate name
    # else returns False
    pass

def test_issue_exists_false_if_no_repo():
    # FSCache.repo_exists(repo_name) returns False
    # if repo does not exist
    pass

def test_issue_exists_false_if_repo_but_no_issue():
    # FSCache.repo_exists(repo_name) returns False
    # if repo exists but issue does not
    pass

def test_issue_exists_true_if_repo_and_issue_exist():
    # FSCache.repo_exists(repo_name) returns True
    # if repo exists and issue also exists
    pass

#def test_zhrr_get_fresh_epic_list_makes_request(mocker: MockerFixture) -> None:
#    mocker.patch("requests.get", return_value=FakeResponse())

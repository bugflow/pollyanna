from domain import (
    Label,
    Issue
)


epic_label = Label(label_name="Epic", label_color="#FFFFFF")
epic_issue = Issue(
    issue_id="123qwe",
    issue_number="123",
    published_at="yesterday, why she had to go I don't know",
    title="do the test",
    state="Rudderless",
    labels=[epic_label, ]
)
non_epic_issue = Issue(
    issue_id="123qwe",
    issue_number="123",
    published_at="yesterday, why she had to go I don't know",
    title="do the test",
    state="Rudderless"
)


def test_epic_works():
    assert epic_issue.is_epic
    assert not non_epic_issue.is_epic

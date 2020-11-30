#!/usr/bin/env python
"""
Generate the current project plan (in RST) from GitHub tickets.
"""
from slugify import slugify
import re


objective_regex = re.compile("objective:.*", re.IGNORECASE)
epic_regex = re.compile("epic", re.IGNORECASE)


class Milestone:
    def __init__(self, milestone_id, title):
        self.milestone_id = milestone_id
        self.title = title
        self.objective_goals = {}  # index by ID
        self.issues = []
    
    def __str__(self):
        return str(self.title)

    @property
    def count_objectives(self):
        return len(self.objective_goals)

    @property
    def slug_id(self):
        return slugify(self.milestone_id)


class Label:
    def __init__(self, label_name=None, label_color=None):
        self.name = label_name
        self.color = label_color

    def __str__(self):
        return self.name


class Issue:
    def __init__(
        self,
        issue_id=None,
        issue_number=None,
        published_at=None,
        title=None,
        state=None,
        milestone=None,
        labels=None,
        goal=None
    ):
        self.issue_id = issue_id
        self.issue_number = issue_number
        self.title = title
        self.state = state
        self.milestone = milestone
        self.labels = labels
        self._goal = goal

    @property
    def slug_id(self):
        return slugify(f"{self.issue_number}")

    @property
    def is_goal(self):
        if self.is_epic and self.objective:
            return True
        return False

    @property
    def is_epic(self):
        if not self.labels:
            return False
        for l in self.labels:
            if epic_regex.match(l.name):
                return True
        return False

    @property
    def objective(self):
        objectives = []
        for l in self.labels:
            if objective_regex.match(l.name):
                objectives.append(l)
        if len(objectives) > 0:
            # FIXME: warning if more than one
            return objectives[0]
        return False

    @property
    def goal(self):
        # FUCK!
        # I cann't navigate epic/ticket containment via GitHub
        # FIXME
        return self

    @property
    def epics(self):
        # FIXME
        return [self,]


class ZenHubPipeLine:
    def __init__(self, *args, **kwargs):
        self.pipeline_id = None


class ZenHubEpic:
    def __init__(self, *args, **kwargs):
        pass

#!/usr/bin/env python
import asyncio
from datetime import datetime
from domain import (
    Milestone,
    Label,
    Issue,
    ZenHubEpic,
    ZenHubPipeLine,
)
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from jinja2 import Template
import json
import requests
from requests.structures import CaseInsensitiveDict


class FSCache:
    def __init__(self, cache_dir=None):
        self._cache_dir = cache_dir


class ZenHubRestRepo:
    def __init__(
            self,
            repo_id=None,
            api_token=None,
            cache_dir=None
    ):
        # config values
        self._repo_id = repo_id
        self._api_token = api_token
        self._cache_dir = cache_dir
        self._CACHE_THRESHOLD = 600  # seconds

        # hardcoded values
        domain = "https://api.zenhub.com"
        path = f"p1/repositories/{self._repo_id}/epics"
        self._base_url = f"{domain}/{path}"
        self._headers = CaseInsensitiveDict()
        self._headers["X-Authentication-Token"] = self._api_token

        # initialise state
        self._epics = {}  # nested under repo_id (composite key)
        self._pipelines = []

        # do the thing!
        self._get_and_process_epics()

    def _get_fresh_epic_list(self):
        response = requests.get(
            f"{self._base_url}",
            headers=self._headers
        )
        if response.ok:
            return response.json()["epic_issues"]
        else:
            raise Exception(f"HTTP Response from ZenHub: {response.status_code}")

    def _get_and_process_epics(self):
        epics = []
        for le in self._get_fresh_epic_list():
            issue_number = int(le["issue_number"])
            local_age = self._local_epic_age(
                issue_number=issue_number,
                repo_name=self._repo_id
            )  # None if cache miss
            if local_age:
                expired = datetime.now() - local_age > self._CACHE_THRESHOLD
            else:
                expired = False
            if (not local_age) or expired:
                epics.append(
                    self._get_fresh_epic(
                        issue_number=issue_number,
                        repo_name=self._repo_id
                    )
                )
            else:
                epics.append(
                    self._get_local_epic(
                        issue_number=issue_number,
                        repo_name=self._repo_id
                    )
                )
        return epics

    def _get_fresh_epic_detail(
            self,
            issue_number=None,
            repo_name=None
    ):
        if not issue_number:
            raise Exception("_get_fresh_epic_detail requires valid int issue_number")
        
        response = requests.get(
            f"{self._base_url}/{issue_number}",
            headers=self._headers
        )
        if response.ok:
            return response.json()
        else:
            raise Exception(response.json())

    def _get_fresh_epic(
            self,
            issue_number=None,
            repo_name=None
    ):
        return self._process_epic(
            self._get_fresh_epic_detail(
                issue_number=issue_number,
                repo_name=repo_name
            )
        )

    def _local_epic_age(self, issue_number=None, repo_name=None):
        print(f"_local_epic_age called with issue_number={issue_number} and repo_name={repo_name}")
        # return age of local copy in seconds
        # or None if not in local repo
        #
        # FIXME: always miss (until we don't)
        return None

    def _get_local_epic(self, issue_id):
        fname = f"{self._cache_dir}/zenhub_epics/{issue_id}.json"
        # if not fname exists return None
        # else deserialise the epic an
        # then ensure it's in memory (so we don't create dupes)
        # then return it
        return None

    def _save_local_epic(self, epic):
        date_stamp = datetime.now() # as YYYY-MM-DD-HH-MM-SS-miliseconds
        fname = f"{self._cache_dir}/{issue_id}/{date_stamp}.json"
        # if the cache_dir doesn't exist, create it
        # if the file doesn't exist, create it
        # if the file does exist, clobber it
        return None

    def _process_epic(self, raw_data):
        # TODO: ensure the raw data is valid
        issue_number = raw_data["issue_number"]
        repo_id = raw_data["repo_id"]
        if repo_id not in self._epics.keys():
            self._epics[repo_id] = {}

        known_issues = self._epics[repo_id].keys()
        if issue_number in known_issues:
            return self._epics[repo_id][issue_number]

        issues = raw_data["issues"]
        total_epic_estimate = raw_data["total_epic_estimates"]
        pipelines = []  # TODO: _process_pipeline?
        for p in raw_data["pipelines"]:
            pipelines.append(self._process_pipeline(p))
        epic = ZenHubEpic(
            issues=issues,
            total_epic_estimate=total_epic_estimate,
            pipelines=pipelines,
            issue_number=issue_number,
            repo_id=repo_id
        )
        self._epics[repo_id][issue_number] = epic
        return epic

    def _process_pipeline(self, raw_data):
            pipeline_id = raw_data["pipeline_id"]
            for p in self._pipelines:
                if p.pipeline_id == pipeline_id:
                    return p
            p = ZenHubPipeLine(
                name=raw_data["name"],
                workspace_id=raw_data["workspace_id"],
                pipeline_id=pipeline_id
            )
            self._pipelines.append(p)
            return p


class GHGraphQLRepo:    
    def __init__(
            self,
            api_token=None,
            repo_name=None,
            repo_owner=None
    ):
        # config values
        self._api_token = api_token
        self._repo_name = repo_name
        self._repo_owner = repo_owner

        # initialise state
        # tickets
        self._issues = []  # all tickets
        self._goals = []  # super-epics
        self._epics = []  # regular epics
        self._non_epic_tickets = []  # all the rest
        # labels
        self._objectives = []
        self._labels = []
        # milestones
        self._milestones = []
        
        # fetch and process ticket data
        raw_data = self._get_raw_data()
        for i_data in raw_data["repository"]["issues"]["nodes"]:
            self._process_issue(i_data)

        # ensure all issues in the correct buckets
        for i in self._issues:
            if i.is_goal:
                self._process_goal(i)
            elif i.is_epic:
                self._process_epic(i)
            else:
                self._process_non_epic_ticket(i)

                
        # ensure all milestones link to their issues
        for i in self._issues:
            m = i.milestone  # may be None
            if m and i not in m.issues:
                m.issues.append(i)

        # sanity check: we expect all issues to link to their milestone
        for m in self._milestones:
            for i in m.issues:
                if m != i.milestone:
                    msg_pre = "wacky issue/milestone link between"
                    msg = f"{msg_pre} {m} and {i}"
                    raise Exception(msg)

        # re-process milestones
        # now to ensure they know their milestone_objectives
        for m in self._milestones:
            for i in m.issues:
                if i.is_goal:
                    obj = i.objective
                    if obj and obj not in m.objectives:
                        m.objectives.append(obj)
            for i in m.issues:
                if i.is_epic:
                    obj = i.objective  # will this work?
                    if obj not in m.objective_goals.keys():
                        m.objective_goals[obj] = []
                    if i not in m.objective_goals[obj]:
                        m.objective_goals[obj].append(i)

        # ensure each goal links to all its epics
        for e in self._epics:
            if e not in e.goal.epics:
                e.goal.epics.append(e)
        # ensure each epic links to it's goal
        for g in self._goals:
            for e in g.epics:
                if g != e.goal:
                    msg_pre = "wacky epic/goal link between"
                    msg = f"{msg_pre} {g} {e}"
                    raise Exception(msg)

        #   goals <--> epics (null goal?)
        #   non-epic_issues <--> epics (null epic?)
        # every milestone has all it's objectives
        # every objective has all it's goals
        # every goal has all it's epics
        # every epic has all it's tickets
        # all dangling non-epic tickets are known
        # all dangling epics are known
        

    def _process_epic(self, epic):
        if epic not in self._epics:
            self._epics.append(epic)
    
    def _process_issue(self, i):
        num = i["number"]
        pub_at = i["publishedAt"]
        title = i["title"]
        state = i["state"]

        m_data =  i["milestone"]
        milestone = self._process_milestone(m_data)

        labels = []
        for l_data in i["labels"]["nodes"]:
            labels.append(self._process_label(l_data))

        # ensure this issue is in the graph
        found = False
        for issue in self._issues:
            if issue.issue_number == num:
                found = issue
        if not found:
            issue = Issue(
                issue_number=num,
                published_at=pub_at,
                title=title,
                state=state,
                milestone=milestone,
                labels=labels)
            self._issues.append(issue)
            found = issue

        # ensure this issue has it's labels
        for label in labels:
            if label not in found.labels:
                found.labels.append(label)

        return found


    def _process_label(self, label):
        label_name = label["name"]
        label_color = label["color"]

        for l in self._labels:
            if l.name == label_name:
                return l
        l = Label(label_name, label_color)
        self._labels.append(l)
        return l

    def _process_milestone(self, milestone_data):
        # do nothing with None Milestone
        if milestone_data:
            milestone_id = milestone_data["id"]
            for m in self._milestones:
                if m.milestone_id == milestone_id:
                    return m
            milestone_title = milestone_data["title"]
            # process issues? process labels?
            m = Milestone(milestone_id, milestone_title)
            self._milestones.append(m)
            return m

    def _process_non_epic_ticket(self, issue):
        # TODO: error if not issue type
        for i in self._non_epic_tickets:
            if i.issue_id == issue.issue_id:
                return i
        self._non_epic_tickets.append(issue)
        return issue

    @property
    def milestones(self):
        return self._milestones

    def _get_raw_data(self):
        # TODO: make graphql query
        # TODO: iterate/combine over pagenated results
        raise Exception("not implemented (yet)")
        github_url = "https://api.github.com/graphql"


class MockGHGraphQLRepo(GHGraphQLRepo):
    def _get_raw_data(self):
        return json.loads(open("mock_results.json","r").read())


class RSTPlanRepo:
    def __init__(
        self,
        template_dir=None,
        output_dir=None
    ):
        self._template_dir = template_dir
        self._output_dir = output_dir

    def milestone_report(self, milestone):
        template = Template(
            open(
                "templates/milestone_template.rst-jnja2",
                "r"
            ).read()
        )
        print(
            template.render(
                milestone=milestone
            )
        )
        #print(milestone.milestone_id)
        #print(milestone.title)
        #print(milestone.objectives)
        #print(milestone.issues)


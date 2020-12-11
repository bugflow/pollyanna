#!/usr/bin/env python


class GenerateThePlanUseCase:
    def __init__(self, github_repo=None, zenhub_repo=None, output_repo=None):
        self._github_repo = github_repo
        self._zenhub_repo = zenhub_repo
        self._output_repo = output_repo

    def execute(self):
        """
        for each milestone:
        * for each objective:
          * create report `plan/{milestone}/{objective}.rst`, containing:
            * objective/milestone masthead
            * milestone text
            * for each goal (if it has epics)
              * open epics list
              * closed epics list
            * for each non-goal ticket
              * open ticket list
              * closed ticket list
        where the open and closed non-epic ticket lists 
        have (coloured?) badges for all labels.

        So when the script is run, these are re-generated.
        """
        # if the epic and issue match
        # add the ZH data to the GH issue
        issues = self._github_repo.issues
        epics = self._zenhub_repo.epics
        # TODO: sort milestones by chronolical order
        milestones = self._github_repo.milestones

        for e in epics:
            e.gh_issues = []
            for issue_num in e.issues:
                for i in issues:
                    if i.issue_number == issue_num:
                        i._zenhub_epic = e

        # iterate over objectives and ensure they list their goals
        # iterate over goals and ensure the list their epics
        # iterate over epics and ensure the list their issues
        # repeat in the other direction...
        # generate the report
        self._output_repo.skeleton()
        counter = 0
        for m in milestones:
            self._output_repo.milestone_report(counter, m)
            counter += 1
        for i in issues:
            self._output_repo.ticket_report(i)
        return "Done"

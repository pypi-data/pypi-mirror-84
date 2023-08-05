#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.projects.branches import Branches
from gerrit.projects.tags import Tags
from gerrit.projects.commit import Commit
from gerrit.projects.dashboards import Dashboards
from gerrit.projects.labels import Labels
from gerrit.projects.webhooks import Webhooks
from gerrit.changes.change import GerritChange
from gerrit.utils.common import check
from gerrit.utils.models import BaseModel


class GerritProject(BaseModel):
    def __init__(self, **kwargs):
        super(GerritProject, self).__init__(**kwargs)
        self.attributes = ["id", "name", "state", "web_links", "gerrit"]

    @property
    def description(self) -> str:
        """
        Retrieves the description of a project.

        :return:
        """
        endpoint = "/projects/%s/description" % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_description(self, input_: dict) -> str:
        """
        Sets the description of a project.

        .. code-block:: python

            input_ = {
                "description": "Plugin for Gerrit that handles the replication.",,
                "commit_message": "Update the project description"
            }
            project = gerrit.projects.get('myproject')
            result = project.set_description(input_)

        :param input_: the ProjectDescriptionInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#project-description-input
        :return:
        """
        endpoint = "/projects/%s/description" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def delete_description(self):
        """
        Deletes the description of a project.

        :return:
        """
        endpoint = "/projects/%s/description" % self.id
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))

    def delete(self):
        """
        Delete the project, requires delete-project plugin

        :return:
        """
        endpoint = "/projects/%s/delete-project~delete" % self.id
        self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))

    @property
    def parent(self) -> str:
        """
        Retrieves the name of a project’s parent project. For the All-Projects root project an empty string is returned.

        :return:
        """
        endpoint = "/projects/%s/parent" % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_parent(self, input_: dict) -> str:
        """
        Sets the parent project for a project.

        .. code-block:: python

            input_ = {
                "parent": "Public-Plugins",
                "commit_message": "Update the project parent"
            }
            project = gerrit.projects.get('myproject')
            result = project.set_parent(input_)

        :param input_: The ProjectParentInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#project-parent-input
        :return:
        """
        endpoint = "/projects/%s/parent" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    @property
    def HEAD(self) -> str:
        """
        Retrieves for a project the name of the branch to which HEAD points.

        :return:
        """
        endpoint = "/projects/%s/HEAD" % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_HEAD(self, input_: dict) -> str:
        """
        Sets HEAD for a project.

        .. code-block:: python

            input_ = {
                "ref": "refs/heads/stable"
            }
            project = gerrit.projects.get('myproject')
            result = project.set_HEAD(input_)

        :param input_: The HeadInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#head-input
        :return:
        """
        endpoint = "/projects/%s/HEAD" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    @property
    def config(self) -> dict:
        """
        Gets some configuration information about a project.
        Note that this config info is not simply the contents of project.config; it generally contains fields that may
        have been inherited from parent projects.

        :return:
        """
        endpoint = "/projects/%s/config" % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_config(self, input_: dict) -> dict:
        """
        Sets the configuration of a project.

        .. code-block:: python

            input_ = {
                "description": "demo project",
                "use_contributor_agreements": "FALSE",
                "use_content_merge": "INHERIT",
                "use_signed_off_by": "INHERIT",
                "create_new_change_for_all_not_in_target": "INHERIT",
                "enable_signed_push": "INHERIT",
                "require_signed_push": "INHERIT",
                "reject_implicit_merges": "INHERIT",
                "require_change_id": "TRUE",
                "max_object_size_limit": "10m",
                "submit_type": "REBASE_IF_NECESSARY",
                "state": "ACTIVE"
            }
            project = gerrit.projects.get('myproject')
            result = project.set_config(input_)

        :param input_: the ConfigInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#config-info
        :return:
        """
        endpoint = "/projects/%s/config" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def get_statistics(self) -> dict:
        """
        Return statistics for the repository of a project.

        :return:
        """
        endpoint = "/projects/%s/statistics.git" % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def run_garbage_collection(self, input_: dict) -> str:
        """
        Run the Git garbage collection for the repository of a project.

        .. code-block:: python

            input_ = {
                "show_progress": "true"
            }
            project = gerrit.projects.get('myproject')
            result = project.run_garbage_collection(input_)

        :param input_: the GCInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#gc-input
        :return:
        """
        endpoint = "/projects/%s/gc" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    @check
    def ban_commits(self, input_: dict) -> dict:
        """
        Marks commits as banned for the project.

        .. code-block:: python

            input_ = {
                "commits": [
                  "a8a477efffbbf3b44169bb9a1d3a334cbbd9aa96",
                  "cf5b56541f84b8b57e16810b18daca9c3adc377b"
                ],
                "reason": "Violates IP"
            }
            project = gerrit.projects.get('myproject')
            result = project.ban_commits(input_)

        :param input_: the BanInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#ban-input
        :return:
        """
        endpoint = "/projects/%s/ban" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    @property
    def access_rights(self) -> dict:
        """
        Lists the access rights for a single project.

        :return:
        """
        endpoint = "/projects/%s/access" % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_access_rights(self, input_: dict) -> dict:
        """
        Sets access rights for the project using the diff schema provided by ProjectAccessInput.
        https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#set-access

        :param input_: the ProjectAccessInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#project-access-input
        :return:
        """
        endpoint = "/projects/%s/access" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def create_change(self, input_: dict):
        """
        Create Change for review.

        .. code-block:: python

            input_ = {
                "subject": "Let's support 100% Gerrit workflow direct in browser",
                "branch": "stable",
                "topic": "create-change-in-browser",
                "status": "NEW"
            }

            project = gerrit.projects.get('myproject')
            result = project.create_change(input_)

        :param input_:
        :return:
        """
        endpoint = "/projects/%s/create.change" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return GerritChange.parse(result, gerrit=self.gerrit)

    @check
    def create_access_rights_change(self, input_: dict) -> dict:
        """
        Sets access rights for the project using the diff schema provided by ProjectAccessInput
        This takes the same input as Update Access Rights, but creates a pending change for review. Like Create Change,
        it returns a ChangeInfo entity describing the resulting change.
        https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#create-access-change

        :param input_: the ProjectAccessInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#project-access-input
        :return:
        """
        endpoint = "/projects/%s/access:review" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return GerritChange.parse(result, gerrit=self.gerrit)

    def check_access(self, options: str) -> dict:
        """
        runs access checks for other users.

        :param options:
          Check Access Options
            * Account(account): The account for which to check access. Mandatory.
            * Permission(perm): The ref permission for which to check access.
              If not specified, read access to at least branch is checked.
            * Ref(ref): The branch for which to check access. This must be given if perm is specified.

        :return:
        """
        endpoint = "/projects/%s/check.access?%s" % (self.id, options)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def index(self, input_: dict):
        """
        Adds or updates the current project (and children, if specified) in the secondary index.
        The indexing task is executed asynchronously in background and this command returns immediately
        if async is specified in the input.

        .. code-block:: python

            input_ = {
                "index_children": "true"
                "async": "true"
            }
            project = gerrit.projects.get('myproject')
            result = project.index(input_)

        :param input_: the IndexProjectInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#index-project-input
        :return:
        """
        endpoint = "/projects/%s/index" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )

    def index_all_changes(self):
        """
        Adds or updates the current project (and children, if specified) in the secondary index.
        The indexing task is executed asynchronously in background and this command returns immediately
        if async is specified in the input.

        :return:
        """
        endpoint = "/projects/%s/index.changes" % self.id
        self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))

    @check
    def check_consistency(self, input_: dict) -> dict:
        """
        Performs consistency checks on the project.

        .. code-block:: python

            input_ = {
                "auto_closeable_changes_check": {
                    "fix": 'true',
                    "branch": "refs/heads/master",
                    "max_commits": 100
                }
            }

            project = gerrit.projects.get('myproject')
            result = project.check_consistency(input_)

        :param input_: the CheckProjectInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#check-project-input
        :return:
        """
        endpoint = "/projects/%s/check" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    @property
    def branches(self) -> Branches:
        """
        List the branches of a project. except the refs/meta/config

        :return:
        """
        return Branches(self.id, self.gerrit)

    @property
    def child_projects(self) -> list:
        """
        List the direct child projects of a project.

        :return:
        """
        endpoint = "/projects/%s/children/" % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return [self.gerrit.projects.get(item.get("id")) for item in result]

    @property
    def tags(self) -> Tags:
        """
        List the tags of a project.

        :return:
        """
        return Tags(self.id, self.gerrit)

    def get_commit(self, commit: str) -> Commit:
        """
        Retrieves a commit of a project.

        :return:
        """
        endpoint = "/projects/%s/commits/%s" % (self.id, commit)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Commit.parse(result, project=self.id, gerrit=self.gerrit)

    @property
    def dashboards(self) -> Dashboards:
        """
        gerrit dashboards operations

        :return:
        """
        return Dashboards(project=self.id, gerrit=self.gerrit)

    @property
    def labels(self) -> Labels:
        """
        gerrit labels operations

        :return:
        """
        return Labels(project=self.id, gerrit=self.gerrit)

    @property
    def webhooks(self) -> Webhooks:
        """
        gerrit webhooks operations, requires delete-project plugin

        :return:
        """
        return Webhooks(project=self.id, gerrit=self.gerrit)

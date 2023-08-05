#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.groups.group import GerritGroup
from gerrit.utils.common import check


class GerritGroups:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    def list(self) -> list:
        """
        Lists the groups accessible by the caller.

        :return:
        """
        endpoint = "/groups/"
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)

        groups = []
        for key, value in result.items():
            group = value
            group.update({"name": key})
            groups.append(group)

        return GerritGroup.parse_list(groups, gerrit=self.gerrit)

    def search(self, name: str) -> list:
        """
        Query Groups

        :param name: group name
        :return:
        """
        endpoint = "/groups/?query=inname:%s" % name
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return GerritGroup.parse_list(result, gerrit=self.gerrit)

    def get(self, id_: str) -> GerritGroup:
        """
        Retrieves a group.

        :param id_: group id
        :return:
        """
        endpoint = "/groups/%s" % id_
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return GerritGroup.parse(result, gerrit=self.gerrit)

    @check
    def create(self, name: str, input_: dict) -> GerritGroup:
        """
        Creates a new Gerrit internal group.

        .. code-block:: python

            input_ = {
                "description": "contains all committers for MyProject2",
                "visible_to_all": 'true',
                "owner": "Administrators",
                "owner_id": "af01a8cb8cbd8ee7be072b98b1ee882867c0cf06"
            }
            new_group = gerrit.groups.create('My-Project2-Committers', input_)

        :param name: group name
        :param input_: the GroupInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-groups.html#group-input
        :return:
        """
        endpoint = "/groups/%s" % name
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return GerritGroup.parse(result, gerrit=self.gerrit)

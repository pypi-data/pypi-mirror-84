#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from urllib.parse import quote
from gerrit.utils.common import check
from gerrit.utils.models import BaseModel


class Edit(BaseModel):
    def __init__(self, **kwargs):
        super(Edit, self).__init__(**kwargs)
        self.attributes = [
            "ref",
            "base_revision",
            "base_patch_set_number",
            "commit",
            "change",
            "gerrit",
        ]

    def get_change_file_content(self, file: str) -> str:
        """
        Retrieves content of a file from a change edit.
        The content of the file is returned as text encoded inside base64.

        :param file: the file path
        :return:
        """
        endpoint = "/changes/%s/edit/%s" % (self.change, quote(file, safe=""))
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def get_file_meta_data(self, file: str) -> dict:
        """
        Retrieves meta data of a file from a change edit.

        :param file: the file path
        :return:
        """
        endpoint = "/changes/%s/edit/%s/meta" % (self.change, quote(file, safe=""))
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def put_change_file_content(self, file: str, file_content: str):
        """
        Put content of a file to a change edit.

        :param file: the file path
        :param file_content: the content of the file need to change
        :return:
        """
        endpoint = "/changes/%s/edit/%s" % (self.change, quote(file, safe=""))
        base_url = self.gerrit.get_endpoint_url(endpoint)
        self.gerrit.requester.put(
            base_url, data=file_content, headers={"Content-Type": "plain/text"}
        )

    def restore_file_content(self, file: str):
        """
        restores file content

        :param file: Path to file to restore.
        :return:
        """
        input_ = {"restore_path": file}
        endpoint = "/changes/%s/edit" % self.change
        base_url = self.gerrit.get_endpoint_url(endpoint)
        self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )

    def rename_file(self, old_path: str, new_path: str):
        """
        rename file

        :param old_path: Old path to file to rename.
        :param new_path: New path to file to rename.
        :return:
        """
        input_ = {"old_path": old_path, "new_path": new_path}
        endpoint = "/changes/%s/edit" % self.change
        base_url = self.gerrit.get_endpoint_url(endpoint)
        self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )

    def delete_file(self, file: str):
        """
        Deletes a file from a change edit.

        :param file: Path to file to delete.
        :return:
        """
        endpoint = "/changes/%s/edit/%s" % (self.change, quote(file, safe=""))
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))

    @check
    def change_commit_message(self, input_: dict):
        """
        Modify commit message.

        .. code-block:: python

            input_ = {
                "message": "New commit message\\n\\nChange-Id: I10394472cbd17dd12454f229e4f6de00b143a444"
            }

            change = gerrit.changes.get('myProject~stable~I10394472cbd17dd12454f229e4f6de00b143a444')
            edit = change.get_edit()
            edit.change_commit_message(input_)

        :param input_: the ChangeEditMessageInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-edit-message-input
        :return:
        """
        endpoint = "/changes/%s/edit:message" % self.change
        base_url = self.gerrit.get_endpoint_url(endpoint)
        self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )

    def get_commit_message(self):
        """
        Retrieves commit message from change edit.
        The commit message is returned as base64 encoded string.

        :return:
        """
        endpoint = "/changes/%s/edit:message" % self.change
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def publish(self, input_: dict):
        """
        Promotes change edit to a regular patch set.

        .. code-block:: python

            input_ = {
                "notify": "NONE"
            }

            change = gerrit.changes.get('myProject~stable~I10394472cbd17dd12454f229e4f6de00b143a444')
            edit = change.get_edit()
            edit.publish(input_)

        :param input_: the PublishChangeEditInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#publish-change-edit-input
        :return:
        """
        endpoint = "/changes/%s/edit:publish" % self.change
        base_url = self.gerrit.get_endpoint_url(endpoint)
        self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )

    def rebase(self):
        """
        Rebases change edit on top of latest patch set.
        When change was rebased on top of latest patch set, response '204 No Content' is returned.
        When change edit is already based on top of the latest patch set, the response '409 Conflict' is returned.

        :return:
        """
        endpoint = "/changes/%s/edit:rebase" % self.change
        self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))

    def delete(self):
        """
        Deletes change edit.

        :return:
        """
        endpoint = "/changes/%s/edit" % self.change
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))

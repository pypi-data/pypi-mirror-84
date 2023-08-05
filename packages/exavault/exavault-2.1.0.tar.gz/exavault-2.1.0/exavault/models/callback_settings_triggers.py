# coding: utf-8

"""
    ExaVault API

    See our API reference documentation at https://www.exavault.com/developer/api-docs/  # noqa: E501

    OpenAPI spec version: 2.0
    Contact: support@exavault.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class CallbackSettingsTriggers(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'upload': 'bool',
        'download': 'bool',
        'delete': 'bool',
        'create_folder': 'bool',
        'rename': 'bool',
        'move': 'bool',
        'copy': 'bool',
        'compress': 'bool',
        'extract': 'bool',
        'share_folder': 'bool',
        'send_files': 'bool',
        'receive_files': 'bool',
        'update_share': 'bool',
        'update_receive': 'bool',
        'delete_send': 'bool',
        'delete_receive': 'bool',
        'delete_share': 'bool',
        'create_notification': 'bool',
        'update_notification': 'bool',
        'delete_notification': 'bool',
        'create_user': 'bool',
        'update_user': 'bool',
        'delete_user': 'bool',
        'user_connect': 'bool',
        'user_disconnect': 'bool'
    }

    attribute_map = {
        'upload': 'upload',
        'download': 'download',
        'delete': 'delete',
        'create_folder': 'createFolder',
        'rename': 'rename',
        'move': 'move',
        'copy': 'copy',
        'compress': 'compress',
        'extract': 'extract',
        'share_folder': 'shareFolder',
        'send_files': 'sendFiles',
        'receive_files': 'receiveFiles',
        'update_share': 'updateShare',
        'update_receive': 'updateReceive',
        'delete_send': 'deleteSend',
        'delete_receive': 'deleteReceive',
        'delete_share': 'deleteShare',
        'create_notification': 'createNotification',
        'update_notification': 'updateNotification',
        'delete_notification': 'deleteNotification',
        'create_user': 'createUser',
        'update_user': 'updateUser',
        'delete_user': 'deleteUser',
        'user_connect': 'userConnect',
        'user_disconnect': 'userDisconnect'
    }

    def __init__(self, upload=None, download=None, delete=None, create_folder=None, rename=None, move=None, copy=None, compress=None, extract=None, share_folder=None, send_files=None, receive_files=None, update_share=None, update_receive=None, delete_send=None, delete_receive=None, delete_share=None, create_notification=None, update_notification=None, delete_notification=None, create_user=None, update_user=None, delete_user=None, user_connect=None, user_disconnect=None):  # noqa: E501
        """CallbackSettingsTriggers - a model defined in Swagger"""  # noqa: E501
        self._upload = None
        self._download = None
        self._delete = None
        self._create_folder = None
        self._rename = None
        self._move = None
        self._copy = None
        self._compress = None
        self._extract = None
        self._share_folder = None
        self._send_files = None
        self._receive_files = None
        self._update_share = None
        self._update_receive = None
        self._delete_send = None
        self._delete_receive = None
        self._delete_share = None
        self._create_notification = None
        self._update_notification = None
        self._delete_notification = None
        self._create_user = None
        self._update_user = None
        self._delete_user = None
        self._user_connect = None
        self._user_disconnect = None
        self.discriminator = None
        if upload is not None:
            self.upload = upload
        if download is not None:
            self.download = download
        if delete is not None:
            self.delete = delete
        if create_folder is not None:
            self.create_folder = create_folder
        if rename is not None:
            self.rename = rename
        if move is not None:
            self.move = move
        if copy is not None:
            self.copy = copy
        if compress is not None:
            self.compress = compress
        if extract is not None:
            self.extract = extract
        if share_folder is not None:
            self.share_folder = share_folder
        if send_files is not None:
            self.send_files = send_files
        if receive_files is not None:
            self.receive_files = receive_files
        if update_share is not None:
            self.update_share = update_share
        if update_receive is not None:
            self.update_receive = update_receive
        if delete_send is not None:
            self.delete_send = delete_send
        if delete_receive is not None:
            self.delete_receive = delete_receive
        if delete_share is not None:
            self.delete_share = delete_share
        if create_notification is not None:
            self.create_notification = create_notification
        if update_notification is not None:
            self.update_notification = update_notification
        if delete_notification is not None:
            self.delete_notification = delete_notification
        if create_user is not None:
            self.create_user = create_user
        if update_user is not None:
            self.update_user = update_user
        if delete_user is not None:
            self.delete_user = delete_user
        if user_connect is not None:
            self.user_connect = user_connect
        if user_disconnect is not None:
            self.user_disconnect = user_disconnect

    @property
    def upload(self):
        """Gets the upload of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on upload.  # noqa: E501

        :return: The upload of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._upload

    @upload.setter
    def upload(self, upload):
        """Sets the upload of this CallbackSettingsTriggers.

        Trigger callback on upload.  # noqa: E501

        :param upload: The upload of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._upload = upload

    @property
    def download(self):
        """Gets the download of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on download.  # noqa: E501

        :return: The download of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._download

    @download.setter
    def download(self, download):
        """Sets the download of this CallbackSettingsTriggers.

        Trigger callback on download.  # noqa: E501

        :param download: The download of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._download = download

    @property
    def delete(self):
        """Gets the delete of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on delete.  # noqa: E501

        :return: The delete of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._delete

    @delete.setter
    def delete(self, delete):
        """Sets the delete of this CallbackSettingsTriggers.

        Trigger callback on delete.  # noqa: E501

        :param delete: The delete of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._delete = delete

    @property
    def create_folder(self):
        """Gets the create_folder of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on fodler create.  # noqa: E501

        :return: The create_folder of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._create_folder

    @create_folder.setter
    def create_folder(self, create_folder):
        """Sets the create_folder of this CallbackSettingsTriggers.

        Trigger callback on fodler create.  # noqa: E501

        :param create_folder: The create_folder of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._create_folder = create_folder

    @property
    def rename(self):
        """Gets the rename of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on rename.  # noqa: E501

        :return: The rename of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._rename

    @rename.setter
    def rename(self, rename):
        """Sets the rename of this CallbackSettingsTriggers.

        Trigger callback on rename.  # noqa: E501

        :param rename: The rename of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._rename = rename

    @property
    def move(self):
        """Gets the move of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on move.  # noqa: E501

        :return: The move of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._move

    @move.setter
    def move(self, move):
        """Sets the move of this CallbackSettingsTriggers.

        Trigger callback on move.  # noqa: E501

        :param move: The move of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._move = move

    @property
    def copy(self):
        """Gets the copy of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on copy.  # noqa: E501

        :return: The copy of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._copy

    @copy.setter
    def copy(self, copy):
        """Sets the copy of this CallbackSettingsTriggers.

        Trigger callback on copy.  # noqa: E501

        :param copy: The copy of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._copy = copy

    @property
    def compress(self):
        """Gets the compress of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on compress.  # noqa: E501

        :return: The compress of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._compress

    @compress.setter
    def compress(self, compress):
        """Sets the compress of this CallbackSettingsTriggers.

        Trigger callback on compress.  # noqa: E501

        :param compress: The compress of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._compress = compress

    @property
    def extract(self):
        """Gets the extract of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on extract.  # noqa: E501

        :return: The extract of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._extract

    @extract.setter
    def extract(self, extract):
        """Sets the extract of this CallbackSettingsTriggers.

        Trigger callback on extract.  # noqa: E501

        :param extract: The extract of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._extract = extract

    @property
    def share_folder(self):
        """Gets the share_folder of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on share folder create.  # noqa: E501

        :return: The share_folder of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._share_folder

    @share_folder.setter
    def share_folder(self, share_folder):
        """Sets the share_folder of this CallbackSettingsTriggers.

        Trigger callback on share folder create.  # noqa: E501

        :param share_folder: The share_folder of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._share_folder = share_folder

    @property
    def send_files(self):
        """Gets the send_files of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on send files.  # noqa: E501

        :return: The send_files of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._send_files

    @send_files.setter
    def send_files(self, send_files):
        """Sets the send_files of this CallbackSettingsTriggers.

        Trigger callback on send files.  # noqa: E501

        :param send_files: The send_files of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._send_files = send_files

    @property
    def receive_files(self):
        """Gets the receive_files of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on receive folder create.  # noqa: E501

        :return: The receive_files of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._receive_files

    @receive_files.setter
    def receive_files(self, receive_files):
        """Sets the receive_files of this CallbackSettingsTriggers.

        Trigger callback on receive folder create.  # noqa: E501

        :param receive_files: The receive_files of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._receive_files = receive_files

    @property
    def update_share(self):
        """Gets the update_share of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on share folder update.  # noqa: E501

        :return: The update_share of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._update_share

    @update_share.setter
    def update_share(self, update_share):
        """Sets the update_share of this CallbackSettingsTriggers.

        Trigger callback on share folder update.  # noqa: E501

        :param update_share: The update_share of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._update_share = update_share

    @property
    def update_receive(self):
        """Gets the update_receive of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on receive folder update.  # noqa: E501

        :return: The update_receive of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._update_receive

    @update_receive.setter
    def update_receive(self, update_receive):
        """Sets the update_receive of this CallbackSettingsTriggers.

        Trigger callback on receive folder update.  # noqa: E501

        :param update_receive: The update_receive of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._update_receive = update_receive

    @property
    def delete_send(self):
        """Gets the delete_send of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on send files delete.  # noqa: E501

        :return: The delete_send of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._delete_send

    @delete_send.setter
    def delete_send(self, delete_send):
        """Sets the delete_send of this CallbackSettingsTriggers.

        Trigger callback on send files delete.  # noqa: E501

        :param delete_send: The delete_send of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._delete_send = delete_send

    @property
    def delete_receive(self):
        """Gets the delete_receive of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on receive folder delete.  # noqa: E501

        :return: The delete_receive of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._delete_receive

    @delete_receive.setter
    def delete_receive(self, delete_receive):
        """Sets the delete_receive of this CallbackSettingsTriggers.

        Trigger callback on receive folder delete.  # noqa: E501

        :param delete_receive: The delete_receive of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._delete_receive = delete_receive

    @property
    def delete_share(self):
        """Gets the delete_share of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on share folder delete.  # noqa: E501

        :return: The delete_share of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._delete_share

    @delete_share.setter
    def delete_share(self, delete_share):
        """Sets the delete_share of this CallbackSettingsTriggers.

        Trigger callback on share folder delete.  # noqa: E501

        :param delete_share: The delete_share of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._delete_share = delete_share

    @property
    def create_notification(self):
        """Gets the create_notification of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on notification create.  # noqa: E501

        :return: The create_notification of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._create_notification

    @create_notification.setter
    def create_notification(self, create_notification):
        """Sets the create_notification of this CallbackSettingsTriggers.

        Trigger callback on notification create.  # noqa: E501

        :param create_notification: The create_notification of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._create_notification = create_notification

    @property
    def update_notification(self):
        """Gets the update_notification of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on notification update.  # noqa: E501

        :return: The update_notification of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._update_notification

    @update_notification.setter
    def update_notification(self, update_notification):
        """Sets the update_notification of this CallbackSettingsTriggers.

        Trigger callback on notification update.  # noqa: E501

        :param update_notification: The update_notification of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._update_notification = update_notification

    @property
    def delete_notification(self):
        """Gets the delete_notification of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on notification delete.  # noqa: E501

        :return: The delete_notification of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._delete_notification

    @delete_notification.setter
    def delete_notification(self, delete_notification):
        """Sets the delete_notification of this CallbackSettingsTriggers.

        Trigger callback on notification delete.  # noqa: E501

        :param delete_notification: The delete_notification of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._delete_notification = delete_notification

    @property
    def create_user(self):
        """Gets the create_user of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on user create.  # noqa: E501

        :return: The create_user of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._create_user

    @create_user.setter
    def create_user(self, create_user):
        """Sets the create_user of this CallbackSettingsTriggers.

        Trigger callback on user create.  # noqa: E501

        :param create_user: The create_user of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._create_user = create_user

    @property
    def update_user(self):
        """Gets the update_user of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on user update.  # noqa: E501

        :return: The update_user of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._update_user

    @update_user.setter
    def update_user(self, update_user):
        """Sets the update_user of this CallbackSettingsTriggers.

        Trigger callback on user update.  # noqa: E501

        :param update_user: The update_user of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._update_user = update_user

    @property
    def delete_user(self):
        """Gets the delete_user of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on user delete.  # noqa: E501

        :return: The delete_user of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._delete_user

    @delete_user.setter
    def delete_user(self, delete_user):
        """Sets the delete_user of this CallbackSettingsTriggers.

        Trigger callback on user delete.  # noqa: E501

        :param delete_user: The delete_user of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._delete_user = delete_user

    @property
    def user_connect(self):
        """Gets the user_connect of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on user connect.  # noqa: E501

        :return: The user_connect of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._user_connect

    @user_connect.setter
    def user_connect(self, user_connect):
        """Sets the user_connect of this CallbackSettingsTriggers.

        Trigger callback on user connect.  # noqa: E501

        :param user_connect: The user_connect of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._user_connect = user_connect

    @property
    def user_disconnect(self):
        """Gets the user_disconnect of this CallbackSettingsTriggers.  # noqa: E501

        Trigger callback on user disconnect.  # noqa: E501

        :return: The user_disconnect of this CallbackSettingsTriggers.  # noqa: E501
        :rtype: bool
        """
        return self._user_disconnect

    @user_disconnect.setter
    def user_disconnect(self, user_disconnect):
        """Sets the user_disconnect of this CallbackSettingsTriggers.

        Trigger callback on user disconnect.  # noqa: E501

        :param user_disconnect: The user_disconnect of this CallbackSettingsTriggers.  # noqa: E501
        :type: bool
        """

        self._user_disconnect = user_disconnect

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(CallbackSettingsTriggers, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CallbackSettingsTriggers):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

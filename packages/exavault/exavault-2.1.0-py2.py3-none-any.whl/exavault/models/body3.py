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

class Body3(object):
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
        'action': 'str',
        'usernames': 'list[str]',
        'send_email': 'bool',
        'recipients': 'list[str]',
        'message': 'str'
    }

    attribute_map = {
        'action': 'action',
        'usernames': 'usernames',
        'send_email': 'sendEmail',
        'recipients': 'recipients',
        'message': 'message'
    }

    def __init__(self, action=None, usernames=None, send_email=None, recipients=None, message=None):  # noqa: E501
        """Body3 - a model defined in Swagger"""  # noqa: E501
        self._action = None
        self._usernames = None
        self._send_email = None
        self._recipients = None
        self._message = None
        self.discriminator = None
        if action is not None:
            self.action = action
        if usernames is not None:
            self.usernames = usernames
        if send_email is not None:
            self.send_email = send_email
        if recipients is not None:
            self.recipients = recipients
        if message is not None:
            self.message = message

    @property
    def action(self):
        """Gets the action of this Body3.  # noqa: E501

        Type of action be notified about. Notifications will only be sent for the given type of action. Valid choices are **upload**, **download**, **delete** or **all** (upload/download/delete)  # noqa: E501

        :return: The action of this Body3.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this Body3.

        Type of action be notified about. Notifications will only be sent for the given type of action. Valid choices are **upload**, **download**, **delete** or **all** (upload/download/delete)  # noqa: E501

        :param action: The action of this Body3.  # noqa: E501
        :type: str
        """
        allowed_values = ["upload", "download", "delete", "all"]  # noqa: E501
        if action not in allowed_values:
            raise ValueError(
                "Invalid value for `action` ({0}), must be one of {1}"  # noqa: E501
                .format(action, allowed_values)
            )

        self._action = action

    @property
    def usernames(self):
        """Gets the usernames of this Body3.  # noqa: E501

        Determines which users' actions should trigger the notification.   Rather than listing  individual users, you can also use 3 special options:  - **notice\\_user\\_all** for activity by any user or share recipient - **notice\\_user\\_all\\_users** for activity only by user accounts - **notice\\_user\\_all\\_recipient** for activity only by share recipients  # noqa: E501

        :return: The usernames of this Body3.  # noqa: E501
        :rtype: list[str]
        """
        return self._usernames

    @usernames.setter
    def usernames(self, usernames):
        """Sets the usernames of this Body3.

        Determines which users' actions should trigger the notification.   Rather than listing  individual users, you can also use 3 special options:  - **notice\\_user\\_all** for activity by any user or share recipient - **notice\\_user\\_all\\_users** for activity only by user accounts - **notice\\_user\\_all\\_recipient** for activity only by share recipients  # noqa: E501

        :param usernames: The usernames of this Body3.  # noqa: E501
        :type: list[str]
        """

        self._usernames = usernames

    @property
    def send_email(self):
        """Gets the send_email of this Body3.  # noqa: E501

        Whether an email should be sent to the recipients when matching activity happens.  # noqa: E501

        :return: The send_email of this Body3.  # noqa: E501
        :rtype: bool
        """
        return self._send_email

    @send_email.setter
    def send_email(self, send_email):
        """Sets the send_email of this Body3.

        Whether an email should be sent to the recipients when matching activity happens.  # noqa: E501

        :param send_email: The send_email of this Body3.  # noqa: E501
        :type: bool
        """

        self._send_email = send_email

    @property
    def recipients(self):
        """Gets the recipients of this Body3.  # noqa: E501

        Email addresses to send notification emails to. If empty, sends to the current user's email address.  # noqa: E501

        :return: The recipients of this Body3.  # noqa: E501
        :rtype: list[str]
        """
        return self._recipients

    @recipients.setter
    def recipients(self, recipients):
        """Sets the recipients of this Body3.

        Email addresses to send notification emails to. If empty, sends to the current user's email address.  # noqa: E501

        :param recipients: The recipients of this Body3.  # noqa: E501
        :type: list[str]
        """

        self._recipients = recipients

    @property
    def message(self):
        """Gets the message of this Body3.  # noqa: E501

        Custom message to insert into the notification emails, along with the matching activity.  # noqa: E501

        :return: The message of this Body3.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this Body3.

        Custom message to insert into the notification emails, along with the matching activity.  # noqa: E501

        :param message: The message of this Body3.  # noqa: E501
        :type: str
        """

        self._message = message

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
        if issubclass(Body3, dict):
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
        if not isinstance(other, Body3):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

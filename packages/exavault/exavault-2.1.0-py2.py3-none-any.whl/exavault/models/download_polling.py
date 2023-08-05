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

class DownloadPolling(object):
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
        'zip': 'str',
        'percent': 'int'
    }

    attribute_map = {
        'zip': 'zip',
        'percent': 'percent'
    }

    def __init__(self, zip=None, percent=None):  # noqa: E501
        """DownloadPolling - a model defined in Swagger"""  # noqa: E501
        self._zip = None
        self._percent = None
        self.discriminator = None
        if zip is not None:
            self.zip = zip
        if percent is not None:
            self.percent = percent

    @property
    def zip(self):
        """Gets the zip of this DownloadPolling.  # noqa: E501

        Name of the zip file.  # noqa: E501

        :return: The zip of this DownloadPolling.  # noqa: E501
        :rtype: str
        """
        return self._zip

    @zip.setter
    def zip(self, zip):
        """Sets the zip of this DownloadPolling.

        Name of the zip file.  # noqa: E501

        :param zip: The zip of this DownloadPolling.  # noqa: E501
        :type: str
        """

        self._zip = zip

    @property
    def percent(self):
        """Gets the percent of this DownloadPolling.  # noqa: E501

        Indicates archiving process completeness.  # noqa: E501

        :return: The percent of this DownloadPolling.  # noqa: E501
        :rtype: int
        """
        return self._percent

    @percent.setter
    def percent(self, percent):
        """Sets the percent of this DownloadPolling.

        Indicates archiving process completeness.  # noqa: E501

        :param percent: The percent of this DownloadPolling.  # noqa: E501
        :type: int
        """

        self._percent = percent

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
        if issubclass(DownloadPolling, dict):
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
        if not isinstance(other, DownloadPolling):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

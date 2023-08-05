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

class Error401(object):
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
        'response_status': 'int',
        'errors': 'list[Error401Errors]'
    }

    attribute_map = {
        'response_status': 'responseStatus',
        'errors': 'errors'
    }

    def __init__(self, response_status=None, errors=None):  # noqa: E501
        """Error401 - a model defined in Swagger"""  # noqa: E501
        self._response_status = None
        self._errors = None
        self.discriminator = None
        self.response_status = response_status
        if errors is not None:
            self.errors = errors

    @property
    def response_status(self):
        """Gets the response_status of this Error401.  # noqa: E501

        HTTP Status Code  # noqa: E501

        :return: The response_status of this Error401.  # noqa: E501
        :rtype: int
        """
        return self._response_status

    @response_status.setter
    def response_status(self, response_status):
        """Sets the response_status of this Error401.

        HTTP Status Code  # noqa: E501

        :param response_status: The response_status of this Error401.  # noqa: E501
        :type: int
        """
        if response_status is None:
            raise ValueError("Invalid value for `response_status`, must not be `None`")  # noqa: E501

        self._response_status = response_status

    @property
    def errors(self):
        """Gets the errors of this Error401.  # noqa: E501


        :return: The errors of this Error401.  # noqa: E501
        :rtype: list[Error401Errors]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this Error401.


        :param errors: The errors of this Error401.  # noqa: E501
        :type: list[Error401Errors]
        """

        self._errors = errors

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
        if issubclass(Error401, dict):
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
        if not isinstance(other, Error401):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

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

class AnyOfResourceResponseIncludedItems(object):
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
        # *EV* Added the id and type 
        'id': 'int',
        'type': 'str'
        # */EV* 
    }

    attribute_map = { 
        # *EV* Added the id and type 
        'id': 'id',
        'type': 'type'
        # */EV* 
    }

    def __init__(self, id=None, type=None):  # noqa: E501
        """AnyOfResourceResponseIncludedItems - a model defined in Swagger"""  # noqa: E501
        # *EV* Added everything in this method 
        self._id = None
        self._type = None
        if id is not None:
            self.id = id
        if type is not None:
            self.type = type
        self.discriminator = "type"
        # */EV*

    # *EV* Added method to indicate what kind of object was returned 
    def get_real_child_model(self, data):
        """Returns the type of object for the included object"""
        if self.type == "user":
            return "User"
        elif self.type == "share":
            return "Share"
        elif self.type == "notification":
            return "Notification"
        elif self.type == "account":
            return "Account"
        elif self.type == "resource":
            return "Resource"
        else:
            return self.type
    # */EV*
    
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
        if issubclass(AnyOfResourceResponseIncludedItems, dict):
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
        if not isinstance(other, AnyOfResourceResponseIncludedItems):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

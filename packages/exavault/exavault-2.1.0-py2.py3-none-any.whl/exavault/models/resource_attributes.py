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

class ResourceAttributes(object):
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
        'hash': 'str',
        'name': 'str',
        'extension': 'str',
        'type': 'str',
        'created_by': 'str',
        'upload_date': 'datetime',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'accessed_at': 'datetime',
        'created_time': 'int',
        'updated_time': 'int',
        'accessed_time': 'int',
        'path': 'str',
        'size': 'int',
        'file_count': 'int',
        'previewable': 'bool'
    }

    attribute_map = {
        'hash': 'hash',
        'name': 'name',
        'extension': 'extension',
        'type': 'type',
        'created_by': 'createdBy',
        'upload_date': 'uploadDate',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'accessed_at': 'accessedAt',
        'created_time': 'createdTime',
        'updated_time': 'updatedTime',
        'accessed_time': 'accessedTime',
        'path': 'path',
        'size': 'size',
        'file_count': 'fileCount',
        'previewable': 'previewable'
    }

    def __init__(self, hash=None, name=None, extension=None, type=None, created_by=None, upload_date=None, created_at=None, updated_at=None, accessed_at=None, created_time=None, updated_time=None, accessed_time=None, path=None, size=None, file_count=None, previewable=None):  # noqa: E501
        """ResourceAttributes - a model defined in Swagger"""  # noqa: E501
        self._hash = None
        self._name = None
        self._extension = None
        self._type = None
        self._created_by = None
        self._upload_date = None
        self._created_at = None
        self._updated_at = None
        self._accessed_at = None
        self._created_time = None
        self._updated_time = None
        self._accessed_time = None
        self._path = None
        self._size = None
        self._file_count = None
        self._previewable = None
        self.discriminator = None
        if hash is not None:
            self.hash = hash
        if name is not None:
            self.name = name
        if extension is not None:
            self.extension = extension
        if type is not None:
            self.type = type
        if created_by is not None:
            self.created_by = created_by
        if upload_date is not None:
            self.upload_date = upload_date
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if accessed_at is not None:
            self.accessed_at = accessed_at
        if created_time is not None:
            self.created_time = created_time
        if updated_time is not None:
            self.updated_time = updated_time
        if accessed_time is not None:
            self.accessed_time = accessed_time
        if path is not None:
            self.path = path
        if size is not None:
            self.size = size
        if file_count is not None:
            self.file_count = file_count
        if previewable is not None:
            self.previewable = previewable

    @property
    def hash(self):
        """Gets the hash of this ResourceAttributes.  # noqa: E501

        Unique hash of the resource.  # noqa: E501

        :return: The hash of this ResourceAttributes.  # noqa: E501
        :rtype: str
        """
        return self._hash

    @hash.setter
    def hash(self, hash):
        """Sets the hash of this ResourceAttributes.

        Unique hash of the resource.  # noqa: E501

        :param hash: The hash of this ResourceAttributes.  # noqa: E501
        :type: str
        """

        self._hash = hash

    @property
    def name(self):
        """Gets the name of this ResourceAttributes.  # noqa: E501

        Resource name, e.g. the name of the file or folder.  # noqa: E501

        :return: The name of this ResourceAttributes.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ResourceAttributes.

        Resource name, e.g. the name of the file or folder.  # noqa: E501

        :param name: The name of this ResourceAttributes.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def extension(self):
        """Gets the extension of this ResourceAttributes.  # noqa: E501

        Resource extension. Property exists only if resource `type` is file.  # noqa: E501

        :return: The extension of this ResourceAttributes.  # noqa: E501
        :rtype: str
        """
        return self._extension

    @extension.setter
    def extension(self, extension):
        """Sets the extension of this ResourceAttributes.

        Resource extension. Property exists only if resource `type` is file.  # noqa: E501

        :param extension: The extension of this ResourceAttributes.  # noqa: E501
        :type: str
        """

        self._extension = extension

    @property
    def type(self):
        """Gets the type of this ResourceAttributes.  # noqa: E501

        Type of the resource.  # noqa: E501

        :return: The type of this ResourceAttributes.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ResourceAttributes.

        Type of the resource.  # noqa: E501

        :param type: The type of this ResourceAttributes.  # noqa: E501
        :type: str
        """
        allowed_values = ["file", "dir"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def created_by(self):
        """Gets the created_by of this ResourceAttributes.  # noqa: E501

        Username of the creator.  # noqa: E501

        :return: The created_by of this ResourceAttributes.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ResourceAttributes.

        Username of the creator.  # noqa: E501

        :param created_by: The created_by of this ResourceAttributes.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def upload_date(self):
        """Gets the upload_date of this ResourceAttributes.  # noqa: E501

        Timestamp of resource upload.  # noqa: E501

        :return: The upload_date of this ResourceAttributes.  # noqa: E501
        :rtype: datetime
        """
        return self._upload_date

    @upload_date.setter
    def upload_date(self, upload_date):
        """Sets the upload_date of this ResourceAttributes.

        Timestamp of resource upload.  # noqa: E501

        :param upload_date: The upload_date of this ResourceAttributes.  # noqa: E501
        :type: datetime
        """

        self._upload_date = upload_date

    @property
    def created_at(self):
        """Gets the created_at of this ResourceAttributes.  # noqa: E501

        Date-time of resource creation.  # noqa: E501

        :return: The created_at of this ResourceAttributes.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ResourceAttributes.

        Date-time of resource creation.  # noqa: E501

        :param created_at: The created_at of this ResourceAttributes.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this ResourceAttributes.  # noqa: E501

        Date-time of resource modification.  # noqa: E501

        :return: The updated_at of this ResourceAttributes.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ResourceAttributes.

        Date-time of resource modification.  # noqa: E501

        :param updated_at: The updated_at of this ResourceAttributes.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def accessed_at(self):
        """Gets the accessed_at of this ResourceAttributes.  # noqa: E501

        Date-time of the time when resource was accessed.  # noqa: E501

        :return: The accessed_at of this ResourceAttributes.  # noqa: E501
        :rtype: datetime
        """
        return self._accessed_at

    @accessed_at.setter
    def accessed_at(self, accessed_at):
        """Sets the accessed_at of this ResourceAttributes.

        Date-time of the time when resource was accessed.  # noqa: E501

        :param accessed_at: The accessed_at of this ResourceAttributes.  # noqa: E501
        :type: datetime
        """

        self._accessed_at = accessed_at

    @property
    def created_time(self):
        """Gets the created_time of this ResourceAttributes.  # noqa: E501

        UNIX timestamp of resource creation  # noqa: E501

        :return: The created_time of this ResourceAttributes.  # noqa: E501
        :rtype: int
        """
        return self._created_time

    @created_time.setter
    def created_time(self, created_time):
        """Sets the created_time of this ResourceAttributes.

        UNIX timestamp of resource creation  # noqa: E501

        :param created_time: The created_time of this ResourceAttributes.  # noqa: E501
        :type: int
        """

        self._created_time = created_time

    @property
    def updated_time(self):
        """Gets the updated_time of this ResourceAttributes.  # noqa: E501

        UNIX timestamp of resource modification  # noqa: E501

        :return: The updated_time of this ResourceAttributes.  # noqa: E501
        :rtype: int
        """
        return self._updated_time

    @updated_time.setter
    def updated_time(self, updated_time):
        """Sets the updated_time of this ResourceAttributes.

        UNIX timestamp of resource modification  # noqa: E501

        :param updated_time: The updated_time of this ResourceAttributes.  # noqa: E501
        :type: int
        """

        self._updated_time = updated_time

    @property
    def accessed_time(self):
        """Gets the accessed_time of this ResourceAttributes.  # noqa: E501

        UNIX timestamp of last access  # noqa: E501

        :return: The accessed_time of this ResourceAttributes.  # noqa: E501
        :rtype: int
        """
        return self._accessed_time

    @accessed_time.setter
    def accessed_time(self, accessed_time):
        """Sets the accessed_time of this ResourceAttributes.

        UNIX timestamp of last access  # noqa: E501

        :param accessed_time: The accessed_time of this ResourceAttributes.  # noqa: E501
        :type: int
        """

        self._accessed_time = accessed_time

    @property
    def path(self):
        """Gets the path of this ResourceAttributes.  # noqa: E501

        Full path to the resource.  # noqa: E501

        :return: The path of this ResourceAttributes.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this ResourceAttributes.

        Full path to the resource.  # noqa: E501

        :param path: The path of this ResourceAttributes.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def size(self):
        """Gets the size of this ResourceAttributes.  # noqa: E501

        Resource size in bytes  # noqa: E501

        :return: The size of this ResourceAttributes.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this ResourceAttributes.

        Resource size in bytes  # noqa: E501

        :param size: The size of this ResourceAttributes.  # noqa: E501
        :type: int
        """

        self._size = size

    @property
    def file_count(self):
        """Gets the file_count of this ResourceAttributes.  # noqa: E501

        Number of files within folder. null if resource type is a file.  # noqa: E501

        :return: The file_count of this ResourceAttributes.  # noqa: E501
        :rtype: int
        """
        return self._file_count

    @file_count.setter
    def file_count(self, file_count):
        """Sets the file_count of this ResourceAttributes.

        Number of files within folder. null if resource type is a file.  # noqa: E501

        :param file_count: The file_count of this ResourceAttributes.  # noqa: E501
        :type: int
        """

        self._file_count = file_count

    @property
    def previewable(self):
        """Gets the previewable of this ResourceAttributes.  # noqa: E501

        Can resource be previewed. Property equals `null` if resource `type` is dir.  # noqa: E501

        :return: The previewable of this ResourceAttributes.  # noqa: E501
        :rtype: bool
        """
        return self._previewable

    @previewable.setter
    def previewable(self, previewable):
        """Sets the previewable of this ResourceAttributes.

        Can resource be previewed. Property equals `null` if resource `type` is dir.  # noqa: E501

        :param previewable: The previewable of this ResourceAttributes.  # noqa: E501
        :type: bool
        """

        self._previewable = previewable

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
        if issubclass(ResourceAttributes, dict):
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
        if not isinstance(other, ResourceAttributes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

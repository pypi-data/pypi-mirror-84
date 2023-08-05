# coding: utf-8

"""
    Managed Ray API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from openapi_client.configuration import Configuration


class WriteProjectCollaborator(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'permission_level': 'PermissionLevel',
        'value': 'WriteProjectCollaboratorValue'
    }

    attribute_map = {
        'permission_level': 'permission_level',
        'value': 'value'
    }

    def __init__(self, permission_level=None, value=None, local_vars_configuration=None):  # noqa: E501
        """WriteProjectCollaborator - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._permission_level = None
        self._value = None
        self.discriminator = None

        self.permission_level = permission_level
        self.value = value

    @property
    def permission_level(self):
        """Gets the permission_level of this WriteProjectCollaborator.  # noqa: E501


        :return: The permission_level of this WriteProjectCollaborator.  # noqa: E501
        :rtype: PermissionLevel
        """
        return self._permission_level

    @permission_level.setter
    def permission_level(self, permission_level):
        """Sets the permission_level of this WriteProjectCollaborator.


        :param permission_level: The permission_level of this WriteProjectCollaborator.  # noqa: E501
        :type: PermissionLevel
        """
        if self.local_vars_configuration.client_side_validation and permission_level is None:  # noqa: E501
            raise ValueError("Invalid value for `permission_level`, must not be `None`")  # noqa: E501

        self._permission_level = permission_level

    @property
    def value(self):
        """Gets the value of this WriteProjectCollaborator.  # noqa: E501


        :return: The value of this WriteProjectCollaborator.  # noqa: E501
        :rtype: WriteProjectCollaboratorValue
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this WriteProjectCollaborator.


        :param value: The value of this WriteProjectCollaborator.  # noqa: E501
        :type: WriteProjectCollaboratorValue
        """
        if self.local_vars_configuration.client_side_validation and value is None:  # noqa: E501
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, WriteProjectCollaborator):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, WriteProjectCollaborator):
            return True

        return self.to_dict() != other.to_dict()

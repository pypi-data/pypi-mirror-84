# coding: utf-8

"""
    Onepanel

    Onepanel API  # noqa: E501

    The version of the OpenAPI document: 0.15.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from onepanel.core.api.configuration import Configuration


class WorkspaceStatus(object):
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
        'phase': 'str',
        'started_at': 'str',
        'paused_at': 'str',
        'terminated_at': 'str'
    }

    attribute_map = {
        'phase': 'phase',
        'started_at': 'startedAt',
        'paused_at': 'pausedAt',
        'terminated_at': 'terminatedAt'
    }

    def __init__(self, phase=None, started_at=None, paused_at=None, terminated_at=None, local_vars_configuration=None):  # noqa: E501
        """WorkspaceStatus - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._phase = None
        self._started_at = None
        self._paused_at = None
        self._terminated_at = None
        self.discriminator = None

        if phase is not None:
            self.phase = phase
        if started_at is not None:
            self.started_at = started_at
        if paused_at is not None:
            self.paused_at = paused_at
        if terminated_at is not None:
            self.terminated_at = terminated_at

    @property
    def phase(self):
        """Gets the phase of this WorkspaceStatus.  # noqa: E501


        :return: The phase of this WorkspaceStatus.  # noqa: E501
        :rtype: str
        """
        return self._phase

    @phase.setter
    def phase(self, phase):
        """Sets the phase of this WorkspaceStatus.


        :param phase: The phase of this WorkspaceStatus.  # noqa: E501
        :type: str
        """

        self._phase = phase

    @property
    def started_at(self):
        """Gets the started_at of this WorkspaceStatus.  # noqa: E501


        :return: The started_at of this WorkspaceStatus.  # noqa: E501
        :rtype: str
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at):
        """Sets the started_at of this WorkspaceStatus.


        :param started_at: The started_at of this WorkspaceStatus.  # noqa: E501
        :type: str
        """

        self._started_at = started_at

    @property
    def paused_at(self):
        """Gets the paused_at of this WorkspaceStatus.  # noqa: E501


        :return: The paused_at of this WorkspaceStatus.  # noqa: E501
        :rtype: str
        """
        return self._paused_at

    @paused_at.setter
    def paused_at(self, paused_at):
        """Sets the paused_at of this WorkspaceStatus.


        :param paused_at: The paused_at of this WorkspaceStatus.  # noqa: E501
        :type: str
        """

        self._paused_at = paused_at

    @property
    def terminated_at(self):
        """Gets the terminated_at of this WorkspaceStatus.  # noqa: E501


        :return: The terminated_at of this WorkspaceStatus.  # noqa: E501
        :rtype: str
        """
        return self._terminated_at

    @terminated_at.setter
    def terminated_at(self, terminated_at):
        """Sets the terminated_at of this WorkspaceStatus.


        :param terminated_at: The terminated_at of this WorkspaceStatus.  # noqa: E501
        :type: str
        """

        self._terminated_at = terminated_at

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
        if not isinstance(other, WorkspaceStatus):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, WorkspaceStatus):
            return True

        return self.to_dict() != other.to_dict()

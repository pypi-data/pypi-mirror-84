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


class Workspace(object):
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
        'uid': 'str',
        'name': 'str',
        'version': 'str',
        'created_at': 'str',
        'parameters': 'list[Parameter]',
        'workspace_template': 'WorkspaceTemplate',
        'status': 'WorkspaceStatus',
        'labels': 'list[KeyValue]',
        'url': 'str',
        'template_parameters': 'list[Parameter]'
    }

    attribute_map = {
        'uid': 'uid',
        'name': 'name',
        'version': 'version',
        'created_at': 'createdAt',
        'parameters': 'parameters',
        'workspace_template': 'workspaceTemplate',
        'status': 'status',
        'labels': 'labels',
        'url': 'url',
        'template_parameters': 'templateParameters'
    }

    def __init__(self, uid=None, name=None, version=None, created_at=None, parameters=None, workspace_template=None, status=None, labels=None, url=None, template_parameters=None, local_vars_configuration=None):  # noqa: E501
        """Workspace - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._uid = None
        self._name = None
        self._version = None
        self._created_at = None
        self._parameters = None
        self._workspace_template = None
        self._status = None
        self._labels = None
        self._url = None
        self._template_parameters = None
        self.discriminator = None

        if uid is not None:
            self.uid = uid
        if name is not None:
            self.name = name
        if version is not None:
            self.version = version
        if created_at is not None:
            self.created_at = created_at
        if parameters is not None:
            self.parameters = parameters
        if workspace_template is not None:
            self.workspace_template = workspace_template
        if status is not None:
            self.status = status
        if labels is not None:
            self.labels = labels
        if url is not None:
            self.url = url
        if template_parameters is not None:
            self.template_parameters = template_parameters

    @property
    def uid(self):
        """Gets the uid of this Workspace.  # noqa: E501


        :return: The uid of this Workspace.  # noqa: E501
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this Workspace.


        :param uid: The uid of this Workspace.  # noqa: E501
        :type: str
        """

        self._uid = uid

    @property
    def name(self):
        """Gets the name of this Workspace.  # noqa: E501


        :return: The name of this Workspace.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Workspace.


        :param name: The name of this Workspace.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def version(self):
        """Gets the version of this Workspace.  # noqa: E501


        :return: The version of this Workspace.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Workspace.


        :param version: The version of this Workspace.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def created_at(self):
        """Gets the created_at of this Workspace.  # noqa: E501


        :return: The created_at of this Workspace.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Workspace.


        :param created_at: The created_at of this Workspace.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def parameters(self):
        """Gets the parameters of this Workspace.  # noqa: E501


        :return: The parameters of this Workspace.  # noqa: E501
        :rtype: list[Parameter]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this Workspace.


        :param parameters: The parameters of this Workspace.  # noqa: E501
        :type: list[Parameter]
        """

        self._parameters = parameters

    @property
    def workspace_template(self):
        """Gets the workspace_template of this Workspace.  # noqa: E501


        :return: The workspace_template of this Workspace.  # noqa: E501
        :rtype: WorkspaceTemplate
        """
        return self._workspace_template

    @workspace_template.setter
    def workspace_template(self, workspace_template):
        """Sets the workspace_template of this Workspace.


        :param workspace_template: The workspace_template of this Workspace.  # noqa: E501
        :type: WorkspaceTemplate
        """

        self._workspace_template = workspace_template

    @property
    def status(self):
        """Gets the status of this Workspace.  # noqa: E501


        :return: The status of this Workspace.  # noqa: E501
        :rtype: WorkspaceStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Workspace.


        :param status: The status of this Workspace.  # noqa: E501
        :type: WorkspaceStatus
        """

        self._status = status

    @property
    def labels(self):
        """Gets the labels of this Workspace.  # noqa: E501


        :return: The labels of this Workspace.  # noqa: E501
        :rtype: list[KeyValue]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this Workspace.


        :param labels: The labels of this Workspace.  # noqa: E501
        :type: list[KeyValue]
        """

        self._labels = labels

    @property
    def url(self):
        """Gets the url of this Workspace.  # noqa: E501


        :return: The url of this Workspace.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this Workspace.


        :param url: The url of this Workspace.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def template_parameters(self):
        """Gets the template_parameters of this Workspace.  # noqa: E501


        :return: The template_parameters of this Workspace.  # noqa: E501
        :rtype: list[Parameter]
        """
        return self._template_parameters

    @template_parameters.setter
    def template_parameters(self, template_parameters):
        """Sets the template_parameters of this Workspace.


        :param template_parameters: The template_parameters of this Workspace.  # noqa: E501
        :type: list[Parameter]
        """

        self._template_parameters = template_parameters

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
        if not isinstance(other, Workspace):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Workspace):
            return True

        return self.to_dict() != other.to_dict()

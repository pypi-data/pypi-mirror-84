# Copyright 2020 The Tekton Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    Tekton

    Tekton Pipeline  # noqa: E501

    The version of the OpenAPI document: v0.17.2
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tekton.configuration import Configuration


class V1beta1PipelineSpec(object):
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
        'description': 'str',
        '_finally': 'list[V1beta1PipelineTask]',
        'params': 'list[V1beta1ParamSpec]',
        'resources': 'list[V1beta1PipelineDeclaredResource]',
        'results': 'list[V1beta1PipelineResult]',
        'tasks': 'list[V1beta1PipelineTask]',
        'workspaces': 'list[V1beta1PipelineWorkspaceDeclaration]'
    }

    attribute_map = {
        'description': 'description',
        '_finally': 'finally',
        'params': 'params',
        'resources': 'resources',
        'results': 'results',
        'tasks': 'tasks',
        'workspaces': 'workspaces'
    }

    def __init__(self, description=None, _finally=None, params=None, resources=None, results=None, tasks=None, workspaces=None, local_vars_configuration=None):  # noqa: E501
        """V1beta1PipelineSpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._description = None
        self.__finally = None
        self._params = None
        self._resources = None
        self._results = None
        self._tasks = None
        self._workspaces = None
        self.discriminator = None

        if description is not None:
            self.description = description
        if _finally is not None:
            self._finally = _finally
        if params is not None:
            self.params = params
        if resources is not None:
            self.resources = resources
        if results is not None:
            self.results = results
        if tasks is not None:
            self.tasks = tasks
        if workspaces is not None:
            self.workspaces = workspaces

    @property
    def description(self):
        """Gets the description of this V1beta1PipelineSpec.  # noqa: E501

        Description is a user-facing description of the pipeline that may be used to populate a UI.  # noqa: E501

        :return: The description of this V1beta1PipelineSpec.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this V1beta1PipelineSpec.

        Description is a user-facing description of the pipeline that may be used to populate a UI.  # noqa: E501

        :param description: The description of this V1beta1PipelineSpec.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def _finally(self):
        """Gets the _finally of this V1beta1PipelineSpec.  # noqa: E501

        Finally declares the list of Tasks that execute just before leaving the Pipeline i.e. either after all Tasks are finished executing successfully or after a failure which would result in ending the Pipeline  # noqa: E501

        :return: The _finally of this V1beta1PipelineSpec.  # noqa: E501
        :rtype: list[V1beta1PipelineTask]
        """
        return self.__finally

    @_finally.setter
    def _finally(self, _finally):
        """Sets the _finally of this V1beta1PipelineSpec.

        Finally declares the list of Tasks that execute just before leaving the Pipeline i.e. either after all Tasks are finished executing successfully or after a failure which would result in ending the Pipeline  # noqa: E501

        :param _finally: The _finally of this V1beta1PipelineSpec.  # noqa: E501
        :type: list[V1beta1PipelineTask]
        """

        self.__finally = _finally

    @property
    def params(self):
        """Gets the params of this V1beta1PipelineSpec.  # noqa: E501

        Params declares a list of input parameters that must be supplied when this Pipeline is run.  # noqa: E501

        :return: The params of this V1beta1PipelineSpec.  # noqa: E501
        :rtype: list[V1beta1ParamSpec]
        """
        return self._params

    @params.setter
    def params(self, params):
        """Sets the params of this V1beta1PipelineSpec.

        Params declares a list of input parameters that must be supplied when this Pipeline is run.  # noqa: E501

        :param params: The params of this V1beta1PipelineSpec.  # noqa: E501
        :type: list[V1beta1ParamSpec]
        """

        self._params = params

    @property
    def resources(self):
        """Gets the resources of this V1beta1PipelineSpec.  # noqa: E501

        Resources declares the names and types of the resources given to the Pipeline's tasks as inputs and outputs.  # noqa: E501

        :return: The resources of this V1beta1PipelineSpec.  # noqa: E501
        :rtype: list[V1beta1PipelineDeclaredResource]
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this V1beta1PipelineSpec.

        Resources declares the names and types of the resources given to the Pipeline's tasks as inputs and outputs.  # noqa: E501

        :param resources: The resources of this V1beta1PipelineSpec.  # noqa: E501
        :type: list[V1beta1PipelineDeclaredResource]
        """

        self._resources = resources

    @property
    def results(self):
        """Gets the results of this V1beta1PipelineSpec.  # noqa: E501

        Results are values that this pipeline can output once run  # noqa: E501

        :return: The results of this V1beta1PipelineSpec.  # noqa: E501
        :rtype: list[V1beta1PipelineResult]
        """
        return self._results

    @results.setter
    def results(self, results):
        """Sets the results of this V1beta1PipelineSpec.

        Results are values that this pipeline can output once run  # noqa: E501

        :param results: The results of this V1beta1PipelineSpec.  # noqa: E501
        :type: list[V1beta1PipelineResult]
        """

        self._results = results

    @property
    def tasks(self):
        """Gets the tasks of this V1beta1PipelineSpec.  # noqa: E501

        Tasks declares the graph of Tasks that execute when this Pipeline is run.  # noqa: E501

        :return: The tasks of this V1beta1PipelineSpec.  # noqa: E501
        :rtype: list[V1beta1PipelineTask]
        """
        return self._tasks

    @tasks.setter
    def tasks(self, tasks):
        """Sets the tasks of this V1beta1PipelineSpec.

        Tasks declares the graph of Tasks that execute when this Pipeline is run.  # noqa: E501

        :param tasks: The tasks of this V1beta1PipelineSpec.  # noqa: E501
        :type: list[V1beta1PipelineTask]
        """

        self._tasks = tasks

    @property
    def workspaces(self):
        """Gets the workspaces of this V1beta1PipelineSpec.  # noqa: E501

        Workspaces declares a set of named workspaces that are expected to be provided by a PipelineRun.  # noqa: E501

        :return: The workspaces of this V1beta1PipelineSpec.  # noqa: E501
        :rtype: list[V1beta1PipelineWorkspaceDeclaration]
        """
        return self._workspaces

    @workspaces.setter
    def workspaces(self, workspaces):
        """Sets the workspaces of this V1beta1PipelineSpec.

        Workspaces declares a set of named workspaces that are expected to be provided by a PipelineRun.  # noqa: E501

        :param workspaces: The workspaces of this V1beta1PipelineSpec.  # noqa: E501
        :type: list[V1beta1PipelineWorkspaceDeclaration]
        """

        self._workspaces = workspaces

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
        if not isinstance(other, V1beta1PipelineSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1beta1PipelineSpec):
            return True

        return self.to_dict() != other.to_dict()

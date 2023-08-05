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


class V1beta1ConditionCheckStatusFields(object):
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
        'check': 'V1ContainerState',
        'completion_time': 'V1Time',
        'pod_name': 'str',
        'start_time': 'V1Time'
    }

    attribute_map = {
        'check': 'check',
        'completion_time': 'completionTime',
        'pod_name': 'podName',
        'start_time': 'startTime'
    }

    def __init__(self, check=None, completion_time=None, pod_name=None, start_time=None, local_vars_configuration=None):  # noqa: E501
        """V1beta1ConditionCheckStatusFields - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._check = None
        self._completion_time = None
        self._pod_name = None
        self._start_time = None
        self.discriminator = None

        if check is not None:
            self.check = check
        if completion_time is not None:
            self.completion_time = completion_time
        self.pod_name = pod_name
        if start_time is not None:
            self.start_time = start_time

    @property
    def check(self):
        """Gets the check of this V1beta1ConditionCheckStatusFields.  # noqa: E501


        :return: The check of this V1beta1ConditionCheckStatusFields.  # noqa: E501
        :rtype: V1ContainerState
        """
        return self._check

    @check.setter
    def check(self, check):
        """Sets the check of this V1beta1ConditionCheckStatusFields.


        :param check: The check of this V1beta1ConditionCheckStatusFields.  # noqa: E501
        :type: V1ContainerState
        """

        self._check = check

    @property
    def completion_time(self):
        """Gets the completion_time of this V1beta1ConditionCheckStatusFields.  # noqa: E501


        :return: The completion_time of this V1beta1ConditionCheckStatusFields.  # noqa: E501
        :rtype: V1Time
        """
        return self._completion_time

    @completion_time.setter
    def completion_time(self, completion_time):
        """Sets the completion_time of this V1beta1ConditionCheckStatusFields.


        :param completion_time: The completion_time of this V1beta1ConditionCheckStatusFields.  # noqa: E501
        :type: V1Time
        """

        self._completion_time = completion_time

    @property
    def pod_name(self):
        """Gets the pod_name of this V1beta1ConditionCheckStatusFields.  # noqa: E501

        PodName is the name of the pod responsible for executing this condition check.  # noqa: E501

        :return: The pod_name of this V1beta1ConditionCheckStatusFields.  # noqa: E501
        :rtype: str
        """
        return self._pod_name

    @pod_name.setter
    def pod_name(self, pod_name):
        """Sets the pod_name of this V1beta1ConditionCheckStatusFields.

        PodName is the name of the pod responsible for executing this condition check.  # noqa: E501

        :param pod_name: The pod_name of this V1beta1ConditionCheckStatusFields.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and pod_name is None:  # noqa: E501
            raise ValueError("Invalid value for `pod_name`, must not be `None`")  # noqa: E501

        self._pod_name = pod_name

    @property
    def start_time(self):
        """Gets the start_time of this V1beta1ConditionCheckStatusFields.  # noqa: E501


        :return: The start_time of this V1beta1ConditionCheckStatusFields.  # noqa: E501
        :rtype: V1Time
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this V1beta1ConditionCheckStatusFields.


        :param start_time: The start_time of this V1beta1ConditionCheckStatusFields.  # noqa: E501
        :type: V1Time
        """

        self._start_time = start_time

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
        if not isinstance(other, V1beta1ConditionCheckStatusFields):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1beta1ConditionCheckStatusFields):
            return True

        return self.to_dict() != other.to_dict()

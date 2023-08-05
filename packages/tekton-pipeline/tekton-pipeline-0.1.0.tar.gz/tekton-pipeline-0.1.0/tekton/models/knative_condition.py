#!/usr/bin/env bash

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
    tekton

    Python SDK for tekton  # noqa: E501

    OpenAPI spec version: v0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from tekton.models.knative_volatile_time import KnativeVolatileTime  # noqa: F401,E501


class KnativeCondition(object):
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
        'last_transition_time': 'KnativeVolatileTime',
        'message': 'str',
        'reason': 'str',
        'severity': 'str',
        'status': 'str',
        'type': 'str'
    }

    attribute_map = {
        'last_transition_time': 'lastTransitionTime',
        'message': 'message',
        'reason': 'reason',
        'severity': 'severity',
        'status': 'status',
        'type': 'type'
    }

    def __init__(self, last_transition_time=None, message=None, reason=None, severity=None, status=None, type=None):  # noqa: E501
        """KnativeCondition - a model defined in Swagger"""  # noqa: E501

        self._last_transition_time = None
        self._message = None
        self._reason = None
        self._severity = None
        self._status = None
        self._type = None
        self.discriminator = None

        if last_transition_time is not None:
            self.last_transition_time = last_transition_time
        if message is not None:
            self.message = message
        if reason is not None:
            self.reason = reason
        if severity is not None:
            self.severity = severity
        self.status = status
        self.type = type

    @property
    def last_transition_time(self):
        """Gets the last_transition_time of this KnativeCondition.  # noqa: E501

        LastTransitionTime is the last time the condition transitioned from one status to another. We use VolatileTime in place of metav1.Time to exclude this from creating equality.Semantic differences (all other things held constant).  # noqa: E501

        :return: The last_transition_time of this KnativeCondition.  # noqa: E501
        :rtype: KnativeVolatileTime
        """
        return self._last_transition_time

    @last_transition_time.setter
    def last_transition_time(self, last_transition_time):
        """Sets the last_transition_time of this KnativeCondition.

        LastTransitionTime is the last time the condition transitioned from one status to another. We use VolatileTime in place of metav1.Time to exclude this from creating equality.Semantic differences (all other things held constant).  # noqa: E501

        :param last_transition_time: The last_transition_time of this KnativeCondition.  # noqa: E501
        :type: KnativeVolatileTime
        """

        self._last_transition_time = last_transition_time

    @property
    def message(self):
        """Gets the message of this KnativeCondition.  # noqa: E501

        A human readable message indicating details about the transition.  # noqa: E501

        :return: The message of this KnativeCondition.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this KnativeCondition.

        A human readable message indicating details about the transition.  # noqa: E501

        :param message: The message of this KnativeCondition.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def reason(self):
        """Gets the reason of this KnativeCondition.  # noqa: E501

        The reason for the condition's last transition.  # noqa: E501

        :return: The reason of this KnativeCondition.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this KnativeCondition.

        The reason for the condition's last transition.  # noqa: E501

        :param reason: The reason of this KnativeCondition.  # noqa: E501
        :type: str
        """

        self._reason = reason

    @property
    def severity(self):
        """Gets the severity of this KnativeCondition.  # noqa: E501

        Severity with which to treat failures of this type of condition. When this is not specified, it defaults to Error.  # noqa: E501

        :return: The severity of this KnativeCondition.  # noqa: E501
        :rtype: str
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """Sets the severity of this KnativeCondition.

        Severity with which to treat failures of this type of condition. When this is not specified, it defaults to Error.  # noqa: E501

        :param severity: The severity of this KnativeCondition.  # noqa: E501
        :type: str
        """

        self._severity = severity

    @property
    def status(self):
        """Gets the status of this KnativeCondition.  # noqa: E501

        Status of the condition, one of True, False, Unknown.  # noqa: E501

        :return: The status of this KnativeCondition.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this KnativeCondition.

        Status of the condition, one of True, False, Unknown.  # noqa: E501

        :param status: The status of this KnativeCondition.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def type(self):
        """Gets the type of this KnativeCondition.  # noqa: E501

        Type of condition.  # noqa: E501

        :return: The type of this KnativeCondition.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this KnativeCondition.

        Type of condition.  # noqa: E501

        :param type: The type of this KnativeCondition.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

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
        if issubclass(KnativeCondition, dict):
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
        if not isinstance(other, KnativeCondition):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

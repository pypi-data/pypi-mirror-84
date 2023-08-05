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


class V1beta1PipelineRunStatus(object):
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
        'annotations': 'dict(str, str)',
        'completion_time': 'V1Time',
        'conditions': 'list[KnativeCondition]',
        'observed_generation': 'int',
        'pipeline_results': 'list[V1beta1PipelineRunResult]',
        'pipeline_spec': 'V1beta1PipelineSpec',
        'skipped_tasks': 'list[V1beta1SkippedTask]',
        'start_time': 'V1Time',
        'task_runs': 'dict(str, V1beta1PipelineRunTaskRunStatus)'
    }

    attribute_map = {
        'annotations': 'annotations',
        'completion_time': 'completionTime',
        'conditions': 'conditions',
        'observed_generation': 'observedGeneration',
        'pipeline_results': 'pipelineResults',
        'pipeline_spec': 'pipelineSpec',
        'skipped_tasks': 'skippedTasks',
        'start_time': 'startTime',
        'task_runs': 'taskRuns'
    }

    def __init__(self, annotations=None, completion_time=None, conditions=None, observed_generation=None, pipeline_results=None, pipeline_spec=None, skipped_tasks=None, start_time=None, task_runs=None, local_vars_configuration=None):  # noqa: E501
        """V1beta1PipelineRunStatus - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._annotations = None
        self._completion_time = None
        self._conditions = None
        self._observed_generation = None
        self._pipeline_results = None
        self._pipeline_spec = None
        self._skipped_tasks = None
        self._start_time = None
        self._task_runs = None
        self.discriminator = None

        if annotations is not None:
            self.annotations = annotations
        if completion_time is not None:
            self.completion_time = completion_time
        if conditions is not None:
            self.conditions = conditions
        if observed_generation is not None:
            self.observed_generation = observed_generation
        if pipeline_results is not None:
            self.pipeline_results = pipeline_results
        if pipeline_spec is not None:
            self.pipeline_spec = pipeline_spec
        if skipped_tasks is not None:
            self.skipped_tasks = skipped_tasks
        if start_time is not None:
            self.start_time = start_time
        if task_runs is not None:
            self.task_runs = task_runs

    @property
    def annotations(self):
        """Gets the annotations of this V1beta1PipelineRunStatus.  # noqa: E501

        Annotations is additional Status fields for the Resource to save some additional State as well as convey more information to the user. This is roughly akin to Annotations on any k8s resource, just the reconciler conveying richer information outwards.  # noqa: E501

        :return: The annotations of this V1beta1PipelineRunStatus.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._annotations

    @annotations.setter
    def annotations(self, annotations):
        """Sets the annotations of this V1beta1PipelineRunStatus.

        Annotations is additional Status fields for the Resource to save some additional State as well as convey more information to the user. This is roughly akin to Annotations on any k8s resource, just the reconciler conveying richer information outwards.  # noqa: E501

        :param annotations: The annotations of this V1beta1PipelineRunStatus.  # noqa: E501
        :type: dict(str, str)
        """

        self._annotations = annotations

    @property
    def completion_time(self):
        """Gets the completion_time of this V1beta1PipelineRunStatus.  # noqa: E501


        :return: The completion_time of this V1beta1PipelineRunStatus.  # noqa: E501
        :rtype: V1Time
        """
        return self._completion_time

    @completion_time.setter
    def completion_time(self, completion_time):
        """Sets the completion_time of this V1beta1PipelineRunStatus.


        :param completion_time: The completion_time of this V1beta1PipelineRunStatus.  # noqa: E501
        :type: V1Time
        """

        self._completion_time = completion_time

    @property
    def conditions(self):
        """Gets the conditions of this V1beta1PipelineRunStatus.  # noqa: E501

        Conditions the latest available observations of a resource's current state.  # noqa: E501

        :return: The conditions of this V1beta1PipelineRunStatus.  # noqa: E501
        :rtype: list[KnativeCondition]
        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        """Sets the conditions of this V1beta1PipelineRunStatus.

        Conditions the latest available observations of a resource's current state.  # noqa: E501

        :param conditions: The conditions of this V1beta1PipelineRunStatus.  # noqa: E501
        :type: list[KnativeCondition]
        """

        self._conditions = conditions

    @property
    def observed_generation(self):
        """Gets the observed_generation of this V1beta1PipelineRunStatus.  # noqa: E501

        ObservedGeneration is the 'Generation' of the Service that was last processed by the controller.  # noqa: E501

        :return: The observed_generation of this V1beta1PipelineRunStatus.  # noqa: E501
        :rtype: int
        """
        return self._observed_generation

    @observed_generation.setter
    def observed_generation(self, observed_generation):
        """Sets the observed_generation of this V1beta1PipelineRunStatus.

        ObservedGeneration is the 'Generation' of the Service that was last processed by the controller.  # noqa: E501

        :param observed_generation: The observed_generation of this V1beta1PipelineRunStatus.  # noqa: E501
        :type: int
        """

        self._observed_generation = observed_generation

    @property
    def pipeline_results(self):
        """Gets the pipeline_results of this V1beta1PipelineRunStatus.  # noqa: E501

        PipelineResults are the list of results written out by the pipeline task's containers  # noqa: E501

        :return: The pipeline_results of this V1beta1PipelineRunStatus.  # noqa: E501
        :rtype: list[V1beta1PipelineRunResult]
        """
        return self._pipeline_results

    @pipeline_results.setter
    def pipeline_results(self, pipeline_results):
        """Sets the pipeline_results of this V1beta1PipelineRunStatus.

        PipelineResults are the list of results written out by the pipeline task's containers  # noqa: E501

        :param pipeline_results: The pipeline_results of this V1beta1PipelineRunStatus.  # noqa: E501
        :type: list[V1beta1PipelineRunResult]
        """

        self._pipeline_results = pipeline_results

    @property
    def pipeline_spec(self):
        """Gets the pipeline_spec of this V1beta1PipelineRunStatus.  # noqa: E501


        :return: The pipeline_spec of this V1beta1PipelineRunStatus.  # noqa: E501
        :rtype: V1beta1PipelineSpec
        """
        return self._pipeline_spec

    @pipeline_spec.setter
    def pipeline_spec(self, pipeline_spec):
        """Sets the pipeline_spec of this V1beta1PipelineRunStatus.


        :param pipeline_spec: The pipeline_spec of this V1beta1PipelineRunStatus.  # noqa: E501
        :type: V1beta1PipelineSpec
        """

        self._pipeline_spec = pipeline_spec

    @property
    def skipped_tasks(self):
        """Gets the skipped_tasks of this V1beta1PipelineRunStatus.  # noqa: E501

        list of tasks that were skipped due to when expressions evaluating to false  # noqa: E501

        :return: The skipped_tasks of this V1beta1PipelineRunStatus.  # noqa: E501
        :rtype: list[V1beta1SkippedTask]
        """
        return self._skipped_tasks

    @skipped_tasks.setter
    def skipped_tasks(self, skipped_tasks):
        """Sets the skipped_tasks of this V1beta1PipelineRunStatus.

        list of tasks that were skipped due to when expressions evaluating to false  # noqa: E501

        :param skipped_tasks: The skipped_tasks of this V1beta1PipelineRunStatus.  # noqa: E501
        :type: list[V1beta1SkippedTask]
        """

        self._skipped_tasks = skipped_tasks

    @property
    def start_time(self):
        """Gets the start_time of this V1beta1PipelineRunStatus.  # noqa: E501


        :return: The start_time of this V1beta1PipelineRunStatus.  # noqa: E501
        :rtype: V1Time
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this V1beta1PipelineRunStatus.


        :param start_time: The start_time of this V1beta1PipelineRunStatus.  # noqa: E501
        :type: V1Time
        """

        self._start_time = start_time

    @property
    def task_runs(self):
        """Gets the task_runs of this V1beta1PipelineRunStatus.  # noqa: E501

        map of PipelineRunTaskRunStatus with the taskRun name as the key  # noqa: E501

        :return: The task_runs of this V1beta1PipelineRunStatus.  # noqa: E501
        :rtype: dict(str, V1beta1PipelineRunTaskRunStatus)
        """
        return self._task_runs

    @task_runs.setter
    def task_runs(self, task_runs):
        """Sets the task_runs of this V1beta1PipelineRunStatus.

        map of PipelineRunTaskRunStatus with the taskRun name as the key  # noqa: E501

        :param task_runs: The task_runs of this V1beta1PipelineRunStatus.  # noqa: E501
        :type: dict(str, V1beta1PipelineRunTaskRunStatus)
        """

        self._task_runs = task_runs

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
        if not isinstance(other, V1beta1PipelineRunStatus):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1beta1PipelineRunStatus):
            return True

        return self.to_dict() != other.to_dict()

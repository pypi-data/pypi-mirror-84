# coding: utf-8

#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#

import pprint
import re  # noqa: F401
import six
import typing
from enum import Enum


if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union, Any
    from datetime import datetime
    from ask_smapi_model.v1.skill.asr.evaluations.annotation_with_audio_asset import AnnotationWithAudioAsset as AnnotationWithAudioAsset_102c10aa
    from ask_smapi_model.v1.skill.asr.evaluations.evaluation_result_output import EvaluationResultOutput as EvaluationResultOutput_7d57585d
    from ask_smapi_model.v1.skill.asr.evaluations.evaluation_result_status import EvaluationResultStatus as EvaluationResultStatus_2e2193d
    from ask_smapi_model.v1.skill.asr.evaluations.error_object import ErrorObject as ErrorObject_27eea4fa


class EvaluationResult(object):
    """
    evaluation detailed result


    :param status: 
    :type status: (optional) ask_smapi_model.v1.skill.asr.evaluations.evaluation_result_status.EvaluationResultStatus
    :param annotation: 
    :type annotation: (optional) ask_smapi_model.v1.skill.asr.evaluations.annotation_with_audio_asset.AnnotationWithAudioAsset
    :param output: 
    :type output: (optional) ask_smapi_model.v1.skill.asr.evaluations.evaluation_result_output.EvaluationResultOutput
    :param error: 
    :type error: (optional) ask_smapi_model.v1.skill.asr.evaluations.error_object.ErrorObject

    """
    deserialized_types = {
        'status': 'ask_smapi_model.v1.skill.asr.evaluations.evaluation_result_status.EvaluationResultStatus',
        'annotation': 'ask_smapi_model.v1.skill.asr.evaluations.annotation_with_audio_asset.AnnotationWithAudioAsset',
        'output': 'ask_smapi_model.v1.skill.asr.evaluations.evaluation_result_output.EvaluationResultOutput',
        'error': 'ask_smapi_model.v1.skill.asr.evaluations.error_object.ErrorObject'
    }  # type: Dict

    attribute_map = {
        'status': 'status',
        'annotation': 'annotation',
        'output': 'output',
        'error': 'error'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, status=None, annotation=None, output=None, error=None):
        # type: (Optional[EvaluationResultStatus_2e2193d], Optional[AnnotationWithAudioAsset_102c10aa], Optional[EvaluationResultOutput_7d57585d], Optional[ErrorObject_27eea4fa]) -> None
        """evaluation detailed result

        :param status: 
        :type status: (optional) ask_smapi_model.v1.skill.asr.evaluations.evaluation_result_status.EvaluationResultStatus
        :param annotation: 
        :type annotation: (optional) ask_smapi_model.v1.skill.asr.evaluations.annotation_with_audio_asset.AnnotationWithAudioAsset
        :param output: 
        :type output: (optional) ask_smapi_model.v1.skill.asr.evaluations.evaluation_result_output.EvaluationResultOutput
        :param error: 
        :type error: (optional) ask_smapi_model.v1.skill.asr.evaluations.error_object.ErrorObject
        """
        self.__discriminator_value = None  # type: str

        self.status = status
        self.annotation = annotation
        self.output = output
        self.error = error

    def to_dict(self):
        # type: () -> Dict[str, object]
        """Returns the model properties as a dict"""
        result = {}  # type: Dict

        for attr, _ in six.iteritems(self.deserialized_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else
                    x.value if isinstance(x, Enum) else x,
                    value
                ))
            elif isinstance(value, Enum):
                result[attr] = value.value
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else
                    (item[0], item[1].value)
                    if isinstance(item[1], Enum) else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        # type: () -> str
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        # type: () -> str
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are equal"""
        if not isinstance(other, EvaluationResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other

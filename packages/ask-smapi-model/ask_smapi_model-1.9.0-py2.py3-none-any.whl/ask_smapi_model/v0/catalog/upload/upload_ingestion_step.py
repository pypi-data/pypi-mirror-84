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
    from ask_smapi_model.v0.catalog.upload.ingestion_status import IngestionStatus as IngestionStatus_2b1122e3
    from ask_smapi_model.v0.error import Error as Error_d660d58
    from ask_smapi_model.v0.catalog.upload.ingestion_step_name import IngestionStepName as IngestionStepName_4eaa95a2


class UploadIngestionStep(object):
    """
    Represents a single step in the ingestion process of a new upload.


    :param name: 
    :type name: (optional) ask_smapi_model.v0.catalog.upload.ingestion_step_name.IngestionStepName
    :param status: 
    :type status: (optional) ask_smapi_model.v0.catalog.upload.ingestion_status.IngestionStatus
    :param log_url: Represents the url for the file containing logs of ingestion step.
    :type log_url: (optional) str
    :param errors: This array will contain the errors occurred during the execution of step. Will be empty, if execution succeeded.
    :type errors: (optional) list[ask_smapi_model.v0.error.Error]

    """
    deserialized_types = {
        'name': 'ask_smapi_model.v0.catalog.upload.ingestion_step_name.IngestionStepName',
        'status': 'ask_smapi_model.v0.catalog.upload.ingestion_status.IngestionStatus',
        'log_url': 'str',
        'errors': 'list[ask_smapi_model.v0.error.Error]'
    }  # type: Dict

    attribute_map = {
        'name': 'name',
        'status': 'status',
        'log_url': 'logUrl',
        'errors': 'errors'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, name=None, status=None, log_url=None, errors=None):
        # type: (Optional[IngestionStepName_4eaa95a2], Optional[IngestionStatus_2b1122e3], Optional[str], Optional[List[Error_d660d58]]) -> None
        """Represents a single step in the ingestion process of a new upload.

        :param name: 
        :type name: (optional) ask_smapi_model.v0.catalog.upload.ingestion_step_name.IngestionStepName
        :param status: 
        :type status: (optional) ask_smapi_model.v0.catalog.upload.ingestion_status.IngestionStatus
        :param log_url: Represents the url for the file containing logs of ingestion step.
        :type log_url: (optional) str
        :param errors: This array will contain the errors occurred during the execution of step. Will be empty, if execution succeeded.
        :type errors: (optional) list[ask_smapi_model.v0.error.Error]
        """
        self.__discriminator_value = None  # type: str

        self.name = name
        self.status = status
        self.log_url = log_url
        self.errors = errors

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
        if not isinstance(other, UploadIngestionStep):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other

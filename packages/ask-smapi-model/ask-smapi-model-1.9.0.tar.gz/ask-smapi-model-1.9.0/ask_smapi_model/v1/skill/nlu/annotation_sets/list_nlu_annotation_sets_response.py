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
    from ask_smapi_model.v1.skill.nlu.annotation_sets.pagination_context import PaginationContext as PaginationContext_c92f317b
    from ask_smapi_model.v1.skill.nlu.annotation_sets.links import Links as Links_2dc49e1a
    from ask_smapi_model.v1.skill.nlu.annotation_sets.annotation_set import AnnotationSet as AnnotationSet_b0768ac1


class ListNLUAnnotationSetsResponse(object):
    """

    :param annotation_sets: 
    :type annotation_sets: (optional) list[ask_smapi_model.v1.skill.nlu.annotation_sets.annotation_set.AnnotationSet]
    :param pagination_context: 
    :type pagination_context: (optional) ask_smapi_model.v1.skill.nlu.annotation_sets.pagination_context.PaginationContext
    :param links: 
    :type links: (optional) ask_smapi_model.v1.skill.nlu.annotation_sets.links.Links

    """
    deserialized_types = {
        'annotation_sets': 'list[ask_smapi_model.v1.skill.nlu.annotation_sets.annotation_set.AnnotationSet]',
        'pagination_context': 'ask_smapi_model.v1.skill.nlu.annotation_sets.pagination_context.PaginationContext',
        'links': 'ask_smapi_model.v1.skill.nlu.annotation_sets.links.Links'
    }  # type: Dict

    attribute_map = {
        'annotation_sets': 'annotationSets',
        'pagination_context': 'paginationContext',
        'links': '_links'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, annotation_sets=None, pagination_context=None, links=None):
        # type: (Optional[List[AnnotationSet_b0768ac1]], Optional[PaginationContext_c92f317b], Optional[Links_2dc49e1a]) -> None
        """

        :param annotation_sets: 
        :type annotation_sets: (optional) list[ask_smapi_model.v1.skill.nlu.annotation_sets.annotation_set.AnnotationSet]
        :param pagination_context: 
        :type pagination_context: (optional) ask_smapi_model.v1.skill.nlu.annotation_sets.pagination_context.PaginationContext
        :param links: 
        :type links: (optional) ask_smapi_model.v1.skill.nlu.annotation_sets.links.Links
        """
        self.__discriminator_value = None  # type: str

        self.annotation_sets = annotation_sets
        self.pagination_context = pagination_context
        self.links = links

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
        if not isinstance(other, ListNLUAnnotationSetsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other

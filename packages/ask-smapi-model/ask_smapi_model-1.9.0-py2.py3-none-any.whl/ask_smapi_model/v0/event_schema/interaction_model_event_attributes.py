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
    from ask_smapi_model.v0.event_schema.request_status import RequestStatus as RequestStatus_8267d453
    from ask_smapi_model.v0.event_schema.actor_attributes import ActorAttributes as ActorAttributes_a2b7ca5d
    from ask_smapi_model.v0.event_schema.subscription_attributes import SubscriptionAttributes as SubscriptionAttributes_ee385127
    from ask_smapi_model.v0.event_schema.interaction_model_attributes import InteractionModelAttributes as InteractionModelAttributes_179affa4


class InteractionModelEventAttributes(object):
    """
    Interaction model event specific attributes. 


    :param status: 
    :type status: (optional) ask_smapi_model.v0.event_schema.request_status.RequestStatus
    :param actor: 
    :type actor: (optional) ask_smapi_model.v0.event_schema.actor_attributes.ActorAttributes
    :param interaction_model: 
    :type interaction_model: (optional) ask_smapi_model.v0.event_schema.interaction_model_attributes.InteractionModelAttributes
    :param subscription: 
    :type subscription: (optional) ask_smapi_model.v0.event_schema.subscription_attributes.SubscriptionAttributes

    """
    deserialized_types = {
        'status': 'ask_smapi_model.v0.event_schema.request_status.RequestStatus',
        'actor': 'ask_smapi_model.v0.event_schema.actor_attributes.ActorAttributes',
        'interaction_model': 'ask_smapi_model.v0.event_schema.interaction_model_attributes.InteractionModelAttributes',
        'subscription': 'ask_smapi_model.v0.event_schema.subscription_attributes.SubscriptionAttributes'
    }  # type: Dict

    attribute_map = {
        'status': 'status',
        'actor': 'actor',
        'interaction_model': 'interactionModel',
        'subscription': 'subscription'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, status=None, actor=None, interaction_model=None, subscription=None):
        # type: (Optional[RequestStatus_8267d453], Optional[ActorAttributes_a2b7ca5d], Optional[InteractionModelAttributes_179affa4], Optional[SubscriptionAttributes_ee385127]) -> None
        """Interaction model event specific attributes. 

        :param status: 
        :type status: (optional) ask_smapi_model.v0.event_schema.request_status.RequestStatus
        :param actor: 
        :type actor: (optional) ask_smapi_model.v0.event_schema.actor_attributes.ActorAttributes
        :param interaction_model: 
        :type interaction_model: (optional) ask_smapi_model.v0.event_schema.interaction_model_attributes.InteractionModelAttributes
        :param subscription: 
        :type subscription: (optional) ask_smapi_model.v0.event_schema.subscription_attributes.SubscriptionAttributes
        """
        self.__discriminator_value = None  # type: str

        self.status = status
        self.actor = actor
        self.interaction_model = interaction_model
        self.subscription = subscription

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
        if not isinstance(other, InteractionModelEventAttributes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other

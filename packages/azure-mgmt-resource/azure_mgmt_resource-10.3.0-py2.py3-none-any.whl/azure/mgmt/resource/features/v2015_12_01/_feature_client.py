# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.service_client import SDKClient
from msrest import Serializer, Deserializer

from ._configuration import FeatureClientConfiguration
from .operations import FeatureClientOperationsMixin
from .operations import FeaturesOperations
from . import models


class FeatureClient(FeatureClientOperationsMixin, SDKClient):
    """Azure Feature Exposure Control (AFEC) provides a mechanism for the resource providers to control feature exposure to users. Resource providers typically use this mechanism to provide public/private preview for new features prior to making them generally available. Users need to explicitly register for AFEC features to get access to such functionality.

    :ivar config: Configuration for client.
    :vartype config: FeatureClientConfiguration

    :ivar features: Features operations
    :vartype features: azure.mgmt.resource.features.v2015_12_01.operations.FeaturesOperations

    :param credentials: Credentials needed for the client to connect to Azure.
    :type credentials: :mod:`A msrestazure Credentials
     object<msrestazure.azure_active_directory>`
    :param subscription_id: The ID of the target subscription.
    :type subscription_id: str
    :param str base_url: Service URL
    """

    def __init__(
            self, credentials, subscription_id, base_url=None):

        self.config = FeatureClientConfiguration(credentials, subscription_id, base_url)
        super(FeatureClient, self).__init__(self.config.credentials, self.config)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self.api_version = '2015-12-01'
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.features = FeaturesOperations(
            self._client, self.config, self._serialize, self._deserialize)

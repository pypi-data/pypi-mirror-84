# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .public_key_set import PublicKeySet
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RemoteJsonWebKeySet(PublicKeySet):
    """
    A set of public keys that is retrieved at run-time from a remote location
    to verify the JWT signature. The set should only contain JWK-formatted
    keys.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RemoteJsonWebKeySet object with values from keyword arguments. The default value of the :py:attr:`~oci.apigateway.models.RemoteJsonWebKeySet.type` attribute
        of this class is ``REMOTE_JWKS`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this RemoteJsonWebKeySet.
            Allowed values for this property are: "STATIC_KEYS", "REMOTE_JWKS"
        :type type: str

        :param uri:
            The value to assign to the uri property of this RemoteJsonWebKeySet.
        :type uri: str

        :param is_ssl_verify_disabled:
            The value to assign to the is_ssl_verify_disabled property of this RemoteJsonWebKeySet.
        :type is_ssl_verify_disabled: bool

        :param max_cache_duration_in_hours:
            The value to assign to the max_cache_duration_in_hours property of this RemoteJsonWebKeySet.
        :type max_cache_duration_in_hours: int

        """
        self.swagger_types = {
            'type': 'str',
            'uri': 'str',
            'is_ssl_verify_disabled': 'bool',
            'max_cache_duration_in_hours': 'int'
        }

        self.attribute_map = {
            'type': 'type',
            'uri': 'uri',
            'is_ssl_verify_disabled': 'isSslVerifyDisabled',
            'max_cache_duration_in_hours': 'maxCacheDurationInHours'
        }

        self._type = None
        self._uri = None
        self._is_ssl_verify_disabled = None
        self._max_cache_duration_in_hours = None
        self._type = 'REMOTE_JWKS'

    @property
    def uri(self):
        """
        **[Required]** Gets the uri of this RemoteJsonWebKeySet.
        The uri from which to retrieve the key. It must be accessible
        without authentication.


        :return: The uri of this RemoteJsonWebKeySet.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """
        Sets the uri of this RemoteJsonWebKeySet.
        The uri from which to retrieve the key. It must be accessible
        without authentication.


        :param uri: The uri of this RemoteJsonWebKeySet.
        :type: str
        """
        self._uri = uri

    @property
    def is_ssl_verify_disabled(self):
        """
        Gets the is_ssl_verify_disabled of this RemoteJsonWebKeySet.
        Defines whether or not to uphold SSL verification.


        :return: The is_ssl_verify_disabled of this RemoteJsonWebKeySet.
        :rtype: bool
        """
        return self._is_ssl_verify_disabled

    @is_ssl_verify_disabled.setter
    def is_ssl_verify_disabled(self, is_ssl_verify_disabled):
        """
        Sets the is_ssl_verify_disabled of this RemoteJsonWebKeySet.
        Defines whether or not to uphold SSL verification.


        :param is_ssl_verify_disabled: The is_ssl_verify_disabled of this RemoteJsonWebKeySet.
        :type: bool
        """
        self._is_ssl_verify_disabled = is_ssl_verify_disabled

    @property
    def max_cache_duration_in_hours(self):
        """
        Gets the max_cache_duration_in_hours of this RemoteJsonWebKeySet.
        The duration for which the JWKS should be cached before it is
        fetched again.


        :return: The max_cache_duration_in_hours of this RemoteJsonWebKeySet.
        :rtype: int
        """
        return self._max_cache_duration_in_hours

    @max_cache_duration_in_hours.setter
    def max_cache_duration_in_hours(self, max_cache_duration_in_hours):
        """
        Sets the max_cache_duration_in_hours of this RemoteJsonWebKeySet.
        The duration for which the JWKS should be cached before it is
        fetched again.


        :param max_cache_duration_in_hours: The max_cache_duration_in_hours of this RemoteJsonWebKeySet.
        :type: int
        """
        self._max_cache_duration_in_hours = max_cache_duration_in_hours

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

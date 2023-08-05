# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VaultUsage(object):
    """
    VaultUsage model.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new VaultUsage object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param key_count:
            The value to assign to the key_count property of this VaultUsage.
        :type key_count: int

        :param key_version_count:
            The value to assign to the key_version_count property of this VaultUsage.
        :type key_version_count: int

        :param software_key_count:
            The value to assign to the software_key_count property of this VaultUsage.
        :type software_key_count: int

        :param software_key_version_count:
            The value to assign to the software_key_version_count property of this VaultUsage.
        :type software_key_version_count: int

        """
        self.swagger_types = {
            'key_count': 'int',
            'key_version_count': 'int',
            'software_key_count': 'int',
            'software_key_version_count': 'int'
        }

        self.attribute_map = {
            'key_count': 'keyCount',
            'key_version_count': 'keyVersionCount',
            'software_key_count': 'softwareKeyCount',
            'software_key_version_count': 'softwareKeyVersionCount'
        }

        self._key_count = None
        self._key_version_count = None
        self._software_key_count = None
        self._software_key_version_count = None

    @property
    def key_count(self):
        """
        **[Required]** Gets the key_count of this VaultUsage.
        The number of keys in this vault that persist on a hardware security module (HSM), across all compartments, excluding keys in a `DELETED` state.


        :return: The key_count of this VaultUsage.
        :rtype: int
        """
        return self._key_count

    @key_count.setter
    def key_count(self, key_count):
        """
        Sets the key_count of this VaultUsage.
        The number of keys in this vault that persist on a hardware security module (HSM), across all compartments, excluding keys in a `DELETED` state.


        :param key_count: The key_count of this VaultUsage.
        :type: int
        """
        self._key_count = key_count

    @property
    def key_version_count(self):
        """
        **[Required]** Gets the key_version_count of this VaultUsage.
        The number of key versions in this vault that persist on a hardware security module (HSM), across all compartments, excluding key versions in a `DELETED` state.


        :return: The key_version_count of this VaultUsage.
        :rtype: int
        """
        return self._key_version_count

    @key_version_count.setter
    def key_version_count(self, key_version_count):
        """
        Sets the key_version_count of this VaultUsage.
        The number of key versions in this vault that persist on a hardware security module (HSM), across all compartments, excluding key versions in a `DELETED` state.


        :param key_version_count: The key_version_count of this VaultUsage.
        :type: int
        """
        self._key_version_count = key_version_count

    @property
    def software_key_count(self):
        """
        Gets the software_key_count of this VaultUsage.
        The number of keys in this vault that persist on the server, across all compartments, excluding keys in a `DELETED` state.


        :return: The software_key_count of this VaultUsage.
        :rtype: int
        """
        return self._software_key_count

    @software_key_count.setter
    def software_key_count(self, software_key_count):
        """
        Sets the software_key_count of this VaultUsage.
        The number of keys in this vault that persist on the server, across all compartments, excluding keys in a `DELETED` state.


        :param software_key_count: The software_key_count of this VaultUsage.
        :type: int
        """
        self._software_key_count = software_key_count

    @property
    def software_key_version_count(self):
        """
        Gets the software_key_version_count of this VaultUsage.
        The number of key versions in this vault that persist on the server, across all compartments, excluding key versions in a `DELETED` state.


        :return: The software_key_version_count of this VaultUsage.
        :rtype: int
        """
        return self._software_key_version_count

    @software_key_version_count.setter
    def software_key_version_count(self, software_key_version_count):
        """
        Sets the software_key_version_count of this VaultUsage.
        The number of key versions in this vault that persist on the server, across all compartments, excluding key versions in a `DELETED` state.


        :param software_key_version_count: The software_key_version_count of this VaultUsage.
        :type: int
        """
        self._software_key_version_count = software_key_version_count

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

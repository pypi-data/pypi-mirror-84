# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RRSet(object):
    """
    A collection of DNS records of the same domain and type. For more
    information about record types, see `Resource Record (RR) TYPEs`__.

    __ https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml#dns-parameters-4
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RRSet object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param items:
            The value to assign to the items property of this RRSet.
        :type items: list[Record]

        """
        self.swagger_types = {
            'items': 'list[Record]'
        }

        self.attribute_map = {
            'items': 'items'
        }

        self._items = None

    @property
    def items(self):
        """
        Gets the items of this RRSet.

        :return: The items of this RRSet.
        :rtype: list[Record]
        """
        return self._items

    @items.setter
    def items(self, items):
        """
        Sets the items of this RRSet.

        :param items: The items of this RRSet.
        :type: list[Record]
        """
        self._items = items

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

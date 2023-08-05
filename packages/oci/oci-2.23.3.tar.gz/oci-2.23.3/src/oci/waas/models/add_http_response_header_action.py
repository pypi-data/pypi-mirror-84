# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .header_manipulation_action import HeaderManipulationAction
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddHttpResponseHeaderAction(HeaderManipulationAction):
    """
    An object that represents the action of replacing or adding a header field.
    All prior occurrences of the header with the given name are removed and then the header field with specified value is added.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AddHttpResponseHeaderAction object with values from keyword arguments. The default value of the :py:attr:`~oci.waas.models.AddHttpResponseHeaderAction.action` attribute
        of this class is ``ADD_HTTP_RESPONSE_HEADER`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param action:
            The value to assign to the action property of this AddHttpResponseHeaderAction.
            Allowed values for this property are: "EXTEND_HTTP_RESPONSE_HEADER", "ADD_HTTP_RESPONSE_HEADER", "REMOVE_HTTP_RESPONSE_HEADER"
        :type action: str

        :param header:
            The value to assign to the header property of this AddHttpResponseHeaderAction.
        :type header: str

        :param value:
            The value to assign to the value property of this AddHttpResponseHeaderAction.
        :type value: str

        """
        self.swagger_types = {
            'action': 'str',
            'header': 'str',
            'value': 'str'
        }

        self.attribute_map = {
            'action': 'action',
            'header': 'header',
            'value': 'value'
        }

        self._action = None
        self._header = None
        self._value = None
        self._action = 'ADD_HTTP_RESPONSE_HEADER'

    @property
    def header(self):
        """
        **[Required]** Gets the header of this AddHttpResponseHeaderAction.
        A header field name that conforms to RFC 7230.

        Example: `example_header_name`


        :return: The header of this AddHttpResponseHeaderAction.
        :rtype: str
        """
        return self._header

    @header.setter
    def header(self, header):
        """
        Sets the header of this AddHttpResponseHeaderAction.
        A header field name that conforms to RFC 7230.

        Example: `example_header_name`


        :param header: The header of this AddHttpResponseHeaderAction.
        :type: str
        """
        self._header = header

    @property
    def value(self):
        """
        **[Required]** Gets the value of this AddHttpResponseHeaderAction.
        A header field value that conforms to RFC 7230.

        Example: `example_value`


        :return: The value of this AddHttpResponseHeaderAction.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this AddHttpResponseHeaderAction.
        A header field value that conforms to RFC 7230.

        Example: `example_value`


        :param value: The value of this AddHttpResponseHeaderAction.
        :type: str
        """
        self._value = value

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

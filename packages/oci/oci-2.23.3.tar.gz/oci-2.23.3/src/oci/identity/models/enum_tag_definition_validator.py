# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .base_tag_definition_validator import BaseTagDefinitionValidator
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class EnumTagDefinitionValidator(BaseTagDefinitionValidator):
    """
    Used to validate the value set for a defined tag and contains the list of allowable `values`.

    You must specify at least one valid value in the `values` array. You can't have blank or
    or empty strings (`\"\"`). Duplicate values are not allowed.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new EnumTagDefinitionValidator object with values from keyword arguments. The default value of the :py:attr:`~oci.identity.models.EnumTagDefinitionValidator.validator_type` attribute
        of this class is ``ENUM`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param validator_type:
            The value to assign to the validator_type property of this EnumTagDefinitionValidator.
            Allowed values for this property are: "ENUM", "DEFAULT"
        :type validator_type: str

        :param values:
            The value to assign to the values property of this EnumTagDefinitionValidator.
        :type values: list[str]

        """
        self.swagger_types = {
            'validator_type': 'str',
            'values': 'list[str]'
        }

        self.attribute_map = {
            'validator_type': 'validatorType',
            'values': 'values'
        }

        self._validator_type = None
        self._values = None
        self._validator_type = 'ENUM'

    @property
    def values(self):
        """
        Gets the values of this EnumTagDefinitionValidator.
        The list of allowed values for a definedTag value.


        :return: The values of this EnumTagDefinitionValidator.
        :rtype: list[str]
        """
        return self._values

    @values.setter
    def values(self, values):
        """
        Sets the values of this EnumTagDefinitionValidator.
        The list of allowed values for a definedTag value.


        :param values: The values of this EnumTagDefinitionValidator.
        :type: list[str]
        """
        self._values = values

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

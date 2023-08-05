# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .typed_object import TypedObject
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class OutputField(TypedObject):
    """
    Output fields of an operator.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new OutputField object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.OutputField.model_type` attribute
        of this class is ``OUTPUT_FIELD`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this OutputField.
            Allowed values for this property are: "SHAPE", "INPUT_PORT", "SHAPE_FIELD", "INPUT_FIELD", "DERIVED_FIELD", "MACRO_FIELD", "OUTPUT_FIELD", "DYNAMIC_PROXY_FIELD", "OUTPUT_PORT", "DYNAMIC_INPUT_FIELD", "PROXY_FIELD", "PARAMETER"
        :type model_type: str

        :param key:
            The value to assign to the key property of this OutputField.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this OutputField.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this OutputField.
        :type parent_ref: ParentReference

        :param config_values:
            The value to assign to the config_values property of this OutputField.
        :type config_values: ConfigValues

        :param object_status:
            The value to assign to the object_status property of this OutputField.
        :type object_status: int

        :param name:
            The value to assign to the name property of this OutputField.
        :type name: str

        :param description:
            The value to assign to the description property of this OutputField.
        :type description: str

        :param type:
            The value to assign to the type property of this OutputField.
        :type type: BaseType

        :param labels:
            The value to assign to the labels property of this OutputField.
        :type labels: list[str]

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'config_values': 'ConfigValues',
            'object_status': 'int',
            'name': 'str',
            'description': 'str',
            'type': 'BaseType',
            'labels': 'list[str]'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'config_values': 'configValues',
            'object_status': 'objectStatus',
            'name': 'name',
            'description': 'description',
            'type': 'type',
            'labels': 'labels'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._config_values = None
        self._object_status = None
        self._name = None
        self._description = None
        self._type = None
        self._labels = None
        self._model_type = 'OUTPUT_FIELD'

    @property
    def type(self):
        """
        Gets the type of this OutputField.

        :return: The type of this OutputField.
        :rtype: BaseType
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this OutputField.

        :param type: The type of this OutputField.
        :type: BaseType
        """
        self._type = type

    @property
    def labels(self):
        """
        Gets the labels of this OutputField.
        Labels are keywords or labels that you can add to data assets, dataflows and so on. You can define your own labels and use them to categorize content.


        :return: The labels of this OutputField.
        :rtype: list[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """
        Sets the labels of this OutputField.
        Labels are keywords or labels that you can add to data assets, dataflows and so on. You can define your own labels and use them to categorize content.


        :param labels: The labels of this OutputField.
        :type: list[str]
        """
        self._labels = labels

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

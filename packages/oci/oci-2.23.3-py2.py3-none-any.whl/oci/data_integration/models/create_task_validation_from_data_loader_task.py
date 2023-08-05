# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_task_validation_details import CreateTaskValidationDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateTaskValidationFromDataLoaderTask(CreateTaskValidationDetails):
    """
    The information about a data flow task.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateTaskValidationFromDataLoaderTask object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.CreateTaskValidationFromDataLoaderTask.model_type` attribute
        of this class is ``DATA_LOADER_TASK`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this CreateTaskValidationFromDataLoaderTask.
            Allowed values for this property are: "INTEGRATION_TASK", "DATA_LOADER_TASK"
        :type model_type: str

        :param key:
            The value to assign to the key property of this CreateTaskValidationFromDataLoaderTask.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this CreateTaskValidationFromDataLoaderTask.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this CreateTaskValidationFromDataLoaderTask.
        :type parent_ref: ParentReference

        :param name:
            The value to assign to the name property of this CreateTaskValidationFromDataLoaderTask.
        :type name: str

        :param description:
            The value to assign to the description property of this CreateTaskValidationFromDataLoaderTask.
        :type description: str

        :param object_version:
            The value to assign to the object_version property of this CreateTaskValidationFromDataLoaderTask.
        :type object_version: int

        :param object_status:
            The value to assign to the object_status property of this CreateTaskValidationFromDataLoaderTask.
        :type object_status: int

        :param identifier:
            The value to assign to the identifier property of this CreateTaskValidationFromDataLoaderTask.
        :type identifier: str

        :param input_ports:
            The value to assign to the input_ports property of this CreateTaskValidationFromDataLoaderTask.
        :type input_ports: list[InputPort]

        :param output_ports:
            The value to assign to the output_ports property of this CreateTaskValidationFromDataLoaderTask.
        :type output_ports: list[OutputPort]

        :param parameters:
            The value to assign to the parameters property of this CreateTaskValidationFromDataLoaderTask.
        :type parameters: list[Parameter]

        :param op_config_values:
            The value to assign to the op_config_values property of this CreateTaskValidationFromDataLoaderTask.
        :type op_config_values: ConfigValues

        :param config_provider_delegate:
            The value to assign to the config_provider_delegate property of this CreateTaskValidationFromDataLoaderTask.
        :type config_provider_delegate: ConfigProvider

        :param metadata:
            The value to assign to the metadata property of this CreateTaskValidationFromDataLoaderTask.
        :type metadata: ObjectMetadata

        :param data_flow:
            The value to assign to the data_flow property of this CreateTaskValidationFromDataLoaderTask.
        :type data_flow: DataFlow

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'name': 'str',
            'description': 'str',
            'object_version': 'int',
            'object_status': 'int',
            'identifier': 'str',
            'input_ports': 'list[InputPort]',
            'output_ports': 'list[OutputPort]',
            'parameters': 'list[Parameter]',
            'op_config_values': 'ConfigValues',
            'config_provider_delegate': 'ConfigProvider',
            'metadata': 'ObjectMetadata',
            'data_flow': 'DataFlow'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'name': 'name',
            'description': 'description',
            'object_version': 'objectVersion',
            'object_status': 'objectStatus',
            'identifier': 'identifier',
            'input_ports': 'inputPorts',
            'output_ports': 'outputPorts',
            'parameters': 'parameters',
            'op_config_values': 'opConfigValues',
            'config_provider_delegate': 'configProviderDelegate',
            'metadata': 'metadata',
            'data_flow': 'dataFlow'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._name = None
        self._description = None
        self._object_version = None
        self._object_status = None
        self._identifier = None
        self._input_ports = None
        self._output_ports = None
        self._parameters = None
        self._op_config_values = None
        self._config_provider_delegate = None
        self._metadata = None
        self._data_flow = None
        self._model_type = 'DATA_LOADER_TASK'

    @property
    def data_flow(self):
        """
        Gets the data_flow of this CreateTaskValidationFromDataLoaderTask.

        :return: The data_flow of this CreateTaskValidationFromDataLoaderTask.
        :rtype: DataFlow
        """
        return self._data_flow

    @data_flow.setter
    def data_flow(self, data_flow):
        """
        Sets the data_flow of this CreateTaskValidationFromDataLoaderTask.

        :param data_flow: The data_flow of this CreateTaskValidationFromDataLoaderTask.
        :type: DataFlow
        """
        self._data_flow = data_flow

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

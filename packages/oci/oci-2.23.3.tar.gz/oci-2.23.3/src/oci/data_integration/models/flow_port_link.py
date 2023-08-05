# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class FlowPortLink(object):
    """
    Details about the link between two data flow operators.
    """

    #: A constant which can be used with the model_type property of a FlowPortLink.
    #: This constant has a value of "CONDITIONAL_INPUT_LINK"
    MODEL_TYPE_CONDITIONAL_INPUT_LINK = "CONDITIONAL_INPUT_LINK"

    #: A constant which can be used with the model_type property of a FlowPortLink.
    #: This constant has a value of "OUTPUT_LINK"
    MODEL_TYPE_OUTPUT_LINK = "OUTPUT_LINK"

    #: A constant which can be used with the model_type property of a FlowPortLink.
    #: This constant has a value of "INPUT_LINK"
    MODEL_TYPE_INPUT_LINK = "INPUT_LINK"

    def __init__(self, **kwargs):
        """
        Initializes a new FlowPortLink object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.data_integration.models.InputLink`
        * :class:`~oci.data_integration.models.OutputLink`
        * :class:`~oci.data_integration.models.ConditionalInputLink`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this FlowPortLink.
            Allowed values for this property are: "CONDITIONAL_INPUT_LINK", "OUTPUT_LINK", "INPUT_LINK"
        :type model_type: str

        :param key:
            The value to assign to the key property of this FlowPortLink.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this FlowPortLink.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this FlowPortLink.
        :type parent_ref: ParentReference

        :param object_status:
            The value to assign to the object_status property of this FlowPortLink.
        :type object_status: int

        :param description:
            The value to assign to the description property of this FlowPortLink.
        :type description: str

        :param port:
            The value to assign to the port property of this FlowPortLink.
        :type port: str

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'object_status': 'int',
            'description': 'str',
            'port': 'str'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'object_status': 'objectStatus',
            'description': 'description',
            'port': 'port'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._object_status = None
        self._description = None
        self._port = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['modelType']

        if type == 'INPUT_LINK':
            return 'InputLink'

        if type == 'OUTPUT_LINK':
            return 'OutputLink'

        if type == 'CONDITIONAL_INPUT_LINK':
            return 'ConditionalInputLink'
        else:
            return 'FlowPortLink'

    @property
    def model_type(self):
        """
        **[Required]** Gets the model_type of this FlowPortLink.
        The model type of the object.

        Allowed values for this property are: "CONDITIONAL_INPUT_LINK", "OUTPUT_LINK", "INPUT_LINK"


        :return: The model_type of this FlowPortLink.
        :rtype: str
        """
        return self._model_type

    @model_type.setter
    def model_type(self, model_type):
        """
        Sets the model_type of this FlowPortLink.
        The model type of the object.


        :param model_type: The model_type of this FlowPortLink.
        :type: str
        """
        allowed_values = ["CONDITIONAL_INPUT_LINK", "OUTPUT_LINK", "INPUT_LINK"]
        if not value_allowed_none_or_none_sentinel(model_type, allowed_values):
            raise ValueError(
                "Invalid value for `model_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._model_type = model_type

    @property
    def key(self):
        """
        Gets the key of this FlowPortLink.
        The key of the object.


        :return: The key of this FlowPortLink.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this FlowPortLink.
        The key of the object.


        :param key: The key of this FlowPortLink.
        :type: str
        """
        self._key = key

    @property
    def model_version(self):
        """
        Gets the model_version of this FlowPortLink.
        The model version of an object.


        :return: The model_version of this FlowPortLink.
        :rtype: str
        """
        return self._model_version

    @model_version.setter
    def model_version(self, model_version):
        """
        Sets the model_version of this FlowPortLink.
        The model version of an object.


        :param model_version: The model_version of this FlowPortLink.
        :type: str
        """
        self._model_version = model_version

    @property
    def parent_ref(self):
        """
        Gets the parent_ref of this FlowPortLink.

        :return: The parent_ref of this FlowPortLink.
        :rtype: ParentReference
        """
        return self._parent_ref

    @parent_ref.setter
    def parent_ref(self, parent_ref):
        """
        Sets the parent_ref of this FlowPortLink.

        :param parent_ref: The parent_ref of this FlowPortLink.
        :type: ParentReference
        """
        self._parent_ref = parent_ref

    @property
    def object_status(self):
        """
        Gets the object_status of this FlowPortLink.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :return: The object_status of this FlowPortLink.
        :rtype: int
        """
        return self._object_status

    @object_status.setter
    def object_status(self, object_status):
        """
        Sets the object_status of this FlowPortLink.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :param object_status: The object_status of this FlowPortLink.
        :type: int
        """
        self._object_status = object_status

    @property
    def description(self):
        """
        Gets the description of this FlowPortLink.
        Detailed description for the object.


        :return: The description of this FlowPortLink.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this FlowPortLink.
        Detailed description for the object.


        :param description: The description of this FlowPortLink.
        :type: str
        """
        self._description = description

    @property
    def port(self):
        """
        Gets the port of this FlowPortLink.
        Key of FlowPort reference


        :return: The port of this FlowPortLink.
        :rtype: str
        """
        return self._port

    @port.setter
    def port(self, port):
        """
        Sets the port of this FlowPortLink.
        Key of FlowPort reference


        :param port: The port of this FlowPortLink.
        :type: str
        """
        self._port = port

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

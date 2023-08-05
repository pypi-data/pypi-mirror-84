# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .key import Key
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ForeignKey(Key):
    """
    The foreign key object.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ForeignKey object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.ForeignKey.model_type` attribute
        of this class is ``FOREIGN_KEY`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this ForeignKey.
            Allowed values for this property are: "FOREIGN_KEY", "PRIMARY_KEY", "UNIQUE_KEY"
        :type model_type: str

        :param key:
            The value to assign to the key property of this ForeignKey.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this ForeignKey.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this ForeignKey.
        :type parent_ref: ParentReference

        :param name:
            The value to assign to the name property of this ForeignKey.
        :type name: str

        :param attribute_refs:
            The value to assign to the attribute_refs property of this ForeignKey.
        :type attribute_refs: list[KeyAttribute]

        :param update_rule:
            The value to assign to the update_rule property of this ForeignKey.
        :type update_rule: int

        :param delete_rule:
            The value to assign to the delete_rule property of this ForeignKey.
        :type delete_rule: int

        :param reference_unique_key:
            The value to assign to the reference_unique_key property of this ForeignKey.
        :type reference_unique_key: UniqueKey

        :param object_status:
            The value to assign to the object_status property of this ForeignKey.
        :type object_status: int

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'name': 'str',
            'attribute_refs': 'list[KeyAttribute]',
            'update_rule': 'int',
            'delete_rule': 'int',
            'reference_unique_key': 'UniqueKey',
            'object_status': 'int'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'name': 'name',
            'attribute_refs': 'attributeRefs',
            'update_rule': 'updateRule',
            'delete_rule': 'deleteRule',
            'reference_unique_key': 'referenceUniqueKey',
            'object_status': 'objectStatus'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._name = None
        self._attribute_refs = None
        self._update_rule = None
        self._delete_rule = None
        self._reference_unique_key = None
        self._object_status = None
        self._model_type = 'FOREIGN_KEY'

    @property
    def key(self):
        """
        Gets the key of this ForeignKey.
        The object key.


        :return: The key of this ForeignKey.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this ForeignKey.
        The object key.


        :param key: The key of this ForeignKey.
        :type: str
        """
        self._key = key

    @property
    def model_version(self):
        """
        Gets the model_version of this ForeignKey.
        The object's model version.


        :return: The model_version of this ForeignKey.
        :rtype: str
        """
        return self._model_version

    @model_version.setter
    def model_version(self, model_version):
        """
        Sets the model_version of this ForeignKey.
        The object's model version.


        :param model_version: The model_version of this ForeignKey.
        :type: str
        """
        self._model_version = model_version

    @property
    def parent_ref(self):
        """
        Gets the parent_ref of this ForeignKey.

        :return: The parent_ref of this ForeignKey.
        :rtype: ParentReference
        """
        return self._parent_ref

    @parent_ref.setter
    def parent_ref(self, parent_ref):
        """
        Sets the parent_ref of this ForeignKey.

        :param parent_ref: The parent_ref of this ForeignKey.
        :type: ParentReference
        """
        self._parent_ref = parent_ref

    @property
    def name(self):
        """
        Gets the name of this ForeignKey.
        Free form text without any restriction on permitted characters. Name can have letters, numbers, and special characters. The value is editable and is restricted to 1000 characters.


        :return: The name of this ForeignKey.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ForeignKey.
        Free form text without any restriction on permitted characters. Name can have letters, numbers, and special characters. The value is editable and is restricted to 1000 characters.


        :param name: The name of this ForeignKey.
        :type: str
        """
        self._name = name

    @property
    def attribute_refs(self):
        """
        Gets the attribute_refs of this ForeignKey.
        An array of attribute references.


        :return: The attribute_refs of this ForeignKey.
        :rtype: list[KeyAttribute]
        """
        return self._attribute_refs

    @attribute_refs.setter
    def attribute_refs(self, attribute_refs):
        """
        Sets the attribute_refs of this ForeignKey.
        An array of attribute references.


        :param attribute_refs: The attribute_refs of this ForeignKey.
        :type: list[KeyAttribute]
        """
        self._attribute_refs = attribute_refs

    @property
    def update_rule(self):
        """
        Gets the update_rule of this ForeignKey.
        The update rule.


        :return: The update_rule of this ForeignKey.
        :rtype: int
        """
        return self._update_rule

    @update_rule.setter
    def update_rule(self, update_rule):
        """
        Sets the update_rule of this ForeignKey.
        The update rule.


        :param update_rule: The update_rule of this ForeignKey.
        :type: int
        """
        self._update_rule = update_rule

    @property
    def delete_rule(self):
        """
        Gets the delete_rule of this ForeignKey.
        The delete rule.


        :return: The delete_rule of this ForeignKey.
        :rtype: int
        """
        return self._delete_rule

    @delete_rule.setter
    def delete_rule(self, delete_rule):
        """
        Sets the delete_rule of this ForeignKey.
        The delete rule.


        :param delete_rule: The delete_rule of this ForeignKey.
        :type: int
        """
        self._delete_rule = delete_rule

    @property
    def reference_unique_key(self):
        """
        Gets the reference_unique_key of this ForeignKey.

        :return: The reference_unique_key of this ForeignKey.
        :rtype: UniqueKey
        """
        return self._reference_unique_key

    @reference_unique_key.setter
    def reference_unique_key(self, reference_unique_key):
        """
        Sets the reference_unique_key of this ForeignKey.

        :param reference_unique_key: The reference_unique_key of this ForeignKey.
        :type: UniqueKey
        """
        self._reference_unique_key = reference_unique_key

    @property
    def object_status(self):
        """
        Gets the object_status of this ForeignKey.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :return: The object_status of this ForeignKey.
        :rtype: int
        """
        return self._object_status

    @object_status.setter
    def object_status(self, object_status):
        """
        Sets the object_status of this ForeignKey.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :param object_status: The object_status of this ForeignKey.
        :type: int
        """
        self._object_status = object_status

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

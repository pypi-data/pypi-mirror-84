# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateZoneBaseDetails(object):
    """
    The body for either defining a new zone or migrating a zone from migrationSource. This is determined by the migrationSource discriminator.
    NONE indicates creation of a new zone (default). DYNECT indicates migration from a DynECT zone.

    **Warning:** Oracle recommends that you avoid using any confidential information when you supply string values using the API.
    """

    #: A constant which can be used with the migration_source property of a CreateZoneBaseDetails.
    #: This constant has a value of "NONE"
    MIGRATION_SOURCE_NONE = "NONE"

    #: A constant which can be used with the migration_source property of a CreateZoneBaseDetails.
    #: This constant has a value of "DYNECT"
    MIGRATION_SOURCE_DYNECT = "DYNECT"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateZoneBaseDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.dns.models.CreateZoneDetails`
        * :class:`~oci.dns.models.CreateMigratedDynectZoneDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param migration_source:
            The value to assign to the migration_source property of this CreateZoneBaseDetails.
            Allowed values for this property are: "NONE", "DYNECT"
        :type migration_source: str

        :param name:
            The value to assign to the name property of this CreateZoneBaseDetails.
        :type name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateZoneBaseDetails.
        :type compartment_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateZoneBaseDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateZoneBaseDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'migration_source': 'str',
            'name': 'str',
            'compartment_id': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'migration_source': 'migrationSource',
            'name': 'name',
            'compartment_id': 'compartmentId',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._migration_source = None
        self._name = None
        self._compartment_id = None
        self._freeform_tags = None
        self._defined_tags = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['migrationSource']

        if type == 'NONE':
            return 'CreateZoneDetails'

        if type == 'DYNECT':
            return 'CreateMigratedDynectZoneDetails'
        else:
            return 'CreateZoneBaseDetails'

    @property
    def migration_source(self):
        """
        Gets the migration_source of this CreateZoneBaseDetails.
        Discriminator that is used to determine whether to create a new zone (NONE) or to migrate an existing DynECT zone (DYNECT).

        Allowed values for this property are: "NONE", "DYNECT"


        :return: The migration_source of this CreateZoneBaseDetails.
        :rtype: str
        """
        return self._migration_source

    @migration_source.setter
    def migration_source(self, migration_source):
        """
        Sets the migration_source of this CreateZoneBaseDetails.
        Discriminator that is used to determine whether to create a new zone (NONE) or to migrate an existing DynECT zone (DYNECT).


        :param migration_source: The migration_source of this CreateZoneBaseDetails.
        :type: str
        """
        allowed_values = ["NONE", "DYNECT"]
        if not value_allowed_none_or_none_sentinel(migration_source, allowed_values):
            raise ValueError(
                "Invalid value for `migration_source`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._migration_source = migration_source

    @property
    def name(self):
        """
        **[Required]** Gets the name of this CreateZoneBaseDetails.
        The name of the zone.


        :return: The name of this CreateZoneBaseDetails.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CreateZoneBaseDetails.
        The name of the zone.


        :param name: The name of this CreateZoneBaseDetails.
        :type: str
        """
        self._name = name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateZoneBaseDetails.
        The OCID of the compartment containing the zone.


        :return: The compartment_id of this CreateZoneBaseDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateZoneBaseDetails.
        The OCID of the compartment containing the zone.


        :param compartment_id: The compartment_id of this CreateZoneBaseDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateZoneBaseDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.


        **Example:** `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CreateZoneBaseDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateZoneBaseDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.


        **Example:** `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CreateZoneBaseDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateZoneBaseDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.


        **Example:** `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CreateZoneBaseDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateZoneBaseDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.


        **Example:** `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CreateZoneBaseDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

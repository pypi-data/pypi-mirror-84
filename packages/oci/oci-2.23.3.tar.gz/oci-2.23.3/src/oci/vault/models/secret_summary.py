# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SecretSummary(object):
    """
    The details of the secret, excluding the contents of the secret.
    """

    #: A constant which can be used with the lifecycle_state property of a SecretSummary.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a SecretSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a SecretSummary.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a SecretSummary.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a SecretSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a SecretSummary.
    #: This constant has a value of "SCHEDULING_DELETION"
    LIFECYCLE_STATE_SCHEDULING_DELETION = "SCHEDULING_DELETION"

    #: A constant which can be used with the lifecycle_state property of a SecretSummary.
    #: This constant has a value of "PENDING_DELETION"
    LIFECYCLE_STATE_PENDING_DELETION = "PENDING_DELETION"

    #: A constant which can be used with the lifecycle_state property of a SecretSummary.
    #: This constant has a value of "CANCELLING_DELETION"
    LIFECYCLE_STATE_CANCELLING_DELETION = "CANCELLING_DELETION"

    #: A constant which can be used with the lifecycle_state property of a SecretSummary.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new SecretSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this SecretSummary.
        :type compartment_id: str

        :param defined_tags:
            The value to assign to the defined_tags property of this SecretSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param description:
            The value to assign to the description property of this SecretSummary.
        :type description: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this SecretSummary.
        :type freeform_tags: dict(str, str)

        :param key_id:
            The value to assign to the key_id property of this SecretSummary.
        :type key_id: str

        :param id:
            The value to assign to the id property of this SecretSummary.
        :type id: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this SecretSummary.
        :type lifecycle_details: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this SecretSummary.
            Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "SCHEDULING_DELETION", "PENDING_DELETION", "CANCELLING_DELETION", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param secret_name:
            The value to assign to the secret_name property of this SecretSummary.
        :type secret_name: str

        :param time_created:
            The value to assign to the time_created property of this SecretSummary.
        :type time_created: datetime

        :param time_of_current_version_expiry:
            The value to assign to the time_of_current_version_expiry property of this SecretSummary.
        :type time_of_current_version_expiry: datetime

        :param time_of_deletion:
            The value to assign to the time_of_deletion property of this SecretSummary.
        :type time_of_deletion: datetime

        :param vault_id:
            The value to assign to the vault_id property of this SecretSummary.
        :type vault_id: str

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'defined_tags': 'dict(str, dict(str, object))',
            'description': 'str',
            'freeform_tags': 'dict(str, str)',
            'key_id': 'str',
            'id': 'str',
            'lifecycle_details': 'str',
            'lifecycle_state': 'str',
            'secret_name': 'str',
            'time_created': 'datetime',
            'time_of_current_version_expiry': 'datetime',
            'time_of_deletion': 'datetime',
            'vault_id': 'str'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'defined_tags': 'definedTags',
            'description': 'description',
            'freeform_tags': 'freeformTags',
            'key_id': 'keyId',
            'id': 'id',
            'lifecycle_details': 'lifecycleDetails',
            'lifecycle_state': 'lifecycleState',
            'secret_name': 'secretName',
            'time_created': 'timeCreated',
            'time_of_current_version_expiry': 'timeOfCurrentVersionExpiry',
            'time_of_deletion': 'timeOfDeletion',
            'vault_id': 'vaultId'
        }

        self._compartment_id = None
        self._defined_tags = None
        self._description = None
        self._freeform_tags = None
        self._key_id = None
        self._id = None
        self._lifecycle_details = None
        self._lifecycle_state = None
        self._secret_name = None
        self._time_created = None
        self._time_of_current_version_expiry = None
        self._time_of_deletion = None
        self._vault_id = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this SecretSummary.
        The OCID of the compartment that contains the secret.


        :return: The compartment_id of this SecretSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this SecretSummary.
        The OCID of the compartment that contains the secret.


        :param compartment_id: The compartment_id of this SecretSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this SecretSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this SecretSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this SecretSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this SecretSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def description(self):
        """
        Gets the description of this SecretSummary.
        A brief description of the secret.


        :return: The description of this SecretSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this SecretSummary.
        A brief description of the secret.


        :param description: The description of this SecretSummary.
        :type: str
        """
        self._description = description

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this SecretSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this SecretSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this SecretSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this SecretSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def key_id(self):
        """
        Gets the key_id of this SecretSummary.
        The OCID of the master encryption key that is used to encrypt the secret.


        :return: The key_id of this SecretSummary.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """
        Sets the key_id of this SecretSummary.
        The OCID of the master encryption key that is used to encrypt the secret.


        :param key_id: The key_id of this SecretSummary.
        :type: str
        """
        self._key_id = key_id

    @property
    def id(self):
        """
        **[Required]** Gets the id of this SecretSummary.
        The OCID of the secret.


        :return: The id of this SecretSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SecretSummary.
        The OCID of the secret.


        :param id: The id of this SecretSummary.
        :type: str
        """
        self._id = id

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this SecretSummary.
        Additional information about the secret's current lifecycle state.


        :return: The lifecycle_details of this SecretSummary.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this SecretSummary.
        Additional information about the secret's current lifecycle state.


        :param lifecycle_details: The lifecycle_details of this SecretSummary.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this SecretSummary.
        The current lifecycle state of the secret.

        Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "SCHEDULING_DELETION", "PENDING_DELETION", "CANCELLING_DELETION", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this SecretSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this SecretSummary.
        The current lifecycle state of the secret.


        :param lifecycle_state: The lifecycle_state of this SecretSummary.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "SCHEDULING_DELETION", "PENDING_DELETION", "CANCELLING_DELETION", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def secret_name(self):
        """
        **[Required]** Gets the secret_name of this SecretSummary.
        The name of the secret.


        :return: The secret_name of this SecretSummary.
        :rtype: str
        """
        return self._secret_name

    @secret_name.setter
    def secret_name(self, secret_name):
        """
        Sets the secret_name of this SecretSummary.
        The name of the secret.


        :param secret_name: The secret_name of this SecretSummary.
        :type: str
        """
        self._secret_name = secret_name

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this SecretSummary.
        A property indicating when the secret was created, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this SecretSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this SecretSummary.
        A property indicating when the secret was created, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this SecretSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_of_current_version_expiry(self):
        """
        Gets the time_of_current_version_expiry of this SecretSummary.
        An optional property indicating when the current secret version will expire, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_of_current_version_expiry of this SecretSummary.
        :rtype: datetime
        """
        return self._time_of_current_version_expiry

    @time_of_current_version_expiry.setter
    def time_of_current_version_expiry(self, time_of_current_version_expiry):
        """
        Sets the time_of_current_version_expiry of this SecretSummary.
        An optional property indicating when the current secret version will expire, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_of_current_version_expiry: The time_of_current_version_expiry of this SecretSummary.
        :type: datetime
        """
        self._time_of_current_version_expiry = time_of_current_version_expiry

    @property
    def time_of_deletion(self):
        """
        Gets the time_of_deletion of this SecretSummary.
        An optional property indicating when to delete the secret, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_of_deletion of this SecretSummary.
        :rtype: datetime
        """
        return self._time_of_deletion

    @time_of_deletion.setter
    def time_of_deletion(self, time_of_deletion):
        """
        Sets the time_of_deletion of this SecretSummary.
        An optional property indicating when to delete the secret, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_of_deletion: The time_of_deletion of this SecretSummary.
        :type: datetime
        """
        self._time_of_deletion = time_of_deletion

    @property
    def vault_id(self):
        """
        **[Required]** Gets the vault_id of this SecretSummary.
        The OCID of the Vault in which the secret exists


        :return: The vault_id of this SecretSummary.
        :rtype: str
        """
        return self._vault_id

    @vault_id.setter
    def vault_id(self, vault_id):
        """
        Sets the vault_id of this SecretSummary.
        The OCID of the Vault in which the secret exists


        :param vault_id: The vault_id of this SecretSummary.
        :type: str
        """
        self._vault_id = vault_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

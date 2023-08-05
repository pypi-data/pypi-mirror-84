# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AutoScalingConfiguration(object):
    """
    An autoscaling configuration allows you to dynamically scale the resources in a Compute instance pool.
    For more information, see `Autoscaling`__.

    __ https://docs.cloud.oracle.com/iaas/Content/Compute/Tasks/autoscalinginstancepools.htm
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AutoScalingConfiguration object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this AutoScalingConfiguration.
        :type compartment_id: str

        :param defined_tags:
            The value to assign to the defined_tags property of this AutoScalingConfiguration.
        :type defined_tags: dict(str, dict(str, object))

        :param display_name:
            The value to assign to the display_name property of this AutoScalingConfiguration.
        :type display_name: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this AutoScalingConfiguration.
        :type freeform_tags: dict(str, str)

        :param id:
            The value to assign to the id property of this AutoScalingConfiguration.
        :type id: str

        :param cool_down_in_seconds:
            The value to assign to the cool_down_in_seconds property of this AutoScalingConfiguration.
        :type cool_down_in_seconds: int

        :param is_enabled:
            The value to assign to the is_enabled property of this AutoScalingConfiguration.
        :type is_enabled: bool

        :param resource:
            The value to assign to the resource property of this AutoScalingConfiguration.
        :type resource: Resource

        :param policies:
            The value to assign to the policies property of this AutoScalingConfiguration.
        :type policies: list[AutoScalingPolicy]

        :param time_created:
            The value to assign to the time_created property of this AutoScalingConfiguration.
        :type time_created: datetime

        :param max_resource_count:
            The value to assign to the max_resource_count property of this AutoScalingConfiguration.
        :type max_resource_count: int

        :param min_resource_count:
            The value to assign to the min_resource_count property of this AutoScalingConfiguration.
        :type min_resource_count: int

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'defined_tags': 'dict(str, dict(str, object))',
            'display_name': 'str',
            'freeform_tags': 'dict(str, str)',
            'id': 'str',
            'cool_down_in_seconds': 'int',
            'is_enabled': 'bool',
            'resource': 'Resource',
            'policies': 'list[AutoScalingPolicy]',
            'time_created': 'datetime',
            'max_resource_count': 'int',
            'min_resource_count': 'int'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'defined_tags': 'definedTags',
            'display_name': 'displayName',
            'freeform_tags': 'freeformTags',
            'id': 'id',
            'cool_down_in_seconds': 'coolDownInSeconds',
            'is_enabled': 'isEnabled',
            'resource': 'resource',
            'policies': 'policies',
            'time_created': 'timeCreated',
            'max_resource_count': 'maxResourceCount',
            'min_resource_count': 'minResourceCount'
        }

        self._compartment_id = None
        self._defined_tags = None
        self._display_name = None
        self._freeform_tags = None
        self._id = None
        self._cool_down_in_seconds = None
        self._is_enabled = None
        self._resource = None
        self._policies = None
        self._time_created = None
        self._max_resource_count = None
        self._min_resource_count = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this AutoScalingConfiguration.
        The `OCID`__ of the compartment containing the autoscaling configuration.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this AutoScalingConfiguration.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this AutoScalingConfiguration.
        The `OCID`__ of the compartment containing the autoscaling configuration.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this AutoScalingConfiguration.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this AutoScalingConfiguration.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this AutoScalingConfiguration.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this AutoScalingConfiguration.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this AutoScalingConfiguration.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def display_name(self):
        """
        Gets the display_name of this AutoScalingConfiguration.
        A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.


        :return: The display_name of this AutoScalingConfiguration.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this AutoScalingConfiguration.
        A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.


        :param display_name: The display_name of this AutoScalingConfiguration.
        :type: str
        """
        self._display_name = display_name

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this AutoScalingConfiguration.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this AutoScalingConfiguration.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this AutoScalingConfiguration.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this AutoScalingConfiguration.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def id(self):
        """
        **[Required]** Gets the id of this AutoScalingConfiguration.
        The `OCID`__ of the autoscaling configuration.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this AutoScalingConfiguration.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AutoScalingConfiguration.
        The `OCID`__ of the autoscaling configuration.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this AutoScalingConfiguration.
        :type: str
        """
        self._id = id

    @property
    def cool_down_in_seconds(self):
        """
        Gets the cool_down_in_seconds of this AutoScalingConfiguration.
        The minimum period of time to wait between scaling actions. The cooldown period gives the system time to stabilize
        before rescaling. The minimum value is 300 seconds, which is also the default.


        :return: The cool_down_in_seconds of this AutoScalingConfiguration.
        :rtype: int
        """
        return self._cool_down_in_seconds

    @cool_down_in_seconds.setter
    def cool_down_in_seconds(self, cool_down_in_seconds):
        """
        Sets the cool_down_in_seconds of this AutoScalingConfiguration.
        The minimum period of time to wait between scaling actions. The cooldown period gives the system time to stabilize
        before rescaling. The minimum value is 300 seconds, which is also the default.


        :param cool_down_in_seconds: The cool_down_in_seconds of this AutoScalingConfiguration.
        :type: int
        """
        self._cool_down_in_seconds = cool_down_in_seconds

    @property
    def is_enabled(self):
        """
        Gets the is_enabled of this AutoScalingConfiguration.
        Whether the autoscaling configuration is enabled.


        :return: The is_enabled of this AutoScalingConfiguration.
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """
        Sets the is_enabled of this AutoScalingConfiguration.
        Whether the autoscaling configuration is enabled.


        :param is_enabled: The is_enabled of this AutoScalingConfiguration.
        :type: bool
        """
        self._is_enabled = is_enabled

    @property
    def resource(self):
        """
        **[Required]** Gets the resource of this AutoScalingConfiguration.

        :return: The resource of this AutoScalingConfiguration.
        :rtype: Resource
        """
        return self._resource

    @resource.setter
    def resource(self, resource):
        """
        Sets the resource of this AutoScalingConfiguration.

        :param resource: The resource of this AutoScalingConfiguration.
        :type: Resource
        """
        self._resource = resource

    @property
    def policies(self):
        """
        **[Required]** Gets the policies of this AutoScalingConfiguration.
        Autoscaling policy definitions for the autoscaling configuration. An autoscaling policy defines the criteria that
        trigger autoscaling actions and the actions to take.

        Each autoscaling configuration can have one autoscaling policy.


        :return: The policies of this AutoScalingConfiguration.
        :rtype: list[AutoScalingPolicy]
        """
        return self._policies

    @policies.setter
    def policies(self, policies):
        """
        Sets the policies of this AutoScalingConfiguration.
        Autoscaling policy definitions for the autoscaling configuration. An autoscaling policy defines the criteria that
        trigger autoscaling actions and the actions to take.

        Each autoscaling configuration can have one autoscaling policy.


        :param policies: The policies of this AutoScalingConfiguration.
        :type: list[AutoScalingPolicy]
        """
        self._policies = policies

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this AutoScalingConfiguration.
        The date and time the AutoScalingConfiguration was created, in the format defined by RFC3339.

        Example: `2016-08-25T21:10:29.600Z`


        :return: The time_created of this AutoScalingConfiguration.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this AutoScalingConfiguration.
        The date and time the AutoScalingConfiguration was created, in the format defined by RFC3339.

        Example: `2016-08-25T21:10:29.600Z`


        :param time_created: The time_created of this AutoScalingConfiguration.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def max_resource_count(self):
        """
        Gets the max_resource_count of this AutoScalingConfiguration.
        The maximum number of resources to scale out to.


        :return: The max_resource_count of this AutoScalingConfiguration.
        :rtype: int
        """
        return self._max_resource_count

    @max_resource_count.setter
    def max_resource_count(self, max_resource_count):
        """
        Sets the max_resource_count of this AutoScalingConfiguration.
        The maximum number of resources to scale out to.


        :param max_resource_count: The max_resource_count of this AutoScalingConfiguration.
        :type: int
        """
        self._max_resource_count = max_resource_count

    @property
    def min_resource_count(self):
        """
        Gets the min_resource_count of this AutoScalingConfiguration.
        The minimum number of resources to scale in to.


        :return: The min_resource_count of this AutoScalingConfiguration.
        :rtype: int
        """
        return self._min_resource_count

    @min_resource_count.setter
    def min_resource_count(self, min_resource_count):
        """
        Sets the min_resource_count of this AutoScalingConfiguration.
        The minimum number of resources to scale in to.


        :param min_resource_count: The min_resource_count of this AutoScalingConfiguration.
        :type: int
        """
        self._min_resource_count = min_resource_count

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

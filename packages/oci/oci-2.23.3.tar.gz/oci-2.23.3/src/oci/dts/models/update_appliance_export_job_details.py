# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateApplianceExportJobDetails(object):
    """
    UpdateApplianceExportJobDetails model.
    """

    #: A constant which can be used with the lifecycle_state property of a UpdateApplianceExportJobDetails.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a UpdateApplianceExportJobDetails.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a UpdateApplianceExportJobDetails.
    #: This constant has a value of "INPROGRESS"
    LIFECYCLE_STATE_INPROGRESS = "INPROGRESS"

    #: A constant which can be used with the lifecycle_state property of a UpdateApplianceExportJobDetails.
    #: This constant has a value of "SUCCEEDED"
    LIFECYCLE_STATE_SUCCEEDED = "SUCCEEDED"

    #: A constant which can be used with the lifecycle_state property of a UpdateApplianceExportJobDetails.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a UpdateApplianceExportJobDetails.
    #: This constant has a value of "CANCELLED"
    LIFECYCLE_STATE_CANCELLED = "CANCELLED"

    #: A constant which can be used with the lifecycle_state property of a UpdateApplianceExportJobDetails.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateApplianceExportJobDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param bucket_name:
            The value to assign to the bucket_name property of this UpdateApplianceExportJobDetails.
        :type bucket_name: str

        :param prefix:
            The value to assign to the prefix property of this UpdateApplianceExportJobDetails.
        :type prefix: str

        :param range_start:
            The value to assign to the range_start property of this UpdateApplianceExportJobDetails.
        :type range_start: str

        :param range_end:
            The value to assign to the range_end property of this UpdateApplianceExportJobDetails.
        :type range_end: str

        :param display_name:
            The value to assign to the display_name property of this UpdateApplianceExportJobDetails.
        :type display_name: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this UpdateApplianceExportJobDetails.
            Allowed values for this property are: "CREATING", "ACTIVE", "INPROGRESS", "SUCCEEDED", "FAILED", "CANCELLED", "DELETED"
        :type lifecycle_state: str

        :param lifecycle_state_details:
            The value to assign to the lifecycle_state_details property of this UpdateApplianceExportJobDetails.
        :type lifecycle_state_details: str

        :param manifest_file:
            The value to assign to the manifest_file property of this UpdateApplianceExportJobDetails.
        :type manifest_file: str

        :param manifest_md5:
            The value to assign to the manifest_md5 property of this UpdateApplianceExportJobDetails.
        :type manifest_md5: str

        :param number_of_objects:
            The value to assign to the number_of_objects property of this UpdateApplianceExportJobDetails.
        :type number_of_objects: str

        :param total_size_in_bytes:
            The value to assign to the total_size_in_bytes property of this UpdateApplianceExportJobDetails.
        :type total_size_in_bytes: str

        :param first_object:
            The value to assign to the first_object property of this UpdateApplianceExportJobDetails.
        :type first_object: str

        :param last_object:
            The value to assign to the last_object property of this UpdateApplianceExportJobDetails.
        :type last_object: str

        :param next_object:
            The value to assign to the next_object property of this UpdateApplianceExportJobDetails.
        :type next_object: str

        :param customer_shipping_address:
            The value to assign to the customer_shipping_address property of this UpdateApplianceExportJobDetails.
        :type customer_shipping_address: ShippingAddress

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateApplianceExportJobDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateApplianceExportJobDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'bucket_name': 'str',
            'prefix': 'str',
            'range_start': 'str',
            'range_end': 'str',
            'display_name': 'str',
            'lifecycle_state': 'str',
            'lifecycle_state_details': 'str',
            'manifest_file': 'str',
            'manifest_md5': 'str',
            'number_of_objects': 'str',
            'total_size_in_bytes': 'str',
            'first_object': 'str',
            'last_object': 'str',
            'next_object': 'str',
            'customer_shipping_address': 'ShippingAddress',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'bucket_name': 'bucketName',
            'prefix': 'prefix',
            'range_start': 'rangeStart',
            'range_end': 'rangeEnd',
            'display_name': 'displayName',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_state_details': 'lifecycleStateDetails',
            'manifest_file': 'manifestFile',
            'manifest_md5': 'manifestMd5',
            'number_of_objects': 'numberOfObjects',
            'total_size_in_bytes': 'totalSizeInBytes',
            'first_object': 'firstObject',
            'last_object': 'lastObject',
            'next_object': 'nextObject',
            'customer_shipping_address': 'customerShippingAddress',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._bucket_name = None
        self._prefix = None
        self._range_start = None
        self._range_end = None
        self._display_name = None
        self._lifecycle_state = None
        self._lifecycle_state_details = None
        self._manifest_file = None
        self._manifest_md5 = None
        self._number_of_objects = None
        self._total_size_in_bytes = None
        self._first_object = None
        self._last_object = None
        self._next_object = None
        self._customer_shipping_address = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def bucket_name(self):
        """
        Gets the bucket_name of this UpdateApplianceExportJobDetails.

        :return: The bucket_name of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """
        Sets the bucket_name of this UpdateApplianceExportJobDetails.

        :param bucket_name: The bucket_name of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._bucket_name = bucket_name

    @property
    def prefix(self):
        """
        Gets the prefix of this UpdateApplianceExportJobDetails.
        List of objects with names matching this prefix would be part of this export job.


        :return: The prefix of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        """
        Sets the prefix of this UpdateApplianceExportJobDetails.
        List of objects with names matching this prefix would be part of this export job.


        :param prefix: The prefix of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._prefix = prefix

    @property
    def range_start(self):
        """
        Gets the range_start of this UpdateApplianceExportJobDetails.
        Object names returned by a list query must be greater or equal to this parameter.


        :return: The range_start of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._range_start

    @range_start.setter
    def range_start(self, range_start):
        """
        Sets the range_start of this UpdateApplianceExportJobDetails.
        Object names returned by a list query must be greater or equal to this parameter.


        :param range_start: The range_start of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._range_start = range_start

    @property
    def range_end(self):
        """
        Gets the range_end of this UpdateApplianceExportJobDetails.
        Object names returned by a list query must be strictly less than this parameter.


        :return: The range_end of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._range_end

    @range_end.setter
    def range_end(self, range_end):
        """
        Sets the range_end of this UpdateApplianceExportJobDetails.
        Object names returned by a list query must be strictly less than this parameter.


        :param range_end: The range_end of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._range_end = range_end

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdateApplianceExportJobDetails.

        :return: The display_name of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateApplianceExportJobDetails.

        :param display_name: The display_name of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this UpdateApplianceExportJobDetails.
        Allowed values for this property are: "CREATING", "ACTIVE", "INPROGRESS", "SUCCEEDED", "FAILED", "CANCELLED", "DELETED"


        :return: The lifecycle_state of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this UpdateApplianceExportJobDetails.

        :param lifecycle_state: The lifecycle_state of this UpdateApplianceExportJobDetails.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "INPROGRESS", "SUCCEEDED", "FAILED", "CANCELLED", "DELETED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            raise ValueError(
                "Invalid value for `lifecycle_state`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_state_details(self):
        """
        Gets the lifecycle_state_details of this UpdateApplianceExportJobDetails.
        A property that can contain details on the lifecycle.


        :return: The lifecycle_state_details of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._lifecycle_state_details

    @lifecycle_state_details.setter
    def lifecycle_state_details(self, lifecycle_state_details):
        """
        Sets the lifecycle_state_details of this UpdateApplianceExportJobDetails.
        A property that can contain details on the lifecycle.


        :param lifecycle_state_details: The lifecycle_state_details of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._lifecycle_state_details = lifecycle_state_details

    @property
    def manifest_file(self):
        """
        Gets the manifest_file of this UpdateApplianceExportJobDetails.
        Manifest File associated with this export job.


        :return: The manifest_file of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._manifest_file

    @manifest_file.setter
    def manifest_file(self, manifest_file):
        """
        Sets the manifest_file of this UpdateApplianceExportJobDetails.
        Manifest File associated with this export job.


        :param manifest_file: The manifest_file of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._manifest_file = manifest_file

    @property
    def manifest_md5(self):
        """
        Gets the manifest_md5 of this UpdateApplianceExportJobDetails.
        md5 digest of the manifest file.


        :return: The manifest_md5 of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._manifest_md5

    @manifest_md5.setter
    def manifest_md5(self, manifest_md5):
        """
        Sets the manifest_md5 of this UpdateApplianceExportJobDetails.
        md5 digest of the manifest file.


        :param manifest_md5: The manifest_md5 of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._manifest_md5 = manifest_md5

    @property
    def number_of_objects(self):
        """
        Gets the number_of_objects of this UpdateApplianceExportJobDetails.
        Total number of objects that are exported in this job.


        :return: The number_of_objects of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._number_of_objects

    @number_of_objects.setter
    def number_of_objects(self, number_of_objects):
        """
        Sets the number_of_objects of this UpdateApplianceExportJobDetails.
        Total number of objects that are exported in this job.


        :param number_of_objects: The number_of_objects of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._number_of_objects = number_of_objects

    @property
    def total_size_in_bytes(self):
        """
        Gets the total_size_in_bytes of this UpdateApplianceExportJobDetails.
        Total size of objects in Bytes that are exported in this job.


        :return: The total_size_in_bytes of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._total_size_in_bytes

    @total_size_in_bytes.setter
    def total_size_in_bytes(self, total_size_in_bytes):
        """
        Sets the total_size_in_bytes of this UpdateApplianceExportJobDetails.
        Total size of objects in Bytes that are exported in this job.


        :param total_size_in_bytes: The total_size_in_bytes of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._total_size_in_bytes = total_size_in_bytes

    @property
    def first_object(self):
        """
        Gets the first_object of this UpdateApplianceExportJobDetails.
        First object in the list of objects that are exported in this job.


        :return: The first_object of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._first_object

    @first_object.setter
    def first_object(self, first_object):
        """
        Sets the first_object of this UpdateApplianceExportJobDetails.
        First object in the list of objects that are exported in this job.


        :param first_object: The first_object of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._first_object = first_object

    @property
    def last_object(self):
        """
        Gets the last_object of this UpdateApplianceExportJobDetails.
        Last object in the list of objects that are exported in this job.


        :return: The last_object of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._last_object

    @last_object.setter
    def last_object(self, last_object):
        """
        Sets the last_object of this UpdateApplianceExportJobDetails.
        Last object in the list of objects that are exported in this job.


        :param last_object: The last_object of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._last_object = last_object

    @property
    def next_object(self):
        """
        Gets the next_object of this UpdateApplianceExportJobDetails.
        First object from which the next potential export job could start.


        :return: The next_object of this UpdateApplianceExportJobDetails.
        :rtype: str
        """
        return self._next_object

    @next_object.setter
    def next_object(self, next_object):
        """
        Sets the next_object of this UpdateApplianceExportJobDetails.
        First object from which the next potential export job could start.


        :param next_object: The next_object of this UpdateApplianceExportJobDetails.
        :type: str
        """
        self._next_object = next_object

    @property
    def customer_shipping_address(self):
        """
        Gets the customer_shipping_address of this UpdateApplianceExportJobDetails.

        :return: The customer_shipping_address of this UpdateApplianceExportJobDetails.
        :rtype: ShippingAddress
        """
        return self._customer_shipping_address

    @customer_shipping_address.setter
    def customer_shipping_address(self, customer_shipping_address):
        """
        Sets the customer_shipping_address of this UpdateApplianceExportJobDetails.

        :param customer_shipping_address: The customer_shipping_address of this UpdateApplianceExportJobDetails.
        :type: ShippingAddress
        """
        self._customer_shipping_address = customer_shipping_address

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateApplianceExportJobDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this UpdateApplianceExportJobDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateApplianceExportJobDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this UpdateApplianceExportJobDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateApplianceExportJobDetails.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this UpdateApplianceExportJobDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateApplianceExportJobDetails.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this UpdateApplianceExportJobDetails.
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

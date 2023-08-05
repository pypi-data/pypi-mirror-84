# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class WorkRequest(object):
    """
    A Data Flow work request object.
    """

    #: A constant which can be used with the operation property of a WorkRequest.
    #: This constant has a value of "CREATE_PRIVATE_ENDPOINT"
    OPERATION_CREATE_PRIVATE_ENDPOINT = "CREATE_PRIVATE_ENDPOINT"

    #: A constant which can be used with the operation property of a WorkRequest.
    #: This constant has a value of "UPDATE_PRIVATE_ENDPOINT"
    OPERATION_UPDATE_PRIVATE_ENDPOINT = "UPDATE_PRIVATE_ENDPOINT"

    #: A constant which can be used with the operation property of a WorkRequest.
    #: This constant has a value of "DELETE_PRIVATE_ENDPOINT"
    OPERATION_DELETE_PRIVATE_ENDPOINT = "DELETE_PRIVATE_ENDPOINT"

    #: A constant which can be used with the operation property of a WorkRequest.
    #: This constant has a value of "MOVE_PRIVATE_ENDPOINT"
    OPERATION_MOVE_PRIVATE_ENDPOINT = "MOVE_PRIVATE_ENDPOINT"

    #: A constant which can be used with the status property of a WorkRequest.
    #: This constant has a value of "ACCEPTED"
    STATUS_ACCEPTED = "ACCEPTED"

    #: A constant which can be used with the status property of a WorkRequest.
    #: This constant has a value of "CANCELLED"
    STATUS_CANCELLED = "CANCELLED"

    #: A constant which can be used with the status property of a WorkRequest.
    #: This constant has a value of "CANCELLING"
    STATUS_CANCELLING = "CANCELLING"

    #: A constant which can be used with the status property of a WorkRequest.
    #: This constant has a value of "FAILED"
    STATUS_FAILED = "FAILED"

    #: A constant which can be used with the status property of a WorkRequest.
    #: This constant has a value of "INPROGRESS"
    STATUS_INPROGRESS = "INPROGRESS"

    #: A constant which can be used with the status property of a WorkRequest.
    #: This constant has a value of "SUCCEEDED"
    STATUS_SUCCEEDED = "SUCCEEDED"

    def __init__(self, **kwargs):
        """
        Initializes a new WorkRequest object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this WorkRequest.
        :type compartment_id: str

        :param id:
            The value to assign to the id property of this WorkRequest.
        :type id: str

        :param operation:
            The value to assign to the operation property of this WorkRequest.
            Allowed values for this property are: "CREATE_PRIVATE_ENDPOINT", "UPDATE_PRIVATE_ENDPOINT", "DELETE_PRIVATE_ENDPOINT", "MOVE_PRIVATE_ENDPOINT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type operation: str

        :param percent_complete:
            The value to assign to the percent_complete property of this WorkRequest.
        :type percent_complete: float

        :param resources:
            The value to assign to the resources property of this WorkRequest.
        :type resources: list[WorkRequestResource]

        :param status:
            The value to assign to the status property of this WorkRequest.
            Allowed values for this property are: "ACCEPTED", "CANCELLED", "CANCELLING", "FAILED", "INPROGRESS", "SUCCEEDED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type status: str

        :param time_accepted:
            The value to assign to the time_accepted property of this WorkRequest.
        :type time_accepted: datetime

        :param time_started:
            The value to assign to the time_started property of this WorkRequest.
        :type time_started: datetime

        :param time_finished:
            The value to assign to the time_finished property of this WorkRequest.
        :type time_finished: datetime

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'id': 'str',
            'operation': 'str',
            'percent_complete': 'float',
            'resources': 'list[WorkRequestResource]',
            'status': 'str',
            'time_accepted': 'datetime',
            'time_started': 'datetime',
            'time_finished': 'datetime'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'id': 'id',
            'operation': 'operation',
            'percent_complete': 'percentComplete',
            'resources': 'resources',
            'status': 'status',
            'time_accepted': 'timeAccepted',
            'time_started': 'timeStarted',
            'time_finished': 'timeFinished'
        }

        self._compartment_id = None
        self._id = None
        self._operation = None
        self._percent_complete = None
        self._resources = None
        self._status = None
        self._time_accepted = None
        self._time_started = None
        self._time_finished = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this WorkRequest.
        The OCID of a compartment.


        :return: The compartment_id of this WorkRequest.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this WorkRequest.
        The OCID of a compartment.


        :param compartment_id: The compartment_id of this WorkRequest.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def id(self):
        """
        **[Required]** Gets the id of this WorkRequest.
        The OCID of a work request.


        :return: The id of this WorkRequest.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WorkRequest.
        The OCID of a work request.


        :param id: The id of this WorkRequest.
        :type: str
        """
        self._id = id

    @property
    def operation(self):
        """
        **[Required]** Gets the operation of this WorkRequest.
        The operation related to this work request.

        Allowed values for this property are: "CREATE_PRIVATE_ENDPOINT", "UPDATE_PRIVATE_ENDPOINT", "DELETE_PRIVATE_ENDPOINT", "MOVE_PRIVATE_ENDPOINT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The operation of this WorkRequest.
        :rtype: str
        """
        return self._operation

    @operation.setter
    def operation(self, operation):
        """
        Sets the operation of this WorkRequest.
        The operation related to this work request.


        :param operation: The operation of this WorkRequest.
        :type: str
        """
        allowed_values = ["CREATE_PRIVATE_ENDPOINT", "UPDATE_PRIVATE_ENDPOINT", "DELETE_PRIVATE_ENDPOINT", "MOVE_PRIVATE_ENDPOINT"]
        if not value_allowed_none_or_none_sentinel(operation, allowed_values):
            operation = 'UNKNOWN_ENUM_VALUE'
        self._operation = operation

    @property
    def percent_complete(self):
        """
        **[Required]** Gets the percent_complete of this WorkRequest.
        Percentage of the request completed.


        :return: The percent_complete of this WorkRequest.
        :rtype: float
        """
        return self._percent_complete

    @percent_complete.setter
    def percent_complete(self, percent_complete):
        """
        Sets the percent_complete of this WorkRequest.
        Percentage of the request completed.


        :param percent_complete: The percent_complete of this WorkRequest.
        :type: float
        """
        self._percent_complete = percent_complete

    @property
    def resources(self):
        """
        **[Required]** Gets the resources of this WorkRequest.
        The resources affected by this work request.


        :return: The resources of this WorkRequest.
        :rtype: list[WorkRequestResource]
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """
        Sets the resources of this WorkRequest.
        The resources affected by this work request.


        :param resources: The resources of this WorkRequest.
        :type: list[WorkRequestResource]
        """
        self._resources = resources

    @property
    def status(self):
        """
        **[Required]** Gets the status of this WorkRequest.
        The status of the work request.

        Allowed values for this property are: "ACCEPTED", "CANCELLED", "CANCELLING", "FAILED", "INPROGRESS", "SUCCEEDED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The status of this WorkRequest.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this WorkRequest.
        The status of the work request.


        :param status: The status of this WorkRequest.
        :type: str
        """
        allowed_values = ["ACCEPTED", "CANCELLED", "CANCELLING", "FAILED", "INPROGRESS", "SUCCEEDED"]
        if not value_allowed_none_or_none_sentinel(status, allowed_values):
            status = 'UNKNOWN_ENUM_VALUE'
        self._status = status

    @property
    def time_accepted(self):
        """
        Gets the time_accepted of this WorkRequest.
        The date and time the request was created, as described in
        `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :return: The time_accepted of this WorkRequest.
        :rtype: datetime
        """
        return self._time_accepted

    @time_accepted.setter
    def time_accepted(self, time_accepted):
        """
        Sets the time_accepted of this WorkRequest.
        The date and time the request was created, as described in
        `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :param time_accepted: The time_accepted of this WorkRequest.
        :type: datetime
        """
        self._time_accepted = time_accepted

    @property
    def time_started(self):
        """
        Gets the time_started of this WorkRequest.
        The date and time the request was started, as described in
        `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :return: The time_started of this WorkRequest.
        :rtype: datetime
        """
        return self._time_started

    @time_started.setter
    def time_started(self, time_started):
        """
        Sets the time_started of this WorkRequest.
        The date and time the request was started, as described in
        `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :param time_started: The time_started of this WorkRequest.
        :type: datetime
        """
        self._time_started = time_started

    @property
    def time_finished(self):
        """
        Gets the time_finished of this WorkRequest.
        The date and time the object was finished, as described in
        `RFC 3339`__.

        __ https://tools.ietf.org/rfc/rfc3339


        :return: The time_finished of this WorkRequest.
        :rtype: datetime
        """
        return self._time_finished

    @time_finished.setter
    def time_finished(self, time_finished):
        """
        Sets the time_finished of this WorkRequest.
        The date and time the object was finished, as described in
        `RFC 3339`__.

        __ https://tools.ietf.org/rfc/rfc3339


        :param time_finished: The time_finished of this WorkRequest.
        :type: datetime
        """
        self._time_finished = time_finished

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

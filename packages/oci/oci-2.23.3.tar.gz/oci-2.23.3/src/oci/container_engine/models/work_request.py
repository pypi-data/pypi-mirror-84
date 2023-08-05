# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class WorkRequest(object):
    """
    An asynchronous work request.
    """

    #: A constant which can be used with the operation_type property of a WorkRequest.
    #: This constant has a value of "CLUSTER_CREATE"
    OPERATION_TYPE_CLUSTER_CREATE = "CLUSTER_CREATE"

    #: A constant which can be used with the operation_type property of a WorkRequest.
    #: This constant has a value of "CLUSTER_UPDATE"
    OPERATION_TYPE_CLUSTER_UPDATE = "CLUSTER_UPDATE"

    #: A constant which can be used with the operation_type property of a WorkRequest.
    #: This constant has a value of "CLUSTER_DELETE"
    OPERATION_TYPE_CLUSTER_DELETE = "CLUSTER_DELETE"

    #: A constant which can be used with the operation_type property of a WorkRequest.
    #: This constant has a value of "NODEPOOL_CREATE"
    OPERATION_TYPE_NODEPOOL_CREATE = "NODEPOOL_CREATE"

    #: A constant which can be used with the operation_type property of a WorkRequest.
    #: This constant has a value of "NODEPOOL_UPDATE"
    OPERATION_TYPE_NODEPOOL_UPDATE = "NODEPOOL_UPDATE"

    #: A constant which can be used with the operation_type property of a WorkRequest.
    #: This constant has a value of "NODEPOOL_DELETE"
    OPERATION_TYPE_NODEPOOL_DELETE = "NODEPOOL_DELETE"

    #: A constant which can be used with the operation_type property of a WorkRequest.
    #: This constant has a value of "WORKREQUEST_CANCEL"
    OPERATION_TYPE_WORKREQUEST_CANCEL = "WORKREQUEST_CANCEL"

    #: A constant which can be used with the status property of a WorkRequest.
    #: This constant has a value of "ACCEPTED"
    STATUS_ACCEPTED = "ACCEPTED"

    #: A constant which can be used with the status property of a WorkRequest.
    #: This constant has a value of "IN_PROGRESS"
    STATUS_IN_PROGRESS = "IN_PROGRESS"

    #: A constant which can be used with the status property of a WorkRequest.
    #: This constant has a value of "FAILED"
    STATUS_FAILED = "FAILED"

    #: A constant which can be used with the status property of a WorkRequest.
    #: This constant has a value of "SUCCEEDED"
    STATUS_SUCCEEDED = "SUCCEEDED"

    #: A constant which can be used with the status property of a WorkRequest.
    #: This constant has a value of "CANCELING"
    STATUS_CANCELING = "CANCELING"

    #: A constant which can be used with the status property of a WorkRequest.
    #: This constant has a value of "CANCELED"
    STATUS_CANCELED = "CANCELED"

    def __init__(self, **kwargs):
        """
        Initializes a new WorkRequest object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this WorkRequest.
        :type id: str

        :param operation_type:
            The value to assign to the operation_type property of this WorkRequest.
            Allowed values for this property are: "CLUSTER_CREATE", "CLUSTER_UPDATE", "CLUSTER_DELETE", "NODEPOOL_CREATE", "NODEPOOL_UPDATE", "NODEPOOL_DELETE", "WORKREQUEST_CANCEL", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type operation_type: str

        :param status:
            The value to assign to the status property of this WorkRequest.
            Allowed values for this property are: "ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELING", "CANCELED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type status: str

        :param compartment_id:
            The value to assign to the compartment_id property of this WorkRequest.
        :type compartment_id: str

        :param resources:
            The value to assign to the resources property of this WorkRequest.
        :type resources: list[WorkRequestResource]

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
            'id': 'str',
            'operation_type': 'str',
            'status': 'str',
            'compartment_id': 'str',
            'resources': 'list[WorkRequestResource]',
            'time_accepted': 'datetime',
            'time_started': 'datetime',
            'time_finished': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'operation_type': 'operationType',
            'status': 'status',
            'compartment_id': 'compartmentId',
            'resources': 'resources',
            'time_accepted': 'timeAccepted',
            'time_started': 'timeStarted',
            'time_finished': 'timeFinished'
        }

        self._id = None
        self._operation_type = None
        self._status = None
        self._compartment_id = None
        self._resources = None
        self._time_accepted = None
        self._time_started = None
        self._time_finished = None

    @property
    def id(self):
        """
        Gets the id of this WorkRequest.
        The OCID of the work request.


        :return: The id of this WorkRequest.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WorkRequest.
        The OCID of the work request.


        :param id: The id of this WorkRequest.
        :type: str
        """
        self._id = id

    @property
    def operation_type(self):
        """
        Gets the operation_type of this WorkRequest.
        The type of work the work request is doing.

        Allowed values for this property are: "CLUSTER_CREATE", "CLUSTER_UPDATE", "CLUSTER_DELETE", "NODEPOOL_CREATE", "NODEPOOL_UPDATE", "NODEPOOL_DELETE", "WORKREQUEST_CANCEL", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The operation_type of this WorkRequest.
        :rtype: str
        """
        return self._operation_type

    @operation_type.setter
    def operation_type(self, operation_type):
        """
        Sets the operation_type of this WorkRequest.
        The type of work the work request is doing.


        :param operation_type: The operation_type of this WorkRequest.
        :type: str
        """
        allowed_values = ["CLUSTER_CREATE", "CLUSTER_UPDATE", "CLUSTER_DELETE", "NODEPOOL_CREATE", "NODEPOOL_UPDATE", "NODEPOOL_DELETE", "WORKREQUEST_CANCEL"]
        if not value_allowed_none_or_none_sentinel(operation_type, allowed_values):
            operation_type = 'UNKNOWN_ENUM_VALUE'
        self._operation_type = operation_type

    @property
    def status(self):
        """
        Gets the status of this WorkRequest.
        The current status of the work request.

        Allowed values for this property are: "ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELING", "CANCELED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The status of this WorkRequest.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this WorkRequest.
        The current status of the work request.


        :param status: The status of this WorkRequest.
        :type: str
        """
        allowed_values = ["ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELING", "CANCELED"]
        if not value_allowed_none_or_none_sentinel(status, allowed_values):
            status = 'UNKNOWN_ENUM_VALUE'
        self._status = status

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this WorkRequest.
        The OCID of the compartment in which the work request exists.


        :return: The compartment_id of this WorkRequest.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this WorkRequest.
        The OCID of the compartment in which the work request exists.


        :param compartment_id: The compartment_id of this WorkRequest.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def resources(self):
        """
        Gets the resources of this WorkRequest.
        The resources this work request affects.


        :return: The resources of this WorkRequest.
        :rtype: list[WorkRequestResource]
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """
        Sets the resources of this WorkRequest.
        The resources this work request affects.


        :param resources: The resources of this WorkRequest.
        :type: list[WorkRequestResource]
        """
        self._resources = resources

    @property
    def time_accepted(self):
        """
        Gets the time_accepted of this WorkRequest.
        The time the work request was accepted.


        :return: The time_accepted of this WorkRequest.
        :rtype: datetime
        """
        return self._time_accepted

    @time_accepted.setter
    def time_accepted(self, time_accepted):
        """
        Sets the time_accepted of this WorkRequest.
        The time the work request was accepted.


        :param time_accepted: The time_accepted of this WorkRequest.
        :type: datetime
        """
        self._time_accepted = time_accepted

    @property
    def time_started(self):
        """
        Gets the time_started of this WorkRequest.
        The time the work request was started.


        :return: The time_started of this WorkRequest.
        :rtype: datetime
        """
        return self._time_started

    @time_started.setter
    def time_started(self, time_started):
        """
        Sets the time_started of this WorkRequest.
        The time the work request was started.


        :param time_started: The time_started of this WorkRequest.
        :type: datetime
        """
        self._time_started = time_started

    @property
    def time_finished(self):
        """
        Gets the time_finished of this WorkRequest.
        The time the work request was finished.


        :return: The time_finished of this WorkRequest.
        :rtype: datetime
        """
        return self._time_finished

    @time_finished.setter
    def time_finished(self, time_finished):
        """
        Sets the time_finished of this WorkRequest.
        The time the work request was finished.


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

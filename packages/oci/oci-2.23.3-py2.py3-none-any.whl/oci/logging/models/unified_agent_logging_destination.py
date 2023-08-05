# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UnifiedAgentLoggingDestination(object):
    """
    Logging destination object.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UnifiedAgentLoggingDestination object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param log_object_id:
            The value to assign to the log_object_id property of this UnifiedAgentLoggingDestination.
        :type log_object_id: str

        """
        self.swagger_types = {
            'log_object_id': 'str'
        }

        self.attribute_map = {
            'log_object_id': 'logObjectId'
        }

        self._log_object_id = None

    @property
    def log_object_id(self):
        """
        **[Required]** Gets the log_object_id of this UnifiedAgentLoggingDestination.
        The OCID of the resource.


        :return: The log_object_id of this UnifiedAgentLoggingDestination.
        :rtype: str
        """
        return self._log_object_id

    @log_object_id.setter
    def log_object_id(self, log_object_id):
        """
        Sets the log_object_id of this UnifiedAgentLoggingDestination.
        The OCID of the resource.


        :param log_object_id: The log_object_id of this UnifiedAgentLoggingDestination.
        :type: str
        """
        self._log_object_id = log_object_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

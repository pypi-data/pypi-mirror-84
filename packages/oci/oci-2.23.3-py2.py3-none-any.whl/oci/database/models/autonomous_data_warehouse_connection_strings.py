# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AutonomousDataWarehouseConnectionStrings(object):
    """
    **Deprecated.** For information about connection strings to connect to an Oracle Autonomous Data Warehouse, see :func:`autonomous_database_connection_strings`.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AutonomousDataWarehouseConnectionStrings object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param high:
            The value to assign to the high property of this AutonomousDataWarehouseConnectionStrings.
        :type high: str

        :param medium:
            The value to assign to the medium property of this AutonomousDataWarehouseConnectionStrings.
        :type medium: str

        :param low:
            The value to assign to the low property of this AutonomousDataWarehouseConnectionStrings.
        :type low: str

        :param all_connection_strings:
            The value to assign to the all_connection_strings property of this AutonomousDataWarehouseConnectionStrings.
        :type all_connection_strings: dict(str, str)

        """
        self.swagger_types = {
            'high': 'str',
            'medium': 'str',
            'low': 'str',
            'all_connection_strings': 'dict(str, str)'
        }

        self.attribute_map = {
            'high': 'high',
            'medium': 'medium',
            'low': 'low',
            'all_connection_strings': 'allConnectionStrings'
        }

        self._high = None
        self._medium = None
        self._low = None
        self._all_connection_strings = None

    @property
    def high(self):
        """
        Gets the high of this AutonomousDataWarehouseConnectionStrings.
        The High database service provides the highest level of resources to each SQL statement resulting in the highest performance, but supports the fewest number of concurrent SQL statements.


        :return: The high of this AutonomousDataWarehouseConnectionStrings.
        :rtype: str
        """
        return self._high

    @high.setter
    def high(self, high):
        """
        Sets the high of this AutonomousDataWarehouseConnectionStrings.
        The High database service provides the highest level of resources to each SQL statement resulting in the highest performance, but supports the fewest number of concurrent SQL statements.


        :param high: The high of this AutonomousDataWarehouseConnectionStrings.
        :type: str
        """
        self._high = high

    @property
    def medium(self):
        """
        Gets the medium of this AutonomousDataWarehouseConnectionStrings.
        The Medium database service provides a lower level of resources to each SQL statement potentially resulting a lower level of performance, but supports more concurrent SQL statements.


        :return: The medium of this AutonomousDataWarehouseConnectionStrings.
        :rtype: str
        """
        return self._medium

    @medium.setter
    def medium(self, medium):
        """
        Sets the medium of this AutonomousDataWarehouseConnectionStrings.
        The Medium database service provides a lower level of resources to each SQL statement potentially resulting a lower level of performance, but supports more concurrent SQL statements.


        :param medium: The medium of this AutonomousDataWarehouseConnectionStrings.
        :type: str
        """
        self._medium = medium

    @property
    def low(self):
        """
        Gets the low of this AutonomousDataWarehouseConnectionStrings.
        The Low database service provides the least level of resources to each SQL statement, but supports the most number of concurrent SQL statements.


        :return: The low of this AutonomousDataWarehouseConnectionStrings.
        :rtype: str
        """
        return self._low

    @low.setter
    def low(self, low):
        """
        Sets the low of this AutonomousDataWarehouseConnectionStrings.
        The Low database service provides the least level of resources to each SQL statement, but supports the most number of concurrent SQL statements.


        :param low: The low of this AutonomousDataWarehouseConnectionStrings.
        :type: str
        """
        self._low = low

    @property
    def all_connection_strings(self):
        """
        Gets the all_connection_strings of this AutonomousDataWarehouseConnectionStrings.
        Returns all connection strings that can be used to connect to the Autonomous Data Warehouse.
        For more information, please see `Predefined Database Service Names for Autonomous Transaction Processing`__

        __ https://docs.oracle.com/en/cloud/paas/atp-cloud/atpug/connect-predefined.html#GUID-9747539B-FD46-44F1-8FF8-F5AC650F15BE


        :return: The all_connection_strings of this AutonomousDataWarehouseConnectionStrings.
        :rtype: dict(str, str)
        """
        return self._all_connection_strings

    @all_connection_strings.setter
    def all_connection_strings(self, all_connection_strings):
        """
        Sets the all_connection_strings of this AutonomousDataWarehouseConnectionStrings.
        Returns all connection strings that can be used to connect to the Autonomous Data Warehouse.
        For more information, please see `Predefined Database Service Names for Autonomous Transaction Processing`__

        __ https://docs.oracle.com/en/cloud/paas/atp-cloud/atpug/connect-predefined.html#GUID-9747539B-FD46-44F1-8FF8-F5AC650F15BE


        :param all_connection_strings: The all_connection_strings of this AutonomousDataWarehouseConnectionStrings.
        :type: dict(str, str)
        """
        self._all_connection_strings = all_connection_strings

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

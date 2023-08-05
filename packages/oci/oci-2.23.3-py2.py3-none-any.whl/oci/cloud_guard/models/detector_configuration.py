# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DetectorConfiguration(object):
    """
    A single configuration applied to a detector
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DetectorConfiguration object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param config_key:
            The value to assign to the config_key property of this DetectorConfiguration.
        :type config_key: str

        :param name:
            The value to assign to the name property of this DetectorConfiguration.
        :type name: str

        :param value:
            The value to assign to the value property of this DetectorConfiguration.
        :type value: str

        :param data_type:
            The value to assign to the data_type property of this DetectorConfiguration.
        :type data_type: str

        :param values:
            The value to assign to the values property of this DetectorConfiguration.
        :type values: list[ConfigValue]

        """
        self.swagger_types = {
            'config_key': 'str',
            'name': 'str',
            'value': 'str',
            'data_type': 'str',
            'values': 'list[ConfigValue]'
        }

        self.attribute_map = {
            'config_key': 'configKey',
            'name': 'name',
            'value': 'value',
            'data_type': 'dataType',
            'values': 'values'
        }

        self._config_key = None
        self._name = None
        self._value = None
        self._data_type = None
        self._values = None

    @property
    def config_key(self):
        """
        **[Required]** Gets the config_key of this DetectorConfiguration.
        Unique name of the configuration


        :return: The config_key of this DetectorConfiguration.
        :rtype: str
        """
        return self._config_key

    @config_key.setter
    def config_key(self, config_key):
        """
        Sets the config_key of this DetectorConfiguration.
        Unique name of the configuration


        :param config_key: The config_key of this DetectorConfiguration.
        :type: str
        """
        self._config_key = config_key

    @property
    def name(self):
        """
        **[Required]** Gets the name of this DetectorConfiguration.
        configuration name


        :return: The name of this DetectorConfiguration.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this DetectorConfiguration.
        configuration name


        :param name: The name of this DetectorConfiguration.
        :type: str
        """
        self._name = name

    @property
    def value(self):
        """
        Gets the value of this DetectorConfiguration.
        configuration value


        :return: The value of this DetectorConfiguration.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this DetectorConfiguration.
        configuration value


        :param value: The value of this DetectorConfiguration.
        :type: str
        """
        self._value = value

    @property
    def data_type(self):
        """
        Gets the data_type of this DetectorConfiguration.
        configuration data type


        :return: The data_type of this DetectorConfiguration.
        :rtype: str
        """
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        """
        Sets the data_type of this DetectorConfiguration.
        configuration data type


        :param data_type: The data_type of this DetectorConfiguration.
        :type: str
        """
        self._data_type = data_type

    @property
    def values(self):
        """
        Gets the values of this DetectorConfiguration.
        List of configuration values


        :return: The values of this DetectorConfiguration.
        :rtype: list[ConfigValue]
        """
        return self._values

    @values.setter
    def values(self, values):
        """
        Sets the values of this DetectorConfiguration.
        List of configuration values


        :param values: The values of this DetectorConfiguration.
        :type: list[ConfigValue]
        """
        self._values = values

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class HealthCheck(object):
    """
    Health checks monitor the status of your origin servers and only route traffic to the origins that pass the health check. If the health check fails, origin is automatically removed from the load balancing.
    There is roughly one health check per EDGE POP per period. Any checks that pass will be reported as \"healthy\".
    """

    #: A constant which can be used with the method property of a HealthCheck.
    #: This constant has a value of "GET"
    METHOD_GET = "GET"

    #: A constant which can be used with the method property of a HealthCheck.
    #: This constant has a value of "HEAD"
    METHOD_HEAD = "HEAD"

    #: A constant which can be used with the method property of a HealthCheck.
    #: This constant has a value of "POST"
    METHOD_POST = "POST"

    #: A constant which can be used with the expected_response_code_group property of a HealthCheck.
    #: This constant has a value of "2XX"
    EXPECTED_RESPONSE_CODE_GROUP_2_XX = "2XX"

    #: A constant which can be used with the expected_response_code_group property of a HealthCheck.
    #: This constant has a value of "3XX"
    EXPECTED_RESPONSE_CODE_GROUP_3_XX = "3XX"

    #: A constant which can be used with the expected_response_code_group property of a HealthCheck.
    #: This constant has a value of "4XX"
    EXPECTED_RESPONSE_CODE_GROUP_4_XX = "4XX"

    #: A constant which can be used with the expected_response_code_group property of a HealthCheck.
    #: This constant has a value of "5XX"
    EXPECTED_RESPONSE_CODE_GROUP_5_XX = "5XX"

    def __init__(self, **kwargs):
        """
        Initializes a new HealthCheck object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param is_enabled:
            The value to assign to the is_enabled property of this HealthCheck.
        :type is_enabled: bool

        :param method:
            The value to assign to the method property of this HealthCheck.
            Allowed values for this property are: "GET", "HEAD", "POST", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type method: str

        :param path:
            The value to assign to the path property of this HealthCheck.
        :type path: str

        :param headers:
            The value to assign to the headers property of this HealthCheck.
        :type headers: dict(str, str)

        :param expected_response_code_group:
            The value to assign to the expected_response_code_group property of this HealthCheck.
            Allowed values for items in this list are: "2XX", "3XX", "4XX", "5XX", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type expected_response_code_group: list[str]

        :param is_response_text_check_enabled:
            The value to assign to the is_response_text_check_enabled property of this HealthCheck.
        :type is_response_text_check_enabled: bool

        :param expected_response_text:
            The value to assign to the expected_response_text property of this HealthCheck.
        :type expected_response_text: str

        :param interval_in_seconds:
            The value to assign to the interval_in_seconds property of this HealthCheck.
        :type interval_in_seconds: int

        :param timeout_in_seconds:
            The value to assign to the timeout_in_seconds property of this HealthCheck.
        :type timeout_in_seconds: int

        :param healthy_threshold:
            The value to assign to the healthy_threshold property of this HealthCheck.
        :type healthy_threshold: int

        :param unhealthy_threshold:
            The value to assign to the unhealthy_threshold property of this HealthCheck.
        :type unhealthy_threshold: int

        """
        self.swagger_types = {
            'is_enabled': 'bool',
            'method': 'str',
            'path': 'str',
            'headers': 'dict(str, str)',
            'expected_response_code_group': 'list[str]',
            'is_response_text_check_enabled': 'bool',
            'expected_response_text': 'str',
            'interval_in_seconds': 'int',
            'timeout_in_seconds': 'int',
            'healthy_threshold': 'int',
            'unhealthy_threshold': 'int'
        }

        self.attribute_map = {
            'is_enabled': 'isEnabled',
            'method': 'method',
            'path': 'path',
            'headers': 'headers',
            'expected_response_code_group': 'expectedResponseCodeGroup',
            'is_response_text_check_enabled': 'isResponseTextCheckEnabled',
            'expected_response_text': 'expectedResponseText',
            'interval_in_seconds': 'intervalInSeconds',
            'timeout_in_seconds': 'timeoutInSeconds',
            'healthy_threshold': 'healthyThreshold',
            'unhealthy_threshold': 'unhealthyThreshold'
        }

        self._is_enabled = None
        self._method = None
        self._path = None
        self._headers = None
        self._expected_response_code_group = None
        self._is_response_text_check_enabled = None
        self._expected_response_text = None
        self._interval_in_seconds = None
        self._timeout_in_seconds = None
        self._healthy_threshold = None
        self._unhealthy_threshold = None

    @property
    def is_enabled(self):
        """
        Gets the is_enabled of this HealthCheck.
        Enables or disables the health checks.


        :return: The is_enabled of this HealthCheck.
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """
        Sets the is_enabled of this HealthCheck.
        Enables or disables the health checks.


        :param is_enabled: The is_enabled of this HealthCheck.
        :type: bool
        """
        self._is_enabled = is_enabled

    @property
    def method(self):
        """
        Gets the method of this HealthCheck.
        An HTTP verb (i.e. HEAD, GET, or POST) to use when performing the health check.

        Allowed values for this property are: "GET", "HEAD", "POST", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The method of this HealthCheck.
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method):
        """
        Sets the method of this HealthCheck.
        An HTTP verb (i.e. HEAD, GET, or POST) to use when performing the health check.


        :param method: The method of this HealthCheck.
        :type: str
        """
        allowed_values = ["GET", "HEAD", "POST"]
        if not value_allowed_none_or_none_sentinel(method, allowed_values):
            method = 'UNKNOWN_ENUM_VALUE'
        self._method = method

    @property
    def path(self):
        """
        Gets the path of this HealthCheck.
        Path to visit on your origins when performing the health check.


        :return: The path of this HealthCheck.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        Sets the path of this HealthCheck.
        Path to visit on your origins when performing the health check.


        :param path: The path of this HealthCheck.
        :type: str
        """
        self._path = path

    @property
    def headers(self):
        """
        Gets the headers of this HealthCheck.
        HTTP header fields to include in health check requests, expressed as `\"name\": \"value\"` properties. Because HTTP header field names are case-insensitive, any use of names that are case-insensitive equal to other names will be rejected. If Host is not specified, requests will include a Host header field with value matching the policy's protected domain. If User-Agent is not specified, requests will include a User-Agent header field with value \"waf health checks\".

        **Note:** The only currently-supported header fields are Host and User-Agent.


        :return: The headers of this HealthCheck.
        :rtype: dict(str, str)
        """
        return self._headers

    @headers.setter
    def headers(self, headers):
        """
        Sets the headers of this HealthCheck.
        HTTP header fields to include in health check requests, expressed as `\"name\": \"value\"` properties. Because HTTP header field names are case-insensitive, any use of names that are case-insensitive equal to other names will be rejected. If Host is not specified, requests will include a Host header field with value matching the policy's protected domain. If User-Agent is not specified, requests will include a User-Agent header field with value \"waf health checks\".

        **Note:** The only currently-supported header fields are Host and User-Agent.


        :param headers: The headers of this HealthCheck.
        :type: dict(str, str)
        """
        self._headers = headers

    @property
    def expected_response_code_group(self):
        """
        Gets the expected_response_code_group of this HealthCheck.
        The HTTP response codes that signify a healthy state.
        - **2XX:** Success response code group.
        - **3XX:** Redirection response code group.
        - **4XX:** Client errors response code group.
        - **5XX:** Server errors response code group.

        Allowed values for items in this list are: "2XX", "3XX", "4XX", "5XX", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The expected_response_code_group of this HealthCheck.
        :rtype: list[str]
        """
        return self._expected_response_code_group

    @expected_response_code_group.setter
    def expected_response_code_group(self, expected_response_code_group):
        """
        Sets the expected_response_code_group of this HealthCheck.
        The HTTP response codes that signify a healthy state.
        - **2XX:** Success response code group.
        - **3XX:** Redirection response code group.
        - **4XX:** Client errors response code group.
        - **5XX:** Server errors response code group.


        :param expected_response_code_group: The expected_response_code_group of this HealthCheck.
        :type: list[str]
        """
        allowed_values = ["2XX", "3XX", "4XX", "5XX"]
        if expected_response_code_group:
            expected_response_code_group[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in expected_response_code_group]
        self._expected_response_code_group = expected_response_code_group

    @property
    def is_response_text_check_enabled(self):
        """
        Gets the is_response_text_check_enabled of this HealthCheck.
        Enables or disables additional check for predefined text in addition to response code.


        :return: The is_response_text_check_enabled of this HealthCheck.
        :rtype: bool
        """
        return self._is_response_text_check_enabled

    @is_response_text_check_enabled.setter
    def is_response_text_check_enabled(self, is_response_text_check_enabled):
        """
        Sets the is_response_text_check_enabled of this HealthCheck.
        Enables or disables additional check for predefined text in addition to response code.


        :param is_response_text_check_enabled: The is_response_text_check_enabled of this HealthCheck.
        :type: bool
        """
        self._is_response_text_check_enabled = is_response_text_check_enabled

    @property
    def expected_response_text(self):
        """
        Gets the expected_response_text of this HealthCheck.
        Health check will search for the given text in a case-sensitive manner within the response body and will fail if the text is not found.


        :return: The expected_response_text of this HealthCheck.
        :rtype: str
        """
        return self._expected_response_text

    @expected_response_text.setter
    def expected_response_text(self, expected_response_text):
        """
        Sets the expected_response_text of this HealthCheck.
        Health check will search for the given text in a case-sensitive manner within the response body and will fail if the text is not found.


        :param expected_response_text: The expected_response_text of this HealthCheck.
        :type: str
        """
        self._expected_response_text = expected_response_text

    @property
    def interval_in_seconds(self):
        """
        Gets the interval_in_seconds of this HealthCheck.
        Time between health checks of an individual origin server, in seconds.


        :return: The interval_in_seconds of this HealthCheck.
        :rtype: int
        """
        return self._interval_in_seconds

    @interval_in_seconds.setter
    def interval_in_seconds(self, interval_in_seconds):
        """
        Sets the interval_in_seconds of this HealthCheck.
        Time between health checks of an individual origin server, in seconds.


        :param interval_in_seconds: The interval_in_seconds of this HealthCheck.
        :type: int
        """
        self._interval_in_seconds = interval_in_seconds

    @property
    def timeout_in_seconds(self):
        """
        Gets the timeout_in_seconds of this HealthCheck.
        Response timeout represents wait time until request is considered failed, in seconds.


        :return: The timeout_in_seconds of this HealthCheck.
        :rtype: int
        """
        return self._timeout_in_seconds

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, timeout_in_seconds):
        """
        Sets the timeout_in_seconds of this HealthCheck.
        Response timeout represents wait time until request is considered failed, in seconds.


        :param timeout_in_seconds: The timeout_in_seconds of this HealthCheck.
        :type: int
        """
        self._timeout_in_seconds = timeout_in_seconds

    @property
    def healthy_threshold(self):
        """
        Gets the healthy_threshold of this HealthCheck.
        Number of successful health checks after which the server is marked up.


        :return: The healthy_threshold of this HealthCheck.
        :rtype: int
        """
        return self._healthy_threshold

    @healthy_threshold.setter
    def healthy_threshold(self, healthy_threshold):
        """
        Sets the healthy_threshold of this HealthCheck.
        Number of successful health checks after which the server is marked up.


        :param healthy_threshold: The healthy_threshold of this HealthCheck.
        :type: int
        """
        self._healthy_threshold = healthy_threshold

    @property
    def unhealthy_threshold(self):
        """
        Gets the unhealthy_threshold of this HealthCheck.
        Number of failed health checks after which the server is marked down.


        :return: The unhealthy_threshold of this HealthCheck.
        :rtype: int
        """
        return self._unhealthy_threshold

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, unhealthy_threshold):
        """
        Sets the unhealthy_threshold of this HealthCheck.
        Number of failed health checks after which the server is marked down.


        :param unhealthy_threshold: The unhealthy_threshold of this HealthCheck.
        :type: int
        """
        self._unhealthy_threshold = unhealthy_threshold

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class HealthChecksVantagePointSummary(object):
    """
    Information about a vantage point.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new HealthChecksVantagePointSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this HealthChecksVantagePointSummary.
        :type display_name: str

        :param provider_name:
            The value to assign to the provider_name property of this HealthChecksVantagePointSummary.
        :type provider_name: str

        :param name:
            The value to assign to the name property of this HealthChecksVantagePointSummary.
        :type name: str

        :param geo:
            The value to assign to the geo property of this HealthChecksVantagePointSummary.
        :type geo: Geolocation

        :param routing:
            The value to assign to the routing property of this HealthChecksVantagePointSummary.
        :type routing: list[Routing]

        """
        self.swagger_types = {
            'display_name': 'str',
            'provider_name': 'str',
            'name': 'str',
            'geo': 'Geolocation',
            'routing': 'list[Routing]'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'provider_name': 'providerName',
            'name': 'name',
            'geo': 'geo',
            'routing': 'routing'
        }

        self._display_name = None
        self._provider_name = None
        self._name = None
        self._geo = None
        self._routing = None

    @property
    def display_name(self):
        """
        Gets the display_name of this HealthChecksVantagePointSummary.
        The display name for the vantage point. Display names are determined by
        the best information available and may change over time.


        :return: The display_name of this HealthChecksVantagePointSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this HealthChecksVantagePointSummary.
        The display name for the vantage point. Display names are determined by
        the best information available and may change over time.


        :param display_name: The display_name of this HealthChecksVantagePointSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def provider_name(self):
        """
        Gets the provider_name of this HealthChecksVantagePointSummary.
        The organization on whose infrastructure this vantage point resides.
        Provider names are not unique, as Oracle Cloud Infrastructure maintains
        many vantage points in each major provider.


        :return: The provider_name of this HealthChecksVantagePointSummary.
        :rtype: str
        """
        return self._provider_name

    @provider_name.setter
    def provider_name(self, provider_name):
        """
        Sets the provider_name of this HealthChecksVantagePointSummary.
        The organization on whose infrastructure this vantage point resides.
        Provider names are not unique, as Oracle Cloud Infrastructure maintains
        many vantage points in each major provider.


        :param provider_name: The provider_name of this HealthChecksVantagePointSummary.
        :type: str
        """
        self._provider_name = provider_name

    @property
    def name(self):
        """
        Gets the name of this HealthChecksVantagePointSummary.
        The unique, permanent name for the vantage point.


        :return: The name of this HealthChecksVantagePointSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this HealthChecksVantagePointSummary.
        The unique, permanent name for the vantage point.


        :param name: The name of this HealthChecksVantagePointSummary.
        :type: str
        """
        self._name = name

    @property
    def geo(self):
        """
        Gets the geo of this HealthChecksVantagePointSummary.

        :return: The geo of this HealthChecksVantagePointSummary.
        :rtype: Geolocation
        """
        return self._geo

    @geo.setter
    def geo(self, geo):
        """
        Sets the geo of this HealthChecksVantagePointSummary.

        :param geo: The geo of this HealthChecksVantagePointSummary.
        :type: Geolocation
        """
        self._geo = geo

    @property
    def routing(self):
        """
        Gets the routing of this HealthChecksVantagePointSummary.
        An array of objects that describe how traffic to this vantage point is
        routed, including which prefixes and ASNs connect it to the internet.

        The addresses are sorted from the most-specific to least-specific
        prefix (the smallest network to largest network). When a prefix has
        multiple origin ASNs (MOAS routing), they are sorted by weight
        (highest to lowest). Weight is determined by the total percentage of
        peers observing the prefix originating from an ASN. Only present if
        `fields` includes `routing`. The field will be null if the address's
        routing information is unknown.


        :return: The routing of this HealthChecksVantagePointSummary.
        :rtype: list[Routing]
        """
        return self._routing

    @routing.setter
    def routing(self, routing):
        """
        Sets the routing of this HealthChecksVantagePointSummary.
        An array of objects that describe how traffic to this vantage point is
        routed, including which prefixes and ASNs connect it to the internet.

        The addresses are sorted from the most-specific to least-specific
        prefix (the smallest network to largest network). When a prefix has
        multiple origin ASNs (MOAS routing), they are sorted by weight
        (highest to lowest). Weight is determined by the total percentage of
        peers observing the prefix originating from an ASN. Only present if
        `fields` includes `routing`. The field will be null if the address's
        routing information is unknown.


        :param routing: The routing of this HealthChecksVantagePointSummary.
        :type: list[Routing]
        """
        self._routing = routing

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AvailabilityDomain(object):
    """
    Availability Domains
    """

    #: A constant which can be used with the ads property of a AvailabilityDomain.
    #: This constant has a value of "AD1"
    ADS_AD1 = "AD1"

    #: A constant which can be used with the ads property of a AvailabilityDomain.
    #: This constant has a value of "AD2"
    ADS_AD2 = "AD2"

    #: A constant which can be used with the ads property of a AvailabilityDomain.
    #: This constant has a value of "AD3"
    ADS_AD3 = "AD3"

    def __init__(self, **kwargs):
        """
        Initializes a new AvailabilityDomain object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param ads:
            The value to assign to the ads property of this AvailabilityDomain.
            Allowed values for this property are: "AD1", "AD2", "AD3"
        :type ads: str

        """
        self.swagger_types = {
            'ads': 'str'
        }

        self.attribute_map = {
            'ads': 'ads'
        }

        self._ads = None

    @property
    def ads(self):
        """
        Gets the ads of this AvailabilityDomain.
        Availability Domain Identifiers

        Allowed values for this property are: "AD1", "AD2", "AD3"


        :return: The ads of this AvailabilityDomain.
        :rtype: str
        """
        return self._ads

    @ads.setter
    def ads(self, ads):
        """
        Sets the ads of this AvailabilityDomain.
        Availability Domain Identifiers


        :param ads: The ads of this AvailabilityDomain.
        :type: str
        """
        allowed_values = ["AD1", "AD2", "AD3"]
        if not value_allowed_none_or_none_sentinel(ads, allowed_values):
            raise ValueError(
                "Invalid value for `ads`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._ads = ads

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ShippingAddress(object):
    """
    ShippingAddress model.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ShippingAddress object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param addressee:
            The value to assign to the addressee property of this ShippingAddress.
        :type addressee: str

        :param care_of:
            The value to assign to the care_of property of this ShippingAddress.
        :type care_of: str

        :param address1:
            The value to assign to the address1 property of this ShippingAddress.
        :type address1: str

        :param address2:
            The value to assign to the address2 property of this ShippingAddress.
        :type address2: str

        :param address3:
            The value to assign to the address3 property of this ShippingAddress.
        :type address3: str

        :param address4:
            The value to assign to the address4 property of this ShippingAddress.
        :type address4: str

        :param city_or_locality:
            The value to assign to the city_or_locality property of this ShippingAddress.
        :type city_or_locality: str

        :param state_or_region:
            The value to assign to the state_or_region property of this ShippingAddress.
        :type state_or_region: str

        :param zipcode:
            The value to assign to the zipcode property of this ShippingAddress.
        :type zipcode: str

        :param country:
            The value to assign to the country property of this ShippingAddress.
        :type country: str

        :param phone_number:
            The value to assign to the phone_number property of this ShippingAddress.
        :type phone_number: str

        :param email:
            The value to assign to the email property of this ShippingAddress.
        :type email: str

        """
        self.swagger_types = {
            'addressee': 'str',
            'care_of': 'str',
            'address1': 'str',
            'address2': 'str',
            'address3': 'str',
            'address4': 'str',
            'city_or_locality': 'str',
            'state_or_region': 'str',
            'zipcode': 'str',
            'country': 'str',
            'phone_number': 'str',
            'email': 'str'
        }

        self.attribute_map = {
            'addressee': 'addressee',
            'care_of': 'careOf',
            'address1': 'address1',
            'address2': 'address2',
            'address3': 'address3',
            'address4': 'address4',
            'city_or_locality': 'cityOrLocality',
            'state_or_region': 'stateOrRegion',
            'zipcode': 'zipcode',
            'country': 'country',
            'phone_number': 'phoneNumber',
            'email': 'email'
        }

        self._addressee = None
        self._care_of = None
        self._address1 = None
        self._address2 = None
        self._address3 = None
        self._address4 = None
        self._city_or_locality = None
        self._state_or_region = None
        self._zipcode = None
        self._country = None
        self._phone_number = None
        self._email = None

    @property
    def addressee(self):
        """
        Gets the addressee of this ShippingAddress.

        :return: The addressee of this ShippingAddress.
        :rtype: str
        """
        return self._addressee

    @addressee.setter
    def addressee(self, addressee):
        """
        Sets the addressee of this ShippingAddress.

        :param addressee: The addressee of this ShippingAddress.
        :type: str
        """
        self._addressee = addressee

    @property
    def care_of(self):
        """
        Gets the care_of of this ShippingAddress.

        :return: The care_of of this ShippingAddress.
        :rtype: str
        """
        return self._care_of

    @care_of.setter
    def care_of(self, care_of):
        """
        Sets the care_of of this ShippingAddress.

        :param care_of: The care_of of this ShippingAddress.
        :type: str
        """
        self._care_of = care_of

    @property
    def address1(self):
        """
        Gets the address1 of this ShippingAddress.

        :return: The address1 of this ShippingAddress.
        :rtype: str
        """
        return self._address1

    @address1.setter
    def address1(self, address1):
        """
        Sets the address1 of this ShippingAddress.

        :param address1: The address1 of this ShippingAddress.
        :type: str
        """
        self._address1 = address1

    @property
    def address2(self):
        """
        Gets the address2 of this ShippingAddress.

        :return: The address2 of this ShippingAddress.
        :rtype: str
        """
        return self._address2

    @address2.setter
    def address2(self, address2):
        """
        Sets the address2 of this ShippingAddress.

        :param address2: The address2 of this ShippingAddress.
        :type: str
        """
        self._address2 = address2

    @property
    def address3(self):
        """
        Gets the address3 of this ShippingAddress.

        :return: The address3 of this ShippingAddress.
        :rtype: str
        """
        return self._address3

    @address3.setter
    def address3(self, address3):
        """
        Sets the address3 of this ShippingAddress.

        :param address3: The address3 of this ShippingAddress.
        :type: str
        """
        self._address3 = address3

    @property
    def address4(self):
        """
        Gets the address4 of this ShippingAddress.

        :return: The address4 of this ShippingAddress.
        :rtype: str
        """
        return self._address4

    @address4.setter
    def address4(self, address4):
        """
        Sets the address4 of this ShippingAddress.

        :param address4: The address4 of this ShippingAddress.
        :type: str
        """
        self._address4 = address4

    @property
    def city_or_locality(self):
        """
        Gets the city_or_locality of this ShippingAddress.

        :return: The city_or_locality of this ShippingAddress.
        :rtype: str
        """
        return self._city_or_locality

    @city_or_locality.setter
    def city_or_locality(self, city_or_locality):
        """
        Sets the city_or_locality of this ShippingAddress.

        :param city_or_locality: The city_or_locality of this ShippingAddress.
        :type: str
        """
        self._city_or_locality = city_or_locality

    @property
    def state_or_region(self):
        """
        Gets the state_or_region of this ShippingAddress.

        :return: The state_or_region of this ShippingAddress.
        :rtype: str
        """
        return self._state_or_region

    @state_or_region.setter
    def state_or_region(self, state_or_region):
        """
        Sets the state_or_region of this ShippingAddress.

        :param state_or_region: The state_or_region of this ShippingAddress.
        :type: str
        """
        self._state_or_region = state_or_region

    @property
    def zipcode(self):
        """
        Gets the zipcode of this ShippingAddress.

        :return: The zipcode of this ShippingAddress.
        :rtype: str
        """
        return self._zipcode

    @zipcode.setter
    def zipcode(self, zipcode):
        """
        Sets the zipcode of this ShippingAddress.

        :param zipcode: The zipcode of this ShippingAddress.
        :type: str
        """
        self._zipcode = zipcode

    @property
    def country(self):
        """
        Gets the country of this ShippingAddress.

        :return: The country of this ShippingAddress.
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """
        Sets the country of this ShippingAddress.

        :param country: The country of this ShippingAddress.
        :type: str
        """
        self._country = country

    @property
    def phone_number(self):
        """
        Gets the phone_number of this ShippingAddress.

        :return: The phone_number of this ShippingAddress.
        :rtype: str
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        """
        Sets the phone_number of this ShippingAddress.

        :param phone_number: The phone_number of this ShippingAddress.
        :type: str
        """
        self._phone_number = phone_number

    @property
    def email(self):
        """
        Gets the email of this ShippingAddress.

        :return: The email of this ShippingAddress.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this ShippingAddress.

        :param email: The email of this ShippingAddress.
        :type: str
        """
        self._email = email

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

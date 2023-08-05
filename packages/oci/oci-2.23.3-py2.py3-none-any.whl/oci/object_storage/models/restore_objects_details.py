# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RestoreObjectsDetails(object):
    """
    RestoreObjectsDetails model.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RestoreObjectsDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param object_name:
            The value to assign to the object_name property of this RestoreObjectsDetails.
        :type object_name: str

        :param hours:
            The value to assign to the hours property of this RestoreObjectsDetails.
        :type hours: int

        :param version_id:
            The value to assign to the version_id property of this RestoreObjectsDetails.
        :type version_id: str

        """
        self.swagger_types = {
            'object_name': 'str',
            'hours': 'int',
            'version_id': 'str'
        }

        self.attribute_map = {
            'object_name': 'objectName',
            'hours': 'hours',
            'version_id': 'versionId'
        }

        self._object_name = None
        self._hours = None
        self._version_id = None

    @property
    def object_name(self):
        """
        **[Required]** Gets the object_name of this RestoreObjectsDetails.
        An object that is in an archive storage tier and needs to be restored.


        :return: The object_name of this RestoreObjectsDetails.
        :rtype: str
        """
        return self._object_name

    @object_name.setter
    def object_name(self, object_name):
        """
        Sets the object_name of this RestoreObjectsDetails.
        An object that is in an archive storage tier and needs to be restored.


        :param object_name: The object_name of this RestoreObjectsDetails.
        :type: str
        """
        self._object_name = object_name

    @property
    def hours(self):
        """
        Gets the hours of this RestoreObjectsDetails.
        The number of hours for which this object will be restored.
        By default objects will be restored for 24 hours. You can instead configure the duration using the hours parameter.


        :return: The hours of this RestoreObjectsDetails.
        :rtype: int
        """
        return self._hours

    @hours.setter
    def hours(self, hours):
        """
        Sets the hours of this RestoreObjectsDetails.
        The number of hours for which this object will be restored.
        By default objects will be restored for 24 hours. You can instead configure the duration using the hours parameter.


        :param hours: The hours of this RestoreObjectsDetails.
        :type: int
        """
        self._hours = hours

    @property
    def version_id(self):
        """
        Gets the version_id of this RestoreObjectsDetails.
        The versionId of the object to restore. Current object version is used by default.


        :return: The version_id of this RestoreObjectsDetails.
        :rtype: str
        """
        return self._version_id

    @version_id.setter
    def version_id(self, version_id):
        """
        Sets the version_id of this RestoreObjectsDetails.
        The versionId of the object to restore. Current object version is used by default.


        :param version_id: The version_id of this RestoreObjectsDetails.
        :type: str
        """
        self._version_id = version_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

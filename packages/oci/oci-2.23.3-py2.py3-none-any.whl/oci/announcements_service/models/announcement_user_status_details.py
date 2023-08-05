# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AnnouncementUserStatusDetails(object):
    """
    An announcement's status regarding whether it has been acknowledged by a user.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AnnouncementUserStatusDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param user_status_announcement_id:
            The value to assign to the user_status_announcement_id property of this AnnouncementUserStatusDetails.
        :type user_status_announcement_id: str

        :param user_id:
            The value to assign to the user_id property of this AnnouncementUserStatusDetails.
        :type user_id: str

        :param time_acknowledged:
            The value to assign to the time_acknowledged property of this AnnouncementUserStatusDetails.
        :type time_acknowledged: datetime

        """
        self.swagger_types = {
            'user_status_announcement_id': 'str',
            'user_id': 'str',
            'time_acknowledged': 'datetime'
        }

        self.attribute_map = {
            'user_status_announcement_id': 'userStatusAnnouncementId',
            'user_id': 'userId',
            'time_acknowledged': 'timeAcknowledged'
        }

        self._user_status_announcement_id = None
        self._user_id = None
        self._time_acknowledged = None

    @property
    def user_status_announcement_id(self):
        """
        **[Required]** Gets the user_status_announcement_id of this AnnouncementUserStatusDetails.
        The OCID of the announcement that this status is associated with.


        :return: The user_status_announcement_id of this AnnouncementUserStatusDetails.
        :rtype: str
        """
        return self._user_status_announcement_id

    @user_status_announcement_id.setter
    def user_status_announcement_id(self, user_status_announcement_id):
        """
        Sets the user_status_announcement_id of this AnnouncementUserStatusDetails.
        The OCID of the announcement that this status is associated with.


        :param user_status_announcement_id: The user_status_announcement_id of this AnnouncementUserStatusDetails.
        :type: str
        """
        self._user_status_announcement_id = user_status_announcement_id

    @property
    def user_id(self):
        """
        **[Required]** Gets the user_id of this AnnouncementUserStatusDetails.
        The OCID of the user that this status is associated with.


        :return: The user_id of this AnnouncementUserStatusDetails.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this AnnouncementUserStatusDetails.
        The OCID of the user that this status is associated with.


        :param user_id: The user_id of this AnnouncementUserStatusDetails.
        :type: str
        """
        self._user_id = user_id

    @property
    def time_acknowledged(self):
        """
        Gets the time_acknowledged of this AnnouncementUserStatusDetails.
        The date and time the announcement was acknowledged, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-01-01T17:43:01.389+0000`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_acknowledged of this AnnouncementUserStatusDetails.
        :rtype: datetime
        """
        return self._time_acknowledged

    @time_acknowledged.setter
    def time_acknowledged(self, time_acknowledged):
        """
        Sets the time_acknowledged of this AnnouncementUserStatusDetails.
        The date and time the announcement was acknowledged, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-01-01T17:43:01.389+0000`

        __ https://tools.ietf.org/html/rfc3339


        :param time_acknowledged: The time_acknowledged of this AnnouncementUserStatusDetails.
        :type: datetime
        """
        self._time_acknowledged = time_acknowledged

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

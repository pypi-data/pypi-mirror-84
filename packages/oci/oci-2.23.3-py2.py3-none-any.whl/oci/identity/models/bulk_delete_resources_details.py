# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class BulkDeleteResourcesDetails(object):
    """
    BulkDeleteResourcesDetails model.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new BulkDeleteResourcesDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param resources:
            The value to assign to the resources property of this BulkDeleteResourcesDetails.
        :type resources: list[BulkActionResource]

        """
        self.swagger_types = {
            'resources': 'list[BulkActionResource]'
        }

        self.attribute_map = {
            'resources': 'resources'
        }

        self._resources = None

    @property
    def resources(self):
        """
        **[Required]** Gets the resources of this BulkDeleteResourcesDetails.
        The resources to be deleted.


        :return: The resources of this BulkDeleteResourcesDetails.
        :rtype: list[BulkActionResource]
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """
        Sets the resources of this BulkDeleteResourcesDetails.
        The resources to be deleted.


        :param resources: The resources of this BulkDeleteResourcesDetails.
        :type: list[BulkActionResource]
        """
        self._resources = resources

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateTargetDetectorRecipe(object):
    """
    The information to be updated in attached Target DetectorRecipe
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateTargetDetectorRecipe object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param target_detector_recipe_id:
            The value to assign to the target_detector_recipe_id property of this UpdateTargetDetectorRecipe.
        :type target_detector_recipe_id: str

        :param detector_rules:
            The value to assign to the detector_rules property of this UpdateTargetDetectorRecipe.
        :type detector_rules: list[UpdateTargetRecipeDetectorRuleDetails]

        """
        self.swagger_types = {
            'target_detector_recipe_id': 'str',
            'detector_rules': 'list[UpdateTargetRecipeDetectorRuleDetails]'
        }

        self.attribute_map = {
            'target_detector_recipe_id': 'targetDetectorRecipeId',
            'detector_rules': 'detectorRules'
        }

        self._target_detector_recipe_id = None
        self._detector_rules = None

    @property
    def target_detector_recipe_id(self):
        """
        **[Required]** Gets the target_detector_recipe_id of this UpdateTargetDetectorRecipe.
        Identifier for DetectorRecipe.


        :return: The target_detector_recipe_id of this UpdateTargetDetectorRecipe.
        :rtype: str
        """
        return self._target_detector_recipe_id

    @target_detector_recipe_id.setter
    def target_detector_recipe_id(self, target_detector_recipe_id):
        """
        Sets the target_detector_recipe_id of this UpdateTargetDetectorRecipe.
        Identifier for DetectorRecipe.


        :param target_detector_recipe_id: The target_detector_recipe_id of this UpdateTargetDetectorRecipe.
        :type: str
        """
        self._target_detector_recipe_id = target_detector_recipe_id

    @property
    def detector_rules(self):
        """
        **[Required]** Gets the detector_rules of this UpdateTargetDetectorRecipe.
        Updates to be applied to Detector Rule associated with the target


        :return: The detector_rules of this UpdateTargetDetectorRecipe.
        :rtype: list[UpdateTargetRecipeDetectorRuleDetails]
        """
        return self._detector_rules

    @detector_rules.setter
    def detector_rules(self, detector_rules):
        """
        Sets the detector_rules of this UpdateTargetDetectorRecipe.
        Updates to be applied to Detector Rule associated with the target


        :param detector_rules: The detector_rules of this UpdateTargetDetectorRecipe.
        :type: list[UpdateTargetRecipeDetectorRuleDetails]
        """
        self._detector_rules = detector_rules

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

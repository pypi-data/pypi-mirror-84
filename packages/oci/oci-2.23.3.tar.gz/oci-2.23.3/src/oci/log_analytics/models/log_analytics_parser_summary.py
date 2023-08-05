# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class LogAnalyticsParserSummary(object):
    """
    LoganParserDetails
    """

    #: A constant which can be used with the type property of a LogAnalyticsParserSummary.
    #: This constant has a value of "XML"
    TYPE_XML = "XML"

    #: A constant which can be used with the type property of a LogAnalyticsParserSummary.
    #: This constant has a value of "JSON"
    TYPE_JSON = "JSON"

    #: A constant which can be used with the type property of a LogAnalyticsParserSummary.
    #: This constant has a value of "REGEX"
    TYPE_REGEX = "REGEX"

    #: A constant which can be used with the type property of a LogAnalyticsParserSummary.
    #: This constant has a value of "ODL"
    TYPE_ODL = "ODL"

    def __init__(self, **kwargs):
        """
        Initializes a new LogAnalyticsParserSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param content:
            The value to assign to the content property of this LogAnalyticsParserSummary.
        :type content: str

        :param description:
            The value to assign to the description property of this LogAnalyticsParserSummary.
        :type description: str

        :param display_name:
            The value to assign to the display_name property of this LogAnalyticsParserSummary.
        :type display_name: str

        :param edit_version:
            The value to assign to the edit_version property of this LogAnalyticsParserSummary.
        :type edit_version: int

        :param encoding:
            The value to assign to the encoding property of this LogAnalyticsParserSummary.
        :type encoding: str

        :param example_content:
            The value to assign to the example_content property of this LogAnalyticsParserSummary.
        :type example_content: str

        :param field_maps:
            The value to assign to the field_maps property of this LogAnalyticsParserSummary.
        :type field_maps: list[LogAnalyticsParserField]

        :param footer_content:
            The value to assign to the footer_content property of this LogAnalyticsParserSummary.
        :type footer_content: str

        :param header_content:
            The value to assign to the header_content property of this LogAnalyticsParserSummary.
        :type header_content: str

        :param name:
            The value to assign to the name property of this LogAnalyticsParserSummary.
        :type name: str

        :param is_default:
            The value to assign to the is_default property of this LogAnalyticsParserSummary.
        :type is_default: bool

        :param is_single_line_content:
            The value to assign to the is_single_line_content property of this LogAnalyticsParserSummary.
        :type is_single_line_content: bool

        :param is_system:
            The value to assign to the is_system property of this LogAnalyticsParserSummary.
        :type is_system: bool

        :param language:
            The value to assign to the language property of this LogAnalyticsParserSummary.
        :type language: str

        :param time_updated:
            The value to assign to the time_updated property of this LogAnalyticsParserSummary.
        :type time_updated: datetime

        :param log_type_test_request_version:
            The value to assign to the log_type_test_request_version property of this LogAnalyticsParserSummary.
        :type log_type_test_request_version: int

        :param mapped_parsers:
            The value to assign to the mapped_parsers property of this LogAnalyticsParserSummary.
        :type mapped_parsers: list[LogAnalyticsParser]

        :param parser_ignoreline_characters:
            The value to assign to the parser_ignoreline_characters property of this LogAnalyticsParserSummary.
        :type parser_ignoreline_characters: str

        :param is_hidden:
            The value to assign to the is_hidden property of this LogAnalyticsParserSummary.
        :type is_hidden: bool

        :param parser_sequence:
            The value to assign to the parser_sequence property of this LogAnalyticsParserSummary.
        :type parser_sequence: int

        :param parser_timezone:
            The value to assign to the parser_timezone property of this LogAnalyticsParserSummary.
        :type parser_timezone: str

        :param parser_filter:
            The value to assign to the parser_filter property of this LogAnalyticsParserSummary.
        :type parser_filter: LogAnalyticsParserFilter

        :param is_parser_written_once:
            The value to assign to the is_parser_written_once property of this LogAnalyticsParserSummary.
        :type is_parser_written_once: bool

        :param parser_functions:
            The value to assign to the parser_functions property of this LogAnalyticsParserSummary.
        :type parser_functions: list[LogAnalyticsParserFunction]

        :param sources_count:
            The value to assign to the sources_count property of this LogAnalyticsParserSummary.
        :type sources_count: int

        :param sources:
            The value to assign to the sources property of this LogAnalyticsParserSummary.
        :type sources: list[LogAnalyticsSource]

        :param should_tokenize_original_text:
            The value to assign to the should_tokenize_original_text property of this LogAnalyticsParserSummary.
        :type should_tokenize_original_text: bool

        :param type:
            The value to assign to the type property of this LogAnalyticsParserSummary.
            Allowed values for this property are: "XML", "JSON", "REGEX", "ODL", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param is_user_deleted:
            The value to assign to the is_user_deleted property of this LogAnalyticsParserSummary.
        :type is_user_deleted: bool

        """
        self.swagger_types = {
            'content': 'str',
            'description': 'str',
            'display_name': 'str',
            'edit_version': 'int',
            'encoding': 'str',
            'example_content': 'str',
            'field_maps': 'list[LogAnalyticsParserField]',
            'footer_content': 'str',
            'header_content': 'str',
            'name': 'str',
            'is_default': 'bool',
            'is_single_line_content': 'bool',
            'is_system': 'bool',
            'language': 'str',
            'time_updated': 'datetime',
            'log_type_test_request_version': 'int',
            'mapped_parsers': 'list[LogAnalyticsParser]',
            'parser_ignoreline_characters': 'str',
            'is_hidden': 'bool',
            'parser_sequence': 'int',
            'parser_timezone': 'str',
            'parser_filter': 'LogAnalyticsParserFilter',
            'is_parser_written_once': 'bool',
            'parser_functions': 'list[LogAnalyticsParserFunction]',
            'sources_count': 'int',
            'sources': 'list[LogAnalyticsSource]',
            'should_tokenize_original_text': 'bool',
            'type': 'str',
            'is_user_deleted': 'bool'
        }

        self.attribute_map = {
            'content': 'content',
            'description': 'description',
            'display_name': 'displayName',
            'edit_version': 'editVersion',
            'encoding': 'encoding',
            'example_content': 'exampleContent',
            'field_maps': 'fieldMaps',
            'footer_content': 'footerContent',
            'header_content': 'headerContent',
            'name': 'name',
            'is_default': 'isDefault',
            'is_single_line_content': 'isSingleLineContent',
            'is_system': 'isSystem',
            'language': 'language',
            'time_updated': 'timeUpdated',
            'log_type_test_request_version': 'logTypeTestRequestVersion',
            'mapped_parsers': 'mappedParsers',
            'parser_ignoreline_characters': 'parserIgnorelineCharacters',
            'is_hidden': 'isHidden',
            'parser_sequence': 'parserSequence',
            'parser_timezone': 'parserTimezone',
            'parser_filter': 'parserFilter',
            'is_parser_written_once': 'isParserWrittenOnce',
            'parser_functions': 'parserFunctions',
            'sources_count': 'sourcesCount',
            'sources': 'sources',
            'should_tokenize_original_text': 'shouldTokenizeOriginalText',
            'type': 'type',
            'is_user_deleted': 'isUserDeleted'
        }

        self._content = None
        self._description = None
        self._display_name = None
        self._edit_version = None
        self._encoding = None
        self._example_content = None
        self._field_maps = None
        self._footer_content = None
        self._header_content = None
        self._name = None
        self._is_default = None
        self._is_single_line_content = None
        self._is_system = None
        self._language = None
        self._time_updated = None
        self._log_type_test_request_version = None
        self._mapped_parsers = None
        self._parser_ignoreline_characters = None
        self._is_hidden = None
        self._parser_sequence = None
        self._parser_timezone = None
        self._parser_filter = None
        self._is_parser_written_once = None
        self._parser_functions = None
        self._sources_count = None
        self._sources = None
        self._should_tokenize_original_text = None
        self._type = None
        self._is_user_deleted = None

    @property
    def content(self):
        """
        Gets the content of this LogAnalyticsParserSummary.
        content


        :return: The content of this LogAnalyticsParserSummary.
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content):
        """
        Sets the content of this LogAnalyticsParserSummary.
        content


        :param content: The content of this LogAnalyticsParserSummary.
        :type: str
        """
        self._content = content

    @property
    def description(self):
        """
        Gets the description of this LogAnalyticsParserSummary.
        description


        :return: The description of this LogAnalyticsParserSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this LogAnalyticsParserSummary.
        description


        :param description: The description of this LogAnalyticsParserSummary.
        :type: str
        """
        self._description = description

    @property
    def display_name(self):
        """
        Gets the display_name of this LogAnalyticsParserSummary.
        display name


        :return: The display_name of this LogAnalyticsParserSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this LogAnalyticsParserSummary.
        display name


        :param display_name: The display_name of this LogAnalyticsParserSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def edit_version(self):
        """
        Gets the edit_version of this LogAnalyticsParserSummary.
        edit version


        :return: The edit_version of this LogAnalyticsParserSummary.
        :rtype: int
        """
        return self._edit_version

    @edit_version.setter
    def edit_version(self, edit_version):
        """
        Sets the edit_version of this LogAnalyticsParserSummary.
        edit version


        :param edit_version: The edit_version of this LogAnalyticsParserSummary.
        :type: int
        """
        self._edit_version = edit_version

    @property
    def encoding(self):
        """
        Gets the encoding of this LogAnalyticsParserSummary.
        encoding


        :return: The encoding of this LogAnalyticsParserSummary.
        :rtype: str
        """
        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        """
        Sets the encoding of this LogAnalyticsParserSummary.
        encoding


        :param encoding: The encoding of this LogAnalyticsParserSummary.
        :type: str
        """
        self._encoding = encoding

    @property
    def example_content(self):
        """
        Gets the example_content of this LogAnalyticsParserSummary.
        example content


        :return: The example_content of this LogAnalyticsParserSummary.
        :rtype: str
        """
        return self._example_content

    @example_content.setter
    def example_content(self, example_content):
        """
        Sets the example_content of this LogAnalyticsParserSummary.
        example content


        :param example_content: The example_content of this LogAnalyticsParserSummary.
        :type: str
        """
        self._example_content = example_content

    @property
    def field_maps(self):
        """
        Gets the field_maps of this LogAnalyticsParserSummary.
        fields Maps


        :return: The field_maps of this LogAnalyticsParserSummary.
        :rtype: list[LogAnalyticsParserField]
        """
        return self._field_maps

    @field_maps.setter
    def field_maps(self, field_maps):
        """
        Sets the field_maps of this LogAnalyticsParserSummary.
        fields Maps


        :param field_maps: The field_maps of this LogAnalyticsParserSummary.
        :type: list[LogAnalyticsParserField]
        """
        self._field_maps = field_maps

    @property
    def footer_content(self):
        """
        Gets the footer_content of this LogAnalyticsParserSummary.
        footer regular expression


        :return: The footer_content of this LogAnalyticsParserSummary.
        :rtype: str
        """
        return self._footer_content

    @footer_content.setter
    def footer_content(self, footer_content):
        """
        Sets the footer_content of this LogAnalyticsParserSummary.
        footer regular expression


        :param footer_content: The footer_content of this LogAnalyticsParserSummary.
        :type: str
        """
        self._footer_content = footer_content

    @property
    def header_content(self):
        """
        Gets the header_content of this LogAnalyticsParserSummary.
        header content


        :return: The header_content of this LogAnalyticsParserSummary.
        :rtype: str
        """
        return self._header_content

    @header_content.setter
    def header_content(self, header_content):
        """
        Sets the header_content of this LogAnalyticsParserSummary.
        header content


        :param header_content: The header_content of this LogAnalyticsParserSummary.
        :type: str
        """
        self._header_content = header_content

    @property
    def name(self):
        """
        Gets the name of this LogAnalyticsParserSummary.
        Name


        :return: The name of this LogAnalyticsParserSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this LogAnalyticsParserSummary.
        Name


        :param name: The name of this LogAnalyticsParserSummary.
        :type: str
        """
        self._name = name

    @property
    def is_default(self):
        """
        Gets the is_default of this LogAnalyticsParserSummary.
        is default flag


        :return: The is_default of this LogAnalyticsParserSummary.
        :rtype: bool
        """
        return self._is_default

    @is_default.setter
    def is_default(self, is_default):
        """
        Sets the is_default of this LogAnalyticsParserSummary.
        is default flag


        :param is_default: The is_default of this LogAnalyticsParserSummary.
        :type: bool
        """
        self._is_default = is_default

    @property
    def is_single_line_content(self):
        """
        Gets the is_single_line_content of this LogAnalyticsParserSummary.
        is single line content


        :return: The is_single_line_content of this LogAnalyticsParserSummary.
        :rtype: bool
        """
        return self._is_single_line_content

    @is_single_line_content.setter
    def is_single_line_content(self, is_single_line_content):
        """
        Sets the is_single_line_content of this LogAnalyticsParserSummary.
        is single line content


        :param is_single_line_content: The is_single_line_content of this LogAnalyticsParserSummary.
        :type: bool
        """
        self._is_single_line_content = is_single_line_content

    @property
    def is_system(self):
        """
        Gets the is_system of this LogAnalyticsParserSummary.
        is system flag


        :return: The is_system of this LogAnalyticsParserSummary.
        :rtype: bool
        """
        return self._is_system

    @is_system.setter
    def is_system(self, is_system):
        """
        Sets the is_system of this LogAnalyticsParserSummary.
        is system flag


        :param is_system: The is_system of this LogAnalyticsParserSummary.
        :type: bool
        """
        self._is_system = is_system

    @property
    def language(self):
        """
        Gets the language of this LogAnalyticsParserSummary.
        language


        :return: The language of this LogAnalyticsParserSummary.
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """
        Sets the language of this LogAnalyticsParserSummary.
        language


        :param language: The language of this LogAnalyticsParserSummary.
        :type: str
        """
        self._language = language

    @property
    def time_updated(self):
        """
        Gets the time_updated of this LogAnalyticsParserSummary.
        last updated date


        :return: The time_updated of this LogAnalyticsParserSummary.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this LogAnalyticsParserSummary.
        last updated date


        :param time_updated: The time_updated of this LogAnalyticsParserSummary.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def log_type_test_request_version(self):
        """
        Gets the log_type_test_request_version of this LogAnalyticsParserSummary.
        log type test request version


        :return: The log_type_test_request_version of this LogAnalyticsParserSummary.
        :rtype: int
        """
        return self._log_type_test_request_version

    @log_type_test_request_version.setter
    def log_type_test_request_version(self, log_type_test_request_version):
        """
        Sets the log_type_test_request_version of this LogAnalyticsParserSummary.
        log type test request version


        :param log_type_test_request_version: The log_type_test_request_version of this LogAnalyticsParserSummary.
        :type: int
        """
        self._log_type_test_request_version = log_type_test_request_version

    @property
    def mapped_parsers(self):
        """
        Gets the mapped_parsers of this LogAnalyticsParserSummary.
        mapped parser list


        :return: The mapped_parsers of this LogAnalyticsParserSummary.
        :rtype: list[LogAnalyticsParser]
        """
        return self._mapped_parsers

    @mapped_parsers.setter
    def mapped_parsers(self, mapped_parsers):
        """
        Sets the mapped_parsers of this LogAnalyticsParserSummary.
        mapped parser list


        :param mapped_parsers: The mapped_parsers of this LogAnalyticsParserSummary.
        :type: list[LogAnalyticsParser]
        """
        self._mapped_parsers = mapped_parsers

    @property
    def parser_ignoreline_characters(self):
        """
        Gets the parser_ignoreline_characters of this LogAnalyticsParserSummary.
        parser ignore line characters


        :return: The parser_ignoreline_characters of this LogAnalyticsParserSummary.
        :rtype: str
        """
        return self._parser_ignoreline_characters

    @parser_ignoreline_characters.setter
    def parser_ignoreline_characters(self, parser_ignoreline_characters):
        """
        Sets the parser_ignoreline_characters of this LogAnalyticsParserSummary.
        parser ignore line characters


        :param parser_ignoreline_characters: The parser_ignoreline_characters of this LogAnalyticsParserSummary.
        :type: str
        """
        self._parser_ignoreline_characters = parser_ignoreline_characters

    @property
    def is_hidden(self):
        """
        Gets the is_hidden of this LogAnalyticsParserSummary.
        is hidden flag


        :return: The is_hidden of this LogAnalyticsParserSummary.
        :rtype: bool
        """
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, is_hidden):
        """
        Sets the is_hidden of this LogAnalyticsParserSummary.
        is hidden flag


        :param is_hidden: The is_hidden of this LogAnalyticsParserSummary.
        :type: bool
        """
        self._is_hidden = is_hidden

    @property
    def parser_sequence(self):
        """
        Gets the parser_sequence of this LogAnalyticsParserSummary.
        sequence


        :return: The parser_sequence of this LogAnalyticsParserSummary.
        :rtype: int
        """
        return self._parser_sequence

    @parser_sequence.setter
    def parser_sequence(self, parser_sequence):
        """
        Sets the parser_sequence of this LogAnalyticsParserSummary.
        sequence


        :param parser_sequence: The parser_sequence of this LogAnalyticsParserSummary.
        :type: int
        """
        self._parser_sequence = parser_sequence

    @property
    def parser_timezone(self):
        """
        Gets the parser_timezone of this LogAnalyticsParserSummary.
        time zone


        :return: The parser_timezone of this LogAnalyticsParserSummary.
        :rtype: str
        """
        return self._parser_timezone

    @parser_timezone.setter
    def parser_timezone(self, parser_timezone):
        """
        Sets the parser_timezone of this LogAnalyticsParserSummary.
        time zone


        :param parser_timezone: The parser_timezone of this LogAnalyticsParserSummary.
        :type: str
        """
        self._parser_timezone = parser_timezone

    @property
    def parser_filter(self):
        """
        Gets the parser_filter of this LogAnalyticsParserSummary.

        :return: The parser_filter of this LogAnalyticsParserSummary.
        :rtype: LogAnalyticsParserFilter
        """
        return self._parser_filter

    @parser_filter.setter
    def parser_filter(self, parser_filter):
        """
        Sets the parser_filter of this LogAnalyticsParserSummary.

        :param parser_filter: The parser_filter of this LogAnalyticsParserSummary.
        :type: LogAnalyticsParserFilter
        """
        self._parser_filter = parser_filter

    @property
    def is_parser_written_once(self):
        """
        Gets the is_parser_written_once of this LogAnalyticsParserSummary.
        write once


        :return: The is_parser_written_once of this LogAnalyticsParserSummary.
        :rtype: bool
        """
        return self._is_parser_written_once

    @is_parser_written_once.setter
    def is_parser_written_once(self, is_parser_written_once):
        """
        Sets the is_parser_written_once of this LogAnalyticsParserSummary.
        write once


        :param is_parser_written_once: The is_parser_written_once of this LogAnalyticsParserSummary.
        :type: bool
        """
        self._is_parser_written_once = is_parser_written_once

    @property
    def parser_functions(self):
        """
        Gets the parser_functions of this LogAnalyticsParserSummary.
        plugin instance list


        :return: The parser_functions of this LogAnalyticsParserSummary.
        :rtype: list[LogAnalyticsParserFunction]
        """
        return self._parser_functions

    @parser_functions.setter
    def parser_functions(self, parser_functions):
        """
        Sets the parser_functions of this LogAnalyticsParserSummary.
        plugin instance list


        :param parser_functions: The parser_functions of this LogAnalyticsParserSummary.
        :type: list[LogAnalyticsParserFunction]
        """
        self._parser_functions = parser_functions

    @property
    def sources_count(self):
        """
        Gets the sources_count of this LogAnalyticsParserSummary.
        sources using this parser


        :return: The sources_count of this LogAnalyticsParserSummary.
        :rtype: int
        """
        return self._sources_count

    @sources_count.setter
    def sources_count(self, sources_count):
        """
        Sets the sources_count of this LogAnalyticsParserSummary.
        sources using this parser


        :param sources_count: The sources_count of this LogAnalyticsParserSummary.
        :type: int
        """
        self._sources_count = sources_count

    @property
    def sources(self):
        """
        Gets the sources of this LogAnalyticsParserSummary.
        sources using list


        :return: The sources of this LogAnalyticsParserSummary.
        :rtype: list[LogAnalyticsSource]
        """
        return self._sources

    @sources.setter
    def sources(self, sources):
        """
        Sets the sources of this LogAnalyticsParserSummary.
        sources using list


        :param sources: The sources of this LogAnalyticsParserSummary.
        :type: list[LogAnalyticsSource]
        """
        self._sources = sources

    @property
    def should_tokenize_original_text(self):
        """
        Gets the should_tokenize_original_text of this LogAnalyticsParserSummary.
        tokenize original text


        :return: The should_tokenize_original_text of this LogAnalyticsParserSummary.
        :rtype: bool
        """
        return self._should_tokenize_original_text

    @should_tokenize_original_text.setter
    def should_tokenize_original_text(self, should_tokenize_original_text):
        """
        Sets the should_tokenize_original_text of this LogAnalyticsParserSummary.
        tokenize original text


        :param should_tokenize_original_text: The should_tokenize_original_text of this LogAnalyticsParserSummary.
        :type: bool
        """
        self._should_tokenize_original_text = should_tokenize_original_text

    @property
    def type(self):
        """
        Gets the type of this LogAnalyticsParserSummary.
        type

        Allowed values for this property are: "XML", "JSON", "REGEX", "ODL", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this LogAnalyticsParserSummary.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this LogAnalyticsParserSummary.
        type


        :param type: The type of this LogAnalyticsParserSummary.
        :type: str
        """
        allowed_values = ["XML", "JSON", "REGEX", "ODL"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def is_user_deleted(self):
        """
        Gets the is_user_deleted of this LogAnalyticsParserSummary.
        user deleted flag


        :return: The is_user_deleted of this LogAnalyticsParserSummary.
        :rtype: bool
        """
        return self._is_user_deleted

    @is_user_deleted.setter
    def is_user_deleted(self, is_user_deleted):
        """
        Sets the is_user_deleted of this LogAnalyticsParserSummary.
        user deleted flag


        :param is_user_deleted: The is_user_deleted of this LogAnalyticsParserSummary.
        :type: bool
        """
        self._is_user_deleted = is_user_deleted

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

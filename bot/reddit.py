import re


class LinkModCommand(object):
    """
    Represents a !linkmod-type string, typically found
    in a Reddit comment or submission.
    """
    __slots__ = ('query', 'multiple')

    COMMAND_PATTERN = re.compile(r'''
    \b  # Start capture on a word boundary (including an exclamation point)
    link
    [^\S\r\n]*  # Optional space after "link" (no newline)
    mod(?P<multiple>s?)  # Also keep track of singular or plural "mod"
    (?:[^\S\r\n]*:[^\S\r\n]*|[^\S\r\n]+)  # Some sort of colon/space separator
    (?P<query>.+?)  # Capture the non-empty query in a named group
    (?:\.|;|$)  # End capture on period, semicolon, or end of line
    ''', re.IGNORECASE | re.MULTILINE | re.VERBOSE)

    def __init__(self, query, multiple):
        self.query = query
        self.multiple = multiple

    def __repr__(self):
        return 'LinkModCommand({!r}, {!r})'.format(self.query, self.multiple)

    def __eq__(self, other):
        return (self.query, self.multiple) == (other.query, other.multiple)

    @classmethod
    def all_in_text(cls, text):
        """
        Generator that yields all valid ``LinkModCommands``
        in the given string.

        :param text: the string to parse for commands
        """
        for match in cls.COMMAND_PATTERN.finditer(text):
            query = match.group('query')
            multiple = bool(match.group('multiple'))

            yield LinkModCommand(query, multiple)

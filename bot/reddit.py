import re


class LinkModCommand(object):
    """
    Represents a !linkmod-type string, typically found
    in a Reddit comment or submission.
    """
    __slots__ = ('query', 'amount')

    COMMAND_PATTERN = re.compile(r'''
    \b  # Start capture on a word boundary (including an exclamation point)
    link
    [^\S\r\n]*  # Optional space after "link" (no newline)
    (?P<amount>\d*)
    [^\S\r\n]*  # Optional space before "mod" (no newline)
    mods?  # Allow singular or plural "mod" but don't keep track of it
    (?:[^\S\r\n]*:[^\S\r\n]*|[^\S\r\n]+)  # Some sort of colon/space separator
    (?P<query>.+?)  # Capture the non-empty query in a named group
    (?:\.|;|$)  # End capture on period, semicolon, or end of line
    ''', re.IGNORECASE | re.MULTILINE | re.VERBOSE)

    def __init__(self, query, amount):
        self.query = query
        self.amount = max(amount, 1)

    def __repr__(self):
        return 'LinkModCommand({!r}, {!r})'.format(self.query, self.amount)

    def __eq__(self, other):
        return (self.query, self.amount) == (other.query, other.amount)

    @classmethod
    def all_in_text(cls, text):
        """
        Generator that yields all valid ``LinkModCommands``
        in the given string.

        :param text: the string to parse for commands
        """
        for match in cls.COMMAND_PATTERN.finditer(text):
            query = match.group('query')
            amount = int(match.group('amount') or 1)

            yield LinkModCommand(query, amount)


def replied_to(comment, redditor):  # pragma: no cover
    """
    Return whether the given comment was directly replied to
    by the given Redditor.

    :param comment: the comment to check
    :param redditor: the Redditor to check for
    :return: whether ``redditor`` replied to ``comment``
    """
    comment.replies.replace_more(limit=None)  # TODO: Necessary?
    return any(reply.author == redditor for reply in comment.replies)

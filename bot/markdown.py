SEARCH_RESULT_FORMAT = ('{title} | {author} | {last_updated} '
                        '| {downloads:,d} | {versions}')
COMMENT_FORMAT = '''###LinkMod:

Title | Author | Last updated | Downloads | Versions
:---|:---|:---|:---|:---
{0}

*****

^Bleep ^bloop, ^I'm ^a ^bot ^that ^links ^Factorio ^mods. ^| \
^Usage: ^(`linkmods: Squeak Through`) ^| \
^[GitHub](https://github.com/Sparta142/factorio-mod-portal-bot)
'''

# Markdown formatting characters to escape in hyperlinks, etc
ESCAPED_CHARACTERS = '\\`*_{}[]()#+-.!'


def escape(s):
    """
    Backslash-escape most Markdown formatting characters
    in a given string.

    :param s: the Markdown string to escape
    :return: the escaped string
    """
    return ''.join('\\' + ch if ch in ESCAPED_CHARACTERS else ch for ch in s)


def hyperlink(text, url):
    """
    Format a hyperlink with the specified text,
    escaping any problem characters as required.

    :param text: the text that should appear in place of the URL
    :param url: the url to link to
    :return: the Markdown-formatted link
    """
    return '[{}]({})'.format(escape(text), escape(url))


def format_search_result(result):
    """
    Format a single SearchResult in Markdown.

    :param result: the search result to format
    :return: the formatted result
    """
    return SEARCH_RESULT_FORMAT.format(
        title=hyperlink(result.title, result.link),
        author=hyperlink(result.author, result.author_link),
        downloads=result.downloads,
        last_updated=result.last_updated,
        versions=result.versions
    )


def format_comment(search_results):
    """
    Format a list of SearchResults in Markdown as a Reddit comment.

    :param search_results: the search results to format with
    :return: the formatted comment
    """
    results_str = '\n'.join(format_search_result(r) for r in search_results)
    return COMMENT_FORMAT.format(results_str)

def hyperlink(text, url):
    """
    Format a hyperlink with the specified text,
    escaping any problem characters as required.

    :param text: the text that should appear in place of the URL
    :param url: the url to link to
    :return: the Markdown-formatted link
    """
    escaped_text = text.replace('[', r'\[').replace(']', r'\]')
    escaped_url = url.replace('(', r'\(').replace(')', r'\)')

    return '[{}]({})'.format(escaped_text, escaped_url)

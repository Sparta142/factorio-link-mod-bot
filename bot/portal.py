import urllib.parse


class ModPortal(object):
    """ Wrapper around the Factorio mod portal website. """

    @staticmethod
    def _sanitize_query(query):
        """
        Sanitize a query string for use with the Factorio mod portal.

        :param query: the string to sanitize
        :return: the sanitized string
        """
        return urllib.parse.quote(query.replace('/', ''))

import lxml.html
import requests
import urllib.parse
from lxml.cssselect import CSSSelector

MOD_PORTAL_URL = 'https://mods.factorio.com'


class SearchResult(object):
    """ Represents a single search result from the mod portal. """

    __slots__ = ('__dict__', 'title', 'link', 'author', 'author_link',
                 'last_updated', 'versions', 'downloads')

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.link = kwargs.get('link')
        self.author = kwargs.get('author')
        self.author_link = kwargs.get('author_link')
        self.last_updated = kwargs.get('last_updated')
        self.versions = kwargs.get('versions')
        self.downloads = kwargs.get('downloads')

    def __str__(self):
        return '{} by {}'.format(self.title, self.author)

    def __eq__(self, other):
        return (self.title == other.title
                and self.link == other.link
                and self.author == other.author
                and self.author_link == other.author_link
                and self.last_updated == other.last_updated
                and self.versions == other.versions
                and self.downloads == other.downloads)

    # noinspection PyCallingNonCallable
    @classmethod
    def from_element(cls, element):
        """
        Create a :class:`SearchResult` from an lxml Element.

        :param element: the element to create a SearchResult from
        :return: the new SearchResult
        """
        element.make_links_absolute(MOD_PORTAL_URL)

        # "Top-level" elements
        mod_card_title = cls.select_title(element)[0]
        mod_card_author = cls.select_author(element)[0]
        mod_card_info = cls.select_info(element)[0]

        # Elements that aren't important enough to be listed above
        link = mod_card_title.find('a')
        author_link = mod_card_author.find('a')
        last_updated = cls.select_last_updated(mod_card_info)[0]
        versions = cls.select_versions(mod_card_info)[0]
        downloads = cls.select_downloads(mod_card_info)[0]

        return SearchResult(
            title=mod_card_title.text_content().strip(),
            link=link.get('href'),
            author=mod_card_author.text_content().strip()[3:],  # Remove 'by '
            author_link=author_link.get('href'),
            last_updated=last_updated.text_content().strip(),
            versions=versions.text_content().strip(),
            downloads=int(downloads.text_content())
        )

    # Precompiled CSS selector functions, for performance reasons
    select_title = CSSSelector('.mod-card-title', translator='html')
    select_author = CSSSelector('.mod-card-author', translator='html')
    select_info = CSSSelector('.mod-card-info', translator='html')
    select_last_updated = CSSSelector('span:nth-of-type(1)', translator='html')
    select_versions = CSSSelector('span:nth-of-type(2)', translator='html')
    select_downloads = CSSSelector('span:nth-of-type(3)', translator='html')


class ModPortal(object):
    """ Wrapper around the Factorio mod portal website. """

    QUERY_URL = MOD_PORTAL_URL + '/query/{}/downloaded/1'

    def __init__(self, user_agent=None):
        self._session = requests.Session()

        if user_agent is not None:
            self._session.headers.update({
                'User-Agent': user_agent
            })

    def search(self, query):
        """
        Search for a query on the Factorio mod portal
        and return the first page of search results.

        :param query: the query string to search for
        """
        response = self._do_search(query)
        return self._parse_mods(response.text)

    @classmethod
    def _parse_mods(cls, html):
        """
        Return a list of all ``.mod-card`` elements in the
        given HTML document.

        :param html: the HTML document to parse for elements
        :return: the list of mod cards
        """
        document = lxml.html.document_fromstring(html)
        results = []

        for element in cls.select_mod_cards(document):
            results.append(SearchResult.from_element(element))

        return results

    def _do_search(self, query):
        """
        Make a web request to the mod portal and return
        the resulting response object.

        :param query: the string to search the mod portal for
        :return: the mod portal response
        """
        query = self._sanitize_query(query)
        url = self.QUERY_URL.format(query)

        return self._session.get(url)

    @staticmethod
    def _sanitize_query(query):
        """
        Sanitize a query string for use with the Factorio mod portal.

        :param query: the string to sanitize
        :return: the sanitized string
        """
        return urllib.parse.quote(query.replace('/', ''))

    # Precompiled CSS selector function, for performance reasons
    select_mod_cards = CSSSelector('.mod-card', translator='html')

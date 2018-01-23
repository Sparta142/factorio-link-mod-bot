import requests
import urllib.parse
from bs4 import BeautifulSoup

MOD_PORTAL_URL = 'https://mods.factorio.com'


class ModCard(object):
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

    def __eq__(self, other):
        return (self.title == other.title
                and self.link == other.link
                and self.author == other.author
                and self.author_link == other.author_link
                and self.last_updated == other.last_updated
                and self.versions == other.versions
                and self.downloads == other.downloads)

    @classmethod
    def from_tag(cls, tag):
        """
        Create a :class:`ModCard` from a BeautifulSoup Tag.

        :param tag: the tag to create a ModCard from
        :return: the new ModCard
        """

        # "Top-level" tags
        mod_card_title = tag.select_one('.mod-card-title')
        mod_card_author = tag.select_one('.mod-card-author')
        mod_card_info = tag.select_one('.mod-card-info')

        # Tags that aren't important enough to be listed above
        link_tag = mod_card_title.find('a')
        author_link_tag = mod_card_author.find('a')
        last_updated_tag = mod_card_info.select_one('span:nth-of-type(1)')
        versions_tag = mod_card_info.select_one('span:nth-of-type(2)')
        downloads_tag = mod_card_info.select_one('span:nth-of-type(3)')

        return ModCard(
            title=mod_card_title.text.strip(),
            link=MOD_PORTAL_URL + link_tag['href'],
            author=mod_card_author.text.strip()[3:],  # Remove 'by '
            author_link=MOD_PORTAL_URL + author_link_tag['href'],
            last_updated=last_updated_tag.text.strip(),
            versions=versions_tag.text.strip(),
            downloads=int(downloads_tag.text.strip())
        )


class ModPortal(object):
    """ Wrapper around the Factorio mod portal website. """

    QUERY_URL = MOD_PORTAL_URL + '/query/'

    def __init__(self, user_agent=None):
        self._session = requests.Session()

        if user_agent is not None:
            self._session.headers.update({
                'User-Agent': user_agent
            })

    @staticmethod
    def _parse_mods(html):
        """
        Generator that yields all ``.mod-card`` tags in
        the given HTML document.

        :param html: the HTMl document to parse for mods
        """
        soup = BeautifulSoup(html, 'lxml')

        for tag in soup.select('.mod-card'):
            yield ModCard.from_tag(tag)

    def _do_search(self, query):
        """
        Make a web request to the mod portal and return
        the resulting response object.

        :param query: the string to search the mod portal for
        :return: the mod portal response
        """
        query = self._sanitize_query(query)
        url = self.QUERY_URL + query

        return self._session.get(url)

    @staticmethod
    def _sanitize_query(query):
        """
        Sanitize a query string for use with the Factorio mod portal.

        :param query: the string to sanitize
        :return: the sanitized string
        """
        return urllib.parse.quote(query.replace('/', ''))

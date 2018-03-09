import lxml.html
import os
from pytest import fixture
from unittest.mock import patch

from bot.portal import SearchResult, ModPortal

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, 'data')


@fixture(scope='session')
def html():
    filename = os.path.join(DATA_DIR, 'example.html')

    # Use ./data/example.html as the example mod portal response HTML
    with open(filename, 'rt', encoding='utf-8') as f:
        return f.read()


class TestSearchResult(object):
    @fixture(scope='session')
    def element(self):
        filename = os.path.join(DATA_DIR, 'example_element.html')

        # Use ./data/example_element.html as the example mod card HTML element
        with open(filename, 'rt', encoding='utf-8') as f:
            return lxml.html.fragment_fromstring(f.read())

    def test_from_tag_all_present(self, element):
        expected = SearchResult(
            title="Bob's Warfare",
            link='https://mods.factorio.com/mod/bobwarfare',
            author='Bobingabout',
            author_link='https://mods.factorio.com/user/Bobingabout',
            last_updated='a day ago',
            versions='0.13 - 0.16',
            downloads=186367
        )
        actual = SearchResult.from_element(element)

        assert actual == expected


# noinspection PyProtectedMember
# noinspection PyShadowingNames
class TestModPortal(object):
    def test_sanitize_query_simple(self):
        sanitized = ModPortal._sanitize_query('helloworld123')
        assert sanitized == 'helloworld123'

    def test_sanitize_query_with_spaces(self):
        sanitized = ModPortal._sanitize_query('hello world 123')
        assert sanitized == 'hello%20world%20123'

    def test_sanitize_query_with_slashes(self):
        sanitized = ModPortal._sanitize_query('hello/world/123')
        assert sanitized == 'helloworld123'

    def test_sanitize_query_with_emoji(self):
        sanitized = ModPortal._sanitize_query('\U0001F600')
        assert sanitized == '%F0%9F%98%80'

    def test_user_agent_is_used_if_present(self):
        portal = ModPortal('my_user_agent')
        assert portal._session.headers['User-Agent'] == 'my_user_agent'

    def test_fallback_on_default_user_agent_if_missing(self):
        portal = ModPortal()
        assert 'User-Agent' in portal._session.headers

    @patch('requests.Session.get')
    def test_do_search_actually_makes_a_web_request(self, get):
        portal = ModPortal()
        portal._do_search('hello')

        get.assert_called_once_with(
            'https://mods.factorio.com/query/hello/downloaded/1')

    def test_parse_mods_yields_all_mods_in_document(self, html):
        mods = list(ModPortal._parse_mods(html))
        assert len(mods) == 20

        # Check that every parsed mod card has no invalid data
        for mod_card in mods:
            for value in vars(mod_card).values():
                assert value is not None

    @patch('requests.Session.get')
    def test_search(self, get, *, html):
        get.return_value.text = html

        portal = ModPortal()
        mods = portal.search('hello')

        # Check that every parsed mod card has no invalid data
        for mod_card in mods:
            for value in vars(mod_card).values():
                assert value is not None

    @patch('requests.Session.get')
    def test_search_exact(self, get, *, html):
        get.return_value.text = html

        portal = ModPortal()
        mods = portal.search_exact("boB'S")

        # Assert that every mod card contains "Bob's"
        for mod_card in mods:
            assert "Bob's" in mod_card.title


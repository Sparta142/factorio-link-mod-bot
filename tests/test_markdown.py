from pytest import fixture

from bot.markdown import hyperlink, format_search_result, format_comment
from bot.portal import SearchResult


class TestHyperlinkFunction(object):
    def test_no_edge_cases(self):
        expected = '[text](http://example.com)'
        actual = hyperlink('text', 'http://example.com')

        assert expected == actual

    def test_square_brackets_in_text(self):
        expected = r'[\]text\[](http://example.com)'
        actual = hyperlink(']text[', 'http://example.com')

        assert expected == actual

    def test_square_brackets_in_url(self):
        expected = '[text](http://example.com/Some_[thing])'
        actual = hyperlink('text', 'http://example.com/Some_[thing]')

        assert expected == actual

    def test_parentheses_in_text(self):
        expected = '[text (thing)](http://example.com)'
        actual = hyperlink('text (thing)', 'http://example.com')

        assert expected == actual

    def test_parentheses_in_url(self):
        expected = r'[text](http://example.com/Some_\(thing\))'
        actual = hyperlink('text', 'http://example.com/Some_(thing)')

        assert expected == actual


class TestFormatFunctions(object):
    @fixture
    def result(self):
        return SearchResult(
            title='SampleMod',
            link='http://example.com/mod/SamplePageMod',
            author='SampleAuthor',
            author_link='http://example.com/user/SamplePageAuthor',
            downloads=123456,
            last_updated='a month ago'
        )

    def test_format_search_result_basic(self, result):
        formatted = format_search_result(result)

        # Just check that it contains all relevant data /somehow/
        assert 'SampleMod' in formatted
        assert 'http://example.com/mod/SamplePageMod' in formatted
        assert 'SampleAuthor' in formatted
        assert 'http://example.com/user/SamplePageAuthor' in formatted
        assert '123,456' in formatted
        assert 'a month ago' in formatted

    def test_format_comment_basic(self, result):
        formatted = format_comment([result] * 7)

        # Just check that it contains all relevant data /somehow/
        assert formatted.count('SampleMod') == 7
        assert formatted.count('http://example.com/mod/SamplePageMod') == 7
        assert formatted.count('SampleAuthor') == 7
        assert formatted.count('http://example.com/user/SamplePageAuthor') == 7
        assert formatted.count('123,456') == 7
        assert formatted.count('a month ago') == 7

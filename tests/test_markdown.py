from bot.markdown import hyperlink


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

from bot.portal import ModPortal


# noinspection PyProtectedMember
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

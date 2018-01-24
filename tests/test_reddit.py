from bot.reddit import LinkModCommand


class TestLinkModCommand(object):
    def test_all_in_text_empty_string(self):
        assert list(LinkModCommand.all_in_text('')) == []

    def test_all_in_text_no_commands(self):
        assert list(LinkModCommand.all_in_text('hello world')) == []

    def test_all_in_text_one_command_singular(self):
        expected = [LinkModCommand('modname', False)]
        actual = list(LinkModCommand.all_in_text('linkmod: modname'))

        assert expected == actual

    def test_all_in_text_two_commands_singular(self):
        expected = [
            LinkModCommand('modname', False),
            LinkModCommand('modname2', False)
        ]
        actual = list(LinkModCommand.all_in_text(
            'linkmod: modname\n!linkmod: modname2'))

        assert expected == actual

    def test_all_in_text_one_command_multiple(self):
        expected = [LinkModCommand('modname', True)]
        actual = list(LinkModCommand.all_in_text('!linkmods: modname'))

        assert expected == actual

    def test_all_in_text_two_commands_multiple(self):
        expected = [
            LinkModCommand('modname', True),
            LinkModCommand('modname2', True)
        ]
        actual = list(LinkModCommand.all_in_text(
            'linkmods: modname\n!linkmods: modname2'))

        assert expected == actual

    def test_pattern_edge_cases(self):
        pattern = LinkModCommand.COMMAND_PATTERN

        # Patterns that should be found
        assert pattern.search('linkmod thing')
        assert pattern.search('!linkmod thing')
        assert pattern.search('link mod thing')
        assert pattern.search('liNK\t  MoD thing')
        assert pattern.search('linkmods thing')
        assert pattern.search('?linkMOD thing')
        assert pattern.search(':link   mod: thing')
        assert pattern.search(':linkMODS: thing')
        assert pattern.search('!!! link mods thing')
        assert pattern.search('linkmod:thing')
        assert pattern.search('&*^%*link\t   \t  MOD:\t\t  thing')

        # Patterns that should not be found
        assert not pattern.search('linkmad thing')
        assert not pattern.search('linkmod')
        assert not pattern.search('linkmods')
        assert not pattern.search('link\nmod thing')
        assert not pattern.search('linkmad thing')
        assert not pattern.search('linkmod:\n thing')
        assert not pattern.search('linkmods\nthing')

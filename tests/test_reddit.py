from bot.reddit import LinkModCommand


class TestLinkModCommand(object):
    def test_all_in_text_empty_string(self):
        assert list(LinkModCommand.all_in_text('')) == []

    def test_all_in_text_no_commands(self):
        assert list(LinkModCommand.all_in_text('hello world')) == []

    def test_all_in_text_one_command_singular(self):
        expected = [LinkModCommand('modname', 1)]
        actual = list(LinkModCommand.all_in_text('linkmod: modname'))

        assert expected == actual

    def test_all_in_text_two_commands_singular(self):
        expected = [
            LinkModCommand('modname', 1),
            LinkModCommand('modname2', 1)
        ]
        actual = list(LinkModCommand.all_in_text(
            'linkmod: modname\n!linkmod: modname2'))

        assert expected == actual

    def test_all_in_text_one_command_multiple(self):
        expected = [LinkModCommand('modname', 6)]
        actual = list(LinkModCommand.all_in_text('!link6mods: modname'))

        assert expected == actual

    def test_all_in_text_two_commands_multiple(self):
        expected = [
            LinkModCommand('modname', 8),
            LinkModCommand('modname2', 20)
        ]
        actual = list(LinkModCommand.all_in_text(
            'link8mods: modname\n!link20mod: modname2'))

        assert expected == actual

    def test_all_in_text_does_not_allow_zero(self):
        expected = [LinkModCommand('modname', 1)]
        actual = list(LinkModCommand.all_in_text('link0mods: modname'))

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
        assert pattern.search('link0mods: thing')
        assert pattern.search('link 1337 mods: thing')
        assert pattern.search('link20 mods thing')
        assert pattern.search('link 1mods: thing')

        # Patterns that should not be found
        assert not pattern.search('linkmad thing')
        assert not pattern.search('linkmod')
        assert not pattern.search('linkmods')
        assert not pattern.search('link\nmod thing')
        assert not pattern.search('linkmad thing')
        assert not pattern.search('linkmod:\n thing')
        assert not pattern.search('linkmods\nthing')
        assert not pattern.search('link-60mods\nthing')

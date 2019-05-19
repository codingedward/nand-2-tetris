import sys

from lexer import Command

class Parser:
    def __init__(self):
        self._pos = 0
        self._tokens = []

    def set_tokens(self, tokens):
        self._tokens = tokens
    
    def has_commands(self):
        return self._pos < len(self._tokens)
    
    def advance(self):
        self._assert_has_commands()
        self._pos += 1

    def reset_pos(self):
        self._pos = 0

    def pos(self):
        return self._pos
    
    def command_type(self):
        self._assert_has_commands()
        return self._tokens[self._pos]["command"]
    
    def symbol(self):
        self._assert_has_commands()
        self._assert_command_one_of(
            'self.symbol', 
            [Command.A_COMMAND, Command.L_COMMAND]
        )
        return self._tokens[self._pos].get('symbol')

    def value(self):
        self._assert_has_commands()
        self._assert_command_one_of('self.value', [Command.A_COMMAND])
        return self._tokens[self._pos].get('value')
    
    def dest(self):
        self._assert_has_commands()
        self._assert_command_one_of(
            'self.dest', 
            [Command.C_COMMAND_JMP, Command.C_COMMAND_COMP]
        )
        return self._tokens[self._pos].get('dest')
    
    def comp(self):
        self._assert_has_commands()
        self._assert_command_one_of(
            'self.comp', 
            [Command.C_COMMAND_JMP, Command.C_COMMAND_COMP]
        )
        return self._tokens[self._pos].get('comp')
    
    def jump(self):
        self._assert_has_commands()
        self._assert_command_one_of('self.jump', [Command.C_COMMAND_JMP])
        return self._tokens[self._pos].get('jump')

    def _assert_command_one_of(self, method, valid):
        if not self.command_type() in valid:
            sys.stderr.write('Wrong attempt to get token in %s' % method)
            sys.exit(1)

    def _assert_has_commands(self):
        if not self.has_commands():
            sys.stderr.write('Parser index out of bounds')
            sys.exit(1)

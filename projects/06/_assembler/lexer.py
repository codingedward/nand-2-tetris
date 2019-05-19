import sys
import re

class Command:
    A_COMMAND = 'A_COMMAND'
    C_COMMAND_COMP = 'C_COMMAND_COMP'
    C_COMMAND_JMP = 'C_COMMAND_JMP'
    L_COMMAND = 'L_COMMAND'

class Lexer:
    def __init__(self):
        self._pos = 0
        self._tokens = []
        self.valid_tokens = [
            (r'[ \t\n\r]+', None),    # Ignore whitespace.
            (r'//[^\n]*', None),    # Ignore comment until new line.
            (r'\(([^0-9][a-zA-Z0-9_\.\$\:]+)\)',  # Match a label.
                Command.L_COMMAND), 
            (r"""                   # Match A-instruction
                @(([^0-9][a-zA-Z0-9_\.\$\:]+)|([0-9]+))""", # Starts with @ followed by a symbol or a number
                Command.A_COMMAND),
            (r"""                   # Match a C-Instruction compute part.
                (([AMD]{1,3})|null) # Destination is either A, M, D, some combination or null
                =
                (
                    ([AMD][+-][AMD1])   # Addition and substraction (supports use of 1).
                    |
                    ([AMD][|&][AMD])    # Bitwise And and Or (supports registers only).
                    |
                    ((-|!)?(0|1|D|A|M)) # Bitwise and Logical Negation
                )
                """, Command.C_COMMAND_COMP),
            (r'(A|D|0);(null|JGT|JEQ|JGE|JLT|JNE|JLE|JMP)', # Jump instruction
                Command.C_COMMAND_JMP) 
        ]

    def lex(self, chars):
        self._pos = 0
        while self._pos < len(chars):
            match = None
            for valid_token in self.valid_tokens:
                pattern, command = valid_token
                regex = re.compile(pattern, re.VERBOSE)
                match = regex.match(chars, self._pos)
                if match:
                    self._add_command(command, match)
                    break
            if match is None:
                sys.stderr.write('Unknown character: %s\n\n' % chars[self._pos])
                sys.exit(1)
            else:
                self._pos = match.end(0)
    
    def tokens(self):
        return self._tokens

    def pos(self):
        return self._pos

    def _add_command(self, command, match):
        if command is Command.L_COMMAND:
            self._add_l_command(match)
        elif command is Command.A_COMMAND:
            self._add_a_command(match)
        elif command is Command.C_COMMAND_COMP:
            self._add_c_command_comp(match)
        elif command is Command.C_COMMAND_JMP:
            self._add_c_command_jump(match)

    def _add_l_command(self, match):
        self._tokens.append({
            'command': Command.L_COMMAND,
            'text': match.group(0),
            'symbol': match.group(1),
        })
    
    def _add_a_command(self, match):
        self._tokens.append({
            'command': Command.A_COMMAND,
            'text': match.group(0),
            'symbol': match.group(2),
            'value': match.group(3),
        })

    def _add_c_command_comp(self, match):
        self._tokens.append({
            'command': Command.C_COMMAND_COMP,
            'text': match.group(0),
            'dest': match.group(1),
            'comp': match.group(3),
        })
    
    def _add_c_command_jump(self, match):
        self._tokens.append({
            'command': Command.C_COMMAND_JMP,
            'text': match.group(0),
            'comp': match.group(1),
            'jump': match.group(2),
        })

    

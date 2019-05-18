import sys
import re

A_COMMAND = 'A_COMMAND'
C_COMMAND_COMP = 'C_COMMAND_COMP'
C_COMMAND_JMP = 'C_COMMAND_JMP'
L_COMMAND = 'L_COMMAND'


valid_tokens = [
    (r'[ \t\n]+', None),    # Ignore whitespace.
    (r'//[^\n]*', None),    # Ignore comment until new line.
    (r'\(([^0-9][a-zA-Z0-9_\.\$\:]+)\)', L_COMMAND), # Match a label.
    (r"""                   # Match A-instruction
        @                   # Starts with @ followed by ...
        (                   
            ([^0-9][a-zA-Z0-9_\.\$\:]+) # a symbol ...
            |
            ([0-9]+)        # or a number.
        )""", A_COMMAND),
    (r"""                   # Match a C-Instruction compute part.
        (
            ([AMD]{1,3})    # Destination is either A, M, D or some combination.
            |
            null            # Null destination.
        )
        =
        (
            ([AMD][+-][AMD1])   # Addition and substraction (supports use of 1).
            |
            ([AMD][|&][AMD])    # Bitwise And and Or (supports registers only).
            |
            (                   # Bitwise and Logical Negation
                (-|!)?
                (0|1|D|A|M)
            )
        )
        """, C_COMMAND_COMP),
    (r'(A|D|0);(null|JGT|JEQ|JGE|JLT|JNE|JLE|JMP)', C_COMMAND_JMP) # Jump instruction
]


def lex(chars):
    tokens = []
    pos = 0
    while pos < len(chars):
        match = None
        for valid_token in valid_tokens:
            pattern, tag = valid_token
            regex = re.compile(pattern, re.VERBOSE)
            match = regex.match(chars, pos)
            if match:
                text = match.group(0)
                if tag is L_COMMAND:
                    token = {
                        "tag": tag,
                        "text": match.group(0),
                        "symbol": match.group(1),
                    }
                    tokens.append(token)
                elif tag is A_COMMAND:
                    token = {
                        "tag": tag,
                        "text": match.group(0),
                        "symbol": match.group(2),
                        "value": match.group(3),
                    }
                    tokens.append(token)
                elif tag is C_COMMAND_COMP:
                    token = {
                        "tag": tag,
                        "text": match.group(0),
                        'dest': match.group(1),
                        "comp": match.group(3),
                    }
                    tokens.append(token)
                elif tag is C_COMMAND_JMP:
                    token = {
                        "tag": tag,
                        "text": match.group(0),
                        "register": match.group(1),
                        "jmp": match.group(2)
                    }
                    tokens.append(token)
                break
        if match is None:
            sys.stderr.write('Unknown character: %s\n\n' % chars[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens

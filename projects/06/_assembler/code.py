import sys
import re

class Code:
    def __init__(self):
        self.dest_map = [
            (r'(AMD|ADM|MAD|MDA|DMA|DAM)', '111'),
            (r'(AM|MA)', '101'),
            (r'(MD|DM)', '011'),
            (r'(AD|DA)', '110'),
            (r'M', '001'),
            (r'D', '010'),
            (r'A', '100'),
            (r'null', '000'),
        ]

        self.jump_map = [
            (r'null', '000'),
            (r'JGT', '001'),
            (r'JEQ', '010'),
            (r'JGE', '011'),
            (r'JLT', '100'),
            (r'JNE', '101'),
            (r'JLE', '110'),
            (r'JMP', '111'),
        ]

        self.comp_map = [
            (r'D\+1', '0011111'),
            (r'A\+1', '0110111'),
            (r'M\+1', '1110111'),
            (r'D\-1', '0001110'),
            (r'A\-1', '0110010'),
            (r'M\-1', '1110010'),
            (r'(D\+A|A\+D)', '0000010'),
            (r'(D\+M|M\+D)', '1000010'),
            (r'D\-A', '0010011'),
            (r'D\-M', '1010011'),
            (r'A\-D', '0000111'),
            (r'M\-D', '1000111'),
            (r'(D&A|A&D)', '0000000'),
            (r'(D&M|M&D)', '1000000'),
            (r'(D\|A|A\|D)', '0010101'),
            (r'(D\|M|M\|D)', '1010101'),
            (r'0', '0101010'),
            (r'1', '0111111'),
            (r'\-1', '0111010'),
            (r'D', '0001100'),
            (r'A', '0110000'),
            (r'M', '1110000'),
            (r'!D', '0001101'),
            (r'!A', '0110001'),
            (r'!M', '1110001'),
            (r'\-D', '0001111'),
            (r'\-A', '0110011'),
            (r'\-M', '1110011'),
        ]

    def dest(self, mnemonic):
        return self._find_match(mnemonic, self.dest_map)

    def comp(self, mnemonic):
        return self._find_match(mnemonic, self.comp_map)
        
    def jump(self, mnemonic):
        return self._find_match(mnemonic, self.jump_map)

    def _find_match(self, mnemonic, match_map):
        pos = 0
        while pos < len(match_map):
            pattern, value = match_map[pos]
            regex = re.compile(pattern)
            if regex.match(mnemonic):
                return value
            pos += 1
        # Could not find match...
        sys.stderr.write('[Code]: Could not match mnemonic: %s' % mnemonic)
        sys.exit(1)

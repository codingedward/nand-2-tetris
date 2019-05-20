#!/usr/bin/python

import os
import sys

from code import Code
from lexer import Lexer, Command
from parser import Parser
from symbol_table import SymbolTable


class Assembler:
    def __init__(self):
        self._code = Code()
        self._lexer = Lexer()
        self._parser = Parser()
        self._symbol_table = SymbolTable()

    def assemble(self, path):
        # Read file content
        content = self._read_file_contents(path)
        # Lex the file contents
        self._lexer.lex(content)
        # Pass the tokens to ther parser
        self._parser.set_tokens(self._lexer.tokens())
        # Build symbols
        self._build_symbols()
        # Translate to symbolless asm
        self._write_symbolless_asm(path)
        # Translate binary
        self._write_binary(path)

    def _write_symbolless_asm(self, path):
        basename = os.path.basename(path)
        name = basename.rsplit('.asm', 1)[0]
        file = open('%s/%sL.asm' % (os.path.dirname(path), name), 'w')
        self._parser.reset_pos()
        while self._parser.has_commands():
            command_type = self._parser.command_type()
            if command_type is Command.L_COMMAND:
                self._parser.advance()
                continue
            elif command_type is Command.A_COMMAND:
                value = None
                symbol = self._parser.symbol()
                if symbol is not None:
                    value = self._symbol_table.get_address(symbol)
                    if value is None:
                        sys.stderr.write('[Assembler]: Symbol not defined %s' % symbol)
                        file.close()
                        sys.exit(1)
                else:
                    value = self._parser.value()
                file.write('@%s' % value)
            elif command_type in [Command.C_COMMAND_JMP, Command.C_COMMAND_COMP]:
                file.write(self._parser.text())
            file.write('\n')
            self._parser.advance()
        file.close()

    def _write_binary(self, path):
        basename = os.path.basename(path)
        name = basename.rsplit('.asm', 1)[0]
        file = open('%s/%s.hack' % (os.path.dirname(path), name), 'w')
        binary = self._translate()
        file.write(binary)
        file.close()

    def _build_symbols(self):
        symbols_count = 0
        self._init_symbol_table()
        # First pass - get label symbols
        while self._parser.has_commands():
            if self._parser.command_type() is Command.L_COMMAND:
                symbol = self._parser.symbol()
                if self._symbol_table.contains(symbol):
                    sys.stderr.write('[Assembler]: Symbol %s is used more than once' % symbol)
                    sys.exit(1)
                address = self._parser.pos() - symbols_count
                self._symbol_table.add_entry(symbol, address)
                symbols_count += 1
            self._parser.advance()
        # Second pass - get variable symbols
        variable_address = 16
        self._parser.reset_pos()
        while self._parser.has_commands():
            command_type = self._parser.command_type()
            if command_type is Command.A_COMMAND:          
                symbol = self._parser.symbol()
                if symbol is not None and \
                        not self._symbol_table.contains(symbol):
                    address = variable_address
                    self._symbol_table.add_entry(symbol, address)
                    variable_address += 1
            self._parser.advance()

    def _translate(self):
        output = ''
        self._parser.reset_pos()
        while self._parser.has_commands():
            command_type = self._parser.command_type()
            if command_type is Command.A_COMMAND:          
                symbol = self._parser.symbol()
                if symbol is not None:
                    if not self._symbol_table.contains(symbol):
                        sys.stderr.write('[Assembler]: Unknown symbol: %s' % symbol)
                        sys.exit(1)
                    address = self._symbol_table.get_address(symbol)
                    output += self._to_binary(address) + '\n'
                else:
                    value = self._parser.value()
                    output += self._to_binary(int(value)) + '\n'
            elif command_type is Command.C_COMMAND_COMP:
                comp = self._code.comp(self._parser.comp())
                dest = self._code.dest(self._parser.dest())
                output += '111' + comp + dest + '000\n'
            elif command_type is Command.C_COMMAND_JMP:
                comp = self._code.comp(self._parser.comp())
                jump = self._code.jump(self._parser.jump())
                output += '111' + comp + '000' + jump + '\n'
            self._parser.advance()
        return output

    def _init_symbol_table(self):
        self._symbol_table.clear()
        entries = {
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'SCREEN': 16384,
            'KBD': 24576,
        }
        # R0 to R15
        for address in range(16):
            entries['R%d' % address] = address
        # Initialize symbol table with predefined symbols
        for key, value in entries.items():
            self._symbol_table.add_entry(key, value)


    def _read_file_contents(self, path):
        file = open(path, 'r')
        content = file.read()
        file.close()
        return content

    def _to_binary(self, value):
        return format(value, '016b')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: %s /path/to/file.asm\n' % sys.argv[0])
        print('Hack Assembler v0.0.1')
        print('By Edward Njoroge 20th May 2019\n')
        sys.exit(1)
    path = sys.argv[1]
    Assembler().assemble(path)
    name = os.path.basename(path).rsplit('.asm', 1)[0]
    print('[Assembler]: Successfully built %s.hack ...\n' % name)
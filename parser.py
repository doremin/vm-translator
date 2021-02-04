from enum import Enum    
from constant import *

class Parser:

    _command_table = {
        "add": C_ARITHMETIC,
        "sub": C_ARITHMETIC,
        "neg": C_ARITHMETIC,
        "eq": C_ARITHMETIC,
        "gt": C_ARITHMETIC,
        "lt": C_ARITHMETIC,
        "and": C_ARITHMETIC,
        "or": C_ARITHMETIC,
        "not": C_ARITHMETIC,
        "push": C_PUSH,
        "pop": C_POP,
        "label": C_LABEL,
        "goto": C_GOTO,
        "if-goto": C_IF,
        "function": C_FUNCTION,
        "return": C_RETURN,
        "call": C_CALL
    }

    _nullary = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not", "return"]
    _unary = ["label", "if-goto", "goto"]
    _binary = ["push", "pop", "function", "call"]

    def __init__(self, raw_data: str):
        self.command_type = None
        self.current_command = None
        self.operator = None
        self.operation_type = None
        self.current_line = 0
        self.raw_data = raw_data

    def has_more_commands(self) -> bool:
        if self.current_line >= len(self.raw_data):
            return False
        return True

    def advance(self):
        self.current_command = self.raw_data[self.current_line].split("//")[0].strip()
        self.current_line += 1

        if len(self.current_command) == 0:
            self.command_type = None
            return

        self.operator = self.current_command.split()[0]
        

        self.command_type = self._command_table[self.operator]
        
        if self.operator in self._nullary:
            self.operation_type = NULLARY
        elif self.operator in self._unary:
            self.operation_type = UNARY
        else:
            self.operation_type = BINARY

    def arg1(self) -> str:
        if self.operation_type == UNARY or self.operation_type == BINARY:
            return self.current_command.split()[1]

    def arg2(self) -> int:
        if self.operation_type == BINARY:
            return self.current_command.split()[2]

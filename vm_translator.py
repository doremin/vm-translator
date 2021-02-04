from argparse import ArgumentParser
from code_writer import CodeWriter
from parser import Parser
from constant import *
from os import path

def parse_args() -> str:
    arg_parser = ArgumentParser(
        description="python3 assembler.py <file_name>"
    )

    arg_parser.add_argument(
        "file_name",
    )

    return arg_parser.parse_args().file_name

def main():
    file_name = parse_args()
    file_name_noext, _ = path.splitext(file_name)

    raw_data = None
    with open(file_name, "r") as stream:
        raw_data = stream.readlines()

    parser = Parser(raw_data)

    code_writer = CodeWriter()
    code_writer.set_file_name(file_name_noext.split("/")[-1] + ".asm")

    while parser.has_more_commands():
        parser.advance()

        if parser.command_type == C_ARITHMETIC:
            code_writer.writer_arithmetic(parser.operator)
        elif parser.command_type == C_PUSH:
            code_writer.write_push_pop(parser.operator, parser.arg1(), parser.arg2())
        elif parser.command_type == C_POP:
            code_writer.write_push_pop(parser.operator, parser.arg1(), parser.arg2())
        elif parser.command_type == C_LABEL:
            pass
        elif parser.command_type == C_GOTO:
            pass
        elif parser.command_type == C_IF:
            pass
        elif parser.command_type == C_FUNCTION:
            pass
        elif parser.command_type == C_RETURN:
            pass
        elif parser.command_type == C_CALL:
            pass
        else:
            pass
    
    code_writer.close()

if __name__ == "__main__":
    main()

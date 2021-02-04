class CodeWriter:
    def __init__(self):
        self.file_name = None
        self.stream = None
        self.differ = 0

    def set_file_name(self, file_name: str):
        self.file_name = file_name
        self.stream = open(self.file_name, "w")

    def writer_arithmetic(self, command: str):
        translated_str = None

        if command == "add":
            translated_str = self._popD() + \
                "@R15\n" + \
                "M=D\n" + \
                self._popD() + \
                "@R15\n" + \
                "D=D+M\n" + \
                self._pushD()
        elif command == "sub":
            translated_str = self._popD() + \
                "@R15\n" + \
                "M=D\n" + \
                self._popD() + \
                "@R15\n" + \
                "D=D-M\n" + \
                self._pushD()
        elif command == "neg":
            translated_str = self._popD() + \
                "@0\n" + \
                "D=A-D\n" + \
                self._pushD()
        elif command == "eq":
            translated_str = self._popD() + \
                "@R15\n" + \
                "M=D\n" + \
                self._popD() + \
                "@R15\n" + \
                "D=D-M\n" + \
                f"@TRUE{self.differ}\n" + \
                "D;JEQ\n" + \
                f"@FALSE{self.differ}\n" + \
                "0;JMP\n" + \
                f"(TRUE{self.differ})\n" + \
                "D=-1\n" + \
                f"@END{self.differ}\n" + \
                "0;JMP\n" + \
                f"(FALSE{self.differ})\n" + \
                "D=0\n" + \
                f"@END{self.differ}\n" + \
                "0;JMP\n" + \
                f"(END{self.differ})\n" + \
                self._pushD()
            self.differ += 1
        elif command == "gt":
            translated_str = self._popD() + \
                "@R15\n" + \
                "M=D\n" + \
                self._popD() + \
                "@R15\n" + \
                "D=D-M\n" + \
                f"@TRUE{self.differ}\n" + \
                "D;JGT\n" + \
                f"@FALSE{self.differ}\n" + \
                "0;JMP\n" + \
                f"(TRUE{self.differ})\n" + \
                "D=-1\n" + \
                f"@END{self.differ}\n" + \
                "0;JMP\n" + \
                f"(FALSE{self.differ})\n" + \
                "D=0\n" + \
                f"@END{self.differ}\n" + \
                "0;JMP\n" + \
                f"(END{self.differ})\n" + \
                self._pushD()
            self.differ += 1
        elif command == "lt":
            translated_str = self._popD() + \
                "@R15\n" + \
                "M=D\n" + \
                self._popD() + \
                "@R15\n" + \
                "D=D-M\n" + \
                f"@TRUE{self.differ}\n" + \
                "D;JLT\n" + \
                f"@FALSE{self.differ}\n" + \
                "0;JMP\n" + \
                f"(TRUE{self.differ})\n" + \
                "D=-1\n" + \
                f"@END{self.differ}\n" + \
                "0;JMP\n" + \
                f"(FALSE{self.differ})\n" + \
                "D=0\n" + \
                f"@END{self.differ}\n" + \
                "0;JMP\n" + \
                f"(END{self.differ})\n" + \
                self._pushD()
            self.differ += 1
        elif command == "and":
            translated_str = self._popD() + \
                "@R15\n" + \
                "M=D\n" + \
                self._popD() + \
                "@R15\n" + \
                "D=D&M\n" + \
                self._pushD()
        elif command == "or":
            translated_str = self._popD() + \
                "@R15\n" + \
                "M=D\n" + \
                self._popD() + \
                "@R15\n" + \
                "D=D|M\n" + \
                self._pushD()
        elif command == "not":
            translated_str = self._popD() + \
                "D=!D\n" + \
                self._pushD()

        self.stream.write(translated_str)

    _segment_table = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
        "pointer": "3",
        "temp": "5"
    }

    def _pushD(self) -> str:
        return "@SP\n" + \
            "A=M\n" + \
            "M=D\n" + \
            "@SP\n" + \
            "M=M+1\n"

    def _popD(self) -> str:
        return "@SP\n" + \
            "M=M-1\n" + \
            "@SP\n" + \
            "A=M\n" + \
            "D=M\n"

    def write_push_pop(self, command: str, segment: str, index: int):
        translated_str = None

        if command == "push":
            translated_str = self._push(segment, index)
        elif command == "pop":
            translated_str = self._pop(segment, index)
        else:
            exit(f"command is {command} in write_push_pop")

        self.stream.write(translated_str)

    def _push(self, segment: str, index: int):
        result_str = None

        if segment == "constant":
            result_str = f"@{index}\n" + \
                "D=A\n" + \
                self._pushD()
        elif segment in ("local", "argument", "this", "that"):
            result_str = f"@{index}\n" + \
                "D=A\n" + \
                f"@{self._segment_table[segment]}\n" + \
                "A=M+D\n" + \
                "D=M\n" + \
                self._pushD()
        elif segment in ("pointer", "temp"):
            result_str = f"@{index}\n" + \
                "D=A\n" + \
                f"@{self._segment_table[segment]}\n" + \
                "A=A+D\n" + \
                "D=M\n" + \
                self._pushD()
        elif segment == "static":
            no_ext = self.file_name.split(".")[0]

            result_str = f"@{no_ext}.{index}\n" + \
                "D=M\n" + \
                self._pushD()
        
        return result_str

    def _pop(self, segment: str, index: int):
        result_str = None

        if segment == "constant":
            result_str = "@SP\n" + \
                "M=M-1\n" + \
                "@SP\n" + \
                "A=M\n" + \
                "D=M\n" + \
                f"@{index}\n" + \
                "M=D\n"
        elif segment in ("local", "argument", "this", "that"):
            result_str = f"@{index}\n" + \
                "D=A\n" + \
                f"@{self._segment_table[segment]}\n" + \
                "D=M+D\n" + \
                "@R15\n" + \
                "M=D\n" + \
                "@SP\n" + \
                "M=M-1\n" + \
                "@SP\n" + \
                "A=M\n" + \
                "D=M\n" + \
                "@R15\n" + \
                "A=M\n" + \
                "M=D\n"
        elif segment in ("pointer", "temp"):
            result_str = f"@{index}\n" + \
                "D=A\n" + \
                f"@{self._segment_table[segment]}\n" + \
                "D=A+D\n" + \
                "@R15\n" + \
                "M=D\n" + \
                "@SP\n" + \
                "M=M-1\n" + \
                "@SP\n" + \
                "A=M\n" + \
                "D=M\n" + \
                "@R15\n" + \
                "A=M\n" + \
                "M=D\n"
        elif segment == "static":
            no_ext = self.file_name.split(".")[0]

            result_str = "@SP\n" + \
                "M=M-1\n" + \
                "@SP\n" + \
                "A=M\n" + \
                "D=M\n" + \
                f"@{no_ext}.{index}\n" + \
                "M=D\n"

        return result_str

    def close(self):
        self.stream.close()
        self.stream = None
        self.file_name = None

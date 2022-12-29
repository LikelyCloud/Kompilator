from context import Context
from exceptions import UndeclaredVariableError, UninitializedVariableError


class CodeGenerator:
    def __init__(self, instructions: list, context: Context):
        self.instructions = instructions
        self.context = context
        self.code = []
        self.generate_code(self.instructions)
        self.code.append("HALT")
        print(self.instructions)
        print(self.context)

    def generate_code(self, instructions: list):
        for instr in instructions:
            if instr[0] == "PROCEDURES":
                pass
            elif instr[0] == "MAIN":
                self.context.current_procedure = "MAIN"
                self.generate_code(instr[1])
            elif instr[0] == "READ":
                var = self.context.get_procedure().get_variable(instr[1])
                if var == None:
                    raise UndeclaredVariableError(
                        f">>> Undeclared variable {instr[1]} in procedure {self.context.current_procedure}")
                else:
                    self.code.append(f"GET {var.memory_address}")
                    var.declared = True
            elif instr[0] == "WRITE":
                if instr[1][0] == "ID":
                    self.check_variable(instr[1][1])
                    # przemysl czy tu byl blad!!!
                    var = self.context.get_procedure(
                    ).get_variable(instr[1][1])
                    self.code.append(f"PUT {var.memory_address}")
                    # print(instr, var)
                elif instr[1][0] == "NUM":
                    self.code.append(f"SET {instr[1][1]}")
                    self.code.append(f"PUT 0")
                """
                if instr[1][0] == "ID":
                    var = self.context.get_procedure(
                    ).get_variable(instr[1][1])
                    if var == None:
                        raise UndeclaredVariableError(
                            f">> Undeclared variable {instr[1][1]} in procedure {self.context.current_procedure}")
                    elif not var.declared:
                        raise UninitializedVariableError(
                            f">> Uninitialized variable {instr[1][1]} in procedure {self.context.current_procedure}")
                    else:
                        self.code.append(f"PUT {var.memory_address}")
                elif instr[1][0] == "NUM":
                    self.code.append(f"SET {instr[1][1]}")
                    self.code.append(f"PUT 0")
                """
            elif instr[0] == "ASSIGN":
                var = self.context.get_procedure().get_variable(instr[1])
                if var == None:
                    raise UndeclaredVariableError(
                        f">>> Undeclared variable {instr[1]} in procedure {self.context.current_procedure}")
                else:
                    if instr[2][0] == "VALUE":
                        if instr[2][1][0] == "ID":
                            self.check_variable(instr[2][1][1])
                            self.code.append(
                                f"LOAD {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                        elif instr[2][1][0] == "NUM":
                            self.code.append(f"SET {instr[2][1][1]}")
                    elif instr[2][0] == "ADD":
                        if instr[2][1][0] == "ID":
                            self.check_variable(instr[2][1][1])
                            if instr[2][2][0] == "ID":
                                self.check_variable(instr[2][2][1])
                                self.code.append(
                                    f"LOAD {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                                self.code.append(
                                    f"ADD {self.context.get_procedure().get_variable(instr[2][2][1]).memory_address}")
                            elif instr[2][2][0] == "NUM":
                                self.code.append(f"SET {instr[2][2][1]}")
                                self.code.append(
                                    f"STORE {self.context.memory_offset}")
                                self.code.append(
                                    f"LOAD {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                                self.code.append(
                                    f"ADD {self.context.memory_offset}")
                        elif instr[2][1][0] == "NUM":
                            if instr[2][2][0] == "ID":
                                self.check_variable(instr[2][2][1])
                                self.code.append(f"SET {instr[2][1][1]}")
                                self.code.append(
                                    f"ADD {self.context.get_procedure().get_variable(instr[2][2][1]).memory_address}")
                            elif instr[2][2][0] == "NUM":
                                self.code.append(f"SET {instr[2][2][1]}")
                                self.code.append(
                                    f"STORE {self.context.memory_offset}")
                                self.code.append(
                                    f"SET {instr[2][1][1]}")
                                self.code.append(
                                    f"ADD {self.context.memory_offset}")
                    elif instr[2][0] == "SUB":
                        self.subtract((instr[2][1], instr[2][2]))
                        """if instr[2][1][0] == "ID":
                            self.check_variable(instr[2][1][1])
                            if instr[2][2][0] == "ID":
                                self.check_variable(instr[2][2][1])
                                self.code.append(
                                    f"LOAD {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                                self.code.append(
                                    f"SUB {self.context.get_procedure().get_variable(instr[2][2][1]).memory_address}")
                            elif instr[2][2][0] == "NUM":
                                self.code.append(f"SET {instr[2][2][1]}")
                                self.code.append(
                                    f"STORE {self.context.memory_offset}")
                                self.code.append(
                                    f"LOAD {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                                self.code.append(
                                    f"SUB {self.context.memory_offset}")
                        elif instr[2][1][0] == "NUM":
                            if instr[2][2][0] == "ID":
                                self.check_variable(instr[2][2][1])
                                self.code.append(f"SET {instr[2][1][1]}")
                                self.code.append(
                                    f"SUB {self.context.get_procedure().get_variable(instr[2][2][1]).memory_address}")
                            elif instr[2][2][0] == "NUM":
                                self.code.append(f"SET {instr[2][2][1]}")
                                self.code.append(
                                    f"STORE {self.context.memory_offset}")
                                self.code.append(
                                    f"SET {instr[2][1][1]}")
                                self.code.append(
                                    f"SUB {self.context.memory_offset}")"""
                    elif instr[2][0] == "MUL":
                        # do poprawy
                        # x * y -> x w pierwszej wolnej komórce, y w drugiej wolnej, wynik w trzeciej wolnej
                        if instr[2][1][0] == "ID":
                            self.check_variable(instr[2][1][1])
                            self.code.append(
                                f"LOAD {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                            self.code.append(
                                f"STORE {self.context.memory_offset}")
                        elif instr[2][1][0] == "NUM":
                            self.code.append(f"SET {instr[2][1][1]}")
                            self.code.append(
                                f"STORE {self.context.memory_offset}")
                        if instr[2][2][0] == "ID":
                            self.check_variable(instr[2][2][1])
                            self.code.append(
                                f"LOAD {self.context.get_procedure().get_variable(instr[2][2][1]).memory_address}")
                            self.code.append(
                                f"STORE {self.context.memory_offset + 1}")
                        elif instr[2][2][0] == "NUM":
                            self.code.append(f"SET {instr[2][2][1]}")
                            self.code.append(
                                f"STORE {self.context.memory_offset + 1}")
                        self.code.append("SET 0")
                        self.code.append(
                            f"STORE {self.context.memory_offset + 2}")

                        line = len(self.code) - 1
                        self.code.append(
                            f"LOAD {self.context.memory_offset + 1}")
                        self.code.append(f"JZERO {line + 19}")
                        self.code.append("HALF")
                        self.code.append("ADD 0")
                        self.code.append(
                            f"STORE {self.context.memory_offset + 3}")
                        self.code.append(
                            f"LOAD {self.context.memory_offset + 1}")
                        self.code.append(
                            f"SUB {self.context.memory_offset + 3}")
                        self.code.append(f"JZERO {line + 12}")
                        self.code.append(
                            f"LOAD {self.context.memory_offset + 2}")
                        self.code.append(f"ADD {self.context.memory_offset}")
                        self.code.append(
                            f"STORE {self.context.memory_offset + 2}")
                        self.code.append(f"LOAD {self.context.memory_offset}")
                        self.code.append("ADD 0")
                        self.code.append(f"STORE {self.context.memory_offset}")
                        self.code.append(
                            f"LOAD {self.context.memory_offset + 1}")
                        self.code.append("HALF")
                        self.code.append(
                            f"STORE {self.context.memory_offset + 1}")
                        self.code.append(f"JUMP {line + 1}")
                        self.code.append(
                            f"LOAD {self.context.memory_offset + 2}")

                    elif instr[2][0] == "DIV":
                        pass
                    elif instr[2][0] == "MOD":
                        pass

                    var.declared = True
                    self.code.append(f"STORE {var.memory_address}")

            elif instr[0] == "IF":
                self.evaluate_condition(instr[1])
                # self.code[-1].replace("ifend",
                #                      str(len(self.code) + len(instr[2])))
                line = len(self.code) - 1  # line to add jump place
                self.generate_code(instr[2])
                self.code[line] += str(len(self.code))
                # replace "ifend" len(self.code)

            elif instr[0] == "IF-ELSE":
                self.evaluate_condition(instr[1])
                line = len(self.code) - 1  # line to add jump place
                self.generate_code(instr[2])
                self.code.append("JUMP ")
                # line do add jump to avoid else code
                line2 = len(self.code) - 1
                self.code[line] += str(len(self.code))
                self.generate_code(instr[3])
                self.code[line2] += str(len(self.code))

            elif instr[0] == "WHILE":
                jump_back = len(self.code)
                self.evaluate_condition(instr[1])
                line = len(self.code) - 1
                self.generate_code(instr[2])
                self.code.append(f"JUMP {jump_back}")
                self.code[line] += str(len(self.code))

            elif instr[0] == "REPEAT":
                jump_back = len(self.code)
                self.generate_code(instr[1])
                self.evaluate_condition(instr[2])
                self.code[-1] += str(jump_back)

    # checks if variable is initialized and throws error otherwise

    def check_variable(self, value: str):
        var = self.context.get_procedure(
        ).get_variable(value)
        if var == None:
            raise UndeclaredVariableError(
                f">> Undeclared variable {value} in procedure {self.context.current_procedure}")
        elif not var.declared:
            raise UninitializedVariableError(
                f">> Uninitialized variable {value} in procedure {self.context.current_procedure}")

    def subtract(self, elements: list):
        if elements[0][0] == "ID":
            self.check_variable(elements[0][1])
            if elements[1][0] == "ID":
                self.check_variable(elements[1][1])
                self.code.append(
                    f"LOAD {self.context.get_procedure().get_variable(elements[0][1]).memory_address}")
                self.code.append(
                    f"SUB {self.context.get_procedure().get_variable(elements[1][1]).memory_address}")
            elif elements[1][0] == "NUM":
                self.code.append(f"SET {elements[1][1]}")
                self.code.append(
                    f"STORE {self.context.memory_offset}")
                self.code.append(
                    f"LOAD {self.context.get_procedure().get_variable(elements[0][1]).memory_address}")
                self.code.append(
                    f"SUB {self.context.memory_offset}")
        elif elements[0][0] == "NUM":
            if elements[1][0] == "ID":
                self.check_variable(elements[1][1])
                self.code.append(f"SET {elements[0][1]}")
                self.code.append(
                    f"SUB {self.context.get_procedure().get_variable(elements[1][1]).memory_address}")
            elif elements[1][0] == "NUM":
                self.code.append(f"SET {elements[1][1]}")
                self.code.append(
                    f"STORE {self.context.memory_offset}")
                self.code.append(
                    f"SET {elements[0][1]}")
                self.code.append(
                    f"SUB {self.context.memory_offset}")

    # przepisz do funkcji zeby nie powtarzac
    # popraw mnozenie
    def evaluate_condition(self, condition):
        if condition[0] == "EQ":
            pass
        elif condition[0] == "NEQ":
            pass
        elif condition[0] == "GT":
            self.subtract(condition[1:])
            self.code.append("JZERO ")
        elif condition[0] == "LT":
            self.subtract((condition[1:])[::-1])  # reverse arguments
            self.code.append("JZERO ")
        elif condition[0] == "GEQ":
            self.subtract((condition[1:])[::-1])
            self.code.append("JPOS ")
        elif condition[0] == "LEQ":
            self.subtract(condition[1:])
            self.code.append("JPOS ")

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
                    self.code.append(f"PUT {var.memory_address}")
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
                        if instr[2][1][0] == "ID":
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
                                    f"SUB {self.context.memory_offset}")
                    elif instr[2][0] == "MUL":
                        pass
                    elif instr[2][0] == "DIV":
                        pass
                    elif instr[2][0] == "MOD":
                        pass
                    var.declared = True
                    self.code.append(f"STORE {var.memory_address}")

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

from context import Context
from exceptions import UndeclaredVariableError, UninitializedVariableError


class CodeGenerator:
    def __init__(self, instructions: list, context: Context):
        self.instructions = instructions
        self.context = context
        self.code = []
        self.generate_code(self.instructions)
        self.code.append("HALT")
        # print(self.instructions)
        # print(self.context)

    def generate_code(self, instructions: list):
        for instr in instructions:
            if instr[0] == "PROCEDURES":
                self.code.append("JUMP ")
                for procedure in instr[1]:
                    self.context.current_procedure = procedure[0]
                    self.context.get_procedure().procedure_address = len(self.code)
                    ##############################
                    # self.code.append(procedure[0])
                    ##############################
                    self.generate_code(procedure[1])
                    self.code.append(
                        "JUMPI " + str(self.context.get_procedure().get_variable("JUMPVAR").memory_address))
            elif instr[0] == "MAIN":
                self.code[0] += str(len(self.code))
                self.context.current_procedure = "MAIN"
                self.context.get_procedure().procedure_address = len(self.code)
                ########################
                # self.code.append("MAIN")
                ########################
                self.generate_code(instr[1])
            elif instr[0] == "READ":
                var = self.context.get_procedure().get_variable(instr[1])
                if var == None:
                    raise UndeclaredVariableError(
                        f">>> Undeclared variable {instr[1]} in procedure {self.context.current_procedure}")
                else:
                    if var.formal:
                        self.code.append("GET 0")
                        self.code.append(f"STOREI {var.memory_address}")
                    else:
                        self.code.append(f"GET {var.memory_address}")
                    var.declared = True
            elif instr[0] == "WRITE":
                if instr[1][0] == "ID":
                    self.check_variable(instr[1][1])
                    # przemysl czy tu byl blad!!!
                    var = self.context.get_procedure(
                    ).get_variable(instr[1][1])
                    if var.formal:
                        self.code.append(f"LOADI {var.memory_address}")
                        self.code.append("PUT 0")
                    else:
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
                            if self.context.get_procedure().get_variable(instr[2][1][1]).formal:
                                self.code.append(
                                    f"LOADI {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                            else:
                                self.code.append(
                                    f"LOAD {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                        elif instr[2][1][0] == "NUM":
                            self.code.append(f"SET {instr[2][1][1]}")
                    elif instr[2][0] == "ADD":
                        if instr[2][1][0] == "ID":
                            self.check_variable(instr[2][1][1])
                            if instr[2][2][0] == "ID":
                                self.check_variable(instr[2][2][1])
                                if self.context.get_procedure().get_variable(instr[2][1][1]).formal:
                                    self.code.append(
                                        f"LOADI {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                                else:
                                    self.code.append(
                                        f"LOAD {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                                # self.code.append(
                                #    f"LOAD {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                                if self.context.get_procedure().get_variable(instr[2][2][1]).formal:
                                    self.code.append(
                                        f"ADDI {self.context.get_procedure().get_variable(instr[2][2][1]).memory_address}")
                                else:
                                    self.code.append(
                                        f"ADD {self.context.get_procedure().get_variable(instr[2][2][1]).memory_address}")
                                # self.code.append(
                                #    f"ADD {self.context.get_procedure().get_variable(instr[2][2][1]).memory_address}")
                            elif instr[2][2][0] == "NUM":
                                self.code.append(f"SET {instr[2][2][1]}")
                                self.code.append(
                                    f"STORE {self.context.memory_offset}")
                                if self.context.get_procedure().get_variable(instr[2][1][1]).formal:
                                    self.code.append(
                                        f"LOADI {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                                else:
                                    self.code.append(
                                        f"LOAD {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                                self.code.append(
                                    f"ADD {self.context.memory_offset}")
                        elif instr[2][1][0] == "NUM":
                            if instr[2][2][0] == "ID":
                                self.check_variable(instr[2][2][1])
                                self.code.append(f"SET {instr[2][1][1]}")
                                if self.context.get_procedure().get_variable(instr[2][2][1]).formal:
                                    self.code.append(
                                        f"ADDI {self.context.get_procedure().get_variable(instr[2][2][1]).memory_address}")
                                else:
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
                            if self.context.get_procedure().get_variable(instr[2][1][1]).formal:
                                self.code.append(
                                    f"LOADI {self.context.get_procedure().get_variable(instr[2][1][1]).memory_address}")
                            else:
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
                            if self.context.get_procedure().get_variable(instr[2][2][1]).formal:
                                self.code.append(
                                    f"LOADI {self.context.get_procedure().get_variable(instr[2][2][1]).memory_address}")
                            else:
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
                        self.divide((instr[2][1], instr[2][2]))
                        self.code.append(
                            f"LOAD {self.context.memory_offset + 3}")
                    elif instr[2][0] == "MOD":
                        self.divide((instr[2][1], instr[2][2]))
                        self.code.append(
                            f"LOAD {self.context.memory_offset}")

                    var.declared = True
                    if var.formal:
                        self.code.append(f"STOREI {var.memory_address}")
                    else:
                        self.code.append(f"STORE {var.memory_address}")

            elif instr[0] == "IF":
                cond = self.evaluate_condition(instr[1])
                # self.code[-1].replace("ifend",
                #                      str(len(self.code) + len(instr[2])))
                line = len(self.code) - 1  # line to add jump place
                self.generate_code(instr[2])
                self.code[line] += str(len(self.code))
                if cond != None:
                    self.code[cond] += str(len(self.code))
                # replace "ifend" len(self.code)

            elif instr[0] == "IF-ELSE":
                cond = self.evaluate_condition(instr[1])
                line = len(self.code) - 1  # line to add jump place
                self.generate_code(instr[2])
                self.code.append("JUMP ")
                # line do add jump to avoid else code
                line2 = len(self.code) - 1
                self.code[line] += str(len(self.code))
                if cond != None:
                    self.code[cond] += str(len(self.code))
                self.generate_code(instr[3])
                self.code[line2] += str(len(self.code))

            elif instr[0] == "WHILE":
                self.context.loop_depth += 1
                jump_back = len(self.code)
                cond = self.evaluate_condition(instr[1])
                line = len(self.code) - 1
                self.generate_code(instr[2])
                self.code.append(f"JUMP {jump_back}")
                self.code[line] += str(len(self.code))
                if cond != None:
                    self.code[cond] += str(len(self.code))
                self.context.loop_depth -= 1
                if self.context.loop_depth == 0:
                    undeclared = list(filter(
                        lambda var: var.used == True and var.declared == False, self.context.get_procedure().variables))
                    if undeclared != []:
                        raise UninitializedVariableError(
                            f">> Uninitialized variable {undeclared[0].name} in procedure {self.context.current_procedure}")

            elif instr[0] == "REPEAT":
                self.context.loop_depth += 1
                jump_back = len(self.code)
                self.generate_code(instr[1])
                cond = self.evaluate_condition(instr[2])
                self.code[-1] += str(jump_back)
                if cond != None:
                    self.code[cond] += str(jump_back)
                self.context.loop_depth -= 1
                if self.context.loop_depth == 0:
                    undeclared = list(filter(
                        lambda var: var.used == True and var.declared == False, self.context.get_procedure().variables))
                    if undeclared != []:
                        raise UninitializedVariableError(
                            f">> Uninitialized variable {undeclared[0].name} in procedure {self.context.current_procedure}")

            elif instr[0] == "PROC_HEAD":
                # ustawiam wartosc declared na rowna wartosci declared parametru procedury
                # for index, variable in enumerate(instr[1][1]):
                #    self.context.get_procedure(instr[1][0]).variables[index].declared = self.context.get_procedure(
                #    ).get_variable(variable).declared
                #####################################################
                for index, variable in enumerate(instr[1][1]):
                    if self.context.get_procedure().get_variable(variable).formal:
                        self.code.append(
                            f"LOAD {self.context.get_procedure().get_variable(variable).memory_address}")
                        # self.code.append(
                        #     f"STORE {self.context.get_procedure(instr[1][0]).variables[index].memory_address}")
                    else:
                        self.code.append(
                            f"SET {self.context.get_procedure().get_variable(variable).memory_address}")
                    self.code.append(
                        f"STORE {self.context.get_procedure(instr[1][0]).variables[index].memory_address}")
                    # ustaw wszystkie zmienne przekazane jako parametry jako zainicjalizowane
                    self.context.get_procedure().get_variable(variable).declared = True
                self.code.append(f"SET {len(self.code) + 3}")
                # self.code.append(
                #    f"STORE {self.context.get_procedure(instr[1][0]).variables[self.context.get_procedure(instr[1][0]).#formal_arguments].memory_address}")
                self.code.append(
                    "STORE " + str(self.context.get_procedure(instr[1][0]).get_variable("JUMPVAR").memory_address))
                self.code.append(
                    f"JUMP {self.context.get_procedure(instr[1][0]).procedure_address}")

    # checks if variable is initialized and throws error otherwise

    def check_variable(self, value: str):
        var = self.context.get_procedure(
        ).get_variable(value)
        if var == None:
            raise UndeclaredVariableError(
                f">> Undeclared variable {value} in procedure {self.context.current_procedure}")
        elif not var.declared:
            if self.context.loop_depth == 0:
                raise UninitializedVariableError(
                    f">> Uninitialized variable {value} in procedure {self.context.current_procedure}")
            var.used = True
            print(
                f">> Warning (possibly uninitialized variable {value} in procedure {self.context.current_procedure})")

    def subtract(self, elements: list):
        if elements[0][0] == "ID":
            self.check_variable(elements[0][1])
            if elements[1][0] == "ID":
                self.check_variable(elements[1][1])
                if self.context.get_procedure().get_variable(elements[0][1]).formal:
                    self.code.append(
                        f"LOADI {self.context.get_procedure().get_variable(elements[0][1]).memory_address}")
                else:
                    self.code.append(
                        f"LOAD {self.context.get_procedure().get_variable(elements[0][1]).memory_address}")
                if self.context.get_procedure().get_variable(elements[1][1]).formal:
                    self.code.append(
                        f"SUBI {self.context.get_procedure().get_variable(elements[1][1]).memory_address}")
                else:
                    self.code.append(
                        f"SUB {self.context.get_procedure().get_variable(elements[1][1]).memory_address}")
            elif elements[1][0] == "NUM":
                self.code.append(f"SET {elements[1][1]}")
                self.code.append(
                    f"STORE {self.context.memory_offset}")
                if self.context.get_procedure().get_variable(elements[0][1]).formal:
                    self.code.append(
                        f"LOADI {self.context.get_procedure().get_variable(elements[0][1]).memory_address}")
                else:
                    self.code.append(
                        f"LOAD {self.context.get_procedure().get_variable(elements[0][1]).memory_address}")
                self.code.append(
                    f"SUB {self.context.memory_offset}")
        elif elements[0][0] == "NUM":
            if elements[1][0] == "ID":
                self.check_variable(elements[1][1])
                self.code.append(f"SET {elements[0][1]}")
                if self.context.get_procedure().get_variable(elements[1][1]).formal:
                    self.code.append(
                        f"SUBI {self.context.get_procedure().get_variable(elements[1][1]).memory_address}")
                else:
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

    def divide(self, elements: list):
        if elements[0][0] == "ID":
            self.check_variable(elements[0][1])
            if self.context.get_procedure().get_variable(elements[0][1]).formal:
                self.code.append(
                    f"LOADI {self.context.get_procedure().get_variable(elements[0][1]).memory_address}")
            else:
                self.code.append(
                    f"LOAD {self.context.get_procedure().get_variable(elements[0][1]).memory_address}")
            self.code.append(
                f"STORE {self.context.memory_offset}")
        elif elements[0][0] == "NUM":
            self.code.append(f"SET {elements[0][1]}")
            self.code.append(
                f"STORE {self.context.memory_offset}")
        if elements[1][0] == "ID":
            self.check_variable(elements[1][1])
            if self.context.get_procedure().get_variable(elements[1][1]).formal:
                self.code.append(
                    f"LOADI {self.context.get_procedure().get_variable(elements[1][1]).memory_address}")
            else:
                self.code.append(
                    f"LOAD {self.context.get_procedure().get_variable(elements[1][1]).memory_address}")
            self.code.append(
                f"STORE {self.context.memory_offset + 1}")
            self.code.append(
                f"STORE {self.context.memory_offset + 2}")
        elif elements[1][0] == "NUM":
            self.code.append(f"SET {elements[1][1]}")
            self.code.append(
                f"STORE {self.context.memory_offset + 1}")
            self.code.append(
                f"STORE {self.context.memory_offset + 2}")
        self.code.append("SET 0")
        self.code.append(
            f"STORE {self.context.memory_offset + 3}")

        self.code.append(f"LOAD {self.context.memory_offset + 1}")
        self.code.append(f"SUB {self.context.memory_offset}")
        self.code.append(f"JPOS {len(self.code) + 5}")
        self.code.append(f"LOAD {self.context.memory_offset + 1}")
        self.code.append("ADD 0")
        self.code.append(f"STORE {self.context.memory_offset + 1}")
        self.code.append(f"JUMP {len(self.code) - 6}")
        self.code.append(f"LOAD {self.context.memory_offset + 1}")
        self.code.append("HALF")
        self.code.append(f"STORE {self.context.memory_offset + 1}")
        self.code.append(f"LOAD {self.context.memory_offset + 2}")
        self.code.append(f"SUB {self.context.memory_offset + 1}")
        self.code.append(f"JPOS {len(self.code) + 17}")
        self.code.append(f"LOAD {self.context.memory_offset + 3}")
        self.code.append("ADD 0")
        self.code.append(f"STORE {self.context.memory_offset + 3}")
        self.code.append(f"LOAD {self.context.memory_offset + 1}")
        self.code.append(f"SUB {self.context.memory_offset}")
        self.code.append(f"JPOS {len(self.code) + 7}")
        self.code.append("SET 1")
        self.code.append(f"ADD {self.context.memory_offset + 3}")
        self.code.append(f"STORE {self.context.memory_offset + 3}")
        self.code.append(f"LOAD {self.context.memory_offset}")
        self.code.append(f"SUB {self.context.memory_offset + 1}")
        self.code.append(f"STORE {self.context.memory_offset}")
        self.code.append(f"LOAD {self.context.memory_offset + 1}")
        self.code.append("HALF")
        self.code.append(f"STORE {self.context.memory_offset + 1}")
        self.code.append(f"JUMP {len(self.code) - 18}")

    # popraw mnozenie
    # w EQ zwracam miejsce z ktorego trzeba skoczyc za koniec kodu warunkowego i w obliczaniu IF, IF-ELSE, ... sprawdzam czy evaluate_condition() zwraca None, jesli nie to sprawdzany warunek to EQ i trzeba dodac adres do JUMP

    def evaluate_condition(self, condition):
        if condition[0] == "EQ":
            self.subtract(condition[1:])
            self.code.append("JPOS ")
            jump_from1 = len(self.code) - 1
            self.subtract((condition[1:])[::-1])
            self.code.append("JPOS ")
            return jump_from1
        elif condition[0] == "NEQ":
            self.subtract(condition[1:])
            self.code.append("JPOS ")
            line = len(self.code) - 1
            self.subtract((condition[1:])[::-1])
            self.code.append("JZERO ")
            self.code[line] += str(len(self.code))
        elif condition[0] == "GT":
            self.subtract(condition[1:])
            self.code.append("JZERO ")
        elif condition[0] == "LT":
            self.subtract((condition[1:])[::-1])
            self.code.append("JZERO ")
        elif condition[0] == "GEQ":
            self.subtract((condition[1:])[::-1])
            self.code.append("JPOS ")
        elif condition[0] == "LEQ":
            self.subtract(condition[1:])
            self.code.append("JPOS ")

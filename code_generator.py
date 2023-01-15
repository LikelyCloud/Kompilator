from context import Context
from exceptions import UndeclaredVariableError, UninitializedVariableError
import itertools


class CodeGenerator:
    def __init__(self, instructions: list, context: Context):
        self.instructions = instructions
        self.context = context
        self.code = []
        self.delete_unused_procedures()
        self.generate_code(self.instructions)
        self.code.append("HALT")
        print(self.instructions)
        print(self.context)

    def generate_code(self, instructions: list):
        for instr in instructions:
            if instr[0] == "PROCEDURES":
                for procedure in instr[1]:
                    # do zmiany: po prostu sprawdz czy sa jakies procedury (nieuzyte beda juz usuniete z ast)
                    if self.context.get_procedure(procedure[0]).used:
                        if self.code == []:
                            self.code.append("JUMP ")
                        self.context.current_procedure = procedure[0]
                        self.context.get_procedure().procedure_address = len(self.code)
                        self.generate_code(procedure[1])
                        self.code.append(
                            "JUMPI " + str(self.context.get_procedure().get_variable("JUMPVAR").memory_address))

            elif instr[0] == "MAIN":
                if self.code != []:
                    self.code[0] += str(len(self.code))
                self.context.current_procedure = "MAIN"
                self.context.get_procedure().procedure_address = len(self.code)
                self.generate_code(instr[1])

            elif instr[0] == "READ":
                var = self.context.get_procedure().get_variable(instr[1])
                if var == None:
                    raise UndeclaredVariableError(
                        f">>> Undeclared variable {instr[1]} in procedure {self.context.current_procedure}")
                else:
                    if var.formal:
                        self.code.append("GET 0")
                        # self.context.acc = None  # undefined value
                        # print(f"WAR {var}")
                        self.code.append(f"STOREI {var.memory_address}")
                    else:
                        self.code.append(f"GET {var.memory_address}")
                    var.declared = True

            elif instr[0] == "WRITE":
                if instr[1][0] == "ID":
                    self.check_variable(instr[1][1])
                    var = self.context.get_procedure(
                    ).get_variable(instr[1][1])
                    if var.formal:
                        self.code.append(f"LOADI {var.memory_address}")
                        self.code.append("PUT 0")
                    else:
                        self.code.append(f"PUT {var.memory_address}")
                elif instr[1][0] == "NUM":
                    self.code.append(f"SET {instr[1][1]}")
                    self.code.append(f"PUT 0")

            elif instr[0] == "ASSIGN":
                var = self.context.get_procedure().get_variable(instr[1])
                if var == None:
                    raise UndeclaredVariableError(
                        f">>> Undeclared variable {instr[1]} in procedure {self.context.current_procedure}")
                else:
                    if instr[2][0] == "VALUE":
                        if instr[2][1][0] == "ID":
                            self.check_variable(instr[2][1][1])
                            self.load_variable(instr[2][1][1])
                            # if self.context
                        elif instr[2][1][0] == "NUM":
                            self.code.append(f"SET {instr[2][1][1]}")
                            # var.value = instr[2][1][1]

                    elif instr[2][0] == "ADD":
                        if instr[2][1][0] == "ID":
                            self.check_variable(instr[2][1][1])
                            if instr[2][2][0] == "ID":  # ID + ID
                                self.check_variable(instr[2][2][1])
                                self.load_variable(instr[2][1][1])
                                self.add_variable(instr[2][2][1])
                            elif instr[2][2][0] == "NUM":  # ID + NUM
                                self.code.append(f"SET {instr[2][2][1]}")
                                self.add_variable(instr[2][1][1])
                        elif instr[2][1][0] == "NUM":
                            if instr[2][2][0] == "ID":  # NUM + ID
                                self.check_variable(instr[2][2][1])
                                self.code.append(f"SET {instr[2][1][1]}")
                                self.add_variable(instr[2][2][1])
                            elif instr[2][2][0] == "NUM":  # NUM + NUM
                                self.code.append(
                                    f"SET {instr[2][1][1] + instr[2][2][1]}")

                    elif instr[2][0] == "SUB":
                        self.subtract((instr[2][1], instr[2][2]))

                    elif instr[2][0] == "MUL":
                        if instr[2][1][0] == "ID":
                            self.check_variable(instr[2][1][1])
                            if instr[2][2][0] == "ID":  # ID * ID
                                self.check_variable(instr[2][2][1])
                                self.load_variable(instr[2][1][1])
                                self.code.append(
                                    f"STORE {self.context.memory_offset}")
                                self.load_variable(instr[2][2][1])
                                self.code.append(
                                    f"STORE {self.context.memory_offset+1}")
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
                                self.code.append(
                                    f"ADD {self.context.memory_offset}")
                                self.code.append(
                                    f"STORE {self.context.memory_offset + 2}")
                                self.code.append(
                                    f"LOAD {self.context.memory_offset}")
                                self.code.append("ADD 0")
                                self.code.append(
                                    f"STORE {self.context.memory_offset}")
                                self.code.append(
                                    f"LOAD {self.context.memory_offset + 1}")
                                self.code.append("HALF")
                                self.code.append(
                                    f"STORE {self.context.memory_offset + 1}")
                                self.code.append(f"JUMP {line + 1}")
                                self.code.append(
                                    f"LOAD {self.context.memory_offset + 2}")

                            elif instr[2][2][0] == "NUM":  # ID * NUM
                                # self.code.append(f"SET {instr[2][2][1]}")
                                # self.add_variable(instr[2][1][1])
                                if instr[2][2][1] == 0:
                                    self.code.append("SET 0")
                                # memory_offset -> obecna wielokrotnosc ID; memory_offset + 1 -> obecny wynik
                                # jesli ID to potega 2
                                elif instr[2][2][1] & (instr[2][2][1] - 1) == 0:
                                    bin_rep = self.get_bin(
                                        instr[2][2][1])[::-1]
                                    self.load_variable(instr[2][1][1])
                                    for _ in bin_rep[1:]:
                                        self.code.append("ADD 0")
                                else:
                                    bin_rep = self.get_bin(
                                        instr[2][2][1])[::-1]
                                    if bin_rep[0] == '0':
                                        self.code.append("SET 0")
                                        self.code.append(
                                            f"STORE {self.context.memory_offset + 1}")
                                        self.load_variable(instr[2][1][1])
                                        self.code.append(
                                            f"STORE {self.context.memory_offset}")
                                    else:
                                        self.load_variable(instr[2][1][1])
                                        self.code.append(
                                            f"STORE {self.context.memory_offset + 1}")
                                        self.code.append(
                                            f"STORE {self.context.memory_offset}")
                                    counter = 1  # ile razy pomnozyc przed dodaniem
                                    for digit in bin_rep[1:]:
                                        if digit == '0':
                                            counter += 1
                                        else:
                                            self.code.append(
                                                f"LOAD {self.context.memory_offset}")
                                            for _ in range(0, counter):
                                                self.code.append("ADD 0")
                                            self.code.append(
                                                f"STORE {self.context.memory_offset}")
                                            self.code.append(
                                                f"ADD {self.context.memory_offset+1}")
                                            self.code.append(
                                                f"STORE {self.context.memory_offset+1}")
                                            counter = 1
                        elif instr[2][1][0] == "NUM":
                            if instr[2][2][0] == "ID":  # NUM * ID
                                # self.check_variable(instr[2][2][1])
                                # self.code.append(f"SET {instr[2][1][1]}")
                                # self.add_variable(instr[2][2][1])
                                self.check_variable(instr[2][2][1])
                                if instr[2][1][1] == 0:
                                    self.code.append("SET 0")
                                # memory_offset -> obecna wielokrotnosc ID; memory_offset + 1 -> obecny wynik
                                # jesli ID to potega 2
                                elif instr[2][1][1] & (instr[2][1][1] - 1) == 0:
                                    bin_rep = self.get_bin(
                                        instr[2][1][1])[::-1]
                                    self.load_variable(instr[2][2][1])
                                    for _ in bin_rep[1:]:
                                        self.code.append("ADD 0")
                                else:
                                    bin_rep = self.get_bin(
                                        instr[2][1][1])[::-1]
                                    if bin_rep[0] == '0':
                                        self.code.append("SET 0")
                                        self.code.append(
                                            f"STORE {self.context.memory_offset + 1}")
                                        self.load_variable(instr[2][2][1])
                                        self.code.append(
                                            f"STORE {self.context.memory_offset}")
                                    else:
                                        self.load_variable(instr[2][2][1])
                                        self.code.append(
                                            f"STORE {self.context.memory_offset + 1}")
                                        self.code.append(
                                            f"STORE {self.context.memory_offset}")
                                    counter = 1  # ile razy pomnozyc przed dodaniem
                                    for digit in bin_rep[1:]:
                                        if digit == '0':
                                            counter += 1
                                        else:
                                            self.code.append(
                                                f"LOAD {self.context.memory_offset}")
                                            for _ in range(0, counter):
                                                self.code.append("ADD 0")
                                            self.code.append(
                                                f"STORE {self.context.memory_offset}")
                                            self.code.append(
                                                f"ADD {self.context.memory_offset+1}")
                                            self.code.append(
                                                f"STORE {self.context.memory_offset+1}")
                                            counter = 1

                            elif instr[2][2][0] == "NUM":  # NUM * NUM
                                self.code.append(
                                    f"SET {instr[2][1][1] * instr[2][2][1]}")
                        # do poprawy
                        # x * y -> x w pierwszej wolnej komórce, y w drugiej wolnej, wynik w trzeciej wolnej
                        """if instr[2][1][0] == "ID":
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
                            f"LOAD {self.context.memory_offset + 2}")"""

                    elif instr[2][0] == "DIV":
                        if instr[2][1][0] == "ID":
                            self.check_variable(instr[2][1][1])
                            if instr[2][2][0] == "ID":  # ID / ID
                                self.check_variable(instr[2][2][1])
                                self.divide((instr[2][1], instr[2][2]))
                                self.code.append(
                                    f"LOAD {self.context.memory_offset + 3}")
                            elif instr[2][2][0] == "NUM":  # ID / NUM
                                if instr[2][2][1] == 0:
                                    self.code.append("SET 0")
                                elif instr[2][2][1] & (instr[2][2][1] - 1) == 0:
                                    bin_rep = self.get_bin(
                                        instr[2][2][1])[::-1]
                                    self.load_variable(instr[2][1][1])
                                    for _ in bin_rep[1:]:
                                        self.code.append("HALF")
                                else:
                                    self.divide((instr[2][1], instr[2][2]))
                                    self.code.append(
                                        f"LOAD {self.context.memory_offset + 3}")
                        elif instr[2][1][0] == "NUM":
                            if instr[2][2][0] == "ID":  # NUM / ID
                                self.check_variable(instr[2][2][1])
                                if instr[2][1][1] == 0:
                                    self.code.append("SET 0")
                                else:
                                    self.divide((instr[2][1], instr[2][2]))
                                    self.code.append(
                                        f"LOAD {self.context.memory_offset + 3}")
                            elif instr[2][2][0] == "NUM":  # NUM / NUM
                                if instr[2][1][1] == 0 or instr[2][2][1] == 0:
                                    self.code.append("SET 0")
                                else:
                                    self.code.append(
                                        f"SET {instr[2][1][1] // instr[2][2][1]}")

                        #self.divide((instr[2][1], instr[2][2]))
                        # self.code.append(
                        #    f"LOAD {self.context.memory_offset + 3}")

                    elif instr[2][0] == "MOD":
                        if instr[2][1][0] == "ID":
                            self.check_variable(instr[2][1][1])
                            if instr[2][2][0] == "ID":  # ID % ID
                                self.check_variable(instr[2][2][1])
                                self.divide((instr[2][1], instr[2][2]))
                                self.code.append(
                                    f"LOAD {self.context.memory_offset}")
                            elif instr[2][2][0] == "NUM":  # ID % NUM
                                if instr[2][2][1] == 0:
                                    self.code.append("SET 0")
                                else:
                                    self.divide((instr[2][1], instr[2][2]))
                                    self.code.append(
                                        f"LOAD {self.context.memory_offset}")
                        elif instr[2][1][0] == "NUM":
                            if instr[2][2][0] == "ID":  # NUM % ID
                                self.check_variable(instr[2][2][1])
                                if instr[2][1][1] == 0:
                                    self.code.append("SET 0")
                                else:
                                    self.divide((instr[2][1], instr[2][2]))
                                    self.code.append(
                                        f"LOAD {self.context.memory_offset}")
                            elif instr[2][2][0] == "NUM":  # NUM % NUM
                                if instr[2][1][1] == 0 or instr[2][2][1] == 0:
                                    self.code.append("SET 0")
                                else:
                                    self.code.append(
                                        f"SET {instr[2][1][1] % instr[2][2][1]}")
                        #self.divide((instr[2][1], instr[2][2]))
                        # self.code.append(
                        #    f"LOAD {self.context.memory_offset}")

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

    # sprawdza czy zmienna jest zadeklarowana i zainicjalizowana

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
            print(
                f">> Warning (possibly uninitialized variable {value} in procedure {self.context.current_procedure})")
        var.used = True

    def load_variable(self, var: str):
        if self.context.get_procedure().get_variable(var).formal:
            self.code.append(
                f"LOADI {self.context.get_procedure().get_variable(var).memory_address}")
        else:
            self.code.append(
                f"LOAD {self.context.get_procedure().get_variable(var).memory_address}")

    def add_variable(self, var: str):
        if self.context.get_procedure().get_variable(var).formal:
            self.code.append(
                f"ADDI {self.context.get_procedure().get_variable(var).memory_address}")
        else:
            self.code.append(
                f"ADD {self.context.get_procedure().get_variable(var).memory_address}")

    def sub_variable(self, var: str):
        if self.context.get_procedure().get_variable(var).formal:
            self.code.append(
                f"SUBI {self.context.get_procedure().get_variable(var).memory_address}")
        else:
            self.code.append(
                f"SUB {self.context.get_procedure().get_variable(var).memory_address}")

    def subtract(self, elements: list):
        if elements[0][0] == "ID":
            self.check_variable(elements[0][1])
            if elements[1][0] == "ID":  # ID - ID
                self.check_variable(elements[1][1])
                self.load_variable(elements[0][1])
                self.sub_variable(elements[1][1])
            elif elements[1][0] == "NUM":  # ID - NUM
                self.code.append(f"SET {elements[1][1]}")
                self.code.append(
                    f"STORE {self.context.memory_offset}")
                self.load_variable(elements[0][1])
                self.code.append(
                    f"SUB {self.context.memory_offset}")
        elif elements[0][0] == "NUM":
            if elements[1][0] == "ID":  # NUM - ID
                self.check_variable(elements[1][1])
                self.code.append(f"SET {elements[0][1]}")
                self.sub_variable(elements[1][1])
            elif elements[1][0] == "NUM":  # NUM - NUM
                self.code.append(
                    f"SET {max(elements[0][1] - elements[1][1],0)}")

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

    def delete_unused_procedures(self):
        # nazwy wszystkich procedur
        proc_names = [proc.name for proc in self.context.procedures[:-1]]

        proc_queue = []  # tu beda dodawane procedury wykonane, by sprawdzic jakie w nich beda wykonane procedury
        # wielokrotnie splaszczone ast w main
        main = self.flatten_ast(self.instructions[1][1], [])
        for proc in proc_names:
            if proc in main:
                self.context.get_procedure(
                    proc).used = True  # uzyto danej procedury
                # dodano procedure by sprawdzic czy w niej sa wywolane inne procedury
                proc_queue.append(proc)
                # usunieto procedure by jej dalej nie rozpatrywac
                proc_names.remove(proc)

        proc_queue = list(dict.fromkeys(proc_queue))  # get unique names

        for proc_to_search in proc_queue:
            proc_instr = list(
                filter(lambda body: body[0] == proc_to_search, self.instructions[0][1]))[0][1]  # ast wewnatrz procedury
            flat_proc = self.flatten_ast(proc_instr, [])
            for proc in proc_names:
                if proc in flat_proc:
                    self.context.get_procedure(
                        proc).used = True  # uzyto danej procedury
                    # dodano procedure by sprawdzic czy w niej sa wywolane inne procedury
                    proc_queue.append(proc)
                    # usunieto procedure by jej dalej nie rozpatrywac
                    proc_names.remove(proc)

    def flatten_ast(self, ast, flattened=[]):
        for elem in ast:
            if isinstance(elem, int) or isinstance(elem, str):
                flattened.append(elem)
            else:
                self.flatten_ast(elem, flattened)
        return flattened

    def get_bin(self, value: int):
        return bin(value)[2:]

#from exceptions import *


class Variable:
    # name
    # value
    def __init__(self, name: str, memory_address: int, formal: bool = False, declared: bool = False):
        self.name = name
        self.memory_address = memory_address
        self.formal = formal
        self.declared = declared
        self.used = False

    def __str__(self):
        return f"Name: {self.name}, memory_address: {self.memory_address}, formal: {self.formal}, declared: {self.declared}, used: {self.used}"


class Procedure:
    # name
    # variables
    def __init__(self, name: str):
        self.name = name
        self.variables = []
        self.formal_arguments = 0
        self.procedure_address = None
        self.used = False

    def add_variable(self, variable: Variable):
        self.variables.append(variable)

    def is_variable(self, var_name: str):
        result = list(filter(lambda var: var.name == var_name, self.variables))
        if result != []:
            return True
        return False

    def get_variable(self, var_name: str):
        result = list(filter(lambda var: var.name == var_name, self.variables))
        if result != []:
            return result[0]
        return None

    def __str__(self):
        stringbuilder = f"Procedure {self.name} ({self.used}) : {self.procedure_address} ({self.formal_arguments}); Variables [ "
        for var in self.variables:
            stringbuilder += f"({var}) "
        stringbuilder += "]"
        return stringbuilder


class Context:
    def __init__(self):
        self.procedures = []
        self.current_procedure = ""
        self.memory_offset = 1
        self.loop_depth = 0

    def add_procedure(self, proc: Procedure):
        self.procedures.append(proc)

    def is_procedure(self, proc_name: str):
        result = list(filter(lambda proc: proc.name ==
                      proc_name, self.procedures))
        if result != []:
            return True
        return False

    def get_procedure(self, proc_name: str = ""):
        if proc_name == "":
            proc_name = self.current_procedure

        result = list(filter(lambda proc: proc.name ==
                      proc_name, self.procedures))
        if result != []:
            return result[0]
        return None

    def __str__(self):
        stringbuilder = "Context:\n"
        for proc in self.procedures:
            stringbuilder += f"Procedure {proc.name} ({proc.used}) : {proc.procedure_address} ({proc.formal_arguments}): Variables [ "
            for var in proc.variables:
                stringbuilder += f"({var}) "
            stringbuilder += "]\n"
        return stringbuilder


"""
proc = Procedure("swap")
proc.add_variable(Variable("a", True, 25))
proc.add_variable(Variable("a", True, 25))
print(proc)
proc.get_variable("a").name = "26"
print(proc)
"""

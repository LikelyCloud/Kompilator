class LexerError(Exception):
    pass


class ParserError(Exception):
    pass


class UndeclaredVariableError(Exception):
    pass


class UninitializedVariableError(Exception):
    pass


class VariableRedeclarationError(Exception):
    pass


class UndeclaredProcedureError(Exception):
    pass


class ProcedureRedeclarationError(Exception):
    pass


class ArgumentsProcedureError(Exception):
    pass

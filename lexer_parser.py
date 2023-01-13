import sly
from context import Variable, Procedure, Context
from exceptions import LexerError, ParserError, VariableRedeclarationError, ProcedureRedeclarationError, UndeclaredProcedureError, ArgumentsProcedureError


class Lexer(sly.Lexer):
    tokens = {
        PROCEDURE, PROGRAM, IS, VAR, BEGIN, END,
        IF, THEN, ELSE, ENDIF,
        WHILE, DO, ENDWHILE,
        REPEAT, UNTIL,
        READ, WRITE,
        SEMICOLON, COMMA,
        ASSIGN,
        LEB, RIB,
        ADD, SUB, MUL, DIV, MOD,
        EQ, NEQ, GT, LT, GEQ, LEQ,
        ID, NUM
    }

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    ignore_whitespace = r'\s'
    ignore_comment = r'[\[][^\]]*[\]]'

    BEGIN = r'BEGIN'
    DO = r'DO'
    ENDIF = r'ENDIF'
    ENDWHILE = r'ENDWHILE'
    END = r'END'
    ELSE = r'ELSE'
    IF = r'IF'
    IS = r'IS'
    PROCEDURE = r'PROCEDURE'
    PROGRAM = r'PROGRAM'
    READ = r'READ'
    REPEAT = r'REPEAT'
    THEN = r'THEN'
    VAR = r'VAR'
    UNTIL = r'UNTIL'
    WHILE = r'WHILE'
    WRITE = r'WRITE'

    SEMICOLON = r'[;]'
    COMMA = r'[,]'

    ASSIGN = r':='

    LEB = r'[(]'
    RIB = r'[)]'

    ADD = r'[+]'
    SUB = r'[-]'
    MUL = r'[*]'
    DIV = r'[/]'
    MOD = r'[%]'

    EQ = r'='
    NEQ = r'!='
    LEQ = r'<='
    GEQ = r'>='
    LT = r'<'
    GT = r'>'

    ID = r'[_a-z]+'

    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    def error(self, t):
        raise LexerError(
            f">>> Unrecognized token {t.value[0]} in line {self.lineno}")


class Parser(sly.Parser):
    tokens = Lexer.tokens

    def __init__(self):
        super().__init__()
        self.context = Context()
        self.ast = []

    @_('procedures main')
    def program_all(self, p):
        # return "PROGRAM", p.procedures, p.main
        self.ast = ("PROCEDURES", p.procedures), p.main

    @_('procedures PROCEDURE proc_head IS VAR declarations BEGIN commands END')
    def procedures(self, p):
        # proc_head: nazwa, [zmienne]
        if self.context.is_procedure(p.proc_head[0]):
            raise ProcedureRedeclarationError(
                f">>> Redeclared procedure {p.proc_head[0]} in line {p.lineno}")
        else:
            self.context.add_procedure(
                Procedure(p.proc_head[0]))
            for var in p.proc_head[1]:
                if self.context.get_procedure(p.proc_head[0]).is_variable(var):
                    raise VariableRedeclarationError(
                        f">>> Redeclared variable {var} in line {p.lineno}")
                else:
                    self.context.get_procedure(
                        p.proc_head[0]).add_variable(Variable(var, self.context.memory_offset, True, True))
                    self.context.memory_offset += 1
            self.context.get_procedure(
                p.proc_head[0]).add_variable(Variable("JUMPVAR", self.context.memory_offset))
            self.context.memory_offset += 1
            for var in p.declarations:
                if self.context.get_procedure(p.proc_head[0]).is_variable(var):
                    raise VariableRedeclarationError(
                        f">>> Redeclared variable {var} in line {p.lineno}")
                else:
                    self.context.get_procedure(
                        p.proc_head[0]).add_variable(Variable(var, self.context.memory_offset))
                    self.context.memory_offset += 1
            self.context.get_procedure(
                p.proc_head[0]).formal_arguments = len(p.proc_head[1])
        return p.procedures + [(p.proc_head[0], p.commands)]

    @_('procedures PROCEDURE proc_head IS BEGIN commands END')
    def procedures(self, p):
        # proc_head: nazwa, [zmienne]
        if self.context.is_procedure(p.proc_head[0]):
            raise ProcedureRedeclarationError(
                f">>> Redeclared procedure {p.proc_head[0]} in line {p.lineno}")
        else:
            self.context.add_procedure(
                Procedure(p.proc_head[0]))
            for var in p.proc_head[1]:
                if self.context.get_procedure(p.proc_head[0]).is_variable(var):
                    raise VariableRedeclarationError(
                        f">>> Redeclared variable {var} in line {p.lineno}")
                else:
                    self.context.get_procedure(
                        p.proc_head[0]).add_variable(Variable(var, self.context.memory_offset, True, True))
                    self.context.memory_offset += 1
            self.context.get_procedure(
                p.proc_head[0]).add_variable(Variable("JUMPVAR", self.context.memory_offset))
            self.context.memory_offset += 1
            self.context.get_procedure(
                p.proc_head[0]).formal_arguments = len(p.proc_head[1])
        return p.procedures + [(p.proc_head[0], p.commands)]

    @ _('')
    def procedures(self, p):
        return []

    @ _('PROGRAM IS VAR declarations BEGIN commands END')
    def main(self, p):
        self.context.add_procedure(Procedure("MAIN"))
        for var in p.declarations:
            if self.context.get_procedure("MAIN").is_variable(var):
                raise VariableRedeclarationError(
                    f">>> Redeclared variable {var} in line {p.lineno}")
            else:
                self.context.get_procedure("MAIN").add_variable(
                    Variable(var, self.context.memory_offset))
                self.context.memory_offset += 1
        return "MAIN", p.commands

    @ _('PROGRAM IS BEGIN commands END')
    def main(self, p):
        return "MAIN", p.commands

    @ _('commands command')
    def commands(self, p):
        return p.commands + [p.command]

    @ _('command')
    def commands(self, p):
        return [p.command]

    @ _('ID ASSIGN expression SEMICOLON')
    def command(self, p):
        return "ASSIGN", p.ID, p.expression

    @ _('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return "IF-ELSE", p.condition, p.commands0, p.commands1

    @ _('IF condition THEN commands ENDIF')
    def command(self, p):
        return "IF", p.condition, p.commands

    @ _('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return "WHILE", p.condition, p.commands

    @ _('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p):
        return "REPEAT", p.commands, p.condition

    @ _('proc_head SEMICOLON')
    def command(self, p):
        if not self.context.is_procedure(p.proc_head[0]):
            raise UndeclaredProcedureError(
                f">>> Undeclared procedure {p.proc_head[0]} in line {p.lineno}")
        if self.context.get_procedure(p.proc_head[0]).formal_arguments != len(p.proc_head[1]):
            raise ArgumentsProcedureError(
                f">>> Incorrect number of arguments in procedure {p.proc_head[0]} in line {p.lineno}")
        # zakladam ze wszyskie zmienne przekazane do fuknkcji (nawet te niezainicjalizowane) po wyjsciu beda zainicjalizowane

        #self.context.get_procedure(p.proc_head[0]).used = True
        return "PROC_HEAD", p.proc_head

    @ _('READ ID SEMICOLON')
    def command(self, p):
        return "READ", p.ID

    @ _('WRITE value SEMICOLON')
    def command(self, p):
        return "WRITE", p.value

    @ _('ID LEB declarations RIB')
    def proc_head(self, p):
        # self.context.current_procedure = p.ID
        # print(self.context.current_procedure)
        #print(f"Proc head:{p.ID}")
        # for var in p.declarations:
        # print(var)
        #self.context.get_procedure(p.ID).get_variable(var).declared = True
        return p.ID, p.declarations

    @ _('declarations COMMA ID')
    def declarations(self, p):
        return p.declarations + [p.ID]

    @ _('ID')
    def declarations(self, p):
        return [p.ID]

    @ _('value')
    def expression(self, p):
        return "VALUE", p.value

    @ _('value ADD value')
    def expression(self, p):
        return "ADD", p.value0, p.value1

    @ _('value SUB value')
    def expression(self, p):
        return "SUB", p.value0, p.value1

    @ _('value MUL value')
    def expression(self, p):
        return "MUL", p.value0, p.value1

    @ _('value DIV value')
    def expression(self, p):
        return "DIV", p.value0, p.value1

    @ _('value MOD value')
    def expression(self, p):
        return "MOD", p.value0, p.value1

    @ _('value EQ value')
    def condition(self, p):
        return "EQ", p.value0, p.value1

    @ _('value NEQ value')
    def condition(self, p):
        return "NEQ", p.value0, p.value1

    @ _('value GT value')
    def condition(self, p):
        return "GT", p.value0, p.value1

    @ _('value LT value')
    def condition(self, p):
        return "LT", p.value0, p.value1

    @ _('value GEQ value')
    def condition(self, p):
        return "GEQ", p.value0, p.value1

    @ _('value LEQ value')
    def condition(self, p):
        return "LEQ", p.value0, p.value1

    @ _('NUM')
    def value(self, p):
        return "NUM", p.NUM

    @ _('ID')
    def value(self, p):
        return "ID", p.ID

    def error(self, p):
        raise ParserError(
            f">>> Invalid instruction {p.value} in line {p.lineno}")

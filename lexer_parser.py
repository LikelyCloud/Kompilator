import sly
from exceptions import LexerError


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

    PROCEDURE = r'PROCEDURE'
    PROGRAM = r'PROGRAM'
    IS = r'IS'
    VAR = r'VAR'
    BEGIN = r'BEGIN'
    END = r'END'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    ENDIF = r'ENDIF'
    WHILE = r'WHILE'
    DO = r'DO'
    ENDWHILE = r'ENDWHILE'
    REPEAT = r'REPEAT'
    UNTIL = r'UNTIL'
    READ = r'READ'
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
    GT = r'>'
    LT = r'<'
    GEQ = r'>='
    LEQ = r'<='

    ID = r'[_a-z]+'

    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    def error(self, t):
        raise LexerError(
            f">>> Unrecognized token {t.value[0]} in line {self.lineno}")


# class Parser(sly.Parser):
#    tokens = Lexer.tokens

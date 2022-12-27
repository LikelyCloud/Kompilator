from lexer_parser import Lexer, Parser
import sys
from exceptions import LexerError, ParserError, UndeclaredVariableError, VariableRedeclarationError, UndeclaredProcedureError, ProcedureRedeclarationError, ArgumentsProcedureError


if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser()
    if len(sys.argv) != 3:
        print(">>> Incorrect command!!!\n>>> Expected input: python3 compiler.py <input file> <output file>")
    else:
        with open(sys.argv[1], 'r') as input_file:
            input_content = input_file.read()
        # print(input_content)
        try:
            #tokens = lexer.tokenize(input_content)
            # for tok in tokens:
            #    print(tok)
            parser.parse(lexer.tokenize(input_content))
            code = parser.context
            print(code)
        except LexerError as lexer_error:
            print(lexer_error)

        except ParserError as parser_error:
            print(parser_error)

        except UndeclaredVariableError as undeclared_variable_error:
            print(undeclared_variable_error)

        except VariableRedeclarationError as variable_redeclaration_error:
            print(variable_redeclaration_error)

        except UndeclaredProcedureError as undeclared_procedure_error:
            print(undeclared_procedure_error)

        except ProcedureRedeclarationError as procedure_redeclaration_error:
            print(procedure_redeclaration_error)

        except ArgumentsProcedureError as arguments_procedure_error:
            print(arguments_procedure_error)

# from lexer_parser import Lexer, Parser
from lexer_parser import Lexer
import sys
from exceptions import LexerError

if __name__ == "__main__":
    lexer = Lexer()
    # parser = Parser()
    if len(sys.argv) != 3:
        print(">>> Incorrect command!!!\n>>> Expected input: python3 compiler.py <input file> <output file>")
    else:
        with open(sys.argv[1], 'r') as input_file:
            input_content = input_file.read()
        # print(input_content)
        try:
            tokens = lexer.tokenize(input_content)
            for tok in tokens:
                print(tok)
        except LexerError as lexer_error:
            print(lexer_error)
            # parser.parse(lexer.tokenize(input_content))

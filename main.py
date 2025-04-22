from lexer import tokenize
from parser import Parser

def main():
    # Read the input program from test_program.txt
    with open("test_program.txt", "r") as file:
        code = file.read()

    # Tokenize the input code
    tokens = list(tokenize(code))  # Convert generator to list for reuse
 
    # Parse the tokens into an AST
    parser = Parser(tokens)
    
    print("\nAbstract Syntax Tree (AST):")

    parser.parse()

if __name__ == "__main__":
    main()
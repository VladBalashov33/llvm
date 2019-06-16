from lexer import Lexer
from parser1 import Parser
from CodeGenerator import CodeGen
import sys

with open("text.txt") as file:
    text_input = file.read()

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)
new_tokens = lexer.lex(text_input)

token_stream=[]
for i in new_tokens:
    token_stream.append(i)
    print(i)
#print(token_stream)
print('####################################### End of lexer #######################################')

codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf

pg = Parser(module, builder, printf)
pg.parse()
parser = pg.get_parser()
parse = parser.parse(tokens)
parse.eval()

print('####################################### End of parser #######################################')
#print(module)
print('####################################### End of generator #######################################')






codegen.create_ir()
codegen.save_ir("output.ll")



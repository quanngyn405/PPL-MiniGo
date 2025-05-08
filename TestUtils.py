from antlr4 import *
from CodeGenerator import CodeGenerator
import sys
import os
import glob
import subprocess
from MiniGoLexer import MiniGoLexer
from MiniGoParser import MiniGoParser
from lexererr import *
from ASTGeneration import ASTGeneration
from CodeGenError import *


class TestUtil:
    @staticmethod
    def makeSource(inputStr,num):
        filename = "./testcases/" + str(num) + ".txt"
        file = open(filename,"w")
        file.write(inputStr)
        file.close()
        return FileStream(filename)

class TestCodeGen:
    @staticmethod
    def test(input, expect, num):
        return TestCodeGen.checkStatic(input, expect, num)

    @staticmethod
    def checkStatic(input, expect, num):
        dest = open(f"./solutions/{num}.txt", "w")

        if isinstance(input, str):
            inputfile = TestUtil.makeSource(input, num)
            lexer = MiniGoLexer(inputfile)
            tokens = CommonTokenStream(lexer)
            parser = MiniGoParser(tokens)
            tree = parser.program()
            asttree = ASTGeneration().visit(tree)
            with open(f"./AST/{num}.txt", "w") as x:
                x.write(str(asttree))
        else:
            inputfile = TestUtil.makeSource(str(input), num)
            asttree = input

        codeGen = CodeGenerator()
        base_path = f"java_byte_code/{num}"
        if not os.path.isdir(base_path):
            os.makedirs(base_path)

        jasmin_jar = "../jasmin.jar"
        miniGO_class = "MiniGoClass"
        output_file = f"solutions/{num}.txt"

        codeGen.gen(asttree, base_path)

        # Compile all .j files using Jasmin
        j_files = glob.glob(os.path.join(base_path, "*.j"))
        for j_file in j_files:
            subprocess.run(
                ["java", "-jar", jasmin_jar, os.path.basename(j_file)],
                cwd=base_path,
                stderr=subprocess.STDOUT,
                check=True
            )

        # Run the generated class
        with open(output_file, "w") as f:
            subprocess.run(
                ["java", "-cp", "../_io;.", miniGO_class],
                cwd=base_path,
                stdout=f,
                stderr=subprocess.STDOUT,
                timeout=10,
                check=True
            )

        # except IllegalOperandException as e:
        #     f.write(str(e) + "\n")
        # except IllegalRuntimeException as e:
        #     f.write(str(e) + "\n")
        # except subprocess.CalledProcessError as e:
        #     f.write(f"Subprocess error: {e}\n")
        # except subprocess.TimeoutExpired as e:
        #     f.write(f"Timeout error: {e}\n")
        # except Exception as e:
        #     f.write(f"Unexpected error: {e}\n")

        dest = open("./solutions/" + str(num) + ".txt","r")
        line = dest.read()
        return line == expect















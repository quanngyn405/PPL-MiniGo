"""
 * Initial code for Assignment
 * Programming Language Principles
 * Author: Võ Tiến
 * Link FB : https://www.facebook.com/profile.php?id=100056605580171
 * Link Group : https://www.facebook.com/groups/211867931379013
 * Date: 02.04.2024
"""
import unittest
from TestUtils import TestCodeGen
import inspect
from AST import *

"""
    (cd java_byte_code/test_001 && 
    java  -jar ../jasmin.jar MiniGoClass.j && 
    java -cp ../_io;. MiniGoClass)
"""
class CodeGenSuite(unittest.TestCase):
    def test_000(self):
        input = """
func foo(a int, c int) {
    var b = a + c;
    putInt(b)
}
func main() {
    foo(2, 3)
}
func foo1() int {return 1;}
        """
        self.assertTrue(TestCodeGen.test(input, "5", inspect.stack()[0].function))  

    def test_001(self):
        input = """
func fvoid() {putStringLn("VoTien");}

var global = fint()
func main() {
    fvoid();
    putFloatLn(global + 2.0)

    var local = "a";
    putBoolLn(local <= "b")
    local += "c"
    putStringLn(local)

};

func fint() int {return 1;}
"""
        self.assertTrue(TestCodeGen.test(input,"VoTien\n3.0\ntrue\nac\n",inspect.stack()[0].function)) 

    def test_002(self):
        input = """
func foo() int {return foo1();}
var a = foo() + foo1();
func main() {
    putInt(a)
    a := foo()
    putInt(a)
}
func foo1() int {return 1;}
        """
        self.assertTrue(TestCodeGen.test(input, "21", inspect.stack()[0].function))  
    
    def test_003(self):
        input ="""
func main() {
    putFloat(1.0)
}
        """
        #  Program([FuncDecl("main",[],VoidType(),Block([FuncCall("putFloat",[FloatLiteral(1.0)])]))])
        self.assertTrue(TestCodeGen.test(input, "1.0", inspect.stack()[0].function))

    def test_016(self):
        input = """
func main() {
    putIntLn(5 % 2)
    putIntLn(2 % 5)
}
"""
        self.assertTrue(TestCodeGen.test(input, "1\n2\n", inspect.stack()[0].function))

    def test_019(self):
        input = """
func main() {
    putBoolLn(5.0 > 2.0)
    putBoolLn(5.0 < 2.0)
    putBoolLn(5.0 <= 5.0)
    putBoolLn(5.0 >= 5.0)
    putBoolLn(5.0 == 5.0)
    putBoolLn(5.0 != 5.0)
}
"""
        self.assertTrue(TestCodeGen.test(input, "true\nfalse\ntrue\ntrue\ntrue\nfalse\n", inspect.stack()[0].function))

    def test_020(self):
        input = """
func main() {
    putBoolLn("apple" > "banana")     // False
    putBoolLn("apple" < "banana")     // True
    putBoolLn("apple" <= "apple")     // True
    putBoolLn("banana" >= "apple")    // True
    putBoolLn("hello" == "hello")     // True
    putBoolLn("hello" != "hello")     // False
}
"""
        self.assertTrue(TestCodeGen.test(input, "false\ntrue\ntrue\ntrue\ntrue\nfalse\n", inspect.stack()[0].function))

    def test_024(self):
        input = """
func main() {
    putBoolLn(! true)
    putBoolLn(! false)
    putIntLn(-1)
    putFloatLn(-1.0)
}
     """
        self.assertTrue(TestCodeGen.test(input, "false\ntrue\n-1\n-1.0\n", inspect.stack()[0].function))

    def test_032(self):
        input = """
func foo() int {return 1;}        

func main() {
    putInt(foo())
}
    """
        self.assertTrue(TestCodeGen.test(input, "1", inspect.stack()[0].function))

    def test_033(self):
        input = """
func fooInt(a int) int {  return a; }
func fooFloat(a float) float {  return a; }
func fooString(a string) string { return a; }
func fooBool(a boolean) boolean { return a; }

func main() {
    putInt(fooInt(2));
    putFloat(fooFloat(1.5));
    putString(fooString("S"));
    putBool(fooBool(true));
}
        
        """
        self.assertTrue(TestCodeGen.test(input, "21.5Strue", inspect.stack()[0].function))

    def test_044(self):
        input = """
    func main() {
        var f = true;
        var g boolean;

        putBoolLn(f)
        putBool(g)
    }
     """
        self.assertTrue(TestCodeGen.test(input, "true\nfalse", inspect.stack()[0].function))

    def test_048(self):
        input = """
func main() {
    a := getString()
    putString(a)
    return
}
"""
        self.assertTrue(TestCodeGen.test(input, "VOTIEN", inspect.stack()[0].function))

    def test_051(self):
        input = """
func main() {
    var a = 1 + 2.0;
    var b = 1.0 > 2.0;
    var c = "vo" + "tien";
    var d = "a" < "b";

    putFloatLn(a)
    putBoolLn(b)
    putStringLn(c)
    putBoolLn(d)
}
"""
        self.assertTrue(TestCodeGen.test(input,"3.0\nfalse\nvotien\ntrue\n",inspect.stack()[0].function)) 

    def test_053(self):
        input = """
func main() {
    var a [2] int = [2] int {10, 20};
    putInt(a[0])
}
        """
        self.assertTrue(TestCodeGen.test(input,"10",inspect.stack()[0].function))

    def test_057(self):
        input = """
func main() {
    var a [3] int;
    putInt(a[0])
    putInt(a[1])
}
        """
        self.assertTrue(TestCodeGen.test(input,"00",inspect.stack()[0].function))

    def test_058(self):
        input = """
func main() {
    var a [2][3] int ;
    putInt(a[0][0])
    putInt(a[0][1])
    putInt(a[0][2])
    putInt(a[1][0])
    putInt(a[1][1])
    putInt(a[1][2])
}
        """
        self.assertTrue(TestCodeGen.test(input,"000000",inspect.stack()[0].function))

    def test_059(self):
        input = """
func main() {
    var a [2][3][2] int ;
    putInt(a[0][0][0])
}   
        """
        self.assertTrue(TestCodeGen.test(input,"0",inspect.stack()[0].function))

    def test_065(self):
        input = """
func main() {
    var a [2][3] float;
    a[0][0] += 2.0
    putFloat(a[0][0] + a[0][1])
}   
        """
        self.assertTrue(TestCodeGen.test(input,"2.0",inspect.stack()[0].function))

    def test_077(self):
        input = """
    var a [2] int;
    func main() {
        a[0] := 100
        a[1] += a[0] + a[0]
        putInt(a[1])
    }
    """
        self.assertTrue(TestCodeGen.test(input,"200",inspect.stack()[0].function))

    def test_078(self):
        input = """
    var a [2][2] int;
    func main() {
        a[0][0] := 100
        a[1][1] += a[0][0] + a[0][0]
        putInt(a[1][1])
    }
    """
        self.assertTrue(TestCodeGen.test(input,"200",inspect.stack()[0].function))

    def test_085(self):
        input = """
    func createArray() [3] int {
        return [3] int {10, 20, 30};
    }

    func main() {
        var a [3] int = createArray();
        putInt(a[0]);
        putInt(a[1]);
        putInt(a[2]);
    }
    """
        self.assertTrue(TestCodeGen.test(input,"102030",inspect.stack()[0].function))

    def test_090(self):
        input = """
func main() {
    var a [1] int ;
    a[0] := 1
    putInt(a[0]);
}
    """
        self.assertTrue(TestCodeGen.test(input,"1",inspect.stack()[0].function))

    def test_091(self):
        input = """
func main() {
    var a [1][1][1] int  = [1][1][1] int {{{0}}};
    a[0][0][0] := 1
    putInt(a[0][0][0]);
}
    """
        self.assertTrue(TestCodeGen.test(input,"1",inspect.stack()[0].function))

    def test_096(self):
        input = """
func main() {
    if (true) {
        putBool(true)
    } 
}
    """
        self.assertTrue(TestCodeGen.test(input,"true",inspect.stack()[0].function))

    def test_097(self):
        input = """
func main() {
    if (true) {
        putBool(true)
    } else {
        putBool(false)     
    }
}
    """
        self.assertTrue(TestCodeGen.test(input,"true",inspect.stack()[0].function))

    def test_098(self):
        input = """
func main() {
    if (false) {
        putBool(true)
    } else {
        putBool(false)     
    }
}
    """
        self.assertTrue(TestCodeGen.test(input,"false",inspect.stack()[0].function))

    def test_113(self):
        input = """
func main() {
    var i = 0;
    for i < 3 {
        putInt(i);
        i += 1;
    }
    putInt(i);
}
        """
        self.assertTrue(TestCodeGen.test(input, "0123", inspect.stack()[0].function))

    def test_114(self):
        input = """
func main() {
    var i = 0;
    for i < 5 {
        if (i == 3) {
            break;
        }
        putInt(i);
        i += 1;
    }
    putInt(i);
}
        """
        self.assertTrue(TestCodeGen.test(input, "0123", inspect.stack()[0].function))

    def test_115(self):
        input = """
func main() {
    var i = 0;
    for i < 5 {
        i += 1;
        if (i % 2 == 0) {
            continue;
        }
        putInt(i);
    }
    putInt(i);
}
        """
        self.assertTrue(TestCodeGen.test(input, "1355", inspect.stack()[0].function))

    def test_126(self):
        input = """
func main() {
    var i int = 10;
    for var i int = 0; i < 2; i += 1 {
        putIntLn(i)
        break;
    }
    putInt(i)
}
        """
        self.assertTrue(TestCodeGen.test(input, "0\n10", inspect.stack()[0].function))

    def test_137(self):
      input = """
const a = 1 + 1
const c = 5 - a
func main() {
  var b [a][c] int;
  putInt(b[0][0]);
  b[0][0] := 20;
  putInt(b[0][0]);
}
      """
      self.assertTrue(TestCodeGen.test(input, "020", inspect.stack()[0].function))

#     def test_052(self):
#         input = """
# func main() {
#     var a = 10;
#     var b = 3;
#     var c = a / b;
#     putIntLn(c);
# }
#         """
#         self.assertTrue(TestCodeGen.test(input, "3\n", inspect.stack()[0].function))

#     def test_053(self):
#         input = """
# func add(x int, y int) int {
#     return x + y;
# }

# func main() {
#     var result = add(5, 7);
#     putIntLn(result);
# }
#         """
#         self.assertTrue(TestCodeGen.test(input, "12\n", inspect.stack()[0].function))

#     def test_054(self):
#         input = """
# func concat(a string, b string) string {
#     return a + b;
# }

# func main() {
#     var s = concat("Hello, ", "World!");
#     putStringLn(s);
# }
#         """
#         self.assertTrue(TestCodeGen.test(input, "Hello, World!\n", inspect.stack()[0].function))

#     def test_055(self):
#         input = """
# func main() {
#     var x = 5;
#     var y = 10;
#     var z = x * y + (x - y);
#     putIntLn(z);
# }
#         """
#         self.assertTrue(TestCodeGen.test(input, "45\n", inspect.stack()[0].function))

#     def test_056(self):
#         input = """
# func main() {
#     var a = 5.5;
#     var b = 2.0;
#     var c = a / b;
#     putFloatLn(c);
# }
#         """
#         self.assertTrue(TestCodeGen.test(input, "2.75\n", inspect.stack()[0].function))

#     def test_057(self):
#         input = """
# func double(n int) int {
#     return n * 2;
# }

# func main() {
#     var a = double(4);
#     putIntLn(a);
# }
#         """
#         self.assertTrue(TestCodeGen.test(input, "8\n", inspect.stack()[0].function))

#     def test_058(self):
#         input = """
# func main() {
#     var s = "abc";
#     s += "def";
#     putStringLn(s);
# }
#         """
#         self.assertTrue(TestCodeGen.test(input, "abcdef\n", inspect.stack()[0].function))

#     def test_059(self):
#         input = """
# func main() {
#     putBoolLn(10 == 10);
#     putBoolLn(10 != 5);
#     putBoolLn(5 >= 10);
# }
#         """
#         self.assertTrue(TestCodeGen.test(input, "true\ntrue\nfalse\n", inspect.stack()[0].function))


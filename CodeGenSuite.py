import unittest
from TestUtils import TestCodeGen
import inspect
from AST import *


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
# type Course interface {study();}
# type PPL3 struct {number int;}
# func (p PPL3) study() {putInt(p.number);}

# func main(){
#     var a PPL3 = PPL3 {number: 10}
#     putIntLn(a.number)
#     a.study()
# }
    def test_141(self):
        input = """
type Course interface {study();}
type PPL3 struct {number int;}
func (p PPL3) study() {putInt(p.number);}

func main(){
    var a PPL3 = PPL3 {number: 10}
    putIntLn(a.number)
    a.study()
}
        """
        self.assertTrue(TestCodeGen.test(input, "10\n10", inspect.stack()[0].function))

    def test_142(self):
        input = """
type Course interface {study();}
type PPL3 struct {number int;}
func (p PPL3) study() {putInt(p.number);}

func main(){
    var a Course = nil
    a := PPL3 {number: 10}
    a.study()
}
        """
        self.assertTrue(TestCodeGen.test(input, "10", inspect.stack()[0].function))

    def test_143(self):
        input = """
type PPL3 struct {number int;}

func main(){
    var a PPL3 = PPL3 {number: 10}
    putInt(a.number)
}
        """
        self.assertTrue(TestCodeGen.test(input, "10", inspect.stack()[0].function))

    def test_144(self):
        input = """
type PPL3 struct {number int;}

func main(){
    var a PPL3
    a.number := 10
    putInt(a.number)
}
        """
        self.assertTrue(TestCodeGen.test(input, "10", inspect.stack()[0].function))

    def test_145(self):
        input = """
type PPL2 struct {number int;}
type PPL3 struct {number int; ppl PPL2;}

func main(){
    var a PPL3
    a.ppl := PPL2 {number: 10}
   putInt(a.ppl.number)
}
        """
        self.assertTrue(TestCodeGen.test(input, "10", inspect.stack()[0].function))

    def test_146(self):
        input = """
type PPL2 struct {number int;}
type PPL3 struct {number int; ppl PPL2;}

func main(){
    var a PPL3
    a.ppl := PPL2 {number: 10}
    a.ppl.number := 100
   putInt(a.ppl.number)
}
        """
        self.assertTrue(TestCodeGen.test(input, "100", inspect.stack()[0].function))        

    def test_147(self):
        input = """
type Study interface { study(); }
type Play interface { play(); }

type PPL3 struct {number int;}

func (p PPL3) study() { putInt(p.number); }
func (p PPL3) play()  { putInt(p.number + 5); }

func main() {
    var a PPL3 = PPL3 {number: 1}
    a.study()
    a.play()
}
        """
        self.assertTrue(TestCodeGen.test(input, "16", inspect.stack()[0].function))


    def test_148(self):
        input = """
type Study interface { study(); }
type Play interface { play(); }

type PPL3 struct {number int;}

func (p PPL3) study() { putInt(p.number); }
func (p PPL3) play()  { putInt(p.number + 5); }

func main() {
    var a PPL3 = PPL3 {number: 1}
    var b Study = a
    var c Play = a
    b.study()
    c.play()
}
        """
        self.assertTrue(TestCodeGen.test(input, "16", inspect.stack()[0].function))

    def test_148(self):
        input = """
type Study interface { study(); }
type Play interface { play(); }

type PPL3 struct {number int;}

func (p PPL3) study() { putInt(p.number); }
func (p PPL3) play()  { putInt(p.number + 5); }

func main() {
    var a PPL3 = PPL3 {number: 1}
    var b Study = a
    var c Play = a
    b.study()
    c.play()
}
        """
        self.assertTrue(TestCodeGen.test(input, "16", inspect.stack()[0].function))

    def test_149(self):
        input = """
type Worker interface { 
    study(); 
    play(); 
}

type PPL4 struct {number int;}
type PPL5 struct {number int;}

// Implement Worker cho PPL4
func (p PPL4) study() { putInt(p.number); }
func (p PPL4) play()  { putInt(p.number + 5); }

// Implement Worker cho PPL5
func (p PPL5) study() { putInt(p.number * 2); }
func (p PPL5) play()  { putInt(p.number * 3); }

func main() {
    var w1 Worker = PPL4 {number: 3}
    var w2 Worker = PPL5 {number: 4}

    w1.study(); // in: 3
    w1.play();  // in: 8

    w2.study(); // in: 8
    w2.play();  // in: 12
}
        """
        self.assertTrue(TestCodeGen.test(input, "38" "812", inspect.stack()[0].function))

    def test_150(self):
        input = """
type Worker interface { 
    study(); 
    play(); 
}

type PPL4 struct {number int;}
type PPL5 struct {number int;}

// Implement Worker cho PPL4
func (p PPL4) study() { putInt(p.number); }
func (p PPL4) play()  { putInt(p.number + 5); }

// Implement Worker cho PPL5
func (p PPL5) study() { putInt(p.number * 2); }

func main() {
    var w1 Worker = PPL4 {number: 3}
    var w2 PPL5 = PPL5 {number: 4}

    w1.study(); // in: 3
    w1.play();  // in: 8

    w2.study(); // in: 8
}
        """
        self.assertTrue(TestCodeGen.test(input, "38" "8", inspect.stack()[0].function))


    def test_151(self):
        input = """
type Speaker interface { speak(); }

type Human struct {name int; }

func (h Human) speak() { putIntLn(h.name); }

func saySomething(s Speaker) {
    s.speak();
}

func main() {
    var h Speaker = Human {name: 2025};
    saySomething(h);
}
        """
        self.assertTrue(TestCodeGen.test(input, "2025\n", inspect.stack()[0].function))


    def test_152(self):
        input = """
type Speaker interface { speak(); }

type Human struct { name int; }

func (h Human) speak() { putIntLn(h.name); }

func main() {
    var people [3]Speaker;

    people[0] := Human {name: 1};
    people[1] := Human {name: 2};
    people[2] := Human {name: 3};

    people[0].speak(); // Output: 1
    people[1].speak(); // Output: 2
    people[2].speak(); // Output: 3
}
        """
        self.assertTrue(TestCodeGen.test(input, "1\n2\n3\n", inspect.stack()[0].function))

    def test_153(self):
        input = """
type Speaker interface { speak(); }

type Human struct { name int; }

func (h Human) speak() { putIntLn(h.name); }

func main() {
    var people [3]Human;

    people[0] := Human {name: 1};
    people[1] := Human {name: 2};
    people[2] := Human {name: 3};

    people[0].speak(); // Output: 1
    people[1].speak(); // Output: 2
    people[2].speak(); // Output: 3
}
        """
        self.assertTrue(TestCodeGen.test(input, "1\n2\n3\n", inspect.stack()[0].function))

    def test_154(self):
        input = """
type Calculator struct { x int; y int; }

func (c Calculator) sum() int {
    return c.x + c.y;
}

func main() {
    var cal Calculator = Calculator {x: 7, y: 8};
    var result int = cal.sum();
    putIntLn(result);
}
        """
        self.assertTrue(TestCodeGen.test(input, "15\n", inspect.stack()[0].function))

    def test_155(self):
        input = """
type Calculator interface { sum() int; }

type BasicCalc struct { x int; y int; }

func (b BasicCalc) sum() int {
    return b.x + b.y;
}

func main() {
    var c Calculator = BasicCalc {x: 5, y: 15};
    var result int = c.sum();
    putIntLn(result);
}
        """
        self.assertTrue(TestCodeGen.test(input, "20\n", inspect.stack()[0].function))

    def test_156(self):
        input = """
type Speaker interface { speak(); }

type Human struct { name int; }

func (h Human) speak() { putIntLn(h.name); }

func sayHello(s Speaker) {
    s.speak();
}

func main() {
    var h Human = Human {name: 100};
    sayHello(h);
}
        """
        self.assertTrue(TestCodeGen.test(input, "100\n", inspect.stack()[0].function))

    def test_157(self):
        input = """
type Calculator interface { sum() int; }

type BasicCalc struct { x int; y int; }

func (b BasicCalc) sum() int {
    return b.x + b.y;
}

func calculate(c Calculator) int {
    return c.sum();
}

func main() {
    var b BasicCalc = BasicCalc {x: 20, y: 30};
    var result int = calculate(b);
    putIntLn(result);
}
        """
        self.assertTrue(TestCodeGen.test(input, "50\n", inspect.stack()[0].function))

    def test_158(self):
        input = """
type Multiplier struct { factor int; }

func (m Multiplier) multiply(value int) int {
    return m.factor * value;
}

func main() {
    var mul Multiplier = Multiplier {factor: 5};
    var result int = mul.multiply(4);
    putIntLn(result);
}
        """
        self.assertTrue(TestCodeGen.test(input, "20\n", inspect.stack()[0].function))

    def test_159(self):
        input = """
type Calculator interface { calculate(a int, b int) int; }

type BasicCalc struct {number int;}

func (b BasicCalc) calculate(a int, b int) int {
    return a + b;
}

func main() {
    var c Calculator = BasicCalc {};
    var result int = c.calculate(15, 25);
    putIntLn(result);
}
        """
        self.assertTrue(TestCodeGen.test(input, "40\n", inspect.stack()[0].function))


    def test_160(self):
        input = """
type Calculator interface { calculate(a int, b int); }

type BasicCalc struct {number int;}

func (b BasicCalc) calculate(a int, b int) {
    putIntLn(a+b);
}

func main() {
    var c Calculator = BasicCalc {};
    c.calculate(15, 25);
}
        """
        self.assertTrue(TestCodeGen.test(input, "40\n", inspect.stack()[0].function))

    def test_161(self):
        input = """
type Calculator interface { calculate(a int, b int); }

type BasicCalc struct {number int;}

func (b BasicCalc) calculate(a int, b int) {
    putIntLn(a+b);
}

func main() {
    var c BasicCalc
    c.calculate(15, 25);
}
        """
        self.assertTrue(TestCodeGen.test(input, "40\n", inspect.stack()[0].function))

    def test_162(self):
        input = """
type Speaker interface { speak(); }

type Human struct { name int; }

func (h Human) speak() {
    putIntLn(h.name);
}

type Classroom struct {
    student Human;
    guest Speaker;
}

func main() {
    var h Human = Human {name: 777};
    var k Speaker = Human {name: 999};
    var room Classroom = Classroom {student: h, guest: k};

    putIntLn(room.student.name);
    room.guest.speak();
}
        """
        self.assertTrue(TestCodeGen.test(input, "777\n999\n", inspect.stack()[0].function))

    def test_163(self):
        input = """
    type Person struct {
        name string;
        age int;
    }
    func main() {
        var p Person = Person{name: "Alice", age: 22};
        putStringLn(p.name);
        putIntLn(p.age);
    }
        """
        self.assertTrue(TestCodeGen.test(input, "Alice\n22\n", inspect.stack()[0].function))

    def test_164(self):
        input = """
    type Greeter interface { greet(); }

    type Person struct {
        name string;
        age int;
    }
    func (p Person) greet() {
        putStringLn(p.name);
    }

    func main() {
        var g Greeter = Person{name: "Bob", age: 30};
        g.greet();
    }
        """
        self.assertTrue(TestCodeGen.test(input, "Bob\n", inspect.stack()[0].function))

    def test_165(self):
        input = """
    type Person struct {
        name string;
        age int;
    }
    func (p Person) agePlus(n int) int {
        return p.age + n;
    }
    func main() {
        var p Person = Person{name: "Charlie", age: 18};
        var result int = p.agePlus(5);
        putIntLn(result);
    }
        """
        self.assertTrue(TestCodeGen.test(input, "23\n", inspect.stack()[0].function))

    def test_166(self):
        input = """
    type Person struct {
        name string;
        age int;
    }
    func sumAges(p1 Person, p2 Person) int {
        return p1.age + p2.age;
    }
    func main() {
        var p1 Person = Person{name: "Dan", age: 20};
        var p2 Person = Person{name: "Eve", age: 25};
        var total int = sumAges(p1, p2);
        putIntLn(total);
    }
        """
        self.assertTrue(TestCodeGen.test(input, "45\n", inspect.stack()[0].function))

    def test_167(self):
        input = """
    type Person struct {
        name string;
        age int;
    }
    func (p Person) printInfo() {
        putStringLn(p.name);
        putIntLn(p.age);
    }
    func main() {
        var people [1]Person
        people[0] := Person{name: "Anna", age: 19};
        people[0].printInfo() 
    }
        """
        self.assertTrue(TestCodeGen.test(input, "Anna\n19\n", inspect.stack()[0].function))

    def test_168(self):
        input = """
    type Speaker interface { speak(); }
    type Person struct {
        name string;
        age int;
    }
    func (p Person) speak() {
        putStringLn(p.name);
    }
    func announce(s Speaker) {
        s.speak();
    }
    func main() {
        var p Person = Person{name: "Grace", age: 27};
        announce(p);
    }
        """
        self.assertTrue(TestCodeGen.test(input, "Grace\n", inspect.stack()[0].function))

    def test_169(self):
        input = """
    type Person struct {
        name string;
        age int;
    }
    func createPerson(n string, a int) Person {
        return Person{name: n, age: a};
    }
    func main() {
        var p Person = createPerson("Helen", 24);
        putStringLn(p.name);
        putIntLn(p.age);
    }
        """
        self.assertTrue(TestCodeGen.test(input, "Helen\n24\n", inspect.stack()[0].function))

    def test_170(self):
        input = """
    type Person struct {
        name string;
        age int;
    }
    func (p Person) isAdult() boolean {
        return p.age >= 18;
    }
    func main() {
        var p Person = Person{name: "Ivy", age: 17};
        if (p.isAdult()) {
            putStringLn("Adult");
        } else {
            putStringLn("Minor");
        }
    }
        """
        self.assertTrue(TestCodeGen.test(input, "Minor\n", inspect.stack()[0].function))

    def test_171(self):
        input = """
    type Person struct {
        name string;
        age int;
    }
    func (p Person) duplicate() Person {
        return Person{name: p.name, age: p.age};
    }
    func main() {
        var p1 Person = Person{name: "Jack", age: 31};
        var p2 Person = p1.duplicate();
        putStringLn(p2.name);
        putIntLn(p2.age);
    }
        """
        self.assertTrue(TestCodeGen.test(input, "Jack\n31\n", inspect.stack()[0].function))

    def test_172(self):
        input = """
    type Person struct {
        name string;
        age int;
    }
    func (p Person) printInfo() {
        putStringLn(p.name);
        putIntLn(p.age);
    }
    func main() {
        var people [2]Person = [2]Person{Person{name: "Anna", age: 19},Person{name: "Bill", age: 21}};
        people[0].printInfo();
        people[1].printInfo();
    }
        """
        self.assertTrue(TestCodeGen.test(input, "Anna\n19\nBill\n21\n", inspect.stack()[0].function))


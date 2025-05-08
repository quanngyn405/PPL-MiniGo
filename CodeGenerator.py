from Utils import *
# from StaticCheck import *
# from StaticError import *
from Emitter import *
from Frame import Frame
from abc import ABC, abstractmethod
from functools import reduce
from Visitor import *
from AST import *

class CodeGenerator(BaseVisitor,Utils):
    def __init__(self):
        self.className = "MiniGoClass"
        self.astTree = None
        self.path = None
        self.emit = None
        self.function = None
        self.list_function = []
        self.arrayCell = None 
        self.arrayCellType = None
        self.list_type = {}
        self.struct: StructType = None

    def init(self):
        mem = [
            Symbol("getInt", MType([], IntType()), CName("io", True)),
            Symbol("putInt", MType([IntType()], VoidType()), CName("io", True)),
            Symbol("putIntLn", MType([IntType()], VoidType()), CName("io", True)),

            Symbol("getFloat", MType([], FloatType()), CName("io", True)),
            Symbol("putFloat", MType([FloatType()], VoidType()), CName("io", True)),
            Symbol("putFloatLn", MType([FloatType()], VoidType()), CName("io", True)),

            Symbol("getString", MType([], StringType()), CName("io", True)),
            Symbol("putString", MType([StringType()], VoidType()), CName("io", True)),
            Symbol("putStringLn", MType([StringType()], VoidType()), CName("io", True)),

            Symbol("getBool", MType([], BoolType()), CName("io", True)),
            Symbol("putBool", MType([BoolType()], VoidType()), CName("io", True)),
            Symbol("putBoolLn", MType([BoolType()], VoidType()), CName("io", True)),

            Symbol("putLn", MType([], VoidType()), CName("io", True)),
        ]
        return mem

    def gen(self, ast, dir_):
        gl = self.init()
        self.astTree = ast
        self.path = dir_
        self.emit = Emitter(dir_ + "/" + self.className + ".j")
        self.visit(ast, gl)
       
    def emitObjectInit(self):
        frame = Frame("<init>", VoidType())  
        self.emit.printout(self.emit.emitMETHOD("<init>", MType([], VoidType()), False, frame)) 
        frame.enterScope(True)  
        self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", Id(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))  # Tạo biến "this" trong phương thức <init>
        
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        self.emit.printout(self.emit.emitREADVAR("this", Id(self.className), 0, frame))  
        self.emit.printout(self.emit.emitINVOKESPECIAL(frame))  
        
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        self.emit.printout(self.emit.emitRETURN(VoidType(), frame))  
        self.emit.printout(self.emit.emitENDMETHOD(frame))  
        frame.exitScope()  

    def emitObjectCInit(self, ast: Program, env):
        frame = Frame("<cinit>", VoidType())  
        self.emit.printout(self.emit.emitMETHOD("<clinit>", MType([], VoidType()), True, frame)) 
        frame.enterScope(True)  
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))

        env['frame'] = frame
        self.visit(Block([Assign(Id(item.varName), item.varInit) for item in ast.decl if isinstance(item, VarDecl) and item.varInit] +
                          [Assign(Id(item.conName), item.iniExpr) for item in ast.decl if isinstance(item, ConstDecl) and item.iniExpr]), env)
        
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        self.emit.printout(self.emit.emitRETURN(VoidType(), frame))  
        self.emit.printout(self.emit.emitENDMETHOD(frame))  
        frame.exitScope()

    def visitProgram(self, ast: Program, c):
        self.list_type = {x.name: x for x in ast.decl if isinstance(x, Type)}

        self.list_function = c + [
            Symbol(item.name, MType(list(map(lambda x: x.parType, item.params)), item.retType), CName(self.className))
            for item in ast.decl if isinstance(item, FuncDecl)
        ]

        for item in ast.decl:
            if isinstance(item, MethodDecl):
                struct_type  = self.list_type.get(item.recType.name)
                if struct_type:
                    struct_type.methods.append(item)
                
        env = {}
        env['env'] = [c]
        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
        env = reduce(lambda a, x: self.visit(x, a) if isinstance(x, (VarDecl, ConstDecl)) else a, ast.decl, env)

        reduce(lambda a, x: self.visit(x, a) if isinstance(x, FuncDecl) else a, ast.decl, env)

        self.emitObjectInit()
        self.emitObjectCInit(ast, env)
        self.emit.printout(self.emit.emitEPILOG())

        for item in self.list_type.values():
            self.struct = item
            self.emit = Emitter(self.path + "/" + item.name + ".j")
            self.visit(item, {
                'env': env['env']
            })
        
        return env

    ## TODO decl ------------------------------
    def visitFuncDecl(self, ast: FuncDecl, o: dict) -> dict:
        self.function = ast
        frame = Frame(ast.name, ast.retType)
        isMain = ast.name == "main"
        if isMain:
            mtype = MType([ArrayType([None],StringType())], VoidType())
        else:
            mtype = MType(list(map(lambda x: x.parType, ast.params)), ast.retType)
        
        env = o.copy()
        env['frame'] = frame
        self.emit.printout(self.emit.emitMETHOD(ast.name, mtype, True, frame))
        frame.enterScope(True)
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        env['env'] = [[]] + env['env']
        if isMain:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayType([None],StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))
        else:
            env = reduce(lambda acc,e: self.visit(e,acc),ast.params,env)

        self.visit(ast.body,env)

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(ast.retType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame)) 
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()
        return o

    def visitParamDecl(self, ast: ParamDecl, o: dict) -> dict:
        frame = o['frame']
        index = frame.getNewIndex()
        param_symbol = Symbol(ast.parName, ast.parType, Index(index))
        o['env'][0].append(param_symbol)
        self.emit.printout(self.emit.emitVAR(index, param_symbol.name, param_symbol.mtype, frame.getStartLabel(), frame.getEndLabel(), frame))
        return o
    
    def visitVarDecl(self, ast: VarDecl, o: dict) -> dict:
        def create_init(varType, o: dict):
            init_map = {
                IntType: lambda: IntLiteral(0),
                FloatType: lambda: FloatLiteral(0.0),
                StringType: lambda: StringLiteral("\"\""),
                BoolType: lambda: BooleanLiteral("false"),
                NilLiteral: lambda: NilLiteral(),
                Id: lambda: StructLiteral(varType.name, []),
            }
            if type(varType) in init_map:
                return init_map[type(varType)]()
           
        env = o.copy()
        env['frame'] = Frame("<my-template>", VoidType())

        varInit = ast.varInit 
        varType = ast.varType 

        if not varInit:
            if type(varType) is ArrayType:
                varInit = ArrayLiteral(varType.dimens, varType.dimens, varType)
            else:
                varInit = create_init(varType, o)
            ast.varInit = varInit

        rhsCode, rhsType = self.visit(varInit, env)

        if not varType:
            varType = rhsType

        if 'frame' not in o:
            o['env'][0].append(Symbol(ast.varName, varType, CName(self.className)))
            self.emit.printout(self.emit.emitATTRIBUTE(ast.varName, varType, True, False, None))
        else:
            frame = o['frame']

            index = frame.getNewIndex()
            o['env'][0].append(Symbol(ast.varName, varType, Index(index))) 

            self.emit.printout(self.emit.emitVAR(index, ast.varName, varType, frame.getStartLabel(), frame.getEndLabel(), frame))  
            rhsCode, rhsType = self.visit(varInit, o)
            if type(varType) is FloatType and type(rhsType) is IntType:
                rhsType = FloatType()
                rhsCode += self.emit.emitI2F(frame)
            self.emit.printout(rhsCode)
            self.emit.printout(self.emit.emitWRITEVAR(ast.varName, varType, index,  frame))                
        return o
    
    def visitFuncCall(self, ast: FuncCall, o: dict) -> dict:
        sym = next(filter(lambda x: x.name == ast.funName, self.list_function), None)
        env = o.copy()
        if o.get('stmt'):
            o["stmt"] = False
            output = "".join([str(self.visit(x, o)[0]) for x in ast.args])
            self.emit.printout(output)
            self.emit.printout(self.emit.emitINVOKESTATIC(f"{sym.value.value}/{ast.funName}",sym.mtype, o['frame']))
            return o
        
        output = "".join([str(self.visit(x, env)[0]) for x in ast.args])
        output += self.emit.emitINVOKESTATIC(f"{sym.value.value}/{ast.funName}",sym.mtype, o['frame'])
        return output, sym.mtype.rettype

    def visitBlock(self, ast: Block, o: dict) -> dict:
        env = o.copy()
        env['env'] = [[]] + env['env']
        env['frame'].enterScope(False)
        self.emit.printout(self.emit.emitLABEL(env['frame'].getStartLabel(), env['frame']))

        for item in ast.member:
            if type(item) is FuncCall or type(item) is MethCall:
                env["stmt"] = True
            self.visit(item, env)

        self.emit.printout(self.emit.emitLABEL(env['frame'].getEndLabel(), env['frame']))
        env['frame'].exitScope()
        return o
    
    def visitId(self, ast: Id, o: dict) -> dict:
        sym = next(filter(lambda x: x.name == ast.name, [j for i in o['env'] for j in i]), None)
        if not sym:
            if o.get('isLeft'):
                return self.emit.emitWRITEVAR("this", Id(""), 0, o['frame']), Id("")
            return self.emit.emitREADVAR("this", Id(""), 0, o['frame']), Id("")
        if o.get('isLeft'): 
            if type(sym.value) is Index:
                return self.emit.emitWRITEVAR(sym.name, sym.mtype, sym.value.value, o['frame']), sym.mtype
            else:         
                return self.emit.emitPUTSTATIC(f"{sym.value.value}/{sym.name}", sym.mtype, o['frame']), sym.mtype        
        if type(sym.value) is Index:
            return self.emit.emitREADVAR(sym.name, sym.mtype, sym.value.value , o['frame']), sym.mtype
        else:         
            return self.emit.emitGETSTATIC(f"{sym.value.value}/{sym.name}", sym.mtype, o['frame']), sym.mtype

    def visitAssign(self, ast: Assign, o: dict) -> dict:
        if type(ast.lhs) is Id and not next(filter(lambda x: x.name == ast.lhs.name, [j for i in o['env'] for j in i]),None):
            return self.visitVarDecl(VarDecl(ast.lhs.name, None, ast.rhs), o)
        if type(ast.lhs) is FieldAccess:
            fieldAccess = ast.lhs
            if type(fieldAccess.receiver) is Id and fieldAccess.receiver.name == "this":
                self.emit.printout(self.emit.emitREADVAR("this", Id(self.struct.name), 0, o['frame']))
                field = self.lookup(fieldAccess.field, self.struct.elements, lambda x: x[0])
                rhsCode, rhsType = self.visit(ast.rhs, o) 
                self.emit.printout(rhsCode)
                self.emit.printout(self.emit.emitPUTFIELD(f"{self.struct.name}/{field[0]}", field[1], o['frame']))
                return o
            elif type(fieldAccess.receiver) is Id:
                code,typ = self.visit(fieldAccess.receiver, o)
                structFound = self.list_type.get(typ.name)
                field = self.lookup(fieldAccess.field, structFound.elements, lambda x: x[0])
                rhsCode, rhsType = self.visit(ast.rhs, o)
                o['isLeft'] = False
                self.emit.printout(code + rhsCode)
                self.emit.printout(self.emit.emitPUTFIELD(f"{structFound.name}/{field[0]}", field[1], o['frame']))
                return o

        if type(ast.lhs) is ArrayCell:
            o['frame'].push()
            o['frame'].push()

        rhsCode, rhsType = self.visit(ast.rhs, o)
        o['isLeft'] = True
        lhsCode, lhsType = self.visit(ast.lhs, o)
        o['isLeft'] = False

        if type(ast.lhs) is ArrayCell:
            o['frame'].pop()
            o['frame'].pop()

        if type(lhsType) is FloatType and type(rhsType) is IntType:
            rhsCode += self.emit.emitI2F(o['frame'])

        o['frame'].push()

        if type(ast.lhs) is ArrayCell:
            self.emit.printout(lhsCode)
            self.emit.printout(rhsCode)
            self.emit.printout(self.emit.emitASTORE(lhsType, o['frame'])) 
        else:
            self.emit.printout(rhsCode)
            self.emit.printout(lhsCode)
        return o

    def visitReturn(self, ast: Return, o: dict) -> dict:
        if ast.expr:
            expr, _ = self.visit(ast.expr, o)
            self.emit.printout(expr)
        self.emit.printout(self.emit.emitRETURN(self.function.retType, o['frame']))
        return o

    ## TODO END decl ------------------------------

    ## TODO basic expression ------------------------------
    def visitBinaryOp(self, ast: BinaryOp, o: dict) -> tuple[str, Type]:
        op = ast.op
        frame = o['frame']
        codeLeft, typeLeft = self.visit(ast.left, o)
        codeRight, typeRight = self.visit(ast.right, o)

        if op in ['+', '-'] and type(typeLeft) in [FloatType, IntType]:
            typeReturn = IntType() if type(typeLeft) is IntType and type(typeRight) is IntType else FloatType()
            if type(typeReturn) is FloatType:
                if type(typeLeft) is IntType:
                    codeLeft += self.emit.emitI2F(frame)
                elif type(typeRight) is IntType:
                    codeRight += self.emit.emitI2F(frame)

            return codeLeft + codeRight + self.emit.emitADDOP(op, typeReturn, frame), typeReturn
        if op in ['*', '/']:
            typeReturn = IntType() if type(typeLeft) is IntType and type(typeRight) is IntType else FloatType()
            if type(typeReturn) is FloatType:
                if type(typeLeft) is IntType:
                    codeLeft += self.emit.emitI2F(frame) 
                elif type(typeRight) is IntType:
                    codeRight += self.emit.emitI2F(frame)
            return codeLeft + codeRight + self.emit.emitMULOP(op, typeReturn, frame), typeReturn
        if op in ['%']:
            return codeLeft + codeRight + self.emit.emitMOD(frame), IntType()
        if op in ['==', '!=', '<', '>', '>=', '<='] and type(typeLeft) in [FloatType, IntType]:
            return codeLeft + codeRight + self.emit.emitREOP(op, typeLeft, frame), BoolType() 
        if op in ['||']:
            return codeLeft + codeRight + self.emit.emitOROP(frame), BoolType()
        if op in ['&&']:
            return codeLeft + codeRight + self.emit.emitANDOP(frame), BoolType()  

              
        if op in ['+', '-'] and type(typeLeft) in [StringType]:
            return codeLeft + codeRight + self.emit.emitINVOKEVIRTUAL("java/lang/String/concat", MType([StringType()], StringType()), frame), StringType() 
        if op in ['==', '!=', '<', '>', '>=', '<='] and type(typeLeft) in [StringType]:
            code = codeLeft + codeRight + self.emit.emitREOP(op, typeLeft, frame)
            return code, BoolType()    
              
    def visitUnaryOp(self, ast: UnaryOp, o: dict) -> tuple[str, Type]:
        if ast.op == '!':
            code, type_return = self.visit(ast.body, o)
            return code + self.emit.emitNOT(BoolType(), o['frame']), BoolType()
        elif ast.op == '-':
            code, type_return = self.visit(ast.body, o)
            return code + self.emit.emitNEGOP(type_return, o['frame']), type_return
    
    def visitIntLiteral(self, ast: IntLiteral, o: dict) -> tuple[str, Type]:
        return self.emit.emitPUSHICONST(ast.value, o['frame']), IntType()
    
    def visitFloatLiteral(self, ast: FloatLiteral, o: dict) -> tuple[str, Type]:
        return self.emit.emitPUSHFCONST(ast.value, o['frame']), FloatType()
    
    def visitBooleanLiteral(self, ast: BooleanLiteral, o: dict) -> tuple[str, Type]:
        return self.emit.emitPUSHICONST(ast.value, o['frame']), BoolType()
    
    def visitStringLiteral(self, ast: StringLiteral, o: dict) -> tuple[str, Type]:
        return self.emit.emitPUSHCONST(ast.value, StringType(), o['frame']), StringType()
    
    ## TODO END basic expression ------------------------------

    def visitArrayCell(self, ast: ArrayCell, o: dict) -> tuple[str, Type]:
        newO = o.copy()
        newO['isLeft'] = False
        codeGen, arrType = self.visit(ast.arr, newO)

        for idx, item in enumerate(ast.idx):
            idxCode, idxType = self.visit(item, newO)
            if isinstance(idxType, Id):  
                idxCode += self.emit.emitREADVAR(idxType.name, IntType(), idxType.value, o['frame'])
            codeGen += idxCode
            if idx != len(ast.idx) - 1:
                codeGen += self.emit.emitALOAD(arrType, o['frame'])

        isFullIndexing = len(arrType.dimens) == len(ast.idx)
        retType = arrType.eleType if isFullIndexing else ArrayType(arrType.dimens[len(ast.idx):], arrType.eleType)

        if not o.get('isLeft'):
            codeGen += self.emit.emitALOAD(retType, o['frame'])
        else:
            self.arrayCell = arrType

        return codeGen, retType
    

    def visitArrayLiteral(self, ast: ArrayLiteral, o: dict) -> tuple[str, Type]:
        def generateArrayCode(data, o: dict) -> tuple[str, Type]:
            frame = o['frame']
            codeGen = self.emit.emitPUSHCONST(len(data), IntType(), frame)

            if not isinstance(data[0], list):
                elementCode, elementType = self.visit(data[0], o)
                codeGen += self.emit.emitNEWARRAY(elementType, frame)

                for idx, item in enumerate(data):
                    codeGen += (
                        self.emit.emitDUP(frame)
                        + self.emit.emitPUSHCONST(idx, IntType(), frame)
                        + self.visit(item, o)[0]
                        + self.emit.emitASTORE(elementType, frame)
                    )
                return codeGen, ArrayType([len(data)], elementType)
            else:
                nestedCode, nestedType = generateArrayCode(data[0], o)
                codeGen += self.emit.emitANEWARRAY(nestedType, frame)

                for idx, item in enumerate(data):
                    codeGen += (
                        self.emit.emitDUP(frame)
                        + self.emit.emitPUSHCONST(idx, IntType(), frame)
                        + generateArrayCode(item, o)[0]
                        + self.emit.emitASTORE(nestedType, frame)
                    )
                return codeGen, ArrayType([len(data)], nestedType)

        if type(ast.value) is ArrayType:
            return self.visit(ast.value, o)

        return generateArrayCode(ast.value, o)

    def visitConstDecl(self, ast: ConstDecl, o: dict) -> dict:
        return self.visit(VarDecl(ast.conName, ast.conType, ast.iniExpr), o)
    
    def visitArrayType(self, ast: ArrayType, o):
        frame = o['frame']
        codeGen = ""

        for dim in ast.dimens:
            dimCode, _ = self.visit(dim, o)
            codeGen += dimCode

        if len(ast.dimens) > 1:
            codeGen += self.emit.emitMULTIANEWARRAY(ast, len(ast.dimens), frame)
        else:
            codeGen += self.emit.emitNEWARRAY(ast.eleType, frame)

        return codeGen, ast

    def visitIf(self, ast: If, o: dict) -> dict:
        frame = o['frame']
        label_exit = frame.getNewLabel()
        label_end_if = frame.getNewLabel()
        condCode, _ = self.visit(ast.expr, o)
        self.emit.printout(condCode)
        self.emit.printout(self.emit.emitIFFALSE(label_end_if, frame))
        self.visit(ast.thenStmt, o)
        self.emit.printout(self.emit.emitGOTO(label_exit, frame))
        self.emit.printout(self.emit.emitLABEL(label_end_if, frame))

        if ast.elseStmt is not None:
            self.visit(ast.elseStmt, o)
        self.emit.printout(self.emit.emitLABEL(label_exit, frame))
        return o
    
    def visitForBasic(self, ast: ForBasic, o: dict) -> dict:
        frame = o['frame']
        frame.enterLoop()
        new_label = frame.getNewLabel()
        break_label = frame.getBreakLabel() 
        cont_label = frame.getContinueLabel()
        self.emit.printout(self.emit.emitLABEL(new_label, frame))
        self.emit.printout(self.visit(ast.cond, o)[0])
        self.emit.printout(self.emit.emitIFFALSE(break_label, frame))
        self.visit(ast.loop, o)
        self.emit.printout(self.emit.emitLABEL(cont_label, frame))
        self.emit.printout(self.emit.emitGOTO(new_label, frame))
        self.emit.printout(self.emit.emitLABEL(break_label, frame))
        frame.exitLoop()
        return o
    
    def visitForStep(self, ast: ForStep, o: dict) -> dict:
        frame = o['frame']
        frame.enterLoop()
        label_new = frame.getNewLabel()
        label_break = frame.getBreakLabel()
        label_continue = frame.getContinueLabel()

        env = o.copy()
        env['env'] = [[]] + env['env']

        self.visit(ast.init, env)

        self.emit.printout(self.emit.emitLABEL(label_new, frame))
        self.emit.printout(self.visit(ast.cond, env)[0])
        self.emit.printout(self.emit.emitIFFALSE(label_break, frame))

        self.visit(ast.loop, env)

        self.emit.printout(self.emit.emitLABEL(label_continue, frame))

        self.visit(ast.upda, env)

        self.emit.printout(self.emit.emitGOTO(label_new, frame))
        self.emit.printout(self.emit.emitLABEL(label_break, frame))

        frame.exitLoop()
        return o

    def visitForEach(self, ast, o: dict) -> dict:
        return o

    def visitContinue(self, ast, o: dict) -> dict:
        self.emit.printout(self.emit.emitGOTO(o['frame'].getContinueLabel(), o['frame']))
        return o

    def visitBreak(self, ast, o: dict) -> dict:
        self.emit.printout(self.emit.emitGOTO(o['frame'].getBreakLabel(), o['frame']))
        return o

    def visitFieldAccess(self, ast: FieldAccess, o: dict) -> tuple[str, Type]:
        code, typ = self.visit(ast.receiver, o)
        if self.struct:
            field = next(filter(lambda x: x[0] == ast.field, self.struct.elements), None)
            return code + self.emit.emitGETFIELD(f"{self.struct.name}/{ast.field}", field[1], o['frame']), field[1]
        else:
            typ = self.list_type[typ.name]
            field = next(filter(lambda x: x[0] == ast.field, typ.elements), None)
            return code + self.emit.emitGETFIELD(f"{typ.name}/{ast.field}", field[1], o['frame']), field[1]
        
        
    def visitMethCall(self, ast: MethCall, o: dict) -> tuple[str, Type]:
        code, typ = self.visit(ast.receiver, o)

        if isinstance(typ, Id):
            typ = self.list_type.get(typ.name)
        
        is_stmt = o.pop("stmt", False)

        for arg in ast.args:
            argCode, _ = self.visit(arg, o)
            code += argCode
        
        returnType = None

        if isinstance(typ, StructType):
            method: MethodDecl = next(filter(lambda x: x.fun.name == ast.metName, typ.methods), None)
            mtype = MType(list(map(lambda x: x.parType, method.fun.params)), method.fun.retType)
            returnType = method.fun.retType
            code += self.emit.emitINVOKEVIRTUAL(f"{typ.name}/{ast.metName}", mtype, o['frame'])
        elif isinstance(typ, InterfaceType):
            method = next(filter(lambda x: x.name == ast.metName, typ.methods), None)
            mtype = MType(list(map(lambda x: x.parType, method.params)), method.retType) 
            returnType = method.retType
            code += self.emit.emitINVOKEINTERFACE(f"{typ.name}/{ast.metName}", mtype, o['frame'], 1)

        if is_stmt:
            self.emit.printout(code)
            return o
        return code, returnType
    
    def visitStructLiteral(self, ast: StructLiteral, o: dict) -> tuple[str, Type]:
        frame = o['frame']
        code = self.emit.emitNEW(ast.name, frame) + self.emit.emitDUP(frame)

        element_codes = [self.visit(item[1], o) for item in ast.elements]
        code += ''.join(c for c, _ in element_codes)

        param_types = [t for _, t in element_codes]
        mtype = MType(param_types, VoidType())
        code += self.emit.emitINVOKESPECIAL(frame, f"{ast.name}/<init>", mtype)

        return code, Id(ast.name)
    
    def visitNilLiteral(self, ast: NilLiteral, o: dict) -> tuple[str, Type]:
        code = self.emit.emitPUSHNULL(o['frame'])
        return code, Id("")
    
    def visitStructType(self, ast: StructType, o):
        self.emit.printout(self.emit.emitPROLOG(ast.name, "java.lang.Object"))

        for item in self.list_type.values():
            if self.checkType(item, ast, [(InterfaceType, StructType)]) and item.name != ast.name:
                self.emit.printout(self.emit.emitIMPLEMENTS(item.name))

        for item in ast.elements:
            self.emit.printout(self.emit.emitATTRIBUTE(item[0], item[1], False, False, None, True))  

        paramList = [ParamDecl(item[0], item[1]) for item in ast.elements]
        blockConstructor = Block([
                                Assign(
                                    FieldAccess(Id("this"), item[0]), 
                                    Id(item[0])
                                )
                                for item in ast.elements
                            ])
        param_constructor = MethodDecl(
            None,  
            None,  
            FuncDecl(
                "<init>",
                paramList,  
                VoidType(),
                blockConstructor
            )
        )
        self.visit(param_constructor, o)

        default_constructor = MethodDecl(
            None, None,
            FuncDecl("<init>", [], VoidType(), Block([]))
        )
        self.visit(default_constructor, o)

        for item in ast.methods:
            self.visit(item, o)

        self.emit.printout(self.emit.emitEPILOG())


    
    def visitMethodDecl(self, ast: MethodDecl, o):
        self.function = ast.fun
        frame = Frame(ast.fun.name, ast.fun.retType)
        mtype = MType([param.parType for param in ast.fun.params], ast.fun.retType)
        
        env = o.copy()
        env['frame'] = frame
        self.emit.printout(self.emit.emitMETHOD(ast.fun.name, mtype, False, frame))
        frame.enterScope(True)
        
        self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", Id(self.struct.name), frame.getStartLabel(), frame.getEndLabel(), frame))
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        
        if ast.receiver is None:
            self.emit.printout(self.emit.emitREADVAR("this", Id(""), 0, frame))
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))  

        env['env'] = [[]] + env['env']
        env = reduce(lambda acc, param: self.visit(param, acc), ast.fun.params, env)

        self.visit(ast.fun.body, env)

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if isinstance(ast.fun.retType, VoidType):
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()
        return o


    def visitInterfaceType(self, ast: InterfaceType, o):
        self.emit.printout(self.emit.emitPROLOG(ast.name, "java.lang.Object", True))
        for item in ast.methods:
            frame = Frame(item.name, item.retType) 
            mtype = MType(list(map(lambda x: x.parType, item.params)), item.retType)
            self.emit.printout(self.emit.emitMETHOD(item.name, mtype, False, frame, isAbstract=True))
            self.emit.printout(self.emit.emitENDMETHOD(frame, True))
        self.emit.printout(self.emit.emitEPILOG())

    def checkParams(self, left_params, right_params):
        for method in right_params:
            check_len = len(method.fun.params) == len(left_params.params)
            if check_len == False:
                return False
            for param, arg in zip(method.fun.params, left_params.params):
                check_type = type(param.parType) == type(arg)
                if check_type == False:
                    return False
        return True

    def checkType(self, LHS_type, RHS_type, list_type_permission: List[tuple[Type, Type]] = [], flag = False):
        if isinstance(RHS_type, StructType) and RHS_type.name == "":
            if isinstance(LHS_type, Id):
                LHS_type = self.lookup(LHS_type.name, self.list_type, lambda x: x.name)  
            return isinstance(LHS_type, StructType) or isinstance(LHS_type, InterfaceType)
        
        if isinstance(LHS_type, Id):
            LHS_type = self.lookup(LHS_type.name, self.list_type, lambda x: x.name)
        if isinstance(RHS_type, Id):
            RHS_type = self.lookup(RHS_type.name, self.list_type, lambda x: x.name) 
        
        if (type(LHS_type), type(RHS_type)) in list_type_permission:
            if isinstance(LHS_type, InterfaceType) and isinstance(RHS_type, StructType):
                check_name = all(map(lambda item: self.lookup(item.name, RHS_type.methods, lambda x: x.fun.name), LHS_type.methods))
                check_type_1 = all(map(lambda item: self.lookup(item.retType, RHS_type.methods, lambda x: x.fun.retType), LHS_type.methods))
                check_type_2 = all(map(lambda item: self.lookup(type(item.retType), RHS_type.methods, lambda x: type(x.fun.retType)), LHS_type.methods))
                check_pr = all(map(lambda item: self.checkParams(item, RHS_type.methods), LHS_type.methods))
                
                if not check_name and not check_type_1 and not check_type_2:
                    return False
                if not check_pr:
                    return False
            return True

        if (isinstance(LHS_type, StructType) and isinstance(RHS_type, StructType)) or (isinstance(LHS_type, InterfaceType) and isinstance(RHS_type, InterfaceType)):
            ret = LHS_type.name == RHS_type.name
            return ret

        if isinstance(LHS_type, ArrayType) and isinstance(RHS_type, ArrayType):
            if type(LHS_type.eleType) == Id and type(RHS_type.eleType) == type(LHS_type.eleType):
                LHS_type = self.lookup(LHS_type.eleType.name, self.list_type, lambda x: x.name)
                RHS_type = self.lookup(RHS_type.eleType.name, self.list_type, lambda x: x.name)
                ret = type(LHS_type) == type(RHS_type)
                return ret

            check_dimens = len(LHS_type.dimens) == len(RHS_type.dimens) and LHS_type.dimens == RHS_type.dimens
            if type(LHS_type.eleType) == FloatType:
                if type(RHS_type.eleType) == IntType:
                    if flag == False:
                        return check_dimens
                    else: return False
                if type(RHS_type.eleType) == FloatType:
                   return check_dimens
            check_arr_type = type(LHS_type.eleType) == type(RHS_type.eleType) 
            return check_dimens and check_arr_type 

        ret_global = type(LHS_type) == type(RHS_type)
        return ret_global
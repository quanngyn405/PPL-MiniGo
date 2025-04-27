.source MiniGoClass.java
.class public MiniGoClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is a F from Label2 to Label3
	ldc 5.5
	fstore_1
.var 2 is b F from Label2 to Label3
	fconst_2
	fstore_2
.var 3 is c F from Label2 to Label3
	fload_1
	fload_2
	fdiv
	fstore_3
	fload_3
	invokestatic io/putFloatLn(F)V
Label3:
Label1:
	return
.limit stack 2
.limit locals 4
.end method

.method public <init>()V
.var 0 is this LMiniGoClass; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
Label1:
	return
.limit stack 1
.limit locals 1
.end method

.method public static <clinit>()V
Label0:
Label2:
Label3:
Label1:
	return
.limit stack 0
.limit locals 0
.end method

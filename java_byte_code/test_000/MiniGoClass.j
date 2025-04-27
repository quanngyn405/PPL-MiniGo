.source MiniGoClass.java
.class public MiniGoClass
.super java.lang.Object

.method public static foo(II)V
Label0:
.var 0 is a I from Label0 to Label1
.var 1 is c I from Label0 to Label1
Label2:
.var 2 is b I from Label2 to Label3
	iload_0
	iload_1
	iadd
	istore_2
	iload_2
	invokestatic io/putInt(I)V
Label3:
Label1:
	return
.limit stack 2
.limit locals 3
.end method

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
	iconst_2
	iconst_3
	invokestatic MiniGoClass/foo(II)V
Label3:
Label1:
	return
.limit stack 2
.limit locals 1
.end method

.method public static foo1()I
Label0:
Label2:
	iconst_1
	ireturn
Label3:
Label1:
.limit stack 1
.limit locals 0
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

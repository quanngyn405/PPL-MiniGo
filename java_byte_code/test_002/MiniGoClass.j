.source MiniGoClass.java
.class public MiniGoClass
.super java.lang.Object
.field static a I

.method public static foo()I
Label0:
Label2:
	invokestatic MiniGoClass/foo1()I
	ireturn
Label3:
Label1:
.limit stack 1
.limit locals 0
.end method

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
	getstatic MiniGoClass/a I
	invokestatic io/putInt(I)V
	invokestatic MiniGoClass/foo()I
	putstatic MiniGoClass/a I
	getstatic MiniGoClass/a I
	invokestatic io/putInt(I)V
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
	invokestatic MiniGoClass/foo()I
	invokestatic MiniGoClass/foo1()I
	iadd
	putstatic MiniGoClass/a I
Label3:
Label1:
	return
.limit stack 2
.limit locals 0
.end method

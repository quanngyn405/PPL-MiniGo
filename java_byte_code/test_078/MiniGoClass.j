.source MiniGoClass.java
.class public MiniGoClass
.super java.lang.Object
.field static a [[I

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
	getstatic MiniGoClass/a [[I
	iconst_0
	aaload
	iconst_0
	bipush 100
	iastore
	getstatic MiniGoClass/a [[I
	iconst_1
	aaload
	iconst_1
	getstatic MiniGoClass/a [[I
	iconst_1
	aaload
	iconst_1
	iaload
	getstatic MiniGoClass/a [[I
	iconst_0
	aaload
	iconst_0
	iaload
	getstatic MiniGoClass/a [[I
	iconst_0
	aaload
	iconst_0
	iaload
	iadd
	iadd
	iastore
	getstatic MiniGoClass/a [[I
	iconst_1
	aaload
	iconst_1
	iaload
	invokestatic io/putInt(I)V
Label3:
Label1:
	return
.limit stack 7
.limit locals 1
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
	iconst_2
	iconst_2
	multianewarray [[I 2
	putstatic MiniGoClass/a [[I
Label3:
Label1:
	return
.limit stack 2
.limit locals 0
.end method

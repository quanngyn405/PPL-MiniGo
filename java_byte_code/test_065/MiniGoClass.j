.source MiniGoClass.java
.class public MiniGoClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is a [[F from Label2 to Label3
	iconst_2
	iconst_3
	multianewarray [[F 2
	astore_1
	aload_1
	iconst_0
	aaload
	iconst_0
	aload_1
	iconst_0
	aaload
	iconst_0
	faload
	fconst_2
	fadd
	fastore
	aload_1
	iconst_0
	aaload
	iconst_0
	faload
	aload_1
	iconst_0
	aaload
	iconst_1
	faload
	fadd
	invokestatic io/putFloat(F)V
Label3:
Label1:
	return
.limit stack 6
.limit locals 2
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

.source MiniGoClass.java
.class public MiniGoClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is a F from Label2 to Label3
	iconst_1
	i2f
	fconst_2
	fadd
	fstore_1
.var 2 is b Z from Label2 to Label3
	fconst_1
	fconst_2
	fcmpl
	ifle Label4
	iconst_1
	goto Label5
Label4:
	iconst_0
Label5:
	istore_2
.var 3 is c Ljava/lang/String; from Label2 to Label3
	ldc "vo"
	ldc "tien"
	invokevirtual java/lang/String/concat(Ljava/lang/String;)Ljava/lang/String;
	astore_3
.var 4 is d Z from Label2 to Label3
	ldc "a"
	ldc "b"
	invokevirtual java/lang/String/compareTo(Ljava/lang/String;)I
	iconst_0
	if_icmpge Label6
	iconst_1
	goto Label7
Label6:
	iconst_0
Label7:
	istore 4
	fload_1
	invokestatic io/putFloatLn(F)V
	iload_2
	invokestatic io/putBoolLn(Z)V
	aload_3
	invokestatic io/putStringLn(Ljava/lang/String;)V
	iload 4
	invokestatic io/putBoolLn(Z)V
Label3:
Label1:
	return
.limit stack 7
.limit locals 5
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

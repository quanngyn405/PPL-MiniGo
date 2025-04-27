.source MiniGoClass.java
.class public MiniGoClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
	ldc "apple"
	ldc "banana"
	invokevirtual java/lang/String/compareTo(Ljava/lang/String;)I
	iconst_0
	if_icmple Label4
	iconst_1
	goto Label5
Label4:
	iconst_0
Label5:
	invokestatic io/putBoolLn(Z)V
	ldc "apple"
	ldc "banana"
	invokevirtual java/lang/String/compareTo(Ljava/lang/String;)I
	iconst_0
	if_icmpge Label6
	iconst_1
	goto Label7
Label6:
	iconst_0
Label7:
	invokestatic io/putBoolLn(Z)V
	ldc "apple"
	ldc "apple"
	invokevirtual java/lang/String/compareTo(Ljava/lang/String;)I
	iconst_0
	if_icmpgt Label8
	iconst_1
	goto Label9
Label8:
	iconst_0
Label9:
	invokestatic io/putBoolLn(Z)V
	ldc "banana"
	ldc "apple"
	invokevirtual java/lang/String/compareTo(Ljava/lang/String;)I
	iconst_0
	if_icmplt Label10
	iconst_1
	goto Label11
Label10:
	iconst_0
Label11:
	invokestatic io/putBoolLn(Z)V
	ldc "hello"
	ldc "hello"
	invokevirtual java/lang/String/compareTo(Ljava/lang/String;)I
	iconst_0
	if_icmpne Label12
	iconst_1
	goto Label13
Label12:
	iconst_0
Label13:
	invokestatic io/putBoolLn(Z)V
	ldc "hello"
	ldc "hello"
	invokevirtual java/lang/String/compareTo(Ljava/lang/String;)I
	iconst_0
	if_icmpeq Label14
	iconst_1
	goto Label15
Label14:
	iconst_0
Label15:
	invokestatic io/putBoolLn(Z)V
Label3:
Label1:
	return
.limit stack 25
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
Label3:
Label1:
	return
.limit stack 0
.limit locals 0
.end method

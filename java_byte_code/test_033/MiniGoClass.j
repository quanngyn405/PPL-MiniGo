.source MiniGoClass.java
.class public MiniGoClass
.super java.lang.Object

.method public static fooInt(I)I
Label0:
.var 0 is a I from Label0 to Label1
Label2:
	iload_0
	ireturn
Label3:
Label1:
.limit stack 1
.limit locals 1
.end method

.method public static fooFloat(F)F
Label0:
.var 0 is a F from Label0 to Label1
Label2:
	fload_0
	freturn
Label3:
Label1:
.limit stack 1
.limit locals 1
.end method

.method public static fooString(Ljava/lang/String;)Ljava/lang/String;
Label0:
.var 0 is a Ljava/lang/String; from Label0 to Label1
Label2:
	aload_0
	areturn
Label3:
Label1:
.limit stack 1
.limit locals 1
.end method

.method public static fooBool(Z)Z
Label0:
.var 0 is a Z from Label0 to Label1
Label2:
	iload_0
	ireturn
Label3:
Label1:
.limit stack 1
.limit locals 1
.end method

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
	iconst_2
	invokestatic MiniGoClass/fooInt(I)I
	invokestatic io/putInt(I)V
	ldc 1.5
	invokestatic MiniGoClass/fooFloat(F)F
	invokestatic io/putFloat(F)V
	ldc "S"
	invokestatic MiniGoClass/fooString(Ljava/lang/String;)Ljava/lang/String;
	invokestatic io/putString(Ljava/lang/String;)V
	iconst_1
	invokestatic MiniGoClass/fooBool(Z)Z
	invokestatic io/putBool(Z)V
Label3:
Label1:
	return
.limit stack 2
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

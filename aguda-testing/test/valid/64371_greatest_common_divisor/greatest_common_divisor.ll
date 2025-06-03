; ModuleID = ""
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare external i32 @"printf"(i8* %".1", ...)

define i32 @"_power"(i32 %".1", i32 %".2")
{
entry:
  %".4" = alloca i32
  store i32 %".1", i32* %".4"
  %".6" = alloca i32
  store i32 %".2", i32* %".6"
  %".8" = alloca i32
  store i32 1, i32* %".8"
  br label %"while_0_cond"
while_0_cond:
  %".11" = load i32, i32* %".6"
  %".12" = icmp sgt i32 %".11", 0
  br i1 %".12", label %"while_0_body", label %"while_0_end"
while_0_body:
  %".14" = load i32, i32* %".8"
  %".15" = load i32, i32* %".4"
  %".16" = mul i32 %".14", %".15"
  store i32 %".16", i32* %".8"
  %".18" = load i32, i32* %".6"
  %".19" = sub i32 %".18", 1
  store i32 %".19", i32* %".6"
  br label %"while_0_cond"
while_0_end:
  %".22" = load i32, i32* %".8"
  ret i32 %".22"
}

@"int_format" = internal constant [3 x i8] c"%d\00"
@"true_str" = internal constant [5 x i8] c"true\00"
@"false_str" = internal constant [6 x i8] c"false\00"
@"unit_str" = internal constant [5 x i8] c"unit\00"
define i32 @"gcd"(i32 %".1", i32 %".2")
{
entry:
  %".4" = alloca i32
  store i32 %".1", i32* %".4"
  %".6" = alloca i32
  store i32 %".2", i32* %".6"
  %".8" = load i32, i32* %".6"
  %".9" = icmp eq i32 %".8", 0
  br i1 %".9", label %"cond_1_then", label %"cond_1_else"
cond_1_then:
  %".11" = load i32, i32* %".4"
  br label %"cond_1_end"
cond_1_else:
  %".13" = load i32, i32* %".6"
  %".14" = load i32, i32* %".4"
  %".15" = load i32, i32* %".6"
  %".16" = srem i32 %".14", %".15"
  %".17" = call i32 @"gcd"(i32 %".13", i32 %".16")
  br label %"cond_1_end"
cond_1_end:
  %".19" = phi  i32 [%".11", %"cond_1_then"], [%".17", %"cond_1_else"]
  ret i32 %".19"
}

define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = alloca i32
  store i32 60, i32* %".5"
  %".7" = alloca i32
  store i32 24, i32* %".7"
  %".9" = load i32, i32* %".5"
  %".10" = load i32, i32* %".7"
  %".11" = call i32 @"gcd"(i32 %".9", i32 %".10")
  %".12" = alloca i32
  store i32 %".11", i32* %".12"
  %".14" = load i32, i32* %".12"
  %".15" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".15", i32 %".14")
  ret i1 0
}

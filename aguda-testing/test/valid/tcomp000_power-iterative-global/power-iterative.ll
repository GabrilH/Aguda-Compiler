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
@"result" = global i32 0
define i32 @"power"(i32 %".1", i32 %".2")
{
entry:
  %".4" = alloca i32
  store i32 %".1", i32* %".4"
  %".6" = alloca i32
  store i32 %".2", i32* %".6"
  store i32 1, i32* @"result"
  br label %"while_1_cond"
while_1_cond:
  %".10" = load i32, i32* %".6"
  %".11" = icmp sgt i32 %".10", 0
  br i1 %".11", label %"while_1_body", label %"while_1_end"
while_1_body:
  %".13" = load i32, i32* @"result"
  %".14" = load i32, i32* %".4"
  %".15" = mul i32 %".13", %".14"
  store i32 %".15", i32* @"result"
  %".17" = load i32, i32* %".6"
  %".18" = sub i32 %".17", 1
  store i32 %".18", i32* %".6"
  br label %"while_1_cond"
while_1_end:
  %".21" = load i32, i32* @"result"
  ret i32 %".21"
}

define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = call i32 @"power"(i32 2, i32 6)
  %".6" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6", i32 %".5")
  ret i1 0
}

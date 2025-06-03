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
define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  br i1 0, label %"bool_2_right", label %"bool_2_end"
bool_1_right:
  br label %"bool_1_end"
bool_1_end:
  %".10" = phi  i1 [%".7", %"bool_2_end"], [1, %"bool_1_right"]
  %".11" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".12" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".13" = select  i1 %".10", i8* %".11", i8* %".12"
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".13")
  ret i1 0
bool_2_right:
  br label %"bool_2_end"
bool_2_end:
  %".7" = phi  i1 [0, %"entry"], [1, %"bool_2_right"]
  br i1 %".7", label %"bool_1_end", label %"bool_1_right"
}

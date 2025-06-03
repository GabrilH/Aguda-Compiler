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
define i32 @"calculate_operations"(i32 %".1", i32 %".2", i32 %".3", i32 %".4", i32 %".5")
{
entry:
  %".7" = alloca i32
  store i32 %".1", i32* %".7"
  %".9" = alloca i32
  store i32 %".2", i32* %".9"
  %".11" = alloca i32
  store i32 %".3", i32* %".11"
  %".13" = alloca i32
  store i32 %".4", i32* %".13"
  %".15" = alloca i32
  store i32 %".5", i32* %".15"
  %".17" = load i32, i32* %".7"
  %".18" = load i32, i32* %".9"
  %".19" = mul i32 %".17", %".18"
  %".20" = alloca i32
  store i32 %".19", i32* %".20"
  %".22" = load i32, i32* %".11"
  %".23" = load i32, i32* %".13"
  %".24" = mul i32 %".22", %".23"
  %".25" = alloca i32
  store i32 %".24", i32* %".25"
  %".27" = load i32, i32* %".20"
  %".28" = load i32, i32* %".25"
  %".29" = sub i32 %".27", %".28"
  %".30" = alloca i32
  store i32 %".29", i32* %".30"
  %".32" = load i32, i32* %".30"
  %".33" = load i32, i32* %".15"
  %".34" = add i32 %".32", %".33"
  %".35" = alloca i32
  store i32 %".34", i32* %".35"
  %".37" = load i32, i32* %".35"
  ret i32 %".37"
}

@"x" = global i32 1
@"y" = global i32 2
@"z" = global i32 3
@"w" = global i32 4
@"v" = global i32 5
define i32 @"final_result"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = load i32, i32* @"x"
  %".6" = load i32, i32* @"y"
  %".7" = load i32, i32* @"z"
  %".8" = load i32, i32* @"w"
  %".9" = load i32, i32* @"v"
  %".10" = call i32 @"calculate_operations"(i32 %".5", i32 %".6", i32 %".7", i32 %".8", i32 %".9")
  ret i32 %".10"
}

define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = load i1, i1* %".3"
  %".6" = call i32 @"final_result"(i1 %".5")
  %".7" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".7", i32 %".6")
  ret i1 0
}

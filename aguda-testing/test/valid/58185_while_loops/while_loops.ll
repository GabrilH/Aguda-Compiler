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
define i1 @"printPattern"(i32 %".1")
{
entry:
  %".3" = alloca i32
  store i32 %".1", i32* %".3"
  %".5" = alloca i32
  store i32 0, i32* %".5"
  br label %"while_1_cond"
while_1_cond:
  %".8" = load i32, i32* %".5"
  %".9" = load i32, i32* %".3"
  %".10" = icmp slt i32 %".8", %".9"
  br i1 %".10", label %"while_1_body", label %"while_1_end"
while_1_body:
  %".12" = alloca i32
  store i32 0, i32* %".12"
  br label %"while_2_cond"
while_1_end:
  ret i1 0
while_2_cond:
  %".15" = load i32, i32* %".12"
  %".16" = load i32, i32* %".5"
  %".17" = icmp sle i32 %".15", %".16"
  br i1 %".17", label %"while_2_body", label %"while_2_end"
while_2_body:
  %".19" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".20" = call i32 (i8*, ...) @"printf"(i8* %".19", i32 5)
  %".21" = load i32, i32* %".12"
  %".22" = add i32 %".21", 1
  store i32 %".22", i32* %".12"
  br label %"while_2_cond"
while_2_end:
  %".25" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".26" = call i32 (i8*, ...) @"printf"(i8* %".25", i32 0)
  %".27" = load i32, i32* %".5"
  %".28" = add i32 %".27", 1
  store i32 %".28", i32* %".5"
  br label %"while_1_cond"
}

define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = call i1 @"printPattern"(i32 5)
  ret i1 %".5"
}

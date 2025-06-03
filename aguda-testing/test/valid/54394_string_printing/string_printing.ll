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
define i1 @"printn"(i1 %".1", i32 %".2")
{
entry:
  %".4" = alloca i1
  store i1 %".1", i1* %".4"
  %".6" = alloca i32
  store i32 %".2", i32* %".6"
  %".8" = alloca i32
  store i32 0, i32* %".8"
  br label %"while_1_cond"
while_1_cond:
  %".11" = load i32, i32* %".8"
  %".12" = load i32, i32* %".6"
  %".13" = icmp slt i32 %".11", %".12"
  br i1 %".13", label %"while_1_body", label %"while_1_end"
while_1_body:
  %".15" = load i1, i1* %".4"
  %".16" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".17" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".18" = select  i1 %".15", i8* %".16", i8* %".17"
  %".19" = call i32 (i8*, ...) @"printf"(i8* %".18")
  %".20" = load i32, i32* %".8"
  %".21" = add i32 %".20", 1
  store i32 %".21", i32* %".8"
  br label %"while_1_cond"
while_1_end:
  ret i1 0
}

define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = call i1 @"printn"(i1 0, i32 4)
  ret i1 %".5"
}

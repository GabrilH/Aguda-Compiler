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
define i1 @"testPositiveAssignment"(i32 %".1")
{
entry:
  %".3" = alloca i32
  store i32 %".1", i32* %".3"
  %".5" = load i32, i32* %".3"
  %".6" = icmp sgt i32 %".5", 0
  br i1 %".6", label %"cond_1_then", label %"cond_1_else"
cond_1_then:
  %".8" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".9" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".10" = select  i1 1, i8* %".8", i8* %".9"
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".10")
  br label %"cond_1_end"
cond_1_else:
  %".13" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".14" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".15" = select  i1 0, i8* %".13", i8* %".14"
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".15")
  br label %"cond_1_end"
cond_1_end:
  %".18" = phi  i1 [0, %"cond_1_then"], [0, %"cond_1_else"]
  ret i1 %".18"
}

define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = call i1 @"testPositiveAssignment"(i32 -10)
  %".6" = call i1 @"testPositiveAssignment"(i32 10)
  ret i1 %".6"
}

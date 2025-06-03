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
define i1 @"is_prime"(i32 %".1")
{
entry:
  %".3" = alloca i32
  store i32 %".1", i32* %".3"
  %".5" = alloca i1
  store i1 1, i1* %".5"
  %".7" = load i32, i32* %".3"
  %".8" = icmp slt i32 %".7", 2
  br i1 %".8", label %"cond_1_then", label %"cond_1_else"
cond_1_then:
  store i1 0, i1* %".5"
  br label %"cond_1_end"
cond_1_else:
  %".12" = alloca i32
  store i32 2, i32* %".12"
  br label %"while_2_cond"
cond_1_end:
  %".35" = phi  i1 [0, %"cond_1_then"], [0, %"while_2_end"]
  %".36" = load i1, i1* %".5"
  ret i1 %".36"
while_2_cond:
  %".15" = load i32, i32* %".12"
  %".16" = load i32, i32* %".12"
  %".17" = mul i32 %".15", %".16"
  %".18" = load i32, i32* %".3"
  %".19" = icmp sle i32 %".17", %".18"
  br i1 %".19", label %"while_2_body", label %"while_2_end"
while_2_body:
  %".21" = load i32, i32* %".3"
  %".22" = load i32, i32* %".12"
  %".23" = srem i32 %".21", %".22"
  %".24" = icmp eq i32 %".23", 0
  br i1 %".24", label %"cond_3_then", label %"cond_3_else"
while_2_end:
  br label %"cond_1_end"
cond_3_then:
  store i1 0, i1* %".5"
  br label %"cond_3_end"
cond_3_else:
  br label %"cond_3_end"
cond_3_end:
  %".29" = phi  i1 [0, %"cond_3_then"], [0, %"cond_3_else"]
  %".30" = load i32, i32* %".12"
  %".31" = add i32 %".30", 1
  store i32 %".31", i32* %".12"
  br label %"while_2_cond"
}

define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = call i1 @"is_prime"(i32 1)
  %".6" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".7" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".8" = select  i1 %".5", i8* %".6", i8* %".7"
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8")
  %".10" = call i1 @"is_prime"(i32 2)
  %".11" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".12" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".13" = select  i1 %".10", i8* %".11", i8* %".12"
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".13")
  %".15" = call i1 @"is_prime"(i32 9)
  %".16" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".17" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".18" = select  i1 %".15", i8* %".16", i8* %".17"
  %".19" = call i32 (i8*, ...) @"printf"(i8* %".18")
  %".20" = call i1 @"is_prime"(i32 13)
  %".21" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".22" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".23" = select  i1 %".20", i8* %".21", i8* %".22"
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".23")
  ret i1 0
}

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
@"ola" = global i1 0
define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = load i1, i1* @"ola"
  br i1 %".5", label %"cond_2_then", label %"cond_2_else"
cond_1_then:
  %".13" = load i1, i1* @"ola"
  br i1 %".13", label %"cond_3_then", label %"cond_3_else"
cond_1_else:
  %".21" = load i1, i1* @"ola"
  br i1 %".21", label %"cond_4_then", label %"cond_4_else"
cond_1_end:
  %".29" = phi  i1 [%".19", %"cond_3_end"], [%".27", %"cond_4_end"]
  %".30" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".31" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".32" = select  i1 %".29", i8* %".30", i8* %".31"
  %".33" = call i32 (i8*, ...) @"printf"(i8* %".32")
  ret i1 0
cond_2_then:
  %".7" = load i1, i1* @"ola"
  br label %"cond_2_end"
cond_2_else:
  %".9" = load i1, i1* @"ola"
  br label %"cond_2_end"
cond_2_end:
  %".11" = phi  i1 [%".7", %"cond_2_then"], [%".9", %"cond_2_else"]
  br i1 %".11", label %"cond_1_then", label %"cond_1_else"
cond_3_then:
  %".15" = load i1, i1* @"ola"
  br label %"cond_3_end"
cond_3_else:
  %".17" = load i1, i1* @"ola"
  br label %"cond_3_end"
cond_3_end:
  %".19" = phi  i1 [%".15", %"cond_3_then"], [%".17", %"cond_3_else"]
  br label %"cond_1_end"
cond_4_then:
  %".23" = load i1, i1* @"ola"
  br label %"cond_4_end"
cond_4_else:
  %".25" = load i1, i1* @"ola"
  br label %"cond_4_end"
cond_4_end:
  %".27" = phi  i1 [%".23", %"cond_4_then"], [%".25", %"cond_4_else"]
  br label %"cond_1_end"
}

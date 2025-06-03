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
define i1 @"printBool"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = load i1, i1* %".3"
  br i1 %".5", label %"cond_1_then", label %"cond_1_else"
cond_1_then:
  %".7" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".8" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".9" = select  i1 1, i8* %".7", i8* %".8"
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".9")
  br label %"cond_1_end"
cond_1_else:
  %".12" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".13" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".14" = select  i1 0, i8* %".12", i8* %".13"
  %".15" = call i32 (i8*, ...) @"printf"(i8* %".14")
  br label %"cond_1_end"
cond_1_end:
  %".17" = phi  i1 [0, %"cond_1_then"], [0, %"cond_1_else"]
  ret i1 %".17"
}

define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  br i1 1, label %"bool_2_right", label %"bool_2_end"
bool_2_right:
  br label %"bool_2_end"
bool_2_end:
  %".7" = phi  i1 [1, %"entry"], [1, %"bool_2_right"]
  %".8" = call i1 @"printBool"(i1 %".7")
  br i1 1, label %"bool_3_right", label %"bool_3_end"
bool_3_right:
  br label %"bool_3_end"
bool_3_end:
  %".11" = phi  i1 [1, %"bool_2_end"], [0, %"bool_3_right"]
  %".12" = call i1 @"printBool"(i1 %".11")
  br i1 1, label %"bool_4_end", label %"bool_4_right"
bool_4_right:
  br label %"bool_4_end"
bool_4_end:
  %".15" = phi  i1 [1, %"bool_3_end"], [0, %"bool_4_right"]
  %".16" = call i1 @"printBool"(i1 %".15")
  br i1 0, label %"bool_5_end", label %"bool_5_right"
bool_5_right:
  br label %"bool_5_end"
bool_5_end:
  %".19" = phi  i1 [0, %"bool_4_end"], [0, %"bool_5_right"]
  %".20" = call i1 @"printBool"(i1 %".19")
  %".21" = xor i1 1, -1
  %".22" = call i1 @"printBool"(i1 %".21")
  %".23" = xor i1 0, -1
  %".24" = call i1 @"printBool"(i1 %".23")
  ret i1 %".24"
}

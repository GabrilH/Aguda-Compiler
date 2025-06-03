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
  %".5" = alloca i32
  store i32 0, i32* %".5"
  %".7" = alloca i32
  store i32 1, i32* %".7"
  %".9" = alloca i32
  store i32 2, i32* %".9"
  br label %"while_1_cond"
while_1_cond:
  %".12" = load i32, i32* %".9"
  %".13" = icmp slt i32 %".12", 4000000
  br i1 %".13", label %"while_1_body", label %"while_1_end"
while_1_body:
  %".15" = load i32, i32* %".9"
  %".16" = srem i32 %".15", 2
  %".17" = icmp eq i32 %".16", 0
  br i1 %".17", label %"cond_2_then", label %"cond_2_else"
while_1_end:
  %".36" = load i32, i32* %".5"
  %".37" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".38" = call i32 (i8*, ...) @"printf"(i8* %".37", i32 %".36")
  ret i1 0
cond_2_then:
  %".19" = load i32, i32* %".5"
  %".20" = load i32, i32* %".9"
  %".21" = add i32 %".19", %".20"
  store i32 %".21", i32* %".5"
  br label %"cond_2_end"
cond_2_else:
  br label %"cond_2_end"
cond_2_end:
  %".25" = phi  i1 [0, %"cond_2_then"], [0, %"cond_2_else"]
  %".26" = load i32, i32* %".7"
  %".27" = alloca i32
  store i32 %".26", i32* %".27"
  %".29" = load i32, i32* %".9"
  store i32 %".29", i32* %".7"
  %".31" = load i32, i32* %".27"
  %".32" = load i32, i32* %".9"
  %".33" = add i32 %".31", %".32"
  store i32 %".33", i32* %".9"
  br label %"while_1_cond"
}

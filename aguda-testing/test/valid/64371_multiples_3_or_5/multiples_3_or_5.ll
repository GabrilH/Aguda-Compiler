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
  store i32 0, i32* %".7"
  br label %"while_1_cond"
while_1_cond:
  %".10" = load i32, i32* %".7"
  %".11" = icmp slt i32 %".10", 1000
  br i1 %".11", label %"while_1_body", label %"while_1_end"
while_1_body:
  %".13" = load i32, i32* %".7"
  %".14" = srem i32 %".13", 3
  %".15" = icmp eq i32 %".14", 0
  br i1 %".15", label %"bool_3_end", label %"bool_3_right"
while_1_end:
  %".34" = load i32, i32* %".5"
  %".35" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".36" = call i32 (i8*, ...) @"printf"(i8* %".35", i32 %".34")
  ret i1 0
cond_2_then:
  %".23" = load i32, i32* %".5"
  %".24" = load i32, i32* %".7"
  %".25" = add i32 %".23", %".24"
  store i32 %".25", i32* %".5"
  br label %"cond_2_end"
cond_2_else:
  br label %"cond_2_end"
cond_2_end:
  %".29" = phi  i1 [0, %"cond_2_then"], [0, %"cond_2_else"]
  %".30" = load i32, i32* %".7"
  %".31" = add i32 %".30", 1
  store i32 %".31", i32* %".7"
  br label %"while_1_cond"
bool_3_right:
  %".17" = load i32, i32* %".7"
  %".18" = srem i32 %".17", 5
  %".19" = icmp eq i32 %".18", 0
  br label %"bool_3_end"
bool_3_end:
  %".21" = phi  i1 [%".15", %"while_1_body"], [%".19", %"bool_3_right"]
  br i1 %".21", label %"cond_2_then", label %"cond_2_else"
}

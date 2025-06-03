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
  store i32 1, i32* %".5"
  %".7" = alloca i32
  store i32 10, i32* %".7"
  %".9" = alloca i32
  store i32 0, i32* %".9"
  br label %"while_1_cond"
while_1_cond:
  %".12" = load i32, i32* %".5"
  %".13" = load i32, i32* %".7"
  %".14" = icmp slt i32 %".12", %".13"
  br i1 %".14", label %"bool_2_right", label %"bool_2_end"
while_1_body:
  %".28" = load i32, i32* %".5"
  %".29" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".30" = call i32 (i8*, ...) @"printf"(i8* %".29", i32 %".28")
  %".31" = load i32, i32* %".7"
  %".32" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".33" = call i32 (i8*, ...) @"printf"(i8* %".32", i32 %".31")
  %".34" = load i32, i32* %".5"
  %".35" = add i32 %".34", 1
  store i32 %".35", i32* %".5"
  %".37" = load i32, i32* %".7"
  %".38" = sub i32 %".37", 1
  store i32 %".38", i32* %".7"
  %".40" = load i32, i32* %".9"
  %".41" = add i32 %".40", 1
  store i32 %".41", i32* %".9"
  br label %"while_1_cond"
while_1_end:
  %".44" = load i32, i32* %".9"
  %".45" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".46" = call i32 (i8*, ...) @"printf"(i8* %".45", i32 %".44")
  %".47" = load i32, i32* %".5"
  %".48" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".49" = call i32 (i8*, ...) @"printf"(i8* %".48", i32 %".47")
  %".50" = load i32, i32* %".7"
  %".51" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".52" = call i32 (i8*, ...) @"printf"(i8* %".51", i32 %".50")
  ret i1 0
bool_2_right:
  %".16" = load i32, i32* %".5"
  %".17" = srem i32 %".16", 3
  %".18" = icmp ne i32 %".17", 0
  br i1 %".18", label %"bool_3_end", label %"bool_3_right"
bool_2_end:
  %".26" = phi  i1 [%".14", %"while_1_cond"], [%".24", %"bool_3_end"]
  br i1 %".26", label %"while_1_body", label %"while_1_end"
bool_3_right:
  %".20" = load i32, i32* %".7"
  %".21" = srem i32 %".20", 5
  %".22" = icmp ne i32 %".21", 0
  br label %"bool_3_end"
bool_3_end:
  %".24" = phi  i1 [%".18", %"bool_2_right"], [%".22", %"bool_3_right"]
  br label %"bool_2_end"
}

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
define i1 @"booleanConfusion"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = alloca i1
  store i1 1, i1* %".5"
  %".7" = alloca i1
  store i1 0, i1* %".7"
  %".9" = load i1, i1* %".5"
  %".10" = xor i1 %".9", -1
  %".11" = alloca i1
  store i1 %".10", i1* %".11"
  %".13" = load i1, i1* %".7"
  %".14" = xor i1 %".13", -1
  %".15" = alloca i1
  store i1 %".14", i1* %".15"
  %".17" = load i1, i1* %".5"
  br i1 %".17", label %"bool_1_right", label %"bool_1_end"
bool_1_right:
  %".19" = load i1, i1* %".7"
  br label %"bool_1_end"
bool_1_end:
  %".21" = phi  i1 [%".17", %"entry"], [%".19", %"bool_1_right"]
  %".22" = alloca i1
  store i1 %".21", i1* %".22"
  %".24" = load i1, i1* %".5"
  br i1 %".24", label %"bool_2_end", label %"bool_2_right"
bool_2_right:
  %".26" = load i1, i1* %".7"
  br label %"bool_2_end"
bool_2_end:
  %".28" = phi  i1 [%".24", %"bool_1_end"], [%".26", %"bool_2_right"]
  %".29" = alloca i1
  store i1 %".28", i1* %".29"
  %".31" = load i1, i1* %".5"
  br i1 %".31", label %"bool_3_right", label %"bool_3_end"
bool_3_right:
  %".33" = load i1, i1* %".7"
  br label %"bool_3_end"
bool_3_end:
  %".35" = phi  i1 [%".31", %"bool_2_end"], [%".33", %"bool_3_right"]
  %".36" = xor i1 %".35", -1
  %".37" = alloca i1
  store i1 %".36", i1* %".37"
  %".39" = load i1, i1* %".5"
  br i1 %".39", label %"bool_4_end", label %"bool_4_right"
bool_4_right:
  %".41" = load i1, i1* %".7"
  br label %"bool_4_end"
bool_4_end:
  %".43" = phi  i1 [%".39", %"bool_3_end"], [%".41", %"bool_4_right"]
  %".44" = xor i1 %".43", -1
  %".45" = alloca i1
  store i1 %".44", i1* %".45"
  %".47" = load i1, i1* %".5"
  br i1 %".47", label %"bool_5_right", label %"bool_5_end"
bool_5_right:
  %".49" = load i1, i1* %".37"
  br label %"bool_5_end"
bool_5_end:
  %".51" = phi  i1 [%".47", %"bool_4_end"], [%".49", %"bool_5_right"]
  %".52" = alloca i1
  store i1 %".51", i1* %".52"
  %".54" = load i1, i1* %".5"
  br i1 %".54", label %"bool_8_end", label %"bool_8_right"
bool_6_right:
  %".64" = load i1, i1* %".29"
  br i1 %".64", label %"bool_9_right", label %"bool_9_end"
bool_6_end:
  %".82" = phi  i1 [%".62", %"bool_7_end"], [%".80", %"bool_9_end"]
  %".83" = alloca i1
  store i1 %".82", i1* %".83"
  %".85" = load i1, i1* %".83"
  ret i1 %".85"
bool_7_right:
  %".60" = load i1, i1* %".15"
  br label %"bool_7_end"
bool_7_end:
  %".62" = phi  i1 [%".58", %"bool_8_end"], [%".60", %"bool_7_right"]
  br i1 %".62", label %"bool_6_end", label %"bool_6_right"
bool_8_right:
  %".56" = load i1, i1* %".11"
  br label %"bool_8_end"
bool_8_end:
  %".58" = phi  i1 [%".54", %"bool_5_end"], [%".56", %"bool_8_right"]
  br i1 %".58", label %"bool_7_right", label %"bool_7_end"
bool_9_right:
  %".66" = load i1, i1* %".15"
  br i1 %".66", label %"bool_10_end", label %"bool_10_right"
bool_9_end:
  %".80" = phi  i1 [%".64", %"bool_6_right"], [%".78", %"bool_10_end"]
  br label %"bool_6_end"
bool_10_right:
  %".68" = load i1, i1* %".45"
  br i1 %".68", label %"bool_11_right", label %"bool_11_end"
bool_10_end:
  %".78" = phi  i1 [%".66", %"bool_9_right"], [%".76", %"bool_11_end"]
  br label %"bool_9_end"
bool_11_right:
  %".70" = load i1, i1* %".11"
  br i1 %".70", label %"bool_12_end", label %"bool_12_right"
bool_11_end:
  %".76" = phi  i1 [%".68", %"bool_10_right"], [%".74", %"bool_12_end"]
  br label %"bool_10_end"
bool_12_right:
  %".72" = load i1, i1* %".52"
  br label %"bool_12_end"
bool_12_end:
  %".74" = phi  i1 [%".70", %"bool_11_right"], [%".72", %"bool_12_right"]
  br label %"bool_11_end"
}

define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = call i1 @"booleanConfusion"(i1 0)
  %".6" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".7" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".8" = select  i1 %".5", i8* %".6", i8* %".7"
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8")
  ret i1 0
}

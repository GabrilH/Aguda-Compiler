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
  %".5" = alloca i1
  store i1 1, i1* %".5"
  %".7" = alloca i1
  store i1 0, i1* %".7"
  %".9" = alloca i1
  store i1 1, i1* %".9"
  %".11" = alloca i1
  store i1 0, i1* %".11"
  %".13" = load i1, i1* %".5"
  br i1 %".13", label %"bool_1_right", label %"bool_1_end"
bool_1_right:
  %".15" = load i1, i1* %".7"
  br i1 %".15", label %"bool_2_end", label %"bool_2_right"
bool_1_end:
  %".21" = phi  i1 [%".13", %"entry"], [%".19", %"bool_2_end"]
  store i1 %".21", i1* %".11"
  %".23" = load i1, i1* %".11"
  %".24" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".25" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".26" = select  i1 %".23", i8* %".24", i8* %".25"
  %".27" = call i32 (i8*, ...) @"printf"(i8* %".26")
  %".28" = load i1, i1* %".5"
  br i1 %".28", label %"bool_4_right", label %"bool_4_end"
bool_2_right:
  %".17" = load i1, i1* %".9"
  br label %"bool_2_end"
bool_2_end:
  %".19" = phi  i1 [%".15", %"bool_1_right"], [%".17", %"bool_2_right"]
  br label %"bool_1_end"
bool_3_right:
  %".34" = load i1, i1* %".9"
  br label %"bool_3_end"
bool_3_end:
  %".36" = phi  i1 [%".32", %"bool_4_end"], [%".34", %"bool_3_right"]
  store i1 %".36", i1* %".11"
  %".38" = load i1, i1* %".11"
  %".39" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".40" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".41" = select  i1 %".38", i8* %".39", i8* %".40"
  %".42" = call i32 (i8*, ...) @"printf"(i8* %".41")
  %".43" = load i1, i1* %".5"
  br i1 %".43", label %"bool_6_right", label %"bool_6_end"
bool_4_right:
  %".30" = load i1, i1* %".7"
  br label %"bool_4_end"
bool_4_end:
  %".32" = phi  i1 [%".28", %"bool_1_end"], [%".30", %"bool_4_right"]
  br i1 %".32", label %"bool_3_end", label %"bool_3_right"
bool_5_right:
  %".50" = load i1, i1* %".7"
  br i1 %".50", label %"bool_7_right", label %"bool_7_end"
bool_5_end:
  %".56" = phi  i1 [%".48", %"bool_6_end"], [%".54", %"bool_7_end"]
  store i1 %".56", i1* %".11"
  %".58" = load i1, i1* %".11"
  %".59" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".60" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".61" = select  i1 %".58", i8* %".59", i8* %".60"
  %".62" = call i32 (i8*, ...) @"printf"(i8* %".61")
  %".63" = load i1, i1* %".5"
  %".64" = xor i1 %".63", -1
  br i1 %".64", label %"bool_8_right", label %"bool_8_end"
bool_6_right:
  %".45" = load i1, i1* %".7"
  br label %"bool_6_end"
bool_6_end:
  %".47" = phi  i1 [%".43", %"bool_3_end"], [%".45", %"bool_6_right"]
  %".48" = xor i1 %".47", -1
  br i1 %".48", label %"bool_5_end", label %"bool_5_right"
bool_7_right:
  %".52" = load i1, i1* %".9"
  br label %"bool_7_end"
bool_7_end:
  %".54" = phi  i1 [%".50", %"bool_5_right"], [%".52", %"bool_7_right"]
  br label %"bool_5_end"
bool_8_right:
  %".66" = load i1, i1* %".7"
  br label %"bool_8_end"
bool_8_end:
  %".68" = phi  i1 [%".64", %"bool_5_end"], [%".66", %"bool_8_right"]
  store i1 %".68", i1* %".11"
  %".70" = load i1, i1* %".11"
  %".71" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".72" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".73" = select  i1 %".70", i8* %".71", i8* %".72"
  %".74" = call i32 (i8*, ...) @"printf"(i8* %".73")
  %".75" = load i1, i1* %".5"
  br i1 %".75", label %"bool_10_end", label %"bool_10_right"
bool_9_right:
  %".81" = load i1, i1* %".9"
  br label %"bool_9_end"
bool_9_end:
  %".83" = phi  i1 [%".79", %"bool_10_end"], [%".81", %"bool_9_right"]
  %".84" = xor i1 %".83", -1
  store i1 %".84", i1* %".11"
  %".86" = load i1, i1* %".11"
  %".87" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".88" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".89" = select  i1 %".86", i8* %".87", i8* %".88"
  %".90" = call i32 (i8*, ...) @"printf"(i8* %".89")
  ret i1 0
bool_10_right:
  %".77" = load i1, i1* %".7"
  br label %"bool_10_end"
bool_10_end:
  %".79" = phi  i1 [%".75", %"bool_8_end"], [%".77", %"bool_10_right"]
  br i1 %".79", label %"bool_9_right", label %"bool_9_end"
}

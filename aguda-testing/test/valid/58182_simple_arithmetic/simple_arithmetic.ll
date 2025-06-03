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
  %".5" = add i32 5, -3
  %".6" = alloca i32
  store i32 %".5", i32* %".6"
  %".8" = load i32, i32* %".6"
  %".9" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".9", i32 %".8")
  %".11" = load i32, i32* %".6"
  %".12" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12", i32 %".11")
  %".14" = sub i32 -10, 2
  %".15" = alloca i32
  store i32 %".14", i32* %".15"
  %".17" = load i32, i32* %".15"
  %".18" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".19" = call i32 (i8*, ...) @"printf"(i8* %".18", i32 %".17")
  %".20" = call i32 @"_power"(i32 5, i32 0)
  %".21" = mul i32 4, %".20"
  %".22" = alloca i32
  store i32 %".21", i32* %".22"
  %".24" = load i32, i32* %".22"
  %".25" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".26" = call i32 (i8*, ...) @"printf"(i8* %".25", i32 %".24")
  %".27" = sdiv i32 20, 3
  %".28" = alloca i32
  store i32 %".27", i32* %".28"
  %".30" = load i32, i32* %".28"
  %".31" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".32" = call i32 (i8*, ...) @"printf"(i8* %".31", i32 %".30")
  %".33" = srem i32 20, 4
  %".34" = alloca i32
  store i32 %".33", i32* %".34"
  %".36" = load i32, i32* %".34"
  %".37" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".38" = call i32 (i8*, ...) @"printf"(i8* %".37", i32 %".36")
  %".39" = sub i32 0, 2
  %".40" = call i32 @"_power"(i32 2, i32 %".39")
  %".41" = mul i32 8, %".40"
  %".42" = sdiv i32 %".41", 2
  %".43" = add i32 3, 1
  %".44" = call i32 @"_power"(i32 4, i32 %".43")
  %".45" = mul i32 3, %".44"
  %".46" = add i32 %".42", %".45"
  %".47" = alloca i32
  store i32 %".46", i32* %".47"
  %".49" = load i32, i32* %".47"
  %".50" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".51" = call i32 (i8*, ...) @"printf"(i8* %".50", i32 %".49")
  ret i1 0
}

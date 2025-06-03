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
define i1 @"modTest"(i32 %".1", i32 %".2")
{
entry:
  %".4" = alloca i32
  store i32 %".1", i32* %".4"
  %".6" = alloca i32
  store i32 %".2", i32* %".6"
  %".8" = load i32, i32* %".4"
  %".9" = load i32, i32* %".6"
  %".10" = srem i32 %".8", %".9"
  %".11" = icmp eq i32 %".10", 0
  ret i1 %".11"
}

define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = alloca i32
  store i32 253540, i32* %".5"
  %".7" = alloca i32
  store i32 27, i32* %".7"
  %".9" = alloca i32
  store i32 2025, i32* %".9"
  %".11" = alloca i32
  store i32 2077, i32* %".11"
  %".13" = alloca i32
  store i32 5, i32* %".13"
  %".15" = load i32, i32* %".5"
  %".16" = load i32, i32* %".13"
  %".17" = call i1 @"modTest"(i32 %".15", i32 %".16")
  %".18" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".19" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".20" = select  i1 %".17", i8* %".18", i8* %".19"
  %".21" = call i32 (i8*, ...) @"printf"(i8* %".20")
  %".22" = load i32, i32* %".7"
  %".23" = load i32, i32* %".13"
  %".24" = call i1 @"modTest"(i32 %".22", i32 %".23")
  %".25" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".26" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".27" = select  i1 %".24", i8* %".25", i8* %".26"
  %".28" = call i32 (i8*, ...) @"printf"(i8* %".27")
  %".29" = load i32, i32* %".9"
  %".30" = load i32, i32* %".13"
  %".31" = call i1 @"modTest"(i32 %".29", i32 %".30")
  %".32" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".33" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".34" = select  i1 %".31", i8* %".32", i8* %".33"
  %".35" = call i32 (i8*, ...) @"printf"(i8* %".34")
  %".36" = load i32, i32* %".11"
  %".37" = load i32, i32* %".13"
  %".38" = call i1 @"modTest"(i32 %".36", i32 %".37")
  %".39" = getelementptr [5 x i8], [5 x i8]* @"true_str", i32 0, i32 0
  %".40" = getelementptr [6 x i8], [6 x i8]* @"false_str", i32 0, i32 0
  %".41" = select  i1 %".38", i8* %".39", i8* %".40"
  %".42" = call i32 (i8*, ...) @"printf"(i8* %".41")
  ret i1 0
}

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
define i32 @"categorizeNumber"(i32 %".1")
{
entry:
  %".3" = alloca i32
  store i32 %".1", i32* %".3"
  %".5" = alloca i32
  store i32 0, i32* %".5"
  %".7" = load i32, i32* %".3"
  %".8" = srem i32 %".7", 2
  %".9" = icmp eq i32 %".8", 0
  %".10" = alloca i1
  store i1 %".9", i1* %".10"
  %".12" = load i32, i32* %".3"
  %".13" = icmp sgt i32 %".12", 0
  %".14" = alloca i1
  store i1 %".13", i1* %".14"
  %".16" = load i32, i32* %".3"
  %".17" = icmp sgt i32 %".16", 100
  %".18" = alloca i1
  store i1 %".17", i1* %".18"
  %".20" = load i1, i1* %".10"
  br i1 %".20", label %"cond_1_then", label %"cond_1_else"
cond_1_then:
  %".22" = load i1, i1* %".14"
  br i1 %".22", label %"cond_2_then", label %"cond_2_else"
cond_1_else:
  %".43" = load i1, i1* %".14"
  br i1 %".43", label %"cond_5_then", label %"cond_5_else"
cond_1_end:
  %".50" = phi  i1 [%".41", %"cond_2_end"], [%".48", %"cond_5_end"]
  %".51" = load i32, i32* %".3"
  %".52" = srem i32 %".51", 5
  %".53" = icmp eq i32 %".52", 0
  br i1 %".53", label %"cond_6_then", label %"cond_6_else"
cond_2_then:
  %".24" = load i1, i1* %".18"
  br i1 %".24", label %"cond_3_then", label %"cond_3_else"
cond_2_else:
  %".32" = load i32, i32* %".3"
  %".33" = icmp eq i32 %".32", 0
  br i1 %".33", label %"cond_4_then", label %"cond_4_else"
cond_2_end:
  %".41" = phi  i1 [%".30", %"cond_3_end"], [%".39", %"cond_4_end"]
  br label %"cond_1_end"
cond_3_then:
  store i32 1, i32* %".5"
  br label %"cond_3_end"
cond_3_else:
  store i32 2, i32* %".5"
  br label %"cond_3_end"
cond_3_end:
  %".30" = phi  i1 [0, %"cond_3_then"], [0, %"cond_3_else"]
  br label %"cond_2_end"
cond_4_then:
  store i32 5, i32* %".5"
  br label %"cond_4_end"
cond_4_else:
  store i32 3, i32* %".5"
  br label %"cond_4_end"
cond_4_end:
  %".39" = phi  i1 [0, %"cond_4_then"], [0, %"cond_4_else"]
  br label %"cond_2_end"
cond_5_then:
  store i32 4, i32* %".5"
  br label %"cond_5_end"
cond_5_else:
  br label %"cond_5_end"
cond_5_end:
  %".48" = phi  i1 [0, %"cond_5_then"], [0, %"cond_5_else"]
  br label %"cond_1_end"
cond_6_then:
  store i32 6, i32* %".5"
  br label %"cond_6_end"
cond_6_else:
  store i32 7, i32* %".5"
  br label %"cond_6_end"
cond_6_end:
  %".59" = phi  i1 [0, %"cond_6_then"], [0, %"cond_6_else"]
  %".60" = load i32, i32* %".3"
  %".61" = icmp slt i32 %".60", -50
  br i1 %".61", label %"cond_7_then", label %"cond_7_else"
cond_7_then:
  store i32 8, i32* %".5"
  br label %"cond_7_end"
cond_7_else:
  br label %"cond_7_end"
cond_7_end:
  %".66" = phi  i1 [0, %"cond_7_then"], [0, %"cond_7_else"]
  %".67" = load i32, i32* %".5"
  ret i32 %".67"
}

define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = call i32 @"categorizeNumber"(i32 150)
  %".6" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6", i32 %".5")
  %".8" = call i32 @"categorizeNumber"(i32 24)
  %".9" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".9", i32 %".8")
  %".11" = call i32 @"categorizeNumber"(i32 0)
  %".12" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12", i32 %".11")
  %".14" = call i32 @"categorizeNumber"(i32 -12)
  %".15" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".15", i32 %".14")
  %".17" = call i32 @"categorizeNumber"(i32 15)
  %".18" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".19" = call i32 (i8*, ...) @"printf"(i8* %".18", i32 %".17")
  %".20" = call i32 @"categorizeNumber"(i32 7)
  %".21" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".22" = call i32 (i8*, ...) @"printf"(i8* %".21", i32 %".20")
  %".23" = call i32 @"categorizeNumber"(i32 -3)
  %".24" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".25" = call i32 (i8*, ...) @"printf"(i8* %".24", i32 %".23")
  %".26" = call i32 @"categorizeNumber"(i32 -75)
  %".27" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".28" = call i32 (i8*, ...) @"printf"(i8* %".27", i32 %".26")
  ret i1 0
}

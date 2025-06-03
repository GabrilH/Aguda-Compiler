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
define i1 @"helloWorld"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = alloca i32
  store i32 10, i32* %".5"
  br label %"while_1_cond"
while_1_cond:
  %".8" = load i32, i32* %".5"
  %".9" = icmp sge i32 %".8", 0
  br i1 %".9", label %"while_1_body", label %"while_1_end"
while_1_body:
  %".11" = load i32, i32* %".5"
  %".12" = icmp eq i32 %".11", 0
  br i1 %".12", label %"cond_2_then", label %"cond_2_else"
while_1_end:
  ret i1 0
cond_2_then:
  %".14" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".15" = call i32 (i8*, ...) @"printf"(i8* %".14", i32 55)
  br label %"cond_2_end"
cond_2_else:
  %".17" = load i32, i32* %".5"
  %".18" = icmp eq i32 %".17", 1
  br i1 %".18", label %"cond_3_then", label %"cond_3_else"
cond_2_end:
  %".28" = phi  i1 [0, %"cond_2_then"], [%".26", %"cond_3_end"]
  %".29" = load i32, i32* %".5"
  %".30" = sub i32 %".29", 1
  store i32 %".30", i32* %".5"
  br label %"while_1_cond"
cond_3_then:
  %".20" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".21" = call i32 (i8*, ...) @"printf"(i8* %".20", i32 77)
  br label %"cond_3_end"
cond_3_else:
  %".23" = getelementptr [3 x i8], [3 x i8]* @"int_format", i32 0, i32 0
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".23", i32 99)
  br label %"cond_3_end"
cond_3_end:
  %".26" = phi  i1 [0, %"cond_3_then"], [0, %"cond_3_else"]
  br label %"cond_2_end"
}

define i1 @"main"(i1 %".1")
{
entry:
  %".3" = alloca i1
  store i1 %".1", i1* %".3"
  %".5" = call i1 @"helloWorld"(i1 0)
  ret i1 %".5"
}

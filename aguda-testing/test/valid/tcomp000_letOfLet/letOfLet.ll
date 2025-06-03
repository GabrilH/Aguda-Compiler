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
  store i32 5, i32* %".5"
  %".7" = alloca i1
  store i1 0, i1* %".7"
  %".9" = alloca i1
  store i1 0, i1* %".9"
  %".11" = alloca i1
  store i1 0, i1* %".11"
  %".13" = alloca i1
  store i1 0, i1* %".13"
  %".15" = alloca i1
  store i1 0, i1* %".15"
  %".17" = alloca i1
  store i1 0, i1* %".17"
  %".19" = alloca i1
  store i1 0, i1* %".19"
  %".21" = alloca i1
  store i1 0, i1* %".21"
  %".23" = alloca i1
  store i1 0, i1* %".23"
  %".25" = alloca i1
  store i1 0, i1* %".25"
  %".27" = alloca i1
  store i1 0, i1* %".27"
  %".29" = alloca i1
  store i1 0, i1* %".29"
  %".31" = alloca i1
  store i1 0, i1* %".31"
  %".33" = alloca i1
  store i1 0, i1* %".33"
  %".35" = alloca i1
  store i1 0, i1* %".35"
  %".37" = alloca i1
  store i1 0, i1* %".37"
  %".39" = alloca i1
  store i1 0, i1* %".39"
  %".41" = alloca i1
  store i1 0, i1* %".41"
  %".43" = alloca i1
  store i1 0, i1* %".43"
  %".45" = alloca i1
  store i1 0, i1* %".45"
  %".47" = alloca i1
  store i1 0, i1* %".47"
  %".49" = alloca i1
  store i1 0, i1* %".49"
  %".51" = alloca i1
  store i1 0, i1* %".51"
  %".53" = alloca i1
  store i1 0, i1* %".53"
  %".55" = alloca i1
  store i1 0, i1* %".55"
  %".57" = alloca i1
  store i1 0, i1* %".57"
  %".59" = alloca i1
  store i1 0, i1* %".59"
  %".61" = alloca i1
  store i1 0, i1* %".61"
  %".63" = alloca i1
  store i1 0, i1* %".63"
  %".65" = alloca i1
  store i1 0, i1* %".65"
  %".67" = alloca i1
  store i1 0, i1* %".67"
  %".69" = alloca i1
  store i1 0, i1* %".69"
  %".71" = alloca i1
  store i1 0, i1* %".71"
  %".73" = alloca i1
  store i1 0, i1* %".73"
  %".75" = alloca i1
  store i1 0, i1* %".75"
  %".77" = alloca i1
  store i1 0, i1* %".77"
  %".79" = alloca i1
  store i1 0, i1* %".79"
  %".81" = alloca i1
  store i1 0, i1* %".81"
  %".83" = alloca i1
  store i1 0, i1* %".83"
  %".85" = alloca i1
  store i1 0, i1* %".85"
  %".87" = alloca i1
  store i1 0, i1* %".87"
  %".89" = alloca i1
  store i1 0, i1* %".89"
  %".91" = alloca i1
  store i1 0, i1* %".91"
  %".93" = alloca i1
  store i1 0, i1* %".93"
  %".95" = alloca i1
  store i1 0, i1* %".95"
  %".97" = alloca i1
  store i1 0, i1* %".97"
  %".99" = alloca i1
  store i1 0, i1* %".99"
  %".101" = alloca i1
  store i1 0, i1* %".101"
  %".103" = alloca i1
  store i1 0, i1* %".103"
  %".105" = alloca i1
  store i1 0, i1* %".105"
  %".107" = alloca i1
  store i1 0, i1* %".107"
  %".109" = alloca i1
  store i1 0, i1* %".109"
  %".111" = alloca i1
  store i1 0, i1* %".111"
  %".113" = alloca i1
  store i1 0, i1* %".113"
  %".115" = alloca i1
  store i1 0, i1* %".115"
  %".117" = alloca i1
  store i1 0, i1* %".117"
  %".119" = alloca i1
  store i1 0, i1* %".119"
  %".121" = alloca i1
  store i1 0, i1* %".121"
  %".123" = alloca i1
  store i1 0, i1* %".123"
  %".125" = alloca i1
  store i1 0, i1* %".125"
  %".127" = alloca i1
  store i1 0, i1* %".127"
  %".129" = alloca i1
  store i1 0, i1* %".129"
  %".131" = alloca i1
  store i1 0, i1* %".131"
  %".133" = alloca i1
  store i1 0, i1* %".133"
  %".135" = alloca i1
  store i1 0, i1* %".135"
  %".137" = alloca i1
  store i1 0, i1* %".137"
  %".139" = alloca i1
  store i1 0, i1* %".139"
  %".141" = load i1, i1* %".139"
  %".142" = getelementptr [5 x i8], [5 x i8]* @"unit_str", i32 0, i32 0
  %".143" = call i32 (i8*, ...) @"printf"(i8* %".142")
  ret i1 0
}

; ModuleID = '<string>'

target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@min = internal unnamed_addr global i32 undef
@min2 = internal unnamed_addr global i32 undef
@fstr0 = internal constant [5 x i8] c"%i \0A\00"
@fstr1 = internal constant [5 x i8] c"%i \0A\00"
@fstr2 = internal constant [5 x i8] c"%i \0A\00"
@fstr3 = internal constant [5 x i8] c"%i \0A\00"
@fstr4 = internal constant [5 x i8] c"%i \0A\00"
@fstr5 = internal constant [5 x i8] c"%i \0A\00"

; Function Attrs: nounwind
define void @main()  {
entry:
  %.9 = tail call i32 @function(i32 2, i32 100)
  %.23 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr1, i64 0, i64 0), i32 3)
  %.35 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr2, i64 0, i64 0), i32 5)
  %.47 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr3, i64 0, i64 0), i32 7)
  %.59 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr4, i64 0, i64 0), i32 9)
  %.71 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr5, i64 0, i64 0), i32 11)
  ret void
}

; Function Attrs: nounwind
declare i32 @printf(i8* nocapture readonly, ...) 

; Function Attrs: nounwind
define i32 @function(i32 %.1, i32 %.2)  {
entry:
  %.12 = icmp sgt i32 %.1, %.2
  br i1 %.12, label %entry.if, label %entry.else

entry.if:                                         ; preds = %entry
  store i32 %.2, i32* @min, align 4
  %.21.pre = load i32, i32* @min2, align 4
  br label %entry.endif

entry.else:                                       ; preds = %entry
  store i32 %.1, i32* @min2, align 4
  br label %entry.endif

entry.endif:                                      ; preds = %entry.else, %entry.if
  %.21 = phi i32 [ %.1, %entry.else ], [ %.21.pre, %entry.if ]
  %.23 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr0, i64 0, i64 0), i32 %.21)
  %.24 = load i32, i32* @min, align 4
  ret i32 %.24
}

; Function Attrs: nounwind
declare void @llvm.stackprotector(i8*, i8**) #0

attributes #0 = { nounwind }

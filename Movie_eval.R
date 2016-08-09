
setwd('/Users/bagjunseong/Documents/Study/BigDataProgramming/Project')
#오픈한글과 KOSAC의 데이터들을 서로 비교해보려했으나 오픈한글의 데이터가 너무 적어 실패
OpenHangle <- read.csv('OpenHangle.txt', encoding = "UTF-8", sep="|", header=TRUE, stringsAsFactors = FALSE)
OpenHangle$pos <- OpenHangle$pos/100
OpenHangle$neg <- OpenHangle$neg/100
with(OpenHangle, plot(neg, rate, cex=1, pch=4, main="OpenHangle"))
OH_result <- lm(OpenHangle$rate ~ OpenHangle$pos + OpenHangle$neg, data = df)
OH_result
summary(OH_result)
plot()
KOSAC <- read.csv('KOSAC.txt', encoding = "UTF-8", sep="|", header=TRUE, stringsAsFactors = FALSE)
KOSAC_result <- lm(KOSAC$rate ~ KOSAC$pos + KOSAC$neg, data = df)
KOSAC_result
summary(KOSAC_result)


#데이터 로드
KOSAC_BIG <- read.csv('KOSAC_BIG.txt', encoding = "UTF-8", sep="|", header=TRUE, stringsAsFactors = FALSE)
Total <- subset(KOSAC_BIG, KOSAC_BIG$pos > 0 || KOSAC_BIG$neg > 0)
m <- lm(Total$rate ~ Total$pos + Total$neg + Total$title, Total = data)
summary(m)
#긍정 부정 수치가 모두 0인 데이터는 제외
#인기있는 영화 Top 5만 분석한다.
#곡성
Wailing <- subset(KOSAC_BIG, (KOSAC_BIG$pos > 0 || KOSAC_BIG$neg > 0) & KOSAC_BIG$title == "곡성(哭聲)")
Wailing$rate <- Wailing$rate/10
View(Wailing)
with(Wailing[1:1000,],
     {plot(NULL, main="Wailing", xlim=c(0.0, 1.0), ylim=c(0.2, 1.0), xlab="Sentiment", ylab="Rate", type="n")
      points(jitter(pos), jitter(rate), cex=0.5, pch=20)
      points(jitter(neg), jitter(rate), cex=0.5, pch="+", col="#FF0000")})
legend("topright", legend=c("Positive", "Negative"), pch=c(20, 43), cex=.8, col=c("black", "red"), bg="gray")
Wailing_m <- lm(Wailing$rate ~ Wailing$pos + Wailing$neg, Wailing = data)
summary(Wailing_m)
confint(Wailing_m)
coef(Wailing_m)
abline(0.76322413, 0.5589246, lty=1)
abline(0.76322413, -0.4377446, lty=2, col="red")
#엑스맨
X_Man <- subset(KOSAC_BIG, (KOSAC_BIG$pos > 0 || KOSAC_BIG$neg > 0) & KOSAC_BIG$title == "엑스맨: 아포칼립스")
X_Man$rate <- X_Man$rate/10
View(X_Man)
with(X_Man[1:1000,],
     {plot(NULL, main="X-Man", xlim=c(0.0, 1.0), ylim=c(0.2, 1.0), xlab="Sentiment", ylab="Rate", type="n")
      points(jitter(pos), jitter(rate), cex=0.5, pch=20)
      points(jitter(neg), jitter(rate), cex=0.5, pch="+", col="#FF0000")})
legend("topright", legend=c("Positive", "Negative"), pch=c(20, 43), cex=.8, col=c("black", "red"), bg="gray")
X_Man_m <- lm(X_Man$rate ~ X_Man$pos + X_Man$neg, X_Man = data)
summary(X_Man_m)
confint(X_Man_m)
coef(X_Man_m)
abline(0.85623770, 0.02144758, lty=1)
abline(0.85623770, -0.07737057, lty=2, col="red")
#아가씨
Handmaiden <- subset(KOSAC_BIG, (KOSAC_BIG$pos > 0 || KOSAC_BIG$neg > 0) & KOSAC_BIG$title == "아가씨")
Handmaiden$rate <- Handmaiden$rate/10
View(Handmaiden)
with(Handmaiden[1:1000,],
     {plot(NULL, main="Handmaiden", xlim=c(0.0, 1.0), ylim=c(0.2, 1.0), xlab="Sentiment", ylab="Rate", type="n")
       points(jitter(pos), jitter(rate), cex=0.5, pch=20)
       points(jitter(neg), jitter(rate), cex=0.5, pch="+", col="#FF0000")})
legend("topright", legend=c("Positive", "Negative"), pch=c(20, 43), cex=.8, col=c("black", "red"), bg="gray")

Handmaiden_m <- lm(Handmaiden$rate ~ Handmaiden$pos + Handmaiden$neg, Handmaiden = data)
summary(Handmaiden_m)
confint(Handmaiden_m)
coef(Handmaiden_m)
abline(0.7332749, 0.1180172, lty=1)
abline(0.7332749, -0.1363458, lty=2, col="red")
#컨저링 2
Conjuring2 <- subset(KOSAC_BIG, (KOSAC_BIG$pos > 0 || KOSAC_BIG$neg > 0) & KOSAC_BIG$title == "컨저링 2")
Conjuring2$rate <- Conjuring2$rate/10
View(Conjuring2)
with(Conjuring2[1:1000,],
     {plot(NULL, main="Conjuring2", xlim=c(0.0, 1.0), ylim=c(0.2, 1.0), xlab="Sentiment", ylab="Rate", type="n")
      points(jitter(pos), jitter(rate), cex=0.5, pch=20)
      points(jitter(neg), jitter(rate), cex=0.5, pch="+", col="#FF0000")})
legend("topright", legend=c("Positive", "Negative"), pch=c(20, 43), cex=.8, col=c("black", "red"), bg="gray")
Conjuring2_m <- lm(Conjuring2$rate ~ Conjuring2$pos + Conjuring2$neg, Conjuring2 = data)
summary(Conjuring2_m)
confint(Conjuring2_m)
coef(Conjuring2_m)
abline(0.834636844, 0.047573159, lty=1)
abline(0.834636844, -0.009178332, lty=2, col="red")
#앵그리버드
AngryBird <- subset(KOSAC_BIG, (KOSAC_BIG$pos > 0 || KOSAC_BIG$neg > 0) & KOSAC_BIG$title == "앵그리버드 더 무비")
AngryBird$rate <- AngryBird$rate/10
View(AngryBird)
with(AngryBird[1:1000,],
     {plot(NULL, main="AngryBird", xlim=c(0.0, 1.0), ylim=c(0.2, 1.0), xlab="Sentiment", ylab="Rate", type="n")
      points(jitter(pos), jitter(rate), cex=0.5, pch=20)
      points(jitter(neg), jitter(rate), cex=0.5, pch="+", col="#FF0000")})
legend("topright", legend=c("Positive", "Negative"), pch=c(20, 43), cex=.8, col=c("black", "red"), bg="gray")
AngryBird_m <- lm(AngryBird$rate ~ AngryBird$pos + AngryBird$neg, AngryBird = data)
summary(AngryBird_m)
confint(AngryBird_m)
coef(AngryBird_m)
abline(0.76962021, 0.11161980, lty=1)
abline(0.76962021, 0.01227597, lty=2, col="red")

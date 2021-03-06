rm(list = ls())
#install packages and library
library(readxl)
library(xlsx)
setwd("E:/Hema/Apriori")
library(ROCR)
#install.packages("dplyr")
library(dplyr)
library(caTools)

#load data and select columns
Final1 <- read_excel("logistic.xlsx", sheet = "Sheet2")
prev = Final1[c(1,20)]
View(prev)

#split training and test data
set.seed(14330)
samp<-sample.split(Final1$Acceptance,SplitRatio = 0.70)
train_data<-subset(Final1, samp== TRUE)
test_data<-subset(Final1,samp == FALSE)

#logistic regression
train_data = train_data[-c(1,19)]
Acceptance = glm(Acceptance ~ .,data = train_data, family = binomial)
summary(Acceptance)

#select columns with significant co-relation
colnames(train_data)
train_data = train_data[c(5,10,15,18)]

#build model
Acceptance = glm(Acceptance ~ .,data = train_data, family = binomial)
summary(Acceptance)

#predict based on test data
c1=test_data[c(1)]
test_data = test_data[-c(1,19)]
fitted.results <- predict(Acceptance,newdata=test_data,type='response')
fitted.results <- ifelse(fitted.results > 0.5,1,0)
Modpred <- data.frame(x1=c1,Accept=fitted.results)
View(Modpred)

#accuracy
y_pred <- factor(fitted.results, levels=c(0, 1))
y_act <- test_data$Acceptance
mean(y_pred == y_act) 

#roc curve and area under curve (tpr=true positive rate, fpr= false positive rate)
predict <- predict(Acceptance,test_data, type="response")
table(test_data$Acceptance, predict>0.5)
prediction <- prediction(predict, test_data$Acceptance)
performance <- performance(prediction, measure = "tpr", x.measure = "fpr")
plot(performance)
auc <- performance(prediction, measure = "auc")
auc <- auc@y.values[[1]]
auc

#install.packages("formattable")
library(readxl)
library(xlsx)
library(stringr)
library(splitstackshape)
library(dplyr)
library(formattable)

setwd("C:/Users/Hema.priya/Desktop/Data Manipulation/Latest File")
Final <- read_excel("Final_Latest.xlsx", sheet = "Final")
Final1 = Final[!grepl("hr",Final$bid),]
Final1 = Final1[!grepl("min",Final1$bid),]
Final1 = cSplit(Final1,'bid',sep = "-",type.convert = FALSE)
Final1 = cSplit(Final1,'bid_1',sep = "(",type.convert = FALSE)
Final1 = cSplit(Final1,'bid_1_1',sep = "$",type.convert = FALSE)
#colnames(Final)
options(scipen=999)
Final1 = Final1[,-c("bid_2","bid_1_2","bid_1_1_1")]
Final1$bid_1_1_2 = as.numeric(Final1$bid_1_1_2)
names(Final1)[11] = "Bid Value"
#Final1$`Bid Value`= currency(Final1$`Bid Value`,digits = 0L)
Final1 = subset(Final1,select = -c(description,daysleft,verified,state))
Final1 = Final1[!(Final1$`Bid Value`>= 100000),] 
Final1 = Final1[!(Final1$skillset == "NA"),] 

#Choose the Text File  Installing Packages :
#Installing Packages

install.packages("tm")
install.packages("wordcloud")
install.packages ("RColorBrewer")

#Loading Packages

library(tm)
library(wordcloud)
library(RColorBrewer)

#3.Reading the File

#speech = "E:\\Hema\\Apriori\\skillset"
setwd("E:/Hema/Apriori")
skill ="skillclouddata.txt"

skill_txt = readLines(skill)

#4.Converting the text file into a Corpus

skill<-Corpus(VectorSource(skill_txt))
inspect(skill)[1:10]

#5.Data Cleaning
skill_data<-tm_map(skill,stripWhitespace)
skill_data<-tm_map(skill_data,tolower)
skill_data<-tm_map(skill_data,removeNumbers)
skill_data<-tm_map(skill_data,removePunctuation)
skill_data<-tm_map(skill_data,removeWords, stopwords("english"))
skill_data<-tm_map(skill_data,removeWords,c("and","the","our","that","for","are","also","more","has","must","have","should","this","with"))

#6.Create a Term Document Matrix
tdm_skill<-TermDocumentMatrix (skill_data) #Creates a TDM
TDM1<-as.matrix(tdm_skill) #Convert this into a matrix format
v = sort(rowSums(TDM1), decreasing = TRUE) #Gives you the frequencies for every word
Summary(v)

#7.Creation of word cloud!
wordcloud (skill_data, scale=c(5,0.5), max.words=50, random.order=FALSE, rot.per=0.35, use.r.layout=FALSE, colors=brewer.pal(8, "Dark2"))

#8.Exporting as png.
png("MachineLearningCloud.png", width=12, height=8, units="in", res=300)
wordcloud(dm$word, dm$freq, random.order=FALSE, colors=brewer.pal(8, "Dark2"))
dev.off()


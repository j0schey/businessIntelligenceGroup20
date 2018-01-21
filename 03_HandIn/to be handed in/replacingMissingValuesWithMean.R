install.packages('farff')
library('farff')

## set working directory where missing value-datasets are located
setwd("/businessIntelligenceGroup20/03_HandIn/script output data sets")
getwd()

##! Define the position of the attribute with missing values:
selectedAttributePos <- 189
selectedAttribute <- paste('V',selectedAttributePos,sep='')

##! Define the filename of the dataset containing missing values:
READ_FILE_NAME <- "output_smallMValuesOnLowInfoGain"
READ_FILE_NAME_ARFF <- paste(READ_FILE_NAME,'.arff',sep='')



df <- readARFF(READ_FILE_NAME_ARFF)
colnames(df)[selectedAttributePos] <- 'selectedAttribute'
df_meansPerClass <- aggregate(df$selectedAttribute ~ df$Class, FUN = mean)


colnames(df_meansPerClass)[1] <- "Class"
colnames(df_meansPerClass)[2] <- 'selectedAttribute'

for (i in 1:nrow(df)) {
  if(is.na(df[i, ]$selectedAttribute)) {
    df[i, ]$selectedAttribute <- df_meansPerClass[which(df_meansPerClass$Class == df[i, ]$Class), ]$selectedAttribute
  }
}

colnames(df)[selectedAttributePos] <- selectedAttribute
WRITE_FILE_NAME_ARFF <- paste(READ_FILE_NAME,'_meanValueClass.arff',sep='')

writeARFF(df, WRITE_FILE_NAME_ARFF, relation = 'R_data_frame')


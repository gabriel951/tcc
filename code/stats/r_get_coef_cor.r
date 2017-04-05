# r program to get the coefficient of correlation
library(raster)

FILE_NAME <- "stats.txt"
data <- read.table(FILE_NAME)
names(data) <- c("atr", "way_out")
coef_cor <- cv(data$atr)
cat("coefficient of correlation: ", coef_cor)
cat("\n")

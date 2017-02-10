# r program to draw a pie chart in the screen
library (ggplot2)
library(scales)
library (png)

cat("entered r program to plot stats\n")

# get command line arguments
args <- commandArgs(trailingOnly = TRUE)

# get data and name the column
data <- read.table("temp.txt", sep = ",")
names(data) <- c("valores")

# my plot
my_plot <-  ggplot(data, aes(x = valores)) + 
            geom_histogram(aes(y = (..count..) / sum(..count..)), 
                               binwidth = 0.05, fill = "darkblue") + 
            scale_y_continuous(labels = percent) + 
            ylab("quantidade") + 
            theme_bw()

# save graph
ggsave(filename="temp.png", my_plot)

cat("leaving r program that plot stats\n")

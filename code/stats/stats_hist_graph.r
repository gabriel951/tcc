# r program to draw a histogram chart in the screen
library (ggplot2)
library(scales)
library (png)

cat("entered r program to plot histogram\n")

# get command line arguments
args <- commandArgs(trailingOnly = TRUE)
bin_size <- as.numeric(args)
print("bin size: ")
print(bin_size)

# get data and name the column
data <- read.table("temp.txt", sep = ",")
names(data) <- c("values")

# my plot
my_plot <-  ggplot(data, aes(x = values)) + 
            geom_histogram(aes(y = (..count..) / sum(..count..)), 
                               binwidth = bin_size, fill = "darkblue") + 
            #geom_histogram(binwidth = bin_size) + 
            scale_y_continuous(labels = percent) + 
            ylab("quantidade") + 
            theme_bw()

# save graph
ggsave(filename="temp.png", my_plot)

cat("leaving r program that plot stats\n")

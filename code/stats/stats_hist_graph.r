# r program to draw a histogram chart in the screen
library (ggplot2)
library(scales)
library (png)

cat("entered r program to plot histogram\n")

# get command line arguments
args <- commandArgs(trailingOnly = TRUE)
bin_size <- as.numeric(args[1])
print("bin size: ")
print(bin_size)

# get data and name the column
FILE_NAME <- "stats.txt"
data <- read.table(FILE_NAME)
names(data) <- c("values", "way_out")

# get if we should separate by the way out or not
# 0 if we should NOT split
to_split <- 0

# my plot
if (to_split == 0) 
{
    print("will not split value according to the way out")
    my_plot <-  ggplot(data, aes(x = values)) + 
                geom_histogram(aes(y = (..count..) / sum(..count..)), 
                                   binwidth = bin_size, fill = "darkblue") + 
                #geom_histogram(binwidth = bin_size) + 
                scale_y_continuous(labels = percent) + 
                ylab("quantidade") + 
                xlab("valores") +
                theme_bw()
} else
{
    print("will split value according to the way out")
    my_plot <-  ggplot(data, aes(x = values)) + 
                geom_histogram(aes(y = (..count..) / sum(..count..)), 
                                   binwidth = bin_size, fill = way_out) + 
                #geom_histogram(binwidth = bin_size) + 
                scale_y_continuous(labels = percent) + 
                ylab("quantidade") + 
                theme_bw()
}

# save graph
ggsave(filename="temp.png", my_plot)

cat("leaving r program that plot stats\n")

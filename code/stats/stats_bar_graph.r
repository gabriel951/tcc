# r program to draw a pie chart in the screen
library (ggplot2)
library (png)

cat("entered r program to plot bar graph\n")

# get command line arguments
args <- commandArgs(trailingOnly = TRUE)

# get data and name the column
FILE_NAME <- "stats.txt"
data <- read.table(FILE_NAME)
names(data) <- c("values", "forma_de_saida")

# get if we should separate by the way out or not
# 0 if we should NOT separate
to_split <- 0

# my plot
if (to_split == 0) {
    print("will not split value according to the way out")
    my_plot <-  ggplot(data, aes(values)) + 
                geom_bar(fill = "darkblue") + 
                ylab("quantidade") + 
                theme_bw()
} else {
    print("will split value according to the way out")
    my_plot <-  ggplot(data, aes(values, fill = forma_de_saida)) + 
                geom_bar() + 
                ylab("quantidade") + 
                theme_bw()
}

# save graph
ggsave(filename="temp.png", my_plot)

cat("leaving r program that plot stats\n")

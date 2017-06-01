# r program to plot the performance graphs for the ml models
library (ggplot2)
library(scales)
library (png)

cat("entered r program to plot ml models graph\n")

# get data and name the column
FILE_NAME <- "ml_graph.txt"
data <- read.table(FILE_NAME)
names(data) <- c("data_desc", "sem", "model_name", "f_measure")

# plot 
my_plot <- ggplot(data, aes(x = sem, y = f_measure, color = model_name)) + 
            geom_point() + 
            theme_bw()

# save graph
ggsave(filename="temp.png", my_plot)

cat("leaving r program to plot ml models graph\n")

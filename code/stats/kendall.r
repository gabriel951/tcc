# r program to calculate the kendall tau relation between variables 
# a HUGE thanks to r-tutor: 
#http://www.r-tutor.com/gpu-computing/correlation/kendall-rank-coefficient
print("entered r program that will perform the kendall test")

# get command line arguments
args <- commandArgs(trailingOnly = TRUE)
print("will open file")
print(args)

# get data
print("trying to read")
data <- read.table(args[1], sep = ",", fill = TRUE)
names(data) <- c("reg", "sex", "age", "quota", "school_type", "course", "local", 
                 "way_in", "way_out")

print("able to read table")

# get info 
sex <- as.numeric(factor(data$sex))
age <- as.numeric(factor(data$age))
quota <- as.numeric(factor(data$quota))
school_type <- as.numeric(factor(data$school_type))
print("obtained info")

# bind the info together
my_matrix <- cbind(sex, age, quota, school_type)
cor(my_matrix, method="kendall", use="pairwise")

print("left r program that performs kendall test")

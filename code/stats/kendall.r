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
                 "way_in", "fail_rate", "pass_rate", "drop_rate", "ira", 
                 "improvement_rate", "credit_rate_acc", "hard_rate", "in_condition", 
                 "position", "way_out")

print("able to read table")

# get info 
sex <- as.numeric(factor(data$sex))
age <- as.numeric(factor(data$age))
quota <- as.numeric(factor(data$quota))
school_type <- as.numeric(factor(data$school_type))
course <- as.numeric(factor(data$course))
local <- as.numeric(factor(data$local))
way_in <- as.numeric(factor(data$way_in))
fail_rate <- as.numeric(factor(data$fail_rate))
pass_rate <- as.numeric(factor(data$pass_rate))
drop_rate <- as.numeric(factor(data$drop_rate))
ira <- as.numeric(factor(data$ira))
improvement_rate <- as.numeric(factor(data$improvement_rate))
credit_rate_acc <- as.numeric(factor(data$credit_rate_acc))
hard_rate <- as.numeric(factor(data$hard_rate))
in_condition <- as.numeric(factor(data$in_condition))
position <- as.numeric(factor(data$position))
way_out <- as.numeric(factor(data$way_out))

print("obtained info")

# bind the info together
my_matrix <- cbind(sex, age, quota, school_type, course, local, way_in, 
                   fail_rate, pass_rate, drop_rate, ira, improvement_rate, 
                   credit_rate_acc, hard_rate, in_condition, position, way_out)

cor(my_matrix, method="kendall", use="pairwise")

print("left r program that performs kendall test")

# courses file, contain information relative of what are the mandatory disciplines of
# the courses

class Course():

def register_courses():

def load_course(course_name, year, sem):
    """
    receives a course name, a year and a semester
    loads all the courses and then find the required course
    returns the required course 
    """
    courses = load_all_courses()
    for course in courses:
        if course.name == course_name and course.valid(year, sem):
            return course
    exit('could not load course %s for the year %d and semester %d' % (course_name,
        year, semester))

def is_mand_sub(code_sub, course, stu_year, stu_sem):
    """
    receives the code for a given subject, the course of a student and the year and
    semester the student entered the course
    returns true case the given subject is mandatory, false otherwise
    """
    # load correct course 
    course = load_course(course, stu_year, stu_sem)

    # query course to see if the subject is mandatory and return
    return course.is_mandatory(code_sub)

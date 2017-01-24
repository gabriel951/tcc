# courses file, contain information relative of what are the mandatory disciplines of
# the courses

from basic import *
import pickle

# path for serialized objects
PATH = 'data/'

# name for the course pickle object
NAME_COURSE_PCK = 'course_info'

# TODO: fill the way out student power point
# TODO: handle grades such as AP and DP

class Course():
    """
    class that represent the curriculum of a course
    warning: different curriculums of the same course correspond to different objects
    """
    def __init__(self, name, year_start, sem_start, year_end, sem_end):
        """
        receives the name of the course and the time the current curriculum is valid
        if the course has no year_end or no semester_end then the values passed
        should be infinite
        """
        path = 'curriculum/'

        # instantiate
        self.name = name
        self.year_start = year_start
        self.sem_start = sem_start
        self.year_end = year_end
        self.sem_end = sem_end 
        
        # dictionary of mandatory subjects
        self.mand_sub = {}
        
        # add disciplines to the course
        self.add_subjects(path + name + '_' + str(year_start) + '_' + \
                str(sem_start) + '.txt')
        
        print('added course %s that started on year %d and semester %d' % \
                (self.name, self.year_start, self.sem_start))

    def add_subjects(self, file_name):
        """
        receives a file name containing the code for the mandatory subjects of a
        given course
        add this subjects to the course object
        returns nothing
        """
        # open file for reading
        with open(file_name, 'r') as fp:
            for line in fp:
                # there may be empty lines, i watch for those with my try-except
                try: 
                    # add code of the subject as key and as value in the dictionary
                    # that's because this is the only info we need for now!
                    # maybe this will change in the future
                    code = int(line)
                    self.mand_sub[code] = code
                    assert (code > 99999 and code < 1000000)
                except ValueError:
                    pass

    def is_valid(self, name, year, semester):
        """
        receives a name, a year and a semester
        check if the course self corresponds to the name passed and the curriculum
        matches de year/semester
        returns true case it's a match, false otherwise
        """
        # check if names match
        if self.name != name: 
            return False 
        
        # check if the year/semester passed is not before the course
        if year < self.year_start or \
            (year == self.year_start and semester < self.sem_start):
            return False

        # check if the year/semester passed is not after the course
        if year > self.year_end or \
            (year == self.year_end and semester > self.sem_end):
                return False

        return True

    def is_mandatory(self, code_sub):
        """
        receives the code of a subject
        returns whether the code sub is mandatory or not
        """
        if code_sub in self.mand_sub:
            return True
        return False

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

def load_all_courses(name = NAME_COURSE_PCK, path = PATH):
    """
    unpickle list of all the courses 
    """
    try: 
        courses = pickle.load(open(path + name, 'rb'))
    except FileNotFoundError:
        register_all_courses()
        courses = pickle.load(open(path + name, 'rb'))
    return courses

def load_course(course_name, year, sem):
    """
    receives a course name, a year and a semester
    loads all the courses and then find the required course
    returns the required course 
    """
    courses = load_all_courses()
    for course in courses:
        if course.is_valid(course_name, year, sem):
            return course
    exit('could not load course %s for the year %d and semester %d' % (course_name,
        year, sem))

def register_all_courses(name = NAME_COURSE_PCK, path = PATH):
    """
    opens txt files containing information for the courses, 
    register all the courses in a list
    saves the list as a pickle object
    """
    courses = []

    # computer science courses (bachelor)
    new_course = Course(CIC_BACHELOR, 1988, 2, 2015, 1)
    courses.append(new_course)

    # computer science courses (not bachelor)
    new_course = Course(CIC_NON_BACHELOR, 1997, 1, 2001, 2)
    courses.append(new_course)
    new_course = Course(CIC_NON_BACHELOR, 2002, 1, 2003, 2)
    courses.append(new_course)
    new_course = Course(CIC_NON_BACHELOR, 2004, 1, 2015, 1)
    courses.append(new_course)
    
    # computer engineering
    new_course = Course(COMPUTER_ENGINEERING, 2009, 2, float('inf'), float('inf'))
    courses.append(new_course)

    # software engineering
    new_course = Course(SOFTWARE_ENGINEERING, 2008, 2, float('inf'), float('inf'))
    courses.append(new_course)

    # mechatronics engineering
    new_course = Course(MECHATRONICS_ENGINEERING, 1997, 2, float('inf'), float('inf'))
    courses.append(new_course)

    # network engineering
    new_course = Course(NETWORK_ENGINEERING, 1997, 1, float('inf'), float('inf'))
    courses.append(new_course)

    # save list as a pickle object
    file_target = open(path + name, 'wb')
    pickle.dump(courses, file_target)

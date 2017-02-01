# grades file, contain auxiliar methods to be called by the students module
def get_grade_weight(grade):
    """
    receives a grade, returns the grade weight, case valid
    case not valid, return None
    """
    if grade.lower() == 'sr':
        return 0
    elif grade.lower() == 'ii':
        return 1
    elif grade.lower() == 'mi':
        return 2
    elif grade.lower() == 'mm':
        return 3
    elif grade.lower() == 'ms':
        return 4
    elif grade.lower() == 'ss':
        return 5
    else: 
        return None

def student_dropped(grade):
    """
    receives a grade, returns true if it means the student dropped, false otherwise
    """
    if grade.lower() in ['tj', 'tr']:
        return True
    return False

def student_failed(grade):
    """
    receives a grade, returns true if it means the student passed, false otherwise
    """
    if grade.lower() in ['mi', 'ii', 'sr']:
        return True
    return False

def student_passed(grade):
    """
    receives a grade, returns true if it means the student passed, false otherwise
    """
    if grade.lower() in ['mm', 'ms', 'ss', 'cc', 'ap']:
        return True
    return False

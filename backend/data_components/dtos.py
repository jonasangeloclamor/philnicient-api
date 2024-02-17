class UserCreationDto:
    def __init__(self, firstname, middlename, lastname, username, password, role):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.username = username
        self.password = password
        self.role = role

class UserLoginDto:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class ClassCreationDto:
    def __init__(self, classname, teacher_id):
        self.classname = classname
        self.teacher_id = teacher_id

class ClassUpdationDto:
    def __init__(self, classname=None, teacher_id=None):
        self.classname = classname
        self.teacher_id = teacher_id

class StudentCreationDto:
    def __init__(self, class_id, student_id):
        self.class_id = class_id
        self.student_id = student_id

class DataCreationDto:
    def __init__(self, major_category, number_of_items, total_score, total_time_taken, average_cri, cri_criteria, student_id):
        self.major_category = major_category
        self.number_of_items = number_of_items
        self.total_score = total_score
        self.total_time_taken = total_time_taken
        self.average_cri = average_cri
        self.cri_criteria = cri_criteria
        self.student_id = student_id

class DataUpdationDto:
    def __init__(self, major_category=None, number_of_items=None, total_score=None, total_time_taken=None, average_cri=None, cri_criteria=None, student_id=None):
        self.major_category = major_category
        self.number_of_items = number_of_items
        self.total_score = total_score
        self.total_time_taken = total_time_taken
        self.average_cri = average_cri
        self.cri_criteria = cri_criteria
        self.student_id = student_id

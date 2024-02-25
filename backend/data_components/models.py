class User:
    def __init__(self, id, firstname, middlename, lastname, username, password, role, datetimecreated=None, datetimeupdated=None):
        self.id = id
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.username = username
        self.password = password
        self.role = role
        self.datetimecreated = datetimecreated
        self.datetimeupdated = datetimeupdated

class Class:
    def __init__(self, id, classname, teacher_id, classcode=None, datetimecreated=None, datetimeupdated=None):
        self.id = id
        self.classname = classname
        self.teacher_id = teacher_id
        self.classcode = classcode
        self.datetimecreated = datetimecreated
        self.datetimeupdated = datetimeupdated

class Student:
    def __init__(self, id, class_id, student_id, datetimecreated=None, datetimeupdated=None):
        self.id = id
        self.class_id = class_id
        self.student_id = student_id
        self.datetimecreated = datetimecreated
        self.datetimeupdated = datetimeupdated

class Result:
    def __init__(self, id, major_category, number_of_items, total_score, total_time_taken, average_cri, cri_criteria, student_id, datetimecreated=None, datetimeupdated=None):
        self.id = id
        self.major_category = major_category
        self.number_of_items = number_of_items
        self.total_score = total_score
        self.total_time_taken = total_time_taken
        self.average_cri = average_cri
        self.cri_criteria = cri_criteria
        self.student_id = student_id
        self.datetimecreated = datetimecreated
        self.datetimeupdated = datetimeupdated

class StudentAssessment:
    def __init__(self, id, student_id, assessments=None, datetimecreated=None, datetimeupdated=None):
        self.id = id
        self.student_id = student_id
        self.assessments = assessments if assessments else []
        self.datetimecreated = datetimecreated
        self.datetimeupdated = datetimeupdated

class Assessment:
    def __init__(self, id, question, figure, choices, answer, major_category, student_answer, student_cri, is_for_review, time, student_assessment_id, datetimecreated=None, datetimeupdated=None):
        self.id = id
        self.question = question
        self.figure = figure
        self.choices = choices
        self.answer = answer
        self.major_category = major_category
        self.student_answer = student_answer
        self.student_cri = student_cri
        self.is_for_review = is_for_review
        self.time = time
        self.student_assessment_id = student_assessment_id
        self.datetimecreated = datetimecreated
        self.datetimeupdated = datetimeupdated

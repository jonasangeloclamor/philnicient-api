class UserCreationDto:
    def __init__(self, firstname, middlename, lastname, email, username, password, role):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password
        self.role = role

class UserLoginDto:
    def __init__(self, username_or_email, password):
        self.username_or_email = username_or_email
        self.password = password

class ForgotPasswordRequestDto:
    def __init__(self, email):
        self.email = email

class ForgotPasswordResetDto:
    def __init__(self, email, code, password):
        self.email = email
        self.code = code
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

class ModelResultCreationDto:
    def __init__(self, major_category, number_of_items, total_score, total_time_taken, average_cri, cri_criteria, student_id):
        self.major_category = major_category
        self.number_of_items = number_of_items
        self.total_score = total_score
        self.total_time_taken = total_time_taken
        self.average_cri = average_cri
        self.cri_criteria = cri_criteria
        self.student_id = student_id

class ModelResultUpdationDto:
    def __init__(self, major_category=None, number_of_items=None, total_score=None, total_time_taken=None, average_cri=None, cri_criteria=None, student_id=None):
        self.major_category = major_category
        self.number_of_items = number_of_items
        self.total_score = total_score
        self.total_time_taken = total_time_taken
        self.average_cri = average_cri
        self.cri_criteria = cri_criteria
        self.student_id = student_id

class ModelResultPredictionDto:
    def __init__(self, major_category, number_of_items, total_score, total_time_taken, average_cri):
        self.major_category = major_category
        self.number_of_items = number_of_items
        self.total_score = total_score
        self.total_time_taken = total_time_taken
        self.average_cri = average_cri

class AssessmentResultCreationDto:
    def __init__(self, total_score, student_id):
        self.total_score = total_score
        self.student_id = student_id

class AssessmentCreationDto:
    def __init__(self, student_id):
        self.student_id = student_id

class AssessmentUpdationDto:
    def __init__(self, student_id=None):
        self.student_id = student_id

class QuestionCreationDto:
    def __init__(self, question, figure, choices, answer, major_category, student_answer, student_cri, is_for_review, time, assessment_id):
        self.question = question
        self.figure = figure
        self.choices = choices
        self.answer = answer
        self.major_category = major_category
        self.student_answer = student_answer
        self.student_cri = student_cri
        self.is_for_review = is_for_review
        self.time = time
        self.assessment_id = assessment_id

class QuestionUpdationDto:
    def __init__(self, question=None, figure=None, choices=None, answer=None, major_category=None, student_answer=None, student_cri=None, is_for_review=None, time=None, assessment_id=None):
        self.question = question
        self.figure = figure
        self.choices = choices
        self.answer = answer
        self.major_category = major_category
        self.student_answer = student_answer
        self.student_cri = student_cri
        self.is_for_review = is_for_review
        self.time = time
        self.assessment_id = assessment_id

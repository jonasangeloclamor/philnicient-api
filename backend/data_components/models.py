class User:
    def __init__(self, id, firstname, middlename, lastname, email, username, password, role, datetimecreated=None, datetimeupdated=None):
        self.id = id
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email
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

class ModelResult:
    def __init__(self, id, major_category, number_of_items, total_score, total_time_taken, average_cri, understanding_level, cri_criteria, accuracy, student_id, teacher_id, datetimecreated=None, datetimeupdated=None):
        self.id = id
        self.major_category = major_category
        self.number_of_items = number_of_items
        self.total_score = total_score
        self.total_time_taken = total_time_taken
        self.average_cri = average_cri
        self.understanding_level = understanding_level
        self.cri_criteria = cri_criteria
        self.accuracy = accuracy
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.datetimecreated = datetimecreated
        self.datetimeupdated = datetimeupdated

class AssessmentResult:
    def __init__(self, id, total_items, total_score, basic_theory_score, computer_systems_score, technical_elements_score, development_techniques_score, project_management_score, service_management_score, system_strategy_score, management_strategy_score, corporate_legal_affairs_score, student_id, teacher_id, datetimecreated=None, datetimeupdated=None):
        self.id = id
        self.total_items = total_items
        self.total_score = total_score
        self.basic_theory_score = basic_theory_score
        self.computer_systems_score = computer_systems_score
        self.technical_elements_score = technical_elements_score
        self.development_techniques_score = development_techniques_score
        self.project_management_score = project_management_score
        self.service_management_score = service_management_score
        self.system_strategy_score = system_strategy_score
        self.management_strategy_score = management_strategy_score
        self.corporate_legal_affairs_score = corporate_legal_affairs_score
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.datetimecreated = datetimecreated
        self.datetimeupdated = datetimeupdated

class Assessment:
    def __init__(self, id, student_id, is_submitted, questions=None, datetimecreated=None, datetimeupdated=None):
        self.id = id
        self.student_id = student_id
        self.is_submitted = is_submitted
        self.questions = questions if questions else []
        self.datetimecreated = datetimecreated
        self.datetimeupdated = datetimeupdated

class Question:
    def __init__(self, id, question, figure, choices, answer, major_category, student_answer, student_cri, is_for_review, time, assessment_id, datetimecreated=None, datetimeupdated=None):
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
        self.assessment_id = assessment_id
        self.datetimecreated = datetimecreated
        self.datetimeupdated = datetimeupdated

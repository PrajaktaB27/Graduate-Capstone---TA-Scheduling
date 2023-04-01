"""
studentSurveyModel.py
:Authors: Bobby Brown
:Version: 1.0

studentSurveyModel.py is the object model for creating the student worker survey
via the Qualtrics API for the TA Scheduling backend API.

Qualtrics API reference: https://api.qualtrics.com/5d41105e8d3b7-create-question

"""

from .surveyModel import surveyModel as default
from src.db.DBQuerrier import count_courses_with_hours as count
from src.db.DBQuerrier import get_course_dictionary as courses_dict

#--- Question 9 Definintions
choice_order_def = default.choice_order(count())
##print('choice order', choice_order_def)
# The student_choices can be programatically built using database contents for courses
student_choices = courses_dict()
#print('student_choices', student_choices)

# First section for Q8 matrix
matrix_one = {
    "Answers": {
        "1": {"Display":"Preferred"},
        "2": {"Display":"OK"},
        "3": {"Display":"No"}
    },
    "Choices": student_choices,
    "Configuration": default.configuration,
    "DataExportTag":"Q8#1",
    "QuestionDescription":"PREFERENCE",
    "QuestionID":"QID8#1",
    "QuestionText":"Preference",
    "QuestionType":"Matrix",
    "Selector":"Likert",
    "SubSelector":"SingleAnswer",
}

# Second section for Q8 matrix
matrix_two = {
    "Answers": {
        "1": {"Display":"Yes"},
        "2": {"Display":"Yes, not at SU"},
        "3": {"Display":"No"}
    },
    "Choices": student_choices,
    "Configuration": default.configuration,
    "DataExportTag":"Q8#2",
    "QuestionDescription":"TAKEN",
    "QuestionID":"QID8#2",
    "QuestionText":"Have you taken the class?",
    "QuestionType":"Matrix",
    "Selector":"Likert",
    "SubSelector":"SingleAnswer"
}

# Third section for Q8 matrix - Drop down list for grades
matrix_three = {
    "Answers":{
        "1": {"Display":"A"},
        "2": {"Display":"A-"},
        "3": {"Display":"B+"},
        "4": {"Display":"B"},
        "5": {"Display":"B-"},
        "6": {"Display":"C+"},
        "7": {"Display":"C"}
    },
    "Choices": student_choices,
    "Configuration": default.configuration,
    "DataExportTag":"Q8#3",
    "QuestionDescription":"GRADE",
    "QuestionID":"QID8#3",
    "QuestionText":"Course Grade",
    "QuestionType":"Matrix",
    "Selector":"Likert",
    "SubSelector":"DL",
}

# Student Survey Payload array
data = [
# Question 1 - Student Name - Form Text Entry
{
    "ChoiceOrder": [
        1,
        2
    ],
    "Choices": {
        "1": {
            "Display":"First Name",
        },
        "2": {
            "Display":"Last Name",
        }
    },
    "Configuration": default.configuration,
    "DataExportTag": "Q1",
    "DefaultChoices": False,
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 3,
    "QuestionDescription": "NAME",
    "QuestionID": "QID1",
    "QuestionText": "What is your name?<br>",
    "QuestionType": "TE",
    "Selector": "FORM",
    "Validation": default.validation
},

# Question 2 - Student email - Text Entry
{
    "Configuration": default.configuration,
    "DefaultChoices": False,
    "DataExportTag":"Q2",
    "Language":[],
    "NextAnswerId":1,
    "NextChoiceId":4,
    "QuestionDescription":"EMAIL",
    "QuestionID":"QID2",
    "QuestionText":"What is your Seattle University email address?<br><strong>(Ex: john@seattleu.edu)</strong>",
    "QuestionType":"TE",
    "Selector":"SL",
    "Validation": default.simple_regex_email
},

# Question 3 - Class - Multiple Choice
{
    "ChoiceOrder": [
        1,
        2,
        3,
        4,
        5,
        6
    ],
    "Choices": {
        "1": {"Display":"Undergrad Fr"},
        "2": {"Display":"Undergrad So"},
        "3": {"Display":"Undergrad Jr"},
        "4": {"Display":"Undergrad Sr"},
        "5": {"Display":"Certificate"},
        "6": {"Display":"MSCS"}
    },
    "Configuration": default.configuration,
    "DataExportTag": "Q3",
    "DefaultChoices": False,
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 7,
    "QuestionDescription": "CLASS",
    "QuestionID": "QID3",
    "QuestionText": "Class",
    "QuestionType": "MC",
    "Selector": "SAVR",
    "SubSelector": "TX",
    "Validation": default.validation
},

# Question 4 - Cumulative GPA - Text Entry
{
    "Configuration": default.configuration,
    "DataExportTag": "Q4",
    "DefaultChoices": False,
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "cGPA",
    "QuestionID":"QID4",
    "QuestionText":"What is your Cumulative GPA?<br>",
    "QuestionType": "TE",
    "Selector": "SL",
    "Validation": default.validation
},

# Question 5 - Faculty Reference - Text Entry
{
    "Configuration": default.configuration,
    "DataExportTag": "Q5",
    "DefaultChoices": False,
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "REFERENCE",
    "QuestionID": "QID5",
    "QuestionText": "Faculty Reference is <strong>REQUIRED</strong>! Please enter the SU email address <strong>(Ex: john@seattleu.edu)</strong> of a faculty member who can comment on your ability to perform as a grader/TA/tutor. This does not need be the instructor for the course(s) you are applying for. You must check with the faculty member before using them as a reference.",
    "QuestionType": "TE",
    "Selector": "SL",
    "Validation": default.simple_regex_email
},

# Question 6 - Previous Employee - Multiple Choice
{
    "ChoiceOrder": [
        1,
        2
    ],
    "Choices": {
        "1": {
            "Display": "Yes"
        },
        "2": {
            "Display": "No"
        }
    },
    "Configuration": default.configuration,
    "DataExportTag": "Q6",
    "DefaultChoices": False,
    "Language":[],
    "NextAnswerId":1,
    "NextChoiceId":3,
    "QuestionDescription": "EMPLOYEE",
    "QuestionID": "QID6",
    "QuestionText": "Have you previously been a student employee at Seattle University before?",
    "QuestionType":"MC",
    "Selector":"SAVR",
    "SubSelector":"TX",
    "Validation": default.validation
},

# Question 7 - Pre-arranged - Text Entry
{
    "Configuration": default.configuration,
    "DataExportTag": "Q7",
    "DefaultChoices": False,
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "ARRANGED",
    "QuestionID": "QID7",
    "QuestionText": "Have you already arranged with a faculty member to support a course? If so, please enter the instructor's SU email address <strong>(Ex: john@seattleu.edu)</strong>. Otherwise, leave blank.",
    "QuestionType": "TE",
    "Selector": "SL",
    "Validation": default.simple_regex_email_not_required('QID7')
},

# Question 8
{
    "ChoiceOrder": choice_order_def,
    "Choices": student_choices,
    "Configuration": default.configuration,
    "DataExportTag":"Q8",
    "DefaultChoices":False,
    "Language":[],
    "NextAnswerId":4,
    "NextChoiceId":33,
    "NumberOfQuestions":3,
    "QuestionDescription":"SECTIONS",
    "QuestionID":"QID8",
    "QuestionText":"Indicate the sections you would like to support. For those you mark Preferred or OK,\nanswer the questions in the next two columns.\nIf you have not taken the class, in the Comments block below please explain why you\nare qualified to support the class.",
    "QuestionType":"SBS",
    "Selector":"SBSMatrix",
    "Validation": {
        "Settings": {
            "ForceResponse": "OFF",
            "ForceResponseType":"ON",
            "Type":"None"
        }
    },

    "AdditionalQuestions": {
        "1": matrix_one,
        "2": matrix_two,
        "3": matrix_three
    }
},

# Question 9
{
    "Configuration": default.configuration,
    "DataExportTag": "Q9",
    "DefaultChoices": False,
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription":"COMMENTS",
    "QuestionID": "QID9",
    "QuestionText": "Other questions or comments about your preferences.",
    "QuestionType": "TE",
    "Selector": "SL",
    "Validation": default.validation_off_forced
}
]
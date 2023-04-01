"""
instructorSurveyModel.py
:Authors: Bobby Brown, Avery Dinh
:Version: 1.1.1

instructorSurveyModel.py is the object model for creating the instructor survey
via the Qualtrics API for the TA Scheduling backend API.

Qualtrics API reference: https://api.qualtrics.com/5d41105e8d3b7-create-question

"""
from .surveyModel import surveyModel as default

data = [
# Question 1 Payload - Instructor Name - Form Text Entry
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

# Question 2 - Instructor Email - Text Entry
{
    "Configuration": default.configuration,
    "DataExportTag": "Q2",
    "DefaultChoices": False,
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "EMAIL",
    "QuestionID": "QID2",
    "QuestionText": "What is your Seattle University email address?<br>(Ex: joe@seattleu.edu)",
    "QuestionType": "TE",
    "Selector": "SL",
    "Validation": default.simple_regex_email
},

# Question 3 - Course Number - Text Entry
{
    "Configuration": default.configuration,
    "DataExportTag": "Q3",
    "DefaultChoices": False,
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "COURSE",
    "QuestionID": "QID3",
    "QuestionText":"What is the course number (Example: CPSC-5820-05) for the class you want support for? Please include section number.",
    "QuestionType":"TE",
    "Selector":"SL",
    "Validation": default.custom_regex_course
},

# Question 4 - Student Support Type - Multiple Choice
{
    "ChoiceOrder": [
        "1",
        "2",
        "3"
    ],
    "Choices": {
        "1": {
            "Display": "Grader"
        },
        "2": {
            "Display": "TA"
        },
        "3": {
            "Display": "Tutor"
        }
    },
    "Configuration": default.configuration,
    "DataExportTag": "Q4",
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "SUPPORT",
    "QuestionID": "QID4",
    "QuestionText": "What type of student support is needed?",
    "QuestionType": "MC",
    "Selector": "SAVR",
    "SubSelector": "TX",
    "Validation": default.validation
},

# Question 5 - Student Course Completion - Multiple Choice
{
    "ChoiceOrder": [
        "1",
        "2",
        "3"
    ],
    "Choices": {
        "1": {
            "Display": "Yes"
        },
        "2": {
            "Display": "Preferred"
        },
        "3": {
            "Display": "No"
        }
    },
    "Configuration": default.configuration,
    "DataExportTag": "Q5",
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "COMPLETION",
    "QuestionID": "QID5",
    "QuestionText": "Is it necessary for the student to have completed this course at Seattle U?",
    "QuestionType":"MC",
    "Selector":"SAVR",
    "SubSelector":"TX",
    "Validation": default.validation
},

# Question 6 - Sharing Student Workers - Multiple Choice
{
    "ChoiceOrder": [
        "1",
        "2"
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
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 3,
    "QuestionDescription": "SHARING",
    "QuestionID": "QID6",
    "QuestionText": "If you are teaching a course that has another section with a different faculty member,\nwould you be interested in sharing the student employees?\n(The hours assigned will be combined.)",
    "QuestionType": "MC",
    "Selector": "SAVR",
    "SubSelector": "TX",
    "Validation": default.validation
},

# Question 7 - Number of Student Workers - Text Entry
{
    "Configuration": default.configuration,
    "DataExportTag": "Q7",
    "DefaultChoices": False,
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "NUMBER",
    "QuestionID": "QID7",
    "QuestionText": "How many student employees would you like for this position? (If you would like more\nthan one student, the assigned maximum hours per week will be split across multiple\nstudents.)",
    "QuestionType": "TE",
    "Selector": "SL",
    "Validation": {
        "Settings": {
            "ForceResponse": "ON",
            "Type": "ContentType",
            "MinChars":"1",
            "ContentType": "ValidNumber",
            "ValidNumber": {
                "Min": "1",
                "Max": "4",
                "NumDecimals":"0"
            }
        }
    }
},

# Question 8 - Precoordinated Student Workers - Yes/No
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
            "Display":"No"
        }
    },
    "Configuration": default.configuration,
    "DataExportTag": "Q8",
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "SPECIFIC",
    "QuestionID": "QID8",
    "QuestionText": "Are there any students you do want to work with for this course?",
    "QuestionType": "MC",
    "Selector": "SAVR",
    "SubSelector":"TX",
    "Validation": default.validation
},

# Question 8#1 - Precoordinated Student Workers - Text Entry
# To Qualtrics, question ID is QID9
{
    "Configuration": default.configuration,
    "DataExportTag": "Q8#1",
    "DefaultChoices": False,
    "InPageDisplayLogic": {
        "0": {
            "0": {
                "ChoiceLocator": "q://QID8/SelectableChoice/1",
                "Description": "If SPECIFIC Yes Is Selected",
                "LeftOperand": "q://QID8/SelectableChoice/1",
                "LogicType": "Question",
                "Operator": "Selected",
                "QuestionIDFromLocator": "QID8",
                "QuestionID": "QID8",
                "QuestionIsInLoop": "no",
                "Type": "Expression"
            },
            "Type": "If"
        },
        "inPage": True,
        "Type": "BooleanExpression"
    },
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "SPECIFIC EMAIL",
    "QuestionID": "QID8#1",
    "QuestionText": "Please enter the SU email address for the specific students you have already made previous verbal agreements with, \
                    separated by comma if more than 1.  Example: jsmith@seattleu.edu, johndoe@seattleu.edu",
    "QuestionType": "TE",
    "Selector": "SL",
    "Validation": default.custom_regex_email_only("QID9")
},

# Question 9 - Student Workers to Avoid - Yes/No
# To Qualtrics, this is QID10
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
            "Display":"No"
        }
    },
    "Configuration": default.configuration,
    "DataExportTag": "Q9",
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "AVOID",
    "QuestionID": "QID9",
    "QuestionText": "Are there any students you do <strong>not</strong> want to work with for this course?",
    "QuestionType": "MC",
    "Selector": "SAVR",
    "SubSelector":"TX",
    "Validation": default.validation
},

# Question 9#1 - Student Workers to Avoid - Text Entry
# To Qualtrics, this is QID11
{
    "Configuration": default.configuration,
    "DataExportTag": "Q9#1",
    "DefaultChoices": False,
    "InPageDisplayLogic": {
        "0": {
            "0": {
                "ChoiceLocator": "q://QID10/SelectableChoice/1",
                "Description": "If AVOID Yes Is Selected",
                "LeftOperand": "q://QID10/SelectableChoice/1",
                "LogicType": "Question",
                "Operator": "Selected",
                "QuestionIDFromLocator": "QID10",
                "QuestionID": "QID10",
                "QuestionIsInLoop": "no",
                "Type": "Expression"
            },
            "Type": "If"
        },
        "inPage": True,
        "Type": "BooleanExpression"
    },
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "AVOID EMAIL",
    "QuestionID": "QID9#1",
    "QuestionText": "Please enter the SU email address for the specific students you do not want to work with.\
                    separated by comma if more than 1.  Example: jsmith@seattleu.edu, johndoe@seattleu.edu",
    "QuestionType": "TE",
    "Selector": "SL",
    "Validation": default.custom_regex_email_only("QID11")
},

# Question 10 - Additional Requirements - Text Entry
{
    "Configuration": default.configuration,
    "DataExportTag": "Q10",
    "DefaultChoices": False,
    "Language": [],
    "NextAnswerId": 1,
    "NextChoiceId": 4,
    "QuestionDescription": "COMMENTS",
    "QuestionID": "QID10",
    "QuestionText": "Additional requirements or comments.",
    "QuestionType": "TE",
    "Selector": "ML",
    "Validation": default.validation_off_forced
}
]
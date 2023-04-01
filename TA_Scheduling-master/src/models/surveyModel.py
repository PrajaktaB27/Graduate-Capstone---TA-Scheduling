"""
surveyModel.py
:Authors: Bobby Brown, Avery Dinh
:Version: 1.0.2

surveyModel.py is the object model that holds common settings for creating the 
instructor and student surveys via the Qualtrics API for the TA Scheduling
backend API.

Qualtrics API reference: https://api.qualtrics.com/5d41105e8d3b7-create-question

"""

class surveyModel:
    """
    surveyModel creates an object to access common attributes for Qualtrics 
    survey questions to be used for survey generation.
    """

    configuration = {
        "QuestionDescriptionOption": "SpecifyLabel"
    }

    validation = {
        "Settings": {
            "ForceResponse": "ON",
            "ForceResponseType": "ON",
            "Type": "None"
        }
    }

    validation_off_forced = {
        "Settings": {
            "ForceResponse": "OFF",
            "ForceResponseType": "OFF",
            "Type": "None"
        }
    }
    #TODO: WILL NEED TO UPDATE NOT ENFORCING ALL

    custom_regex_course = {
        "Settings": {
            "ForceResponse": "ON",
            "ForceResponseType": "ON",
            "Type": "CustomValidation",
            "CustomValidation" : {
                "Logic": {
                    "0": {
                        "0": {
                            "QuestionID": "QID3",
                            "QuestionIsInLoop": "no",
                            "ChoiceLocator": "q://QID3/ChoiceTextEntryValue",
                            "Operator": "MatchesRegex",
                            "QuestionIDFromLocator": "QID3",
                            "LeftOperand": "q://QID3/ChoiceTextEntryValue",
                            "RightOperand": "^CPSC-(\d+)-(\d{2})$",#"/^CPSC\\d{4}$/",
                            "Type": "Expression",
                            "LogicType": "Question",
                            "Description": "<span class=\"ConjDesc\">If</span> <span class=\"QuestionDesc\">COURSE</span> <span class=\"LeftOpDesc\">Text Response</span> <span class=\"OpDesc\">Matches Regex</span> <span class=\"RightOpDesc\"> /^CPSC\\d{4}$/ </span>"
                        },
                        "Type": "If"
                    },
                    "Type": "BooleanExpression"
                },
                "Message": {
                    "messageID": "MS_2t6VtUTLnp4LJQ2",
                    "subMessageID": "VE_ERROR",
                    "libraryID": "UR_8DiObkePqGaOFrU",
                    "description": "Error Text"
                }
            }
        }
    }

    custom_regex_email_only = lambda questionID : {
        "Settings": {
            "ForceResponse": "ON",
            "ForceResponseType": "ON",
            "Type": "CustomValidation",
            "CustomValidation" : {
                "Logic": {
                    "0": {
                        "0": {
                            "QuestionID": questionID,#"QID8",
                            "QuestionIsInLoop": "no",
                            "ChoiceLocator": "q://{}/ChoiceTextEntryValue".format(questionID),
                            "Operator": "MatchesRegex",
                            "QuestionIDFromLocator": questionID,#"QID8",
                            "LeftOperand": "q://{}/ChoiceTextEntryValue".format(questionID),
                            "RightOperand": "(@seattleu.edu)$",
                            "Type": "Expression",
                            "LogicType": "Question",
                            "Description": "<span class=\"ConjDesc\">If</span> <span class=\"QuestionDesc\">SPECIFIC</span> <span class=\"LeftOpDesc\">Text Response</span> <span class=\"OpDesc\">Matches Regex</span> <span class=\"RightOpDesc\"> (@seattleu.edu)$ </span>"
                        },
                        "Type": "If"
                    },
                    "Type": "BooleanExpression"
                },
                "Message": {
                    "messageID": "MS_2hm03ivjA1kpQLI",
                    "subMessageID": "VE_ERROR",
                    "libraryID": "UR_8DiObkePqGaOFrU",
                    "description": "Error Text"
                }
            }
        }
    }

    # Simplified regex validation for email
    simple_regex_email = {
        "Settings": {
            "ForceResponse": "ON",
            "ForceResponseType": "ON",
            "Type":"CustomValidation",
            "CustomValidation": {
                "Logic": {
                    "0": {
                        "0": {
                            "ChoiceLocator":"q://QID2/ChoiceTextEntryValue",
                            "Description":"Simplified email validation",
                            "LogicType":"Question",
                            "LeftOperand":"q://QID2/ChoiceTextEntryValue",
                            "Operator":"MatchesRegex",
                            "RightOperand":"^.{3,20}(@seattleu.edu)$",
                            "QuestionID":"QID2",
                            "QuestionIDFromLocator":"QID2",
                            "QuestionIsInLoop":"no",
                            "Type":"Expression",
                        },
                        "Type":"If"
                    },
                    "Type":"BooleanExpression"
                },
                "Message": {
                    "messageID": "MS_2hm03ivjA1kpQLI",
                    "subMessageID": "VE_ERROR",
                    "libraryID": "UR_8DiObkePqGaOFrU",
                    "description": "Error Text"
                }
            }
        }
    }

    # Simplified regex validation for email
    simple_regex_email_not_required = lambda questionID:{
        "Settings": {
            "ForceResponse": "OFF",
            "ForceResponseType": "OFF",
            "Type":"CustomValidation",
            "CustomValidation": {
                "Logic": {
                    "0": {
                        "0": {
                            "ChoiceLocator":"q://{}/ChoiceTextEntryValue".format(questionID),
                            "Description":"Simplified email validation",
                            "LogicType":"Question",
                            "LeftOperand":"q://{}/ChoiceTextEntryValue".format(questionID),
                            "Operator":"MatchesRegex",
                            "RightOperand":"^.{3,20}(@seattleu.edu)$",
                            "QuestionID":questionID,
                            "QuestionIDFromLocator": questionID,
                            "QuestionIsInLoop":"no",
                            "Type":"Expression",
                        },
                        "1": {
                            "QuestionID": questionID,
                            "QuestionIsInLoop": "no",
                            "ChoiceLocator": "q://{}/ChoiceTextEntryValue".format(questionID),
                            "Operator": "Empty",
                            "QuestionIDFromLocator": questionID,
                            "LeftOperand": "q://{}/ChoiceTextEntryValue".format(questionID),
                            "Type": "Expression",
                            "LogicType": "Question",
                            "Description": "<span class=\"ConjDesc\">Or</span> <span class=\"QuestionDesc\">EMAIL</span> <span class=\"LeftOpDesc\">Text Response</span> <span class=\"OpDesc\">Is Empty</span> ",
                            "Conjuction": "Or"
                        },
                        
                        "Type":"If"
                    },
                    "Type":"BooleanExpression"
                },
                "Message": {
                    "messageID": "MS_2hm03ivjA1kpQLI",
                    "subMessageID": "VE_ERROR",
                    "libraryID": "UR_8DiObkePqGaOFrU",
                    "description": "Error Text"
                }
            }
        }
    }

    def choice_order(courses_num: int) -> list:
        """
        choice_order builds a list in the format [1,2,..., courses_db.size]

        for
        "ChoiceOrder": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
        """
        
        choice_order_list = []
        for course in range(1, courses_num + 1):
            choice_order_list.append(course)
        
        return choice_order_list
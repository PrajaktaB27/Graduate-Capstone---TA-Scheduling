import copy
import traceback
from src.db import deps
from src.core.Matcher import *
from src.schemas.course import AssignmentTableInfo

# Do we need to change "DB_NAME" to "Database"?
db = deps.get_db()


# check if pop function gets value from list and handle exception if needed
def check_exception_for_pop(arg_1, aList, arg_2):
    try:
        value = aList.distinct(arg_2).pop()
        if value == "" or value is None or value == "N/A":
            msg = "Not found value for %s" % arg_2
            print(msg)
            return "N/A"
        else:
            msg = "Successfully return %s" % value
            #print(msg)
            return value
    # No field of arg_2 in the list, might be "Not assigned yet"
    except IndexError as e:
        arg_1 = "no or unknown email or courseID" if len(arg_1) == 0 else arg_1
        msg = "%s for %s from %s" % (e, arg_2, arg_1)
        #print(msg)
        return "N/A"


# def convert_GPA_to_grade(GPA):
#     if GPA >= 3.68:
#         return "A"
#     elif GPA >= 3.34:
#         return "A-"
#     elif GPA >= 3.01:
#         return "B+"
#     elif GPA >= 2.68:
#         return "B"
#     elif GPA >= 2.34:
#         return "B-"
#     elif GPA >= 2.01:
#         return "C+"
#     elif GPA >= 1.68:
#         return "C"
#     elif GPA >= 1.34:
#         return "C-"
#     elif GPA >= 1.01:
#         return "D+"
#     elif GPA >= 0.68:
#         return "D"
#     elif GPA >= 0.34:
#         return "D-"
#     else:
#         return "F"


def check_name(firstName, lastName):
    if firstName == "N/A" and lastName == "N/A":
        studentName = "N/A"
    elif firstName == "N/A":
        studentName = lastName
    elif lastName == "N/A":
        studentName = firstName
    else:
        studentName = firstName + " " + lastName

    return studentName


# return specific course detail
def get_course_detail_for_apiCall(courseID: str):
    course = list(db["Courses"].find({"courseID": courseID}, {'_id': 0}))
    for detail in course:
        print(detail)

    return course


# return specific faculty detail
def get_faculty_detail_for_apiCall(email: str):
    faculty = list(db["Faculties"].find({"email": email}, {'_id': 0}))
    for detail in faculty:
        print(detail)

    return faculty


# return all Courses object
def get_course_list():
    courses = list(db["Courses"].find({}, {'_id': 0}))
    for detail in courses:
        print(detail)

    return courses


# return all Students object
def get_student_list():
    students = list(db["Students"].find({}, {'_id': 0}))
    for detail in students:
        print(detail)

    return students


# return all faculties object
def get_faculty_list():
    faculties = list(db["Faculties"].find({}, {'_id': 0}))
    for detail in faculties:
        print(detail)

    return faculties


# return matchedCourse object
def get_current_matchedCourses():
    matchedCourses = list(db["matchedCourses"].find({}, {'_id': 0}))
    for detail in matchedCourses:
        print(detail)

    return matchedCourses


def get_name(email, aList):
    firstName = check_exception_for_pop(email, aList, "firstName")
    lastName = check_exception_for_pop(email, aList, "lastName")
    name = check_name(firstName, lastName)

    return name


def get_assigned_courseIDs(email):
    assigned_courseIDs = db["matchedCourses"].find({"email": email}).distinct("courseID")
    if not assigned_courseIDs: return "No course assigned"

    assigned_courses = []
    for assigned_courseID in assigned_courseIDs:
        assigned_course_detail = {}
        courseName = check_exception_for_pop(email, db["Courses"].find({"courseID": assigned_courseID}), "courseName")
        support_type = check_exception_for_pop(assigned_courseID, db["Faculty_Course"].
                                               find({"courseID": assigned_courseID}), "support_type")

        assigned_course_detail["courseID"] = assigned_courseID
        assigned_course_detail["courseName"] = courseName
        assigned_course_detail["support_type"] = support_type

        assigned_courses.append(assigned_course_detail)

    return assigned_courses


# return array to api call: get_assignment_table()
def get_assignment_table_for_apiCall():
    table = []
    matchedCourses = db["matchedCourses"].find({})

    for matchedCourse in matchedCourses:
        courseID = matchedCourse["courseID"]
        courseName = check_exception_for_pop(courseID, db["Courses"].find({"courseID": courseID}), "courseName")
        # support_type = check_exception_for_pop(courseID, db["Faculty_Course"].
        #                                        find({"courseID": courseID}), "support_type")
        try:
            faculty_response = db["Faculty_Course"].find({"courseID": courseID})[0]
        except Exception as e:
            print(courseID)
        facultyName =faculty_response['faculty_first_name'] + ' ' + \
                                            faculty_response['faculty_last_name']
        stu_email = matchedCourse["email"]
        stu_email = stu_email if stu_email != "" else "Not assigned yet"
        studentName = get_name(stu_email, db["Students"].find({"email": stu_email}))
        preferred = False
        for s in faculty_response['preferred_Student']:
            if s == stu_email:
                preferred = True
                break

        info = AssignmentTableInfo(
            courseID = courseID, 
            courseName= courseName,
            fac_email = faculty_response['email'],
            facultyName = facultyName,
            stu_email= stu_email,
            studentName=studentName,
            is_faculty_preferred= preferred
        )
        #print(info)

        table.append(info)

        #print(info)

    return table


# get faculty full name for student detail
def get_faculty_names_for_student_detail(ref_emails):
    facultyRef_names = []
    for fac_email in ref_emails:
        facultyName = get_name(fac_email, db["Faculties"].find({"email": fac_email}))
        facultyRef_names.append(facultyName)

    return facultyRef_names


def get_courses_preferences(email):
    courses_preferences = []
    student_courses = db["Student_Course"].find({"email": email})
    for student_course in student_courses:
        courses_preference_detail = {}
        courseID = student_course["courseID"]
        courseName = check_exception_for_pop(courseID, db["Courses"].find({"courseID": courseID}), "courseName")
        preferenceLevel = student_course["preferenceLevel"]
        support_type = check_exception_for_pop(courseID, db["Faculty_Course"].
                                               find({"courseID": courseID}), "support_type")
        GPA = student_course["course_GPA"]
        faculty_preferred_students = db["Faculty_Course"].find({"courseID": courseID}).distinct("preferred_Student")
        is_faculty_preferred = True if email in faculty_preferred_students else False

        courses_preference_detail["courseName"] = courseName
        courses_preference_detail["courseID"] = courseID
        courses_preference_detail["support_type"] = support_type
        courses_preference_detail["preferenceLevel"] = preferenceLevel
        courses_preference_detail["GPA"] = GPA
        courses_preference_detail["is_faculty_preferred"] = is_faculty_preferred

        courses_preferences.append(courses_preference_detail)

    return courses_preferences


# return array to api call: get_student_detail()
def get_student_detail_for_apiCall(email: str):
    courses_preferred_info = {}

    studentName = get_name(email, db["Students"].find({"email": email}))
    email_addr = email if email != "Not assigned yet" else "N/A"
    cGPA = check_exception_for_pop(email, db["Students"].find({"email": email}), "cGPA")
    is_employee = check_exception_for_pop(email, db["Students"].find({"email": email}), "employee")
    ref_emails = db["Students"].find({"email": email}).distinct("reference")
    arr_emails = db["Students"].find({"email": email}).distinct("arrange_instructor")
    facultyRef_names = get_faculty_names_for_student_detail(ref_emails) if ref_emails else ["No data"]
    facultyArr_names = get_faculty_names_for_student_detail(arr_emails) if arr_emails else ["No data"]
    assigned_courses = get_assigned_courseIDs(email) if email != "Not assigned yet" else ["No data"]
    courses_preferences = get_courses_preferences(email) if arr_emails else ["No data"]
    comments = db["Students"].find({"email": email}).distinct("comments") 

    courses_preferred_info["student"] = studentName
    courses_preferred_info["email"] = email_addr
    courses_preferred_info["cGPA"] = cGPA
    courses_preferred_info["is_employee"] = is_employee
    courses_preferred_info["facultyArr"] = facultyArr_names
    courses_preferred_info["facultyRef"] = facultyRef_names
    courses_preferred_info["assigned_courses"] = assigned_courses
    courses_preferred_info["courses_preferences"] = courses_preferences
    courses_preferred_info["comments"] = comments

    print(courses_preferred_info)

    return courses_preferred_info


# reassign a new worker to a course
def reassign_worker_in_course_for_apiCall(old_email: str, new_email: str, courseID: str):
    result = db["matchedCourses"].update_one({"email": old_email, "courseID": courseID}, {"$set": {"email": new_email}})

    if result.modified_count > 0:
        result_add = add_facEmail_to_stu_arrange_instructor(new_email, courseID)
        if not result_add:
            print("No faculty email is added to arrange_instructor.")
            return False
        result_remove = remove_facEmail_from_stu_arrange_instructor(old_email, courseID)
        if not result_remove:
            print("No faculty email is removed from arrange_instructor.")
            return False
        return True
    else:
        print("No student email is added to the matched course.")
        return False


# add a faculty email to the student's arrange_instructor array
def add_facEmail_to_stu_arrange_instructor(stu_email, courseID):
    fac_email = check_exception_for_pop(courseID, db["Faculty_Course"].find({"courseID": courseID}), "email")
    result = db["Students"].update_one({"email": stu_email}, {"$push": {"arrange_instructor": fac_email}})

    if result.modified_count > 0:
        return True
    else:
        print("No faculty email is added to arrange_instructor.")
        return False


# remove a faculty email from the student's arrange_instructor array
def remove_facEmail_from_stu_arrange_instructor(stu_email, courseID):
    fac_email = check_exception_for_pop(courseID, db["Faculty_Course"].find({"courseID": courseID}), "email")
    result = db["Students"].update_one({"email": stu_email}, {"$pull": {"arrange_instructor": fac_email}})

    if result.modified_count > 0:
        return True
    else:
        print("No faculty email is removed from arrange_instructor.")
        return False


# assign a new worker to a course, and add faculty email to worker's array of arrange instructor
def assign_worker_to_course_for_apiCall(email: str, courseID: str):
    result_1 = db["matchedCourses"].update_one({"email": "", "courseID": courseID}, {"$set": {"email": email}})
    if result_1.modified_count > 0:
        result_2 = add_facEmail_to_stu_arrange_instructor(email, courseID)
        if result_2:
            msg = "Successfully assign %s to %s." % (email, courseID)
            response = {"status": True, "msg": msg}
            return response
        else:
            db["matchedCourses"].update_one({"email": email, "courseID": courseID}, {"$set": {"email": ""}})
            msg = "Process failed, caused by no faculty email added to arrange_instructor."
            response = {"status": False, "msg": msg}
            return response
    else:
        msg = "Since the quota of %s is full, No student can be assigned to it. " \
              "Please remove the current worker before assigning." % courseID
        print(msg)
        response = {"status": False, "msg": msg}
        return response


# remove a current worker from a course, and remove faculty email from worker's array of arrange instructor
def remove_worker_from_course_for_apiCall(email: str, courseID: str):
    result_1 = db["matchedCourses"].update_one({"email": email, "courseID": courseID}, {"$set": {"email": ""}})
    if result_1.modified_count > 0:
        result_2 = remove_facEmail_from_stu_arrange_instructor(email, courseID)
        if result_2:
            db["matchedCourses"].update_one({"email": "", "courseID": courseID}, {"$set": {"approved": False}})
            msg = "Successfully remove %s from %s, and update approve_type of %s to be False." % (email, courseID,
                                                                                                  courseID)
            print(msg)
            response = {"status": True, "msg": msg}
            return response
        else:
            db["matchedCourses"].update_one({"email": "", "courseID": courseID}, {"$set": {"email": email}})
            msg = "Process failed, caused by no faculty email removed from arrange_instructor."
            print(msg)
            response = {"status": False, "msg": msg}
            return response
    else:
        msg = "No student is removed from %s." % courseID
        print(msg)
        response = {"status": False, "msg": msg}
        return response


# update approved status
def update_approve_status_for_apiCall(email: str, courseID: str):
    arg_1 = "matchedCourse of %s and %s" % (email, courseID)
    approve_status = check_exception_for_pop(arg_1, db["matchedCourses"].find({"email": email, "courseID": courseID}),
                                             "approved")

    if approve_status == "N/A": return "Process of updating approve status failed"

    if approve_status:
        result = db["matchedCourses"].update_one({"email": email, "courseID": courseID}, {"$set": {"approved": False}})
        if result.modified_count > 0:
            msg = "Successfully update approve status to be False"
            print(msg)
        else:
            db["matchedCourses"].update_one({"email": email, "courseID": courseID}, {"$set": {"approved": True}})
            msg = "Process failed to update approve status to be False!"
            print(msg)
        return msg
    else:
        result = db["matchedCourses"].update_one({"email": email, "courseID": courseID}, {"$set": {"approved": True}})
        if result.modified_count > 0:
            msg = "Successfully update approve status to be True"
            print(msg)
        else:
            db["matchedCourses"].update_one({"email": email, "courseID": courseID}, {"$set": {"approved": False}})
            msg = "Process failed to update approve status to be True!"
            print(msg)
        return msg


def get_faculty_course_detail_for_apiCall(courseID: str):
    faculty_course_info = {}
    try:
        fac_response = db["Faculty_Course"].find({"courseID": courseID})[0]
        course = db["Courses"].find({"courseID": courseID})[0]

        # email = check_exception_for_pop(courseID, db["Faculty_Course"].find({"courseID": courseID}), "email")
        # courseName = check_exception_for_pop(courseID, db["Courses"].find({"courseID": courseID}), "courseName")
        # facultyName = get_name(email, db["Faculties"].find({"email": email}))
        # support_type = check_exception_for_pop(courseID, db["Faculty_Course"].find({"courseID": courseID}), "support_type")
        # enrollment = check_exception_for_pop(courseID, db["Courses"].find({"courseID": courseID}), "enrollment")
        # hoursAllowed = check_exception_for_pop(courseID, db["Faculty_Course"].find({"courseID": courseID}), "hoursAllowed")
        # quota = check_exception_for_pop(courseID, db["Faculty_Course"].find({"courseID": courseID}), "number_needed")

        faculty_course_info["courseName"] = course['courseName']
        faculty_course_info["courseID"] = courseID
        faculty_course_info["facultyName"] = fac_response['faculty_first_name'] + ' ' + \
                                            fac_response['faculty_last_name']
        faculty_course_info["support_type"] = fac_response['support_type']
        faculty_course_info["enrollment"] = course['enrollment']
        faculty_course_info["hoursAllowed"] = course['hours_allowed']    
        faculty_course_info["quota"] = fac_response['number_needed']
        faculty_course_info["additional_req"] = fac_response["additional_req"]

        return faculty_course_info
    except Exception as e:
        raise Exception


def get_student_info_list(courseID, emails, student_info):
    # get_student_priority_sort(emails, courseID)

    for email in emails:
        if email == "":
            continue
        student_detail = {}
        #TODO: REDUCE THIS DB ACCESS PRACTICE
        studentName = get_name(email, db["Students"].find({"email": email}))
        msg = "%s in %s" % (email, courseID)
        preferenceLevel = check_exception_for_pop(msg, db["Student_Course"].
                                                  find({"email": email, "courseID": courseID}), "preferenceLevel")
        GPA = check_exception_for_pop(msg, db["Student_Course"].find({"email": email,
                                                                      "courseID": courseID}), "course_GPA")
        cGPA = check_exception_for_pop(msg, db["Students"].find({"email": email}), "cGPA")
        faculty_preferred_students = db["Faculty_Course"].find({"courseID": courseID}).distinct("preferred_Student")
        is_faculty_preferred = True if email in faculty_preferred_students else False

        student_detail["studentName"] = studentName
        student_detail["email"] = email
        student_detail["preferenceLevel"] = preferenceLevel
        student_detail["GPA"] = GPA
        student_detail["cGPA"] = cGPA
        student_detail["is_faculty_preferred"] = is_faculty_preferred

        student_info.append(student_detail)


def get_assigned_student_for_the_course_for_api_call(courseID):
    assigned_students_info = []
    emails = db["matchedCourses"].find({"courseID": courseID}).distinct("email")

    get_student_info_list(courseID, emails, assigned_students_info)

    return assigned_students_info


def get_available_student_for_the_course_for_api_call(courseID):
    available_students_info = []
    assigned_emails = db["matchedCourses"].find({"courseID": courseID}).distinct("email")
    available_emails = db["Student_Course"].find({"$and": [{"courseID": courseID}, {
        "$or": [{"preferenceLevel": "Preferred"}, {"preferenceLevel": "OK"}]}]}).distinct("email")
    
    for assigned_email in assigned_emails:
        if assigned_email in available_emails: available_emails.remove(assigned_email)

    get_student_info_list(courseID, available_emails, available_students_info)

    return available_students_info


def get_email_info_for_Matcher(email, courseID):
    # is_email_ref = email in db["Faculty_Course"].find(
    #     {"courseID": courseID, "additional_req": "testing"}).distinct("preferred_Student")
    # email_cGPA = check_exception_for_pop(email, db["Students"].find({"email": email, "firstName": "testing"}), "cGPA")
    #
    # msg_email_GPA = "%s in %s " % (email, courseID)
    # email_GPA = check_exception_for_pop(msg_email_GPA, db["Student_Course"].find({"email": email, "courseID": courseID, "firstName": "testing"}),
    #                                     "course_GPA")
    #
    # msg_email_preferenceLevel = "%s in %s" % (email, courseID)
    # email_preferenceLevel = check_exception_for_pop(msg_email_preferenceLevel, db["Student_Course"].find(
    #     {"email": email, "courseID": courseID, "other_req": "testing"}), "preferenceLevel")
    #
    # return email_cGPA, email_GPA, is_email_ref, email_preferenceLevel

    print("email: %s" % email)
    is_email_ref = email in db["Faculty_Course"].find(
        {"courseID": courseID}).distinct("preferred_Student")
    email_cGPA = check_exception_for_pop(email, db["Students"].find({"email": email}), "cGPA")

    msg_email_GPA = "%s in %s " % (email, courseID)
    email_GPA = check_exception_for_pop(msg_email_GPA,
                                        db["Student_Course"].find({"email": email, "courseID": courseID}),
                                        "course_GPA")

    msg_email_preferenceLevel = "%s in %s" % (email, courseID)
    email_preferenceLevel = check_exception_for_pop(msg_email_preferenceLevel, db["Student_Course"].find(
        {"email": email, "courseID": courseID}), "preferenceLevel")

    return email_cGPA, email_GPA, is_email_ref, email_preferenceLevel


def get_faculty_requirements_for_Matcher(courseID):
    print("In the get_faculty_requirements_for_Matcher function call:")
    quota = check_exception_for_pop(courseID,
                                    db["Faculty_Course"].find({"courseID": courseID, "additional_req": "testing"}),
                                    "number_needed")
    not_preferred_stu_emails = db["Faculty_Course"].find({"courseID": courseID, "additional_req": "testing"}). \
        distinct("not_preferred_Student")
    preferred_stu_emails = db["Faculty_Course"].find({"courseID": courseID, "additional_req": "testing"}). \
        distinct("preferred_Student")
    should_courseTaken = check_exception_for_pop(courseID, db["Faculty_Course"].find(
        {"courseID": courseID, "additional_req": "testing"}), "courseTaken_preferred")
    to_share_student = check_exception_for_pop(courseID, db["Faculty_Course"].find(
        {"courseID": courseID, "additional_req": "testing"}), "share_student_approved")

    return quota, not_preferred_stu_emails, preferred_stu_emails, should_courseTaken, to_share_student


def get_student_emails_for_Matcher():
    return db["Students"].find({"firstName": "testing"}).distinct("email")


def get_student_preferenceLevel_and_courseTaken_for_Matcher(email, courseID):
    msg_preferenceLevel = "%s in %s" % (email, courseID)
    preferenceLevel = check_exception_for_pop(msg_preferenceLevel, db["Student_Course"].find(
        {"email": email, "courseID": courseID, "other_req": "testing"}), "preferenceLevel")

    msg_courseTaken = "%s in %s" % (email, courseID)
    courseTaken = check_exception_for_pop(msg_courseTaken, db["Student_Course"].find(
        {"email": email, "courseID": courseID, "other_req": "testing"}), "courseTaken")

    return preferenceLevel, courseTaken


def get_courseIDs_for_Matcher():
    return db["Courses"].find({}).distinct("courseID") #FIXME: Courses or Faculty_Courses? 


def update_student_arrange_student_for_Matcher(matchedCourses_Collection):
    print("In the update_student_arrange_student_for_Matcher function call:")
    msgs = []
    try:
        for matchedCourse in matchedCourses_Collection:
            stu_email = matchedCourse.get("email")
            if stu_email == "": continue
            courseID = matchedCourse.get("courseID")
            fac_email = check_exception_for_pop(courseID, db["Faculty_Course"].find(
                {"courseID": courseID}), "email")

            # db["Students"].update_one({"email": stu_email}, {"$push": {"arrange_instructor": fac_email}})

            msgs.append("Successfully push %s into %s's arrange_instructor!" % (fac_email, stu_email))
    except:
        msgs = "FAILED to update arrange_student to student in Mongodb!"

    return msgs


def populate_matchedCourses_Collection_for_Matcher(matchedCourses_Collection):
    try:
        # db["matchedCourses"].insert_many(matchedCourses_Collection)
        msg = "\nSuccessfully populated matchedCourses to MongoDB!\n"
    except:
        msg = "\nFAILED to populate matchedCourses_Collection to Mongodb!\n"

    return msg


def save_surveyID(surveyID: str):
    try:
        db.Survey_ID.insert_one({'surveyID': surveyID, 'pulled': False})
        return True
    except Exception as e:
        print(e)
        return False

def mark_pulled_surveyID(surveyID: str):
    try:
        db.Survey_ID.update_one({'surveyID': surveyID}, {"$set" : {'pulled': True}})
        return True
    except Exception as e:
        print(e)
        return False
    
def check_surveyID_pulled(surveyID: str):
    try:
        db.Survey_ID.find({'surveyID': surveyID})
        return True
    except Exception as e:
        print(e)
        return False

def get_latest_surveyID() -> str:
    try:
        return list(db.Survey_ID.find({}, sort=[('_id', -1)], limit=1))[0]

    except Exception as e:
        print(e)
        return False


def courses_insert_many(courses):
    try:
        db.Courses.insert_many(copy.deepcopy(courses))
        return True
    except Exception as e:
        print('Error while inserting courses')
        print(traceback.format_exc())
        return False

def faculty_response_insert_many(values:list):
    try:
        db.Faculty_Course.insert_many(copy.deepcopy(values))
        return True
    except Exception as e:
        print('Error while inserting courses')
        print(traceback.format_exc())
        return False

# Counts the number of courses with {hours_allowed: {$gt :0}}
def count_courses_with_hours() -> int:
    #print(db.Faculty_Course.count_documents({'hoursAllowed': {'$gt' :0}}))
    return db.Faculty_Course.count_documents({'hoursAllowed': {'$gt' :0}})

# Generates Dictionary of courses for student survey
def get_course_dictionary() -> list:

    student_choices = []
    counter = 1
    #db.Courses.count_documents({'hours_allowed': {'$gt' :0}})
    all_courses = db.Faculty_Course.find({'hoursAllowed': {'$gt' :0}})
        #{'courseID': 1, 'faculty_last_name':1, 'support_type': 1, 'hoursAllowed': 1, 'courseTaken_preferred': 1, 'number_needed':1})

    for row in all_courses:
        course = row["courseID"]
        name = row["faculty_last_name"]
        support = row["support_type"]
        hours = row["hoursAllowed"]
        taken = row["completed"]
        number = row["number_needed"]

        line = course + " - " + name + " - " + support + " - " + str(hours) + " - " + taken

        if number > 1:
            line += " (" + str(number) + " positions available)"
        
        student_choices.append({"Display":line})

    return student_choices

def student_response_insert_many(student_list:list, student_course_list:list):
    try:
        db.Students.insert_many(student_list)
        db.Student_Course.insert_many(student_course_list)
        return True
    except Exception as e:
        print('Error while inserting courses')
        print(traceback.format_exc())
        return False
    
def get_hours_from_course(courseID):
    try:
        course = db.Courses.find({'courseID': courseID})[0]
        return course['hours_allowed']
    except IndexError as e:
        print('No record found for course: ', courseID)
        return 0
    except Exception as e:
        print('Error getting hours')
        print(traceback.format_exc())
        return False
    
def matched_courses_insert_many(course_list):
    try:
        db.matchedCourses.insert_many(course_list)
        return True
    except Exception as e:
        print('Error while inserting courses')
        print(traceback.format_exc())
        return False
from datetime import date
from src.db.DBQuerrier import *
from src.db import DBQuerrier


def get_weight(level):
    return 2 if level == "preferred" or level is True else 1


# return student info for comparison
def get_email_info(email, courseID):
    email_cGPA, email_GPA, is_email_ref, email_preferenceLevel = DBQuerrier.get_email_info_for_Matcher(email, courseID)

    email_ref_weight = get_weight(is_email_ref)
    email_preferenceLevel_weight = get_weight(email_preferenceLevel)

    return email_cGPA, email_GPA, email_ref_weight, email_preferenceLevel_weight


# return true if current email have first priority else turn false
def get_compare(curr_email, compare_email, curr_courseID, compare_courseID):
    if curr_email is None:
        return False
    elif compare_email is None:
        return True

    curr_email_cGPA, curr_email_GPA, curr_email_ref_weight, curr_email_preferenceLevel_weight \
        = get_email_info(curr_email, curr_courseID)
    compare_email_cGPA, compare_email_GPA, compare_email_ref_weight, compare_email_preferenceLevel_weight \
        = get_email_info(compare_email, compare_courseID)

    if curr_email_ref_weight > compare_email_ref_weight:
        return True
    elif curr_email_ref_weight == compare_email_ref_weight:
        if curr_email_preferenceLevel_weight > compare_email_preferenceLevel_weight:
            return True
        elif curr_email_preferenceLevel_weight == compare_email_preferenceLevel_weight:
            if curr_email_GPA > compare_email_GPA:
                return True
            elif curr_email_GPA == compare_email_GPA:
                if curr_email_cGPA >= compare_email_cGPA:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


# insertion sort
def get_student_priority_sort(emails, courseID):
    size = len(emails)

    for i in range(1, size):
        email = emails[i]

        j = i - 1

        while j >= 0 and get_compare(email, emails[j], courseID, courseID):
            emails[j + 1] = emails[j]
            j -= 1
            emails[j + 1] = email


def get_faculty_requirements(courseID):
    return get_faculty_requirements_for_Matcher(courseID)


def get_student_emails():
    return get_student_emails_for_Matcher()


def get_student_preferenceLevel_and_courseTaken(email, courseID):
    return get_student_preferenceLevel_and_courseTaken_for_Matcher(email, courseID)


def set_matchedCourse_into_matchedCourses_Collection(email, approved_status, courseID, matchedCourses_Collection, msg):
    matchedCourse = {"email": email,
                     "approved": approved_status,
                     "courseID": courseID,
                     "latest_updated": date.today()
                     }
    matchedCourses_Collection.append(matchedCourse)
    #print(msg)


def update_student_arrange_student(matchedCourses_Collection):
    msgs = update_student_arrange_student_for_Matcher(matchedCourses_Collection)

    #for msg in msgs:
        #print(msg)


def populate_matchedCourses_Collection(matchedCourses_Collection):
    msg = populate_matchedCourses_Collection_for_Matcher(matchedCourses_Collection)

    #print(msg)


def remove_unsuitable_student_from_course_candidate_list(emails, courseID, not_preferred_stu_emails,
                                                         should_courseTaken):
    print("In the remove_unsuitable_student_from_course_candidate_list function call:")
    # remove not suitable students from the course's student list
    for email in reversed(emails):
        preferenceLevel, courseTaken = get_student_preferenceLevel_and_courseTaken(email, courseID)

        is_not_preferred_stu = email in not_preferred_stu_emails

        if (preferenceLevel == "No") or (is_not_preferred_stu is True) or \
                (should_courseTaken is True and courseTaken is False):
            emails.remove(email)

            print("Remove %s from %s." % (email, courseID))


def assign_faculty_preferred_students_to_course(courseID, quota_of_pos, to_share_student,
                                                      share_student_dict, share_student_res_dict,
                                                      preferred_stu_emails, matchedCourses_Collection):
    #print("In the assign_faculty_preferred_students_to_course function call:")
    #print("courseID: %s" % courseID)
    # assign faculty-preferred students to course quotas
    for preferred_stu_email in preferred_stu_emails:
       #print("preferred_stu_email: %s" % preferred_stu_email)
        if quota_of_pos > 0:
            share_student_res_dict[courseID] = to_share_student
            if courseID[-1] == 1:
                if to_share_student:
                    share_student_dict[courseID] = preferred_stu_email
                email = preferred_stu_email
            else:
                index = 11
                section = "1"
                courseID_section1 = courseID[:index] + section + courseID[index + 1:]
                res = share_student_res_dict[courseID_section1]
                if res:
                    email = share_student_dict[courseID_section1]
                else:
                    email = preferred_stu_email
            msg = "Successfully assign faculty-preferred %s to %s!" % (email, courseID)
            set_matchedCourse_into_matchedCourses_Collection(email, True, courseID,
                                                             matchedCourses_Collection, msg)
            quota_of_pos -= 1
        else:
            print("No quota left in %s for faculty_preferred %s." % (courseID, preferred_stu_email))
    return quota_of_pos


def assign_null_email_to_left_quota(quota_of_pos, courseID, matchedCourses_Collection):
    for i in range(quota_of_pos):
        email = ""
        approved_status = False
        msg = "Assign No.%s empty email(s) to %s." % (i + 1, courseID)

        set_matchedCourse_into_matchedCourses_Collection(email, approved_status, courseID,
                                                         matchedCourses_Collection, msg)


def loop_each_course_to_assign_student(courseIDs, share_student_dict, share_student_res_dict,
                                       matchedCourses_Collection):
    print("\nIn the loop_each_course_to_assign_student function call:")
    for courseID in courseIDs:
        print("In course: ", courseID)
        emails = get_student_emails()
        quota_of_pos, not_preferred_stu_emails, preferred_stu_emails, should_courseTaken, to_share_student = \
            get_faculty_requirements(courseID)

        # remove not suitable students from the course's student list
        remove_unsuitable_student_from_course_candidate_list(emails, courseID, not_preferred_stu_emails,
                                                             should_courseTaken)

        # assign course faculty's preferred students
        get_student_priority_sort(preferred_stu_emails, courseID)

        # assign faculty-preferred students to course quotas
        quota_of_pos = assign_faculty_preferred_students_to_course(courseID, quota_of_pos, to_share_student,
                                                                         share_student_dict, share_student_res_dict,
                                                                         preferred_stu_emails,
                                                                         matchedCourses_Collection)
        #assign_null_email_to_left_quota(quota_of_pos, courseID, matchedCourses_Collection)
        print("")


def start_matching():
    courseIDs = get_courseIDs_for_Matcher()
    share_student_dict = {}
    share_student_res_dict = {}
    matchedCourses_Collection = []

    loop_each_course_to_assign_student(courseIDs, share_student_dict, share_student_res_dict, matchedCourses_Collection)

    update_student_arrange_student(matchedCourses_Collection)
    populate_matchedCourses_Collection(matchedCourses_Collection)

    for matchedCourse in matchedCourses_Collection:
        print(matchedCourse)

    return "\nCongrats!! You have populated matchedCourses_collection successfully."

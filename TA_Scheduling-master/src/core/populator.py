import csv
import codecs
from io import StringIO
import sys, re
import traceback
from typing import List
from src.schemas.FacResponse import FacResponse
from src.schemas.StudentResponse import StudentResponse, StudentCourse
from src.schemas.course import Course, CourseManual, MatchedCourse
from src.db import DBQuerrier
from src.integration import util
from fastapi import UploadFile


def parse_course_file(
    input_file,
    db
):  
    """
    input_file: the file object to be read
    db: the intended collection to have data populated


    #data = Course(**{'courseID': rows['Section'],
                     'enrollment': rows['StudentCount'],
                     'courseName': rows['CourseTitle'],
                     'courseSection': row['']
                     'faculty': rows['Faculty']})
    """
    returnData = []
    try:
        #read the bytes into the csv reader
        csvReader = csv.DictReader(codecs.iterdecode(input_file, 'utf-8-sig'))

        for row in csvReader:
            #need to rule out the ones we don't need
            good_to_go = check_course_row(row)
            if not good_to_go:
                continue
            
            #each row will be a dict, we only extract what we need to save
            row['hours_allowed'] = get_hours(row['StudentCount'])
            #skip if not qualified for support
            if row['hours_allowed'] == 0: continue
            data = Course(**row)
            
            returnData.append(data.dict())
        print(returnData)
        saved =True #DBQuerrier.courses_insert_many(returnData)
        if saved:
            return returnData
        else:
            raise Exception
        
    except Exception as e:
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        raise Exception


def get_hours(e, support_type = '') -> int:
    """
    # students                          # hours per week
    0-14                                      0
    15-19                                     5
    20-24                                     7
    25-29                                     10
    30-34                                     12
    35-40                                     15
    > 40                                      18
 
    Others ---- Prof. Hanks will decide their hours
    Boot Camp (Summer and Winter) -- 40 hours per week (4 x 10 hours per week)?  More in Summer? 
    Professional Development -- 5 hours per week
    Tutors -- 20 hours per week
    """
    try:
        enrollment = int(e)
    except Exception as err:
        print(traceback.format_exc())
        print('StudentCount was not a valid number')

    #dict of hours and corresponding max enrollment # for each
    hours = {0 : 14, 5: 19, 7: 24, 10: 29, 12: 34, 15 : 40, 18: 100}

    #loop through the dict, check against upper bound of enrollment
    for h in hours:
        #check if course enrollment is below upper bound
        if enrollment <= hours[h]:
            return h
    
    #tutor hours is unclear

    #1230, 1420, 1430, and 2430 - will establish a tutoring pool
    #facuties can request Grader/TA in addition
    pass

def check_course_row(row) -> bool:
    """
    Return false for internships, courses with only 1 student, projects
    Otherwise, return True
    """
    kw = ['Project', 'Internship']
    for k in kw:
        if k in row['CourseTitle']:
            return False
    
    #last check for other courses with only 1 student
    if int(row['StudentCount']) <= 1:
        return False

    return True

def parse_faculty_response(
    input_bytes
):
    YES = "1"
    NO = "2"

    file = StringIO(input_bytes.decode())
    
    #print(file)
    try:
        #read the bytes into the csv reader
        csvReader = csv.DictReader(file, delimiter=",")#codecs.iterdecode(file, 'utf-8-sig'))
        data = []
        matchedCourses = []
        for row in csvReader:
            good_to_go = check_response_row(row)

            #FIXME: ASSUMING FACULTIES ENTERED VALID COURSE ID IN THE SURVEY
            row['hoursAllowed'] = DBQuerrier.get_hours_from_course(row['Q3'])
            if not good_to_go or row['hoursAllowed'] == 0:
                continue
            
            #Extra processing when faculties need specific students arranged or ignored.
            row['Q8'] = (row['Q8#1'].replace(' ', '')).split(',') if row['Q8'] == YES else [] 
            row['Q9'] = (row['Q9#1'].replace(' ', '')).split(',') if row['Q9'] == YES else []

            #each row will be a dict, we only extract what we need to save
            r = FacResponse(**row)
            
            #also generate the matchedCourse document also based on quota
            for i in range(0, r.number_needed):
                matchedCourses.append(MatchedCourse(**{'courseID':r.courseID}).dict())
            
            data.append(r.dict())
        #print(matchedCourses)
        inserted = DBQuerrier.matched_courses_insert_many(matchedCourses)
        if not inserted: raise Exception

        updated = DBQuerrier.faculty_response_insert_many(util.translate(data))

        return data if updated else None
    except Exception as e:
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        raise Exception

def check_response_row(row) -> bool:
    """
    Skip on rows that are for meta data (for now, the first 2 rows), 
    and rows that doesn't have a faculty last and first names (either or will work since we can
    narrow them down by course id).
    """
    excludes = ('User Language', "{\"ImportId\":\"userLanguage\"}")

    if row['UserLanguage'] in excludes or row['Q2'] == '':
        #[Q2] may change with the new model
        return False

    return True

def parse_course_list(courses:List[CourseManual]) -> bool:
    #quick input check
    data = []
    for course in courses:
        data.append(course.dict())

    try:  
        DBQuerrier.courses_insert_many(data)
        return True
    except Exception as e:
        print('Encountered error while saving to db: ', e)
        return False
    
def parse_student_response(
    input_bytes
):
    file = StringIO(input_bytes.decode())
    try:
        #read the bytes into the csv reader
        csvReader = csv.DictReader(file, delimiter=",")#codecs.iterdecode(file, 'utf-8-sig'))
        student_data = []
        student_course_data= []
        courseIDs = []
        #TODO: FIGURE OUT THE DATA LOSS FROM QUALTRICS
        #must process the first metadata row to extract courseIDs
        for row in csvReader:
            if len(courseIDs) == 0: 
                courseIDs = extract_courses(row)
            
            good_to_go = check_response_row(row)
            if not good_to_go:
                continue
            #print(row)
            
            #extract answers for arranged instructor into a list, just in case > 1
            row['Q7'] = row['Q7'].split(',')

            #each row will be a dict, we only extract what we need to save
            r = StudentResponse(**row).dict()

            #each row contains course preference, each course has data across 3 columns
            #get the total number of courses put on the survey
                #count = DBQuerrier.count_courses_with_hours()
            for i in range(0, len(courseIDs)):
                #skip those with empty preference fields
                if row['Q8#1_{}'.format(i+1)] == '':
                    print('empty, skipping student ', r['email'])
                    continue
                try:
                    courseID = courseIDs[i]
                    student_course = StudentCourse(**{
                        #course IDs would be in the section Q8#1_{index} with preference level also
                        'preferenceLevel' : row['Q8#1_{}'.format(i+1)],
                        #courseTaken in Q8#2_{index}
                        'courseTaken' : row['Q8#2_{}'.format(i+1)],
                        #course_GPA in Q8#3_{index}
                        'course_GPA' : row['Q8#3_{}'.format(i+1)],
                        'courseID': courseID, 
                        'email': r['email']
                    })
                    student_course_data.append(student_course.dict())
                    
                except Exception as e:
                    print(e)
                    print(row)
        
            student_data.append(r)
        # print(student_data)
        # print(student_course_data)
        updated = DBQuerrier.student_response_insert_many(util.translate(student_data),\
                                                          util.translate(student_course_data))

        return True if updated else False
    except Exception as e:
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        raise Exception
    
def extract_courses(row):
    courseIDs = []
    for col in row:
        if 'Q8#1' in col:
            #extract course ID
            match = re.search("CPSC-(\d+)-(\d{2})", row[col])
            if match: 
                id = match.group(0)
                courseIDs.append(id)
                #print(col)

    return courseIDs
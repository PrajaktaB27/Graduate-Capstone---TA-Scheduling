def export_assignment_table(db) -> dict:
    # ["courseID", "Instructor", "Assignee", "Support type"]
    
    #get all approved records
    data = db['matchedCourses'].find({'email':{ '$exists': True, '$ne': '' }})
    returnData = []

    for item in data:
        # use courseID to find support_type & instructor email from Faculty_course
        fac = db['Faculty_Course'].find({'courseID': item['courseID']})[0]

        # get courseID, student_email
        val = {'courseID': item['courseID'],
               'student_email': item['email'],
               'instructor_email': fac['email'],
               'support_type': fac['support_type']}

        returnData.append(val)
    #print(returnData)
    return returnData


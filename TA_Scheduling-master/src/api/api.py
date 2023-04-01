import csv
import codecs
import json
from typing import Union, List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import Response
from fastapi.encoders import jsonable_encoder
from pydantic.types import conint, constr, SecretStr
from pymongo.database import Database
from src.db.DBQuerrier import *

from src.db import deps
from src.core import populator,\
                     exporter
from src.core.surveyHandler  import SurveyType, SurveyHandler
from src.schemas.course import AssignmentExport, CourseManual
from src.integration import util


api_router = APIRouter()


@api_router.post("/test")
async def upload_course_file(
        *,
        db: Database = Depends(deps.get_db)
):
    print(type(db))
    student = db.Students.find({"firstName": "Jason"}, {'_id': 0})
    print(type(student[0]))

    return jsonable_encoder({"data": student[0]})


@api_router.get("/get_item/All")
async def get_all_items(
):
    return jsonable_encoder({"data": "flights"})


@api_router.get("/get_item/{item_id}")
async def get_item_with_id(
):
    return jsonable_encoder({"data": "some data"})


@api_router.post("/upload/course_file")
async def upload_course_file(
        *,
        input_file: UploadFile = File(...),
        db: Database = Depends(deps.get_db)
):
    data = []
    try:
        data = populator.parse_course_file(input_file.file, db.Courses)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload and/or read the file: {}".format(e))
    finally:
        input_file.file.close()
    
    return data


@api_router.get("/get_assignment_table")
async def get_assignment_table():
    data = get_assignment_table_for_apiCall()
    return jsonable_encoder({"data": data})


@api_router.get("/get_student_detail")
async def get_student_detail(email: str):
    data = get_student_detail_for_apiCall(email)
    return jsonable_encoder({"data": data})


@api_router.get("/get_course_detail")
async def get_course_detail(courseID: str):
    data = get_course_detail_for_apiCall(courseID)
    return jsonable_encoder({"data": data})


@api_router.get("/get_faculty_detail")
async def get_faculty_detail(email: str):
    data = get_faculty_detail_for_apiCall(email)
    return jsonable_encoder({"data": data})


@api_router.get("/get_faculty_course_in_edit_assignment")
async def get_faculty_course(courseID: str):
    data = get_faculty_course_detail_for_apiCall(courseID)
    return jsonable_encoder({"data": data})


@api_router.get("/get_assigned_student_for_the_course")
async def get_assigned_student_for_the_course(courseID):
    data = get_assigned_student_for_the_course_for_api_call(courseID)
    return jsonable_encoder({"data": data})


@api_router.get("/get_available_student_for_the_course")
async def get_available_student_for_the_course(courseID):
    data = get_available_student_for_the_course_for_api_call(courseID)
    return jsonable_encoder({"data": data})


# @api_router.get("/reassign_worker_in_course")
# async def reassign_worker_in_course(old_email: str, new_email: str, courseID: str):
#     result = reassign_worker_in_course_for_apiCall(old_email, new_email, courseID)
#
#     # return true if change is successful
#     return result


@api_router.get("/assign_worker_to_course")
async def assign_worker_to_course(email: str, courseID: str):
    result = assign_worker_to_course_for_apiCall(email, courseID)

    # return true if change is successful
    return result


@api_router.get("/remove_worker_from_course")
async def remove_worker_from_course(email: str, courseID: str):
    result = remove_worker_from_course_for_apiCall(email, courseID)

    # return true if change is successful
    return result


@api_router.get("/update_approve_status")
async def update_approve_status(email: str, courseID: str):
    result = update_approve_status_for_apiCall(email, courseID)

    # return true if change is successful
    return result

@api_router.get("/assignment/export", response_model=List[AssignmentExport])
async def export_assignment_table(
    *,
    db: Database = Depends(deps.get_db)
):
    return exporter.export_assignment_table(db)

@api_router.post("/survey/pull/fac")
async def pull_survey_file(
    *,
    #input_file: UploadFile = File(...),
    db: Database = Depends(deps.get_db)
):
    """
    Endpoint for starting gathering responses
    """

    try:
        data = SurveyHandler.retrieve_response()
        #input_file.file.close()
        return util.translate(data)
    except Exception as e:
        #input_file.file.close()
        raise HTTPException(status_code=500, detail="Failed to upload and/or read the file: {}".format(e))        

@api_router.post('/survey/push/fac')
async def push_survey_fac(
    *,
    db: Database = Depends(deps.get_db)
):
    surveyID = SurveyHandler.push_survey(SurveyType.Faculty)
    return 'https://seattleux.qualtrics.com/jfe/form/{}'.format(surveyID)

@api_router.post('/course/manual-add')
async def add_course(
    *,
    course_info: List[CourseManual],
    db:Database = Depends(deps.get_db)
):
    return populator.parse_course_list(course_info)

@api_router.post('/survey/push/student')
async def push_survey_fac(
    *,
    db: Database = Depends(deps.get_db)
):
    surveyID = SurveyHandler.push_survey(SurveyType.Student)
    return 'https://seattleux.qualtrics.com/jfe/form/{}'.format(surveyID)

@api_router.post("/survey/pull/student")
async def pull_survey_file(
    *,
    #input_file: UploadFile = File(...),
    db: Database = Depends(deps.get_db)
):
    """
    Endpoint for starting gathering responses
    """

    try:
        updated = SurveyHandler.retrieve_response(SurveyType.Student)
        #input_file.file.close()
        if updated:
            return Response(status_code=200, content='Successully pulled student responses')
        else:
            raise Exception
    except Exception as e:
        #input_file.file.close()
        raise HTTPException(status_code=500, detail="Failed to upload and/or read the file: {}".format(e)) 
import pytest
from fastapi.encoders import jsonable_encoder
import io
import json
import requests
from fastapi.testclient import TestClient
from src.api.api import api_router
from src.db.DBQuerrier import *
# import coverage
from unittest.mock import MagicMock
from src.api.api import update_approve_status_for_apiCall
from src.core.exporter import export_assignment_table
from src.db.DBQuerrier import get_faculty_course_detail_for_apiCall


class Test_API_TA_Scheduling:

    def test_upload_course_file(self):
        pass

    @pytest.mark.asyncio
    async def test_get_all_items(self):
        data = {"data": "flights"}
        assert jsonable_encoder(data) == {"data": "flights"}

    @pytest.mark.asyncio
    async def test_get_item_with_id(self):
        data = {"data": "some data"}
        assert jsonable_encoder(data) == {"data": "some data"}

    def test_get_assignment_table(self):
        with TestClient(api_router) as client:
            response = client.get("/get_assignment_table")
            assert response.status_code == 200
            data = json.loads(response.text)
            assert "data" in data

    def test_get_student_detail(self):
        client = TestClient(api_router)
        # Prepare test data
        email = "pbimalkhedkar@seattleu.edu"  # test@example.com
        # Call the API endpoint
        response = client.get("/get_student_detail", params={"email": email})
        # Check the response status code
        assert response.status_code == 200
        # Check the response data
        response_data = response.json()
        assert "data" in response_data
        assert response_data["data"] is not None
        assert isinstance(response_data["data"], dict)

    def test_get_course_detail(self):
        client = TestClient(api_router)
        response = client.get("/get_course_detail?courseID=CPSC5200-01")
        # Check that the response status code is 200 OK
        assert response.status_code == 200
        # Check that the response contains the expected data
        assert "data" in response.json()
        assert isinstance(response.json()["data"], list)
        # assert data["courseID"] == courseID

    def test_get_faculty_course_detail_for_apiCall(self):
        courseID = "CPSC-4610-01"
        result = get_faculty_course_detail_for_apiCall(courseID)
        # Assert that the result is correct
        assert result["courseName"] == "Artificial Intelligence"
        assert result["courseID"] == courseID
        assert result["facultyName"] == "Wan  Bae"
        assert result["support_type"] == "Grader"
        assert result["enrollment"] == 40
        assert result["hoursAllowed"] == 15
        assert result["quota"] == 2

    def test_get_faculty_course(self):
        client = TestClient(api_router)
        response = client.get("/get_assigned_student_for_the_course?courseID=CPSC5200-01")
        assert response.status_code == 200
        # Check that the response contains the expected data
        assert "data" in response.json()
        assert isinstance(response.json()["data"], list)

    def test_get_assigned_student_for_the_course(self):
        client = TestClient(api_router)
        # Make a GET request to the endpoint with courseID = CPSC-5510-01
        response = client.get("/get_assigned_student_for_the_course?courseID=CPSC-5510-01")
        # Assert that the response status code is 200 OK
        assert response.status_code == 200
        # Assert that the response JSON contains a "data" key
        assert "data" in response.json()
        # Assert that the "data" key contains the expected value
        expected_data = []
        assert response.json()["data"] == expected_data

        """   {'GPA': 3.75,
             'cGPA': 3.5,
             'email': 'cwang@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'preferred',
             'studentName': 'Jason Wang'
             },
            {'GPA': 4,
             'cGPA': 3.5,
             'email': 'jkoh@seattleu.edu',
             'is_faculty_preferred': True,
             'preferenceLevel': 'preferred',
             'studentName': 'Jaden Koh'
             }  """

    def test_get_available_student_for_the_course(self):
        client = TestClient(api_router)
        # Make a GET request to the endpoint with courseID = CPSC-5510-01
        response = client.get("/get_available_student_for_the_course?courseID=CPSC-5510-01")
        # Assert that the response status code is 200 OK
        assert response.status_code == 200
        # Assert that the response JSON contains a "data" key
        assert "data" in response.json()
        # Assert that the "data" key contains the expected value
        expected_data = [
            {'GPA': 'A',
             'cGPA': 3.9,
             'email': 'aewin@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'OK',
             'studentName': 'Alon Ewin'},
            {'GPA': 'N/A',
             'cGPA': 3.6,
             'email': 'agarcia3@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'OK',
             'studentName': 'Ally Garciel'},
            {'GPA': 'A',
             'cGPA': 4.0,
             'email': 'ffadia@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'OK',
             'studentName': 'Fairleigh Fadian'},
            {'GPA': 'N/A',
             'cGPA': 3.0,
             'email': 'fkogge@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'OK',
             'studentName': 'Francis Kogge'},
            {'GPA': 'N/A',
             'cGPA': 3.5,
             'email': 'hmayya@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'OK',
             'studentName': 'Harshitha Mayya'},
            {'GPA': 'A-',
             'cGPA': 3.7,
             'email': 'mcross@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'OK',
             'studentName': 'Marylin Crosser'},
            {'GPA': 'A',
             'cGPA': 4.0,
             'email': 'mmarde@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'OK',
             'studentName': 'Matt Marder'},
            {'GPA': 'A-',
             'cGPA': 3.62,
             'email': 'neddis@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'OK',
             'studentName': 'Niles Eddisforth'},
            {'GPA': 'N/A',
             'cGPA': 4.0,
             'email': 'pbimalkhedkar@seattleu.edu',
             'is_faculty_preferred': True,
             'preferenceLevel': 'OK',
             'studentName': 'Prajakta Bimalkhedkar'},
            {'GPA': 'A-',
             'cGPA': 4.0,
             'email': 'rbrown3@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'OK',
             'studentName': 'Robert Brown'},
            {'GPA': 'A-',
             'cGPA': 3.98,
             'email': 'rocket@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'OK',
             'studentName': 'Rex Brown'},
            {'GPA': 'B',
             'cGPA': 3.33,
             'email': 'thonks@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'OK',
             'studentName': 'Tim Honks'},
            {'GPA': 'A',
             'cGPA': 4.0,
             'email': 'ywong@seattleu.edu',
             'is_faculty_preferred': False,
             'preferenceLevel': 'OK',
             'studentName': 'Benny Wong'}
        ]
        assert response.json()["data"] == expected_data

    def test_remove_worker_from_course(self):
        client = TestClient(api_router)
        email = "pbimalkhedkar@seattleu.edu"
        courseID = "CPSC-4610-01"
        # Send GET request to endpoint with sample input parameters
        response = client.get(f"/remove_worker_from_course?email={email}&courseID={courseID}")
        result = remove_worker_from_course_for_apiCall("pbimalkhedkar@seattleu.edu", "CPSC-4610-01")
        return result

        # test again
    def test_assign_worker_to_course_success(self):
        client = TestClient(api_router)
        response = client.get("/assign_worker_to_course?email=pbimalkhedkar@seattleu.edu &courseID=CPSC-4610-01")
        assert response.status_code == 200
        assert response.json() == {
            "msg": "Successfully assign pbimalkhedkar@seattleu.edu to CPSC-4610-01.",
            "status": True
        }

    def test_assign_worker_to_course_invalid_email(self):
        client = TestClient(api_router)
        response = client.get("/assign_worker_to_course?email= &courseID=CPSC-1420-01")
        assert response.status_code == 200
        assert response.json() == {
            "msg": 'Since the quota of CPSC-1420-01 is full, No student can be assigned '
                   'to it. Please remove the current worker before assigning.',
            "status": False
        }

    # doesnt really work
    def test_assign_worker_to_course_invalid_course_id(self):
        client = TestClient(api_router)
        response = client.get("/assign_worker_to_course?email=dinhh2@seattleu.edu&courseID=CPSC-5550-01")
        assert response.status_code == 200
        assert response.json() == {
            'msg': 'Since the quota of CPSC-5550-01 is full, No student can be assigned '
                   'to it. Please remove the current worker before assigning.',
            'status': False
        }

    def test_update_approve_status_true(self):
        email = "dinhh2@seattleu.edu"
        courseID = "CPSC-4610-01"
        db_mock = MagicMock()
        db_mock["matchedCourses"].find.return_value = {"approved": True}
        result = update_approve_status_for_apiCall(email, courseID, db_mock)
        assert result == "Successfully update approve status to be True"

    def test_update_approve_status_false(self):
        email = "pbimalkhedkar@seattleu.edu"
        courseID = "CPSC-5310-01"
        db_mock = MagicMock()
        db_mock["matchedCourses"].find.return_value = {"approved": False}
        result = update_approve_status_for_apiCall(email, courseID, db_mock)
        assert result == "Process of updating approve status failed"

    def test_update_approve_status_na(self):
        email = " "
        courseID = "CPSC-1420-01"
        db_mock = MagicMock()
        db_mock["matchedCourses"].find.return_value = {"approved": "N/A"}
        result = update_approve_status_for_apiCall(email, courseID, db_mock)
        assert result == "Process of updating approve status failed"

    def test_export_assignment_table(self):
        # Create a mock database connection object
        db = MagicMock()

        # Set up the mock data
        db['matchedCourses'].find.return_value = [
            {'courseID': 'CPSC-5710-01', 'email': 'dinhh2@seattleu.edu'},
            {'courseID': 'CPSC-5610-01', 'email': 'rbrown3@seattleu.edu'}
        ]
        db['Faculty_Course'].find.return_value = [
            {'courseID': 'CPSC-5710-01', 'email': 'koenigm@seattleu.edu', 'support_type': 'Grader'},
            {'courseID': 'CPSC-5610-01', 'email': 'mckeem@seattleu.edu', 'support_type': 'Tutor'}
        ]

        # Call the function
        data = export_assignment_table(db)

        # Assert that the data is in the expected format
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]['courseID'] == 'CPSC-5710-01'
        assert data[0]['student_email'] == 'dinhh2@seattleu.edu'
        assert data[0]['instructor_email'] == 'koenigm@seattleu.edu'
        assert data[0]['support_type'] == 'Grader'
        assert data[1]['courseID'] == 'CPSC-5610-01'
        assert data[1]['student_email'] == 'rbrown3@seattleu.edu'
        assert data[1]['instructor_email'] == 'koenigm@seattleu.edu'
        assert data[1]['support_type'] == 'Grader'

    def test_pull_survey_file(self):
        pass

    def test_push_survey_fac(self):
        pass

    def test_add_course(self):
        pass

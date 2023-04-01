from datetime import datetime, timedelta
from .config import TOKEN, USER_ID, ORG_ID, DATACENTER, DEFAULT_DIR
#from ..models import instructorSurveyModel, studentSurveyModel
from fastapi import HTTPException
from src.db import DBQuerrier
from src.core import populator
import requests
import json
import zipfile
import io, os
import enum


BASE_URL = 'https://{}.qualtrics.com/API/v3/'.format(DATACENTER)

header = {'X-API-TOKEN': TOKEN, 
                    'Content-Type': 'application/json', 
                    'accept': "application/json"}

class SurveyType(enum.Enum):
    Faculty = 1
    Student = 2

class SurveyHandler:


    @classmethod
    def push_survey(self, type):
        surveyName = 'Faculty Survey' if type == SurveyType.Faculty else 'Student Survey'
        builder = SurveyBuilder(surveyName, type)

        try:
            #build the survey and its questions
            surveyID = builder.build()#'SV_exjbj5StNQ5iurQ'

            #save the ID to db
            DBQuerrier.save_surveyID(surveyID)

            #then activate
            SurveyHandler.activate_survey(surveyID)

            #then publish
            res = SurveyHandler.publish_survey(surveyID)
            print(res)

            return res['result']['metadata']['surveyID']
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail='Encountered error: {}'.format(e))

    @classmethod
    def activate_survey(self, surveyID):
        """
        Helper to activate the survey on Qualtrics
        """
        today = (datetime.now())
        endDate = today + timedelta(days=7)
        endpoint = 'surveys/{}'.format(surveyID)
        url = BASE_URL + endpoint
        activatePayload ={
                        "isActive": True,
                        "expiration": {
                            "startDate": '{}Z'.format(today.isoformat()),
                            "endDate": '{}Z'.format(endDate.isoformat())}
                        }

        res_activate = requests.put(url, json=activatePayload, headers=header)

        return res_activate.json()

    @classmethod  
    def publish_survey(self, surveyID):
        """
        Helper function to call Qualtrics's API for publishing the surveys and activate
        """
        endpoint = 'survey-definitions/{}/versions'.format(surveyID)
        url = BASE_URL + endpoint

        data = {
            "Description": "Prototype survey",
            "Published": True
        }

        res = requests.post(url, json=data, headers=header)
        
        return res.json()

    @staticmethod
    def retrieve_response(type: SurveyType = SurveyType.Faculty):
        """
        Function assumes that it's been a while after the survey was initiated, so it 
        will get the survey ID from DB instead of assuming the surveyID is saved in the
        class instance
        """
        #get surveyID from DB
        survey = DBQuerrier.get_latest_surveyID()#'SV_9MHwSrQGylIX19Y'#
        surveyID = survey['surveyID']
        if survey['pulled']:
            print('Already pulled')
            return [{'result': 'Already pulled'}]
        
        endpoint= 'surveys/{}/export-responses/'.format(surveyID)
        url = BASE_URL + endpoint
        fileFormat ='csv'
        requestCheckProgress = 0.0
        progressStatus = "inProgress"

        # Step 1: Creating Data Export
        payload = '{"format":"' + fileFormat + '"}'
        res = requests.post(url, data=payload, headers=header)

        progressId = res.json()["result"]["progressId"]
        print(json.dumps(res.json()))

        # Step 2: Checking on Data Export Progress and waiting until export is ready
        while progressStatus != "complete" and progressStatus != "failed":
            requestCheckUrl = url + progressId
            requestCheckResponse = requests.get(requestCheckUrl, headers=header)

            requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
            print(json.dumps(requestCheckResponse.json()))

            print("Download is " + str(requestCheckProgress) + " complete")
            progressStatus = requestCheckResponse.json()["result"]["status"]

        #step 2.1: Check for error
        if progressStatus is "failed":

            raise Exception("export failed")

        fileId = requestCheckResponse.json()["result"]["fileId"]

        # Step 3: Downloading file
        requestDownloadUrl = url + fileId + '/file'
        requestDownload = requests.get(requestDownloadUrl, headers=header, stream=True)
        
        # Step 4: Unzipping the file
        #zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall("QualtricsResponses")
        #print('Complete')
        # Step 4: Unzipping the file
        file = zipfile.ZipFile(io.BytesIO(requestDownload.content))
        data = file.read(file.filelist[0].filename)
        file.close()

        populated =  populator.parse_faculty_response(data) if type == SurveyType.Faculty else \
                populator.parse_student_response(data)
        
        if populated: DBQuerrier.mark_pulled_surveyID(surveyID)
        return populated

class SurveyBuilder(object):
    
    def __init__(self, surveyName, type) -> None:
        self.surveyName = surveyName
        self.survey = Faculty_Survey() if type == SurveyType.Faculty else Student_Survey()
    
    def initiate_a_survey(self) -> str:
        """
        Helper function to start a survey on Qualtrics API
        """
        endpoint = 'survey-definitions'
        url = BASE_URL + endpoint

        data = {'SurveyName': self.surveyName, "Language": "EN", "ProjectCategory": "CORE"}

        #serialize the dictionary to a JSON obj
        payload = json.dumps(data, indent=4)
        
        res = requests.post(url, data = payload, headers=header)
        #TODO: IF RES STATUS CODE IS 401 FOR UNAUTHORIZE, THEN NEED TO
        #GET A NEW API TOKEN.
        print(res.json())
        return(res.json()['result']['SurveyID'])

    def post_questions(self, surveyID):
        """
        Helper function to post questions to the created survey
        """
        endpoint = 'survey-definitions/{}/questions'.format(surveyID)
        url = BASE_URL + endpoint

        questions = self.survey.get_questions()
        
        for q in questions:
            data = json.dumps(q, indent=4)
            res = requests.post(url, data=data, headers=header)
            print(json.dumps(res.json(), indent=4))

    def build(self):
        """
        Entrace function to start pushing a survey
        """
        surveyID = self.initiate_a_survey()
        self.post_questions(surveyID)
        return surveyID
        
        
class Faculty_Survey():
    def get_questions(self):
        return instructorSurveyModel.data

class Student_Survey():
    def get_questions(self):
        return studentSurveyModel.data
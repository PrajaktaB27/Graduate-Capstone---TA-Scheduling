import http from "../http-common";

class PushStudentSurvey {
    async push_student_survey(id){
        return http.post(`survey/push/student`);
    }
}

export default new PushStudentSurvey();
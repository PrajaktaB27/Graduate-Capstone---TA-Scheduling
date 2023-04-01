import http from "../http-common";

class PullStudentSurvey {
    async pull_student_survey(){
        return http.post(`survey/pull/student`);
    }
}

export default new PullStudentSurvey();
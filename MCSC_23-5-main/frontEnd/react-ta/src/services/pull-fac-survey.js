import http from "../http-common";

class PullFacSurvey {
    async pull_faculty_survey(){
        return http.post(`survey/pull/fac`);
    }
}

export default new PullFacSurvey();
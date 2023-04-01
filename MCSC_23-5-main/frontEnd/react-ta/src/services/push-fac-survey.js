import http from "../http-common";

class PushFacSurvey {
    async push_fac_survey(){
        return http.post(`survey/push/fac`);
    }
}

export default new PushFacSurvey();
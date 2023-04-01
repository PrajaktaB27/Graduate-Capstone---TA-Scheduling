import http from "../http-common";

class PreMatchStudent {
    async pre_match_students(){
        return http.get(`pre_match_students`);
    }
}

export default new PreMatchStudent();
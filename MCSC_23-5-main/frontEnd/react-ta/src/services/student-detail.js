import http from "../http-common";

class StudentDetail {
    async get_student_detail(id){
        return http.get(`get_student_detail?email=${id}`);
    }
}

export default new StudentDetail();
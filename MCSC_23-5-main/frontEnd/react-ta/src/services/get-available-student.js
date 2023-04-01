import http from "../http-common";

class GetAvailableStudent {
    async get_available_student(id){
        return http.get(`get_available_student_for_the_course?courseID=${id}`);
    }
}

export default new GetAvailableStudent();
import http from "../http-common";

class GetAssignStudent {
    async get_assign_student(id){
        return http.get(`get_assigned_student_for_the_course?courseID=${id}`);
    }
}

export default new GetAssignStudent();
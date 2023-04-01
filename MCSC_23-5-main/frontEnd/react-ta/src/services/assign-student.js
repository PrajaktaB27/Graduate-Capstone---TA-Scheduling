import http from "../http-common";

class AssignStudent {
    async assign_student(email, id){
        return http.get(`assign_worker_to_course?email=${email}&courseID=${id}`);
    }
}

export default new AssignStudent();
import http from "../http-common";

class UnAssignStudent {
    async un_assign_student(email, id){
        return http.get(`remove_worker_from_course?email=${email}&courseID=${id}`);
    }
}

export default new UnAssignStudent();
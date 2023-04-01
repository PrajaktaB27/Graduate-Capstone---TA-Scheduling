import http from "../http-common";

class AssignmentTableService {
    async get_assignment_table(){
        return http.get('assignment/export');
    }
}

export default new AssignmentTableService();
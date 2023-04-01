import http from "../http-common";

class GetAssignmentTable {
    async get_assignment_table(){
        return http.get(`get_assignment_table`);
    }
}

export default new GetAssignmentTable();
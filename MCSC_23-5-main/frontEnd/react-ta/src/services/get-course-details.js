import http from "../http-common";

class GetCourseDetails {
    async get_course_details(id){
        return http.get(`get_faculty_course_in_edit_assignment?courseID=${id}`);
    }
}

export default new GetCourseDetails();
import http from "../http-common";

class CourseService {
    upload_course(file, onUploadProgress){
        let formData = new FormData();

        formData.append("input_file", file);

        return http.post('upload/course_file', formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
            onUploadProgress,
        });
    }

    post_course(body){
        return http.post('course/manual-add', body);
    }
}
export default new CourseService();

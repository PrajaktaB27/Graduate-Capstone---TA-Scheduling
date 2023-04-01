import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from "react-router-dom";
import { AiFillStar } from "react-icons/ai";
import Swal from 'sweetalert2'
import './studentworkerstyle.css';
import StudentDetail from '../../services/student-detail';
import ReactLoading from 'react-loading'

const StudentWorker = () => { 

    // to set position for loading spinning icon
    const styles = { position: "fixed", bottom: "50%", left: "50%" };

    const navigate = useNavigate();

    const dataFetch = useRef(false);

    // to get the id from previous page (edit assignment page)
    const { id } = useParams();

    // added a linee
    const ColoredLine = ({ color }) => (
        <hr
            style={{
                color: color,
                backgroundColor: color,
                height: 0.5,
            }}
        />
    );

    // to finish loading spinning
    const [done, setDone] = useState(false);
    
    // save student data
    const [studentData, setStudentData] = useState({
        data: 
        {
            student: '',
            email: '',
            cGPA: 0.0,
            is_employee: '',
            facultyArr: [],
            facultyRef: [],
            assigned_courses:
            [
                {
                    courseID: '',
                    courseName: '',
                    support_type: ''
                }
            ],
            courses_preferences: 
            [
                {
                courseName: '',
                courseID: '',
                support_type: '',
                preferenceLevel: '',
                GPA: '',
                is_faculty_preferred: false
                }
            ],
            comments: []
        }
    })

    // calling get student details API from back end
    const fetchData = () => {
        StudentDetail.get_student_detail(id)
        .then(res => {
            console.log(res.data);
            setStudentData(res.data);
            setDone(true);
        })
        .catch(error => {
            Swal.fire(`${error}`, '','error')
            console.log(error);
        })
    }

    useEffect(() => {
        if (dataFetch.current) return;
        dataFetch.current = true;
        fetchData()
    }, [])
    
    // add comma between first and last name
    const addComma = (name) => {
        return name.split(" ").join(", ");
    }

    const convertGPAtoLetter = (GPA) => {
        if (GPA >= 3.68)
            return "A";
        else if (GPA >= 3.34)
            return "A-";
        else if (GPA >= 3.01)
            return "B+";
        else if (GPA >= 2.68)
            return "B";
        else if (GPA >= 2.34)
            return "B-";
        else if (GPA >= 2.01)
            return "C+";
        else if (GPA >= 1.68)
            return "C";
        else if (GPA >= 1.34)
            return "C-";
        else if (GPA >= 1.01)
            return "D+";
        else if (GPA >= 0.68)
            return "D";
        else if (GPA >= 0.34)
            return "D";
        else
            return "F";
    }
        return (
        <div className='studentWorker'>
            {!done ? (
                <div style={styles}>
                <ReactLoading type={"spin"} color={"black"}/>
                </div>
                ) 
            : (
                <span>
                <h1>{studentData.data.student}'s Details</h1>
            <body>
                <table>
                    <tr>
                        <td>Name:</td>
                        <td>{addComma(studentData.data.student)}</td>
                    </tr>
                    <tr>
                        <td>Email:</td>
                        <td>{studentData.data.email}</td>
                    </tr>
                    <tr>
                        <td>Previous Employed:</td>
                        <td>{studentData.data.is_employee}</td>
                    </tr>
                    <tr>
                        <td>Cumulative GPA:</td>
                        <td>{studentData.data.cGPA}</td>
                    </tr>

                    <tr>
                        <td style={{verticalAlign: 'top'}}>Faculty Reference:</td>
                        <td>
                            {studentData.data.facultyRef.map(((s, i )=> {
                                return(
                                    <div>
                                        {s}
                                        {studentData.data.facultyRef.length - 1 !== i && (<ColoredLine color="#0a0a0b"/>)}
                                    </div>
                                    
                                )
                            }))}
                        </td>
                    </tr>

                    <tr>
                        <td style={{verticalAlign: 'top'}}>Arranged Support:</td>
                        <td>
                            {studentData.data.facultyArr.map(((s, i) => {
                                return(
                                    <div>
                                        {s}
                                        {studentData.data.facultyArr.length - 1 !== i && (<ColoredLine color="#0a0a0b"/>)}
                                    </div>
                                )
                            }))}
                        </td>
                    </tr>
                    
                    
                    <tr>
                        <td style={{verticalAlign: 'top'}}>Interested Courses:</td>
                        <td>
                            {studentData.data.courses_preferences.map(((s, i) => {
                                return(
                                    <div style={{textAlign: 'left', paddingLeft: '20px'}}>
                                        Course ID: {s.courseID} {s.is_faculty_preferred === true && <AiFillStar style={{color: 'gold', position: 'absolute', padding: '1'}}/>}
                                        <br></br>
                                        Course Name: {s.courseName}
                                        <br></br>
                                        Position: {s.support_type}
                                        <br></br>
                                        Preference: {s.preferenceLevel}
                                        <br></br>
                                        Grade: {s.GPA === '' ? 'N/A' : s.GPA}
                                        {studentData.data.courses_preferences.length - 1 !== i && (<ColoredLine color="#0a0a0b"/>)}
                                    </div>
                                )
                            }))}
                        </td>
                    </tr>

                    <tr>
                        <td>Comments:</td>
                        <td style={{textAlign: 'left', paddingLeft: '25px'}}>{studentData.data.comments}</td>
                    </tr>
                </table>
                <button class="btn1" onClick={()=> navigate(-1)}>Back</button>
            </body>
            </span>
            )}
        </div>);
}
 
export default StudentWorker;
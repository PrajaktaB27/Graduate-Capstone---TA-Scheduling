import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { AiFillStar } from "react-icons/ai";
import Swal from 'sweetalert2'
import { useParams, useNavigate } from "react-router-dom";
import AssignedStudentURL from '../../services/get-assign-student'
import CourseDetailsURL from '../../services/get-course-details'
import AvailableStudentURL from '../../services/get-available-student'
import AssignStudentURL from '../../services/assign-student'
import UnAssignStudentURL from '../../services/un-assign-student'
import ReactLoading from 'react-loading'

const EditAssignmentTable = () => { 

    // To set load spinning logo position
    const styles = { position: "fixed", bottom: "50%", left: "50%" };

    const navigate = useNavigate();

    // to get the id from previous page (assignment table page)
    const { id } = useParams();

    const dataFetch = useRef(false);

    // added a line
    const ColoredLine = ({ color }) => (
        <hr
            style={{
                color: color,
                backgroundColor: color,
                height: 0.5
            }}
        />
    );
    
    const rankPreference = ["Preferred", "OK" , "No"]

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

    // saved assigned student data
    let [assignedStudentData, setAssignedStudentData] = useState({
        data:
        [
            {
                studentName: '',
                email: '',
                preferenceLevel: '',
                GPA: '',
                cGPA: 0.0,
                is_faculty_preferred: false
            }
        ]
    })

    // saved un-assigned student data
    let [studentData, setStudentData] = useState({
        data: 
        [
            {
                studentName: '',
                email: '',
                preferenceLevel: '',
                GPA: '',
                cGPA: 0.0,
                is_faculty_preferred: false
            }
        ]   
        
    })

    // saved course details 
    let [courseDetails, setCourseDetails] = useState({
        data: 
        [
            {
                courseName: '',
                courseID: '',
                facultyName: '',
                support_type: '',
                enrollment: 0,
                hoursAllowed: 0,
                quota: 0
            }
        ]
    })

    // To finish getting responses from API calls
    let [done, setDone] = useState(false);

    // re-render assign student data and call back end API to update database
    let assignStudent = (props, remaining, i) => {
        if(remaining !== 0) {
            AssignStudentURL.assign_student(props.email, id)
            .then(res => {
                 if(res.data.status === true) {
                    // create a new assigned student data
                    const newAssignStudent = {
                        studentName: props.studentName,
                        email: props.email,
                        preferenceLevel: props.preferenceLevel,
                        GPA: props.GPA,
                        cGPA: props.cGPA,
                        is_faculty_preferred: props.is_faculty_preferred
                    }
                   
                    // copy previous data and add new assigned student data
                    setAssignedStudentData(prevState => ({
                        data:
                        [
                            ...prevState.data,
                            newAssignStudent
                        ]
                    }));
            
                    // remove assigned student from student data
                    setStudentData(prevState => ({
                        data:
                        [
                            ...prevState.data.slice(0, i),
                            ...prevState.data.slice(i + 1)
                        ]
                    }));
                } else {
                    // alert error message from back end
                    Swal.fire(`${res.data.msg}`, '','error')
                }
            })
        } else {
            // prompt user there is no position left
            Swal.fire('There is no remain position left!', '','warning')
            return;
        }
    }

    // remove student from assigned student data
    let unassignStudent = (props, i) => {
        UnAssignStudentURL.un_assign_student(props.email, id)
        .then(res => {
             if(res.data.status === true) {
                // create a new student data
                const newStudent = {
                    studentName: props.studentName,
                    email: props.email,
                    preferenceLevel: props.preferenceLevel,
                    GPA: props.GPA,
                    cGPA: props.cGPA,
                    is_faculty_preferred: props.is_faculty_preferred
                }
               
                // remove assigned student from assign student data
                setAssignedStudentData(preveState => ({
                    data:
                    [
                        ...preveState.data.slice(0, i),
                        ...preveState.data.slice(i + 1)
                    ]
                }))
        
                // copy previous data and add new student into student data
                setStudentData(prevState => ({
                    data:
                    [
                        ...prevState.data,
                        newStudent
                    ]
                }))        
            } else {
                // alert message from back end
                Swal.fire(`${res.data.msg}`, '','error')
            }
        })
    }

    // called three APIs from back end
    const fetchData = () => {
        const getAssignedStudentURL = AssignedStudentURL.get_assign_student(id);
        const getStudentDetails = AvailableStudentURL.get_available_student(id);
        const getCourseDetails = CourseDetailsURL.get_course_details(id);
        axios
            .all([getAssignedStudentURL, getStudentDetails, getCourseDetails])
            .then(
                axios.spread((...allData) => {
                    console.log(allData[1].data)
                    setAssignedStudentData(allData[0].data);
                    setStudentData(allData[1].data);
                    setCourseDetails(allData[2].data);
                    setDone(true);
                })
            )
            .catch(error => {
                Swal.fire(`${error}`, '','error')
            })
    }

    useEffect(() => {
        if (dataFetch.current) return;
        dataFetch.current = true;
        fetchData()
    }, [])
    
        return (
        <span className="EditAssignmentTable">
            {!done ? (
                <div style={styles}>
                <ReactLoading type={"spin"} color={"black"}/>
                </div>
                ) 
            : ( <div>
                    <h2>Edit Assignment for {id}</h2>
                    <span>
                        <table>
                            <tr>
                                <th style={{textAlign: 'center'}}>Course</th>
                                <th style={{textAlign: 'center'}}>Student</th>
                            </tr>
                
                            <tr>
                                <td style={{textAlign: 'left', verticalAlign: 'top'}}>
                                    <ul style={{fontWeight:'bold', fontSize: '25px'}}>{courseDetails.data.courseID}</ul>
                                    <ul>Course Name: {courseDetails.data.courseName}</ul>
                                    <ul>Faculty Name: {courseDetails.data.facultyName}</ul>
                                    <ul>Support Type: {courseDetails.data.support_type}</ul>
                                    <ul>Enrollment: {courseDetails.data.enrollment}</ul>
                                    <ul>Hours Allowed: {courseDetails.data.hoursAllowed}</ul> 
                                    <ul>Position Remaining: {courseDetails.data.quota - assignedStudentData.data.length}</ul>    
                                </td>
        
                                <td style={{textAlign: 'left'}}>
                                    {/* sorting in following order: faculty preferred, student preference level, student GPA */}
                                    {assignedStudentData &&
                                    assignedStudentData.data.sort((a,b) =>
                                        b.is_faculty_preferred - a.is_faculty_preferred || rankPreference.indexOf(a.preferenceLevel) - rankPreference.indexOf(b.preferenceLevel) 
                                        || a.GPA.localeCompare(b.GPA)
                                    ).map(((s, i) => {
                                        return(
                                            <div style={{height: '200px'}}>
                                                <div>
                                                <ul> Student Name: {s.studentName} 
                                                    {s.is_faculty_preferred === true && <AiFillStar style={{color: 'gold', position: 'absolute', padding: '2'}}/>}
                                                </ul>
                                                </div>
                                                <div>
                                                    <ul>Preference: {s.preferenceLevel}</ul>
                                                    <ul>Grade: {s.GPA}</ul>
                                                    {/* <ul>cGPA: {convertGPAtoLetter(s.cGPA)}</ul> */}
                                                </div>
                                                <div style={{height: '60px'}}>
                                                    <span className="btn4">ASSIGNED</span>
                                                    <button className="btn3" onClick={()=> navigate(`student-worker/${s.email}`)}>Details</button>
                                                    <button className="btn2" onClick={() => unassignStudent(s, i)} >Remove</button>
                                                </div>
                                                <ColoredLine color="#0a0a0b"/>
                                            </div>
                                        )
                                    }))}
                                    
                                    {/* sorting in following order: faculty preferred, student preference level, student GPA */}
                                    {studentData && 
                                    studentData.data.sort((a,b) => 
                                        b.is_faculty_preferred - a.is_faculty_preferred || rankPreference.indexOf(a.preferenceLevel) - rankPreference.indexOf(b.preferenceLevel) 
                                        || a.GPA.localeCompare(b.GPA)
                                    ).map(((s, i) => {
                                        return(
                                            <div style={{height: '200px'}}>
                                                <div>
                                                <ul> Student Name: {s.studentName} 
                                                    {s.is_faculty_preferred === true && <AiFillStar style={{color: 'gold', position: 'absolute', padding: '2'}}/>}
                                                </ul>
                                                </div>
                                                <div>
                                                    <ul>Preference: {s.preferenceLevel}</ul>
                                                    <ul>Grade: {s.GPA}</ul>
                                                </div>
                                                <div style={{height: '60px'}}>
                                                    <button className="btn3" onClick={()=> navigate(`student-worker/${s.email}`)}>Details</button>
                                                    <button className="btn1" onClick={() => assignStudent(s, 
                                                        courseDetails.data.quota - assignedStudentData.data.length, i)} >Assign</button>     
                                                </div>
                                                {studentData.data.length - 1 !== i && (<ColoredLine color="#0a0a0b"/>)}
                                            </div>
                                        )
                                    }))}
                                    </td>
                            </tr>
                        </table>
                        <div>
                            <button className="btn1" onClick={()=> navigate(-1)}>Back</button>
                        </div>
                    </span>
                </div>)}
           
        </span>);
}
 
export default EditAssignmentTable;
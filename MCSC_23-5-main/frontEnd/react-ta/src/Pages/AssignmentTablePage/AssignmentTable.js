import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AssignmentTableDetail from '../../services/get-assignment-table'
// import PreMatchStudent from "../../services/pre-match-students";
import CourseModal from './CourseModel.Component'
import { AiFillStar } from "react-icons/ai";
import ReactLoading from 'react-loading';

function sortByKey(courseStudentMap) {
    return courseStudentMap.sort(function(a, b) {
      if (a.courseID < b.courseID) return -1;
      if (a.courseID > b.courseID) return 1;
      return 0;
    });
  }
  var tempCourseId = '';
  function checkDuplicateCourseID(courseID){
    if(courseID === tempCourseId){
        return false;
    }else{
        tempCourseId = courseID;
        return true;
    }
  }
  const noBorderTop = {
    borderTop: '0px'
  };
  const noBorderBottom = {
    borderBottom: '0px'
  };

  function changeBorder() {
        return '';
  }

  const styles = { position: "fixed", top: "50%", left: "50%" };

const AssignmentTable = () => {
    const navigate = useNavigate();
    const [data, setData] = useState([]);
    const [courseID, setCourseID] = useState('')
    const [courseModalIsOpen, setCourseModalOpen] = useState(false);

    useEffect(() => {
        AssignmentTableDetail.get_assignment_table()
        .then (res => {
            setData(res.data.data);
            setDone(true);
         
         }).catch((err) => console.log(err))
    }, [])

    const openCourseModal = (courseID) => {
        setCourseModalOpen(true);
        setCourseID(courseID);
    }

    const closeCourseModal = () => {
        setCourseModalOpen(false);
        setCourseID('');
    }

    // to set the loading spinning
    const [done, setDone] = useState(false);

    var sortedData = sortByKey(data);

    // to get today date
    var today = new Date();
    var day = today.getDate();
    var year = today.getFullYear();
    var month = today.getMonth() + 1;

    const convertMonthToSeason = (day, month) => {
         if(month <= 2){
            return "Winter";
         } else if(month <= 6) {
            if(day <= 18 && month === 3) {
                return "Winter"
            }
            if(day >= 20 && month === 6){
                return "Summer"
            }
            return "Spring";
         } else if(month <= 8) {
            return "Summer";
         } else {
            return "Fall";
         }  
    }

    // const pre_match_students = () => {
    //     setDone(false)
    //     const fetch_data = async () => {
    //         PreMatchStudent.pre_match_students()
    //         .then(res => {
    //         }).catch(error => {
    //             console.log(error)
    //         })

    //         AssignmentTableDetail.get_assignment_table()
    //         .then(res2 => { 
    //             setData(res2.data.data);
    //             setDone(true);
    //         }).catch(error => {
    //             console.log(error)
    //         })
    //     }
    //     fetch_data()
    // }

        return (
            <div className="AssignmentTable">
                {!done ? (
                    <div style={styles}>
                        <ReactLoading type={"spin"} color={"black"}/>
                    </div>
                )
            :(
                <div>
                    {/* <div style={{height: '40px'}}>
                        <button className='btn1' onClick={pre_match_students}>Pre-match students</button>
                    </div> */}
                    <h1>Assignment Table for {convertMonthToSeason(day, month)} Quarter {year}</h1>
                        <div>
                            <table>
                                <tr>
                                    <th>Course</th>
                                    <th>Student</th>
                                </tr>
                                
                                {data.map( item => (
                                <tr style={noBorderBottom}>
                                    { checkDuplicateCourseID(item.courseID) ? (
                                    <td style={noBorderBottom}>{item.courseID}<button style={{fontSize: '15px'}} class="btn1" onClick= {() => navigate(`edit-assignment-table/${item.courseID}`)}>Edit </button>
                                        <button style={{fontSize: '15px'}} class="btn3" onClick={() => openCourseModal(item.courseID)}>Details</button>                                
                                    </td>
                                    ):(
                                    <td style={noBorderTop}></td>
                                    )
                                    }
                                    <td>{item.studentName} {item.is_faculty_preferred === true && <AiFillStar style={{color: 'gold', position: 'absolute', padding: '2'}}/>}</td>        
                                </tr>
                                        )
                                    )
                                } 
                            </table>
                        </div>
                    <button class="btn1" onClick={() => navigate('export')}> Export</button>
                    {
                        courseModalIsOpen ? <CourseModal closeModal={closeCourseModal} modalIsOpen={courseModalIsOpen} courseID={courseID}/> : null
                    }
                </div>
            )}
            </div>
        );
}
 
export default AssignmentTable
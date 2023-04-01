import {React, useEffect, useState } from 'react';
import Modal from 'react-modal'
import CourseDetails from '../../services/get-course-details';
import ReactLoading from 'react-loading'

const CourseModal = ({closeModal, modalIsOpen, courseID}) => {

    const loadingStyles = { position: "fixed", bottom: "50%", left: "50%" };

    const styles = {
        input:{
            width: '70%'
        },
        termInput:{
            width: '10%',
            paddingLeft: '10px'
        }
    }

    const customStyles = {
        content: {
            top: '50%',
            left: '50%',

            bottom: 'auto',
            marginRight: '-50%',
            transform: 'translate(-50%, -50%)',
        }
    }
    const MODAL_STYLES = {
        position: "fixed",
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        //backgroundColor: '#FFF',
        //padding: '50px',
        //zIndex: '1000',
        width: '50%',
        borderRadius: '.5em',
        
    }
    const OVERLAY_STYLE={
        width: '80%',
        //backgroundColor: 'beige',
        paddingLeft:'15%'
    }

    
    const [courseDetails, setCourseDetails] = useState({
        data: 
        [
            {
                courseName: '',
                courseID: '',
                facultyName: '',
                support_type: '',
                enrollment: 0,
                hoursAllowed: 0,
                quota: 0,
                additional_req: ''
            }
        ]
    })

    const [loading, setLoading] = useState(true);

    const fetchData = async () => {
        console.log('getting data')
        return CourseDetails.get_course_details(courseID);

    }

    useEffect(() => {
        
        fetchData().then(res => {
            console.log(res.data);
            //console.log('getting data')
            setCourseDetails(res.data);
            setLoading(false);
        })
        .catch(error => {
            console.log(error);
        })
    }, [])

    return (
        <div>
            {loading ? 
            (<div style={loadingStyles}>
                <ReactLoading type= {"spin"} color={"black"}/>
            </div>)
            : (
                <div>
                    <Modal
                        isOpen={modalIsOpen}
                        //onAfterOpen={afterOpenModal}
                        onRequestClose={closeModal}
                        contentLabel="Course Modal"
                        ariaHideApp={false}
                        style={MODAL_STYLES}//{customStyles}
                    >
                    <div  style={OVERLAY_STYLE}>
                        <b>{courseID}</b>
                        <button className='btn5' onClick={closeModal}>close</button>
                    <body>
                        <table>
                            <tr>
                                <td>Course Name</td>
                                <td>{courseDetails.data.courseName}</td>
                            </tr>
                            <tr>
                                <td>Faculty Name</td>
                                <td>{courseDetails.data.facultyName}</td>
                            </tr>
                            <tr>
                                <td>Support Type</td>
                                <td>{courseDetails.data.support_type}</td>
                            </tr>
                            <tr>
                                <td>Enrollment</td>
                                <td>{courseDetails.data.enrollment}</td>
                            </tr>
                            <tr>
                                <td>Hours Allowed</td>
                                <td>{courseDetails.data.hoursAllowed}</td>
                            </tr>
                            <tr>
                                <td>Addtional Requirements</td>
                                <td>{courseDetails.data.additional_req}</td>
                            </tr>
                        </table>
                    </body>
                    </div>
                    </Modal>
                </div>
            )}
        
        
    </div>
    );
}

export default CourseModal;
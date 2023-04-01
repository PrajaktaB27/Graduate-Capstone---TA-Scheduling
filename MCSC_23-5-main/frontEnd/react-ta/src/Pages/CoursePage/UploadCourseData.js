import React, { useState } from 'react';
import { useNavigate} from "react-router-dom";
import UploadFile from '../../Components/upload-file.component.js'
import CourseService from '../../services/course.service'
import CourseModal from './Modal.Component'
import './uploadCourseStyle.css'

const UploadCourseData = () => { 
    let init_state = {
        "course_ID": '',
        "enrollment": 0,
        'instructor': '',
        'hours':0,
    }
    const navigate = useNavigate();
    const [loaded, setLoaded] = useState(false);
    const [data, setData] = useState([])
    const [numItem, setNumItem] = useState(1)
    const [term, setTerm] = useState('')
    const [modalIsOpen, setIsOpen] = useState(false);
    const [inputs, setInputs] = useState([init_state])

    const styles = {
        table: {
            border: '1px solid black',
            fontFamily:'Times New Roman, Times, serif',
            fontSize: '10px',
        },
        input:{
            width: '70%'
        },
        numberInput:{
            width: '40%'
        },
        termInput:{
            width: '10%',
            paddingLeft: '10px'
        }
    }

    const openModal= () => {
        setIsOpen(true);
    }

    const closeModal= () => {
        setIsOpen(false);
        setNumItem(1)
        //window.location.reload(false);
        //wipe everything's been input
        setInputs([init_state])
        console.log(inputs)
    }

    const handleSubmit = (event) => {
        if(!term){
            alert('Please choose a term')
            return
        }
        inputs.map((item) => {
            //console.log('item is', item)
            item['term'] = term
            return item
        })
        event.preventDefault();
        console.log(JSON.stringify(inputs))
        //post to the backend
        CourseService.post_course(JSON.stringify(inputs))
        .then((res) => {
            alert('New courses added')
            window.location.reload(false);
        })
        .catch((err) => console.log(err))
    }
    const handleChange = (event, indx) => {
        const name = event.target.name;
        const value = event.target.value;
        console.log(event.target)
        setInputs((prevVal) => {
            let temp = prevVal;
            console.log(indx)
            console.log(temp)
            temp[indx][name] = value
            return temp
        })
    }

    const handleAddItem = () => {
        setNumItem(numItem + 1)
        console.log(numItem)
        setInputs((prevVals) => {
            prevVals.push({"course_ID": '',
            "enrollment": '',
            'instructor': '',
            'hours':0})
            return prevVals
        })
        
    }

    const upload = () => {
        return (
            <div>
                <span> Please select the course file to upload </span>

                <UploadFile setLoaded={setLoaded} setData={setData}/>
            </div>
        )    
    }
    

    const show_data = () => {
        return (
            <div>
                <span>Courses Saved</span>
                <table style={styles.table}>
                <tbody>
                <tr>
                    <th>Course ID</th>
                    <th>Instructor</th>
                    <th>Enrollment</th>
                    <th>Hours assigned</th>
                </tr>
                {
                    data.map((item) => {
                        return(
                        <tr>
                            <td>{item.Section} </td>
                            <td>{item.Faculty} </td>
                            <td>{item.StudentCount} </td>
                            <td>{item.hours_allowed} </td>
                        </tr>
                    )})
                }
                </tbody>               
            </table>

            <button class="btn1" onClick={openModal}>Add more courses</button>
            {
                modalIsOpen ? 
                <CourseModal numItem={numItem}
                             handleChange={handleChange}
                             setTerm={setTerm}
                             handleAddItem={handleAddItem}
                             handleSubmit={handleSubmit}
                             closeModal={closeModal}
                             modalIsOpen={modalIsOpen}                            
                /> : ''
            }
            
            </div>
        )
    }

    return (
        <div className='uploadCourseStyle'>
            {
                !loaded ? upload() : show_data()
            }
            
        </div>
    )
}
 
export default UploadCourseData;
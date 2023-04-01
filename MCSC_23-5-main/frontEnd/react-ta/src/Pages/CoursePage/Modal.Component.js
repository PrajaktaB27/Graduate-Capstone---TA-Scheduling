import React from 'react';
import Modal from 'react-modal'

const CourseModal = ({numItem, handleChange, setTerm, handleAddItem, handleSubmit, closeModal, modalIsOpen}) => {
    let terms = ['FQ', ' WQ', 'SQ', 'Summer'];
    let currentYear = (new Date()).getFullYear() - 2000 //getFullYear gives a number back, not string

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

    const afterOpenModal = () => {
        // references are now sync'd and can be accessed.
        //subtitle.style.color = '#f00';
    }

    const add_rows = () => {
        let returnRows = []
        for(let i = 0; i < numItem; i++){
            returnRows.push(<form onSubmit={handleSubmit}>
                <label>
                    Course ID
                    <input 
                        name={"course_ID"}
                        type='text' 
                        onChange={(event) => handleChange(event, i)}
                        style={styles.input}/>
                </label>
                <label>
                Instructor
                    <input 
                        name={"instructor"} 
                        type='text' 
                        onChange={(event) => handleChange(event, i)}
                        style={styles.input}/>
                </label>
                <label>
                Enrollment
                    <input 
                        name={"enrollment"}
                        type='number'
                        onChange={(event) => handleChange(event, i)}
                        style={styles.input}/>
                </label>
                <label>
                Hours assigned
                    <input 
                        name={"hours"} 
                        type='number' 
                        onChange={(event) => handleChange(event, i)}
                        style={styles.input}/>
                </label>
                
            </form>
            )
            
        }
        return returnRows;
    }

    return (
        <div>
          <Modal
            isOpen={modalIsOpen}
            onAfterOpen={afterOpenModal}
            onRequestClose={closeModal}
            contentLabel="Course Modal"
            ariaHideApp={false}
            style={customStyles}
          >
            <div className='header-container'>
                <b>Add More Courses Below</b>
                <button className='btn5' onClick={closeModal}>close</button>
                <div>
                    <span>
                    Select Current Term
                    </span>
                    <div>
                        <select onChange={(event) => setTerm(event.target.value)}>
                            <option value={''}>{'Select..'}</option>
                            {terms.map((term) => {
                                return <option value={term + currentYear}>{term + currentYear}</option>
                            })}
                        </select>
                    </div>            
                </div>
            </div>
            <div>    
                {
                    add_rows()
                }
             </div>
            <button className='btn' onClick={handleAddItem}>Add more</button>
            <button className='btn' onClick={handleSubmit}>Submit</button>
          </Modal>
        </div>
    );
}

export default CourseModal;
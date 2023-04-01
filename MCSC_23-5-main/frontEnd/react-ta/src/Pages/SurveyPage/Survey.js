import React from 'react';
import './surveystyle.css'
import { useState } from "react";
import ReactLoading from 'react-loading';
import { CopyToClipboard } from 'react-copy-to-clipboard'
import Swal from 'sweetalert2'
import PushInstructorSurvey from '../../services/push-fac-survey'
import PullInstructorSurvey from '../../services/pull-fac-survey'
import PushStudentSurvey from '../../services/push-stu-survey'
import PullStudentSurvey from '../../services/pull-stu-survey'

const Survey = () => {
  
  const styles = { position: "fixed", bottom: "50%", left: "50%" };
  
  const [facQualtric, setFacQualtric] = useState([])
  // const [facMessage, setFacMessage] = useState([])
  const [facHidden, setFacHidden] = useState(false)
  const [facStartHidden, setFacStartHidden] = useState(false)

  const [stuStartMessage, setStuStartMessage] = useState([])
  const [stuStartHidden, setStuStartHidden] = useState(false)

  const [spinning, setSpinning] = useState(true)
  const [loadingButton, setLoadingButton] = useState(true)
  const [copyFacHidden, setCopyFacHidden] = useState(false)
  const [copyStuHidden, setCopyStuHidden] = useState(false)
  const [facCopied, setFacCopied] = useState(false)
  const [stuCopied, setStuCopied] = useState(false)
 

  const startInstructorSurvey = () => {
    Swal.fire({
      title: 'Click confirm to start INSTRUCTOR Survey',
      showCancelButton: true,
      confirmButtonText: 'CONFIRM',
    }).then((result) => {
      if(result.isConfirmed){
        setSpinning(false)
        setLoadingButton(false)
        const fetch_data = async () => {
          const res = await PushInstructorSurvey.push_fac_survey()
          .then(res => {
            setFacQualtric(res.data)
            setFacStartHidden(true)
            setCopyFacHidden(true)
            console.log(res.data)
          }).catch(error => {
            Swal.fire(`${error}`, '','error')
            console.log(error)
          })
          setSpinning(true)
          setLoadingButton(true)
        }
        fetch_data()
      }
    })
    
  }

  const finishInstructorSurvey = () => {
    Swal.fire({
      title: 'Click to confirm to finish INSTRUCTOR Survey',
      showCancelButton: true,
      confirmButtonText: 'CONFIRM',
    }).then((result) => {
      if(result.isConfirmed) {
        setSpinning(false)
        setLoadingButton(false)
        const fetch_data = async () => {
          const res = await PullInstructorSurvey.pull_faculty_survey()
          .then(res => {
            if(res.status === 200) {
              Swal.fire(`${res.data}`, '','success')
            }
            else {
              Swal.fire(`${res.data}`, '','error')
            }
          }).catch(error => {
            Swal.fire(`${error}`, '','error')
            console.log(error)
          })
          setSpinning(true)
          setLoadingButton(true)
        }
        fetch_data()
      }
    })
  }
  
  const startStudentSurvey = () => {
    Swal.fire({
      title: 'Click to confirm to start STUDENT Survey',
      showCancelButton: true,
      confirmButtonText: 'CONFIRM',
    }).then((result) => {
      if(result.isConfirmed) {
        setFacStartHidden(false)
        setSpinning(false)
        setLoadingButton(false)
        const fetch_data = async () => {
          const res = await PushStudentSurvey.push_student_survey()
          .then(res => {
            setStuStartMessage(res.data)
            setStuStartHidden(true)
            setCopyStuHidden(true)
            console.log(res.data)
          }).catch(error => {
            Swal.fire(`${error}`, '','error')
            console.log(error)
          })
          setSpinning(true)
          setLoadingButton(true)
        }
        fetch_data()
      }
    })
  }
  
  const finishStudentSurvey = () => {
    Swal.fire({
      title: 'Click to confirm to finish STUDENT Survey',
      showCancelButton: true,
      confirmButtonText: 'CONFIRM',
    }).then((result) => {
      if(result.isConfirmed) {
        setSpinning(false)
        setLoadingButton(false)
        const fetch_data = async () => {
          const res = await PullStudentSurvey.pull_student_survey()
          .then(res => {
            if(res.status === 200) {
              Swal.fire(`${res.data}`, '','success')
            }
            else {
              Swal.fire(`${res.data}`, '','error')
              // alert(res.data.content);
            }
          }).catch(error => {
            Swal.fire(`${error}`, '','error')
            console.log(error)
          })
          setSpinning(true)
          setLoadingButton(true)
        }
        fetch_data()
      }
    })
  }
  
  
  return (
        <div>
          <h1>Survey</h1>
          {loadingButton && 
          <div>
              <section class="section">
                <div class="box-main">
                <div>
                  <button id='instructor-start' className='survey-btn' onClick={startInstructorSurvey}>START INSTRUCTOR SURVEY</button>
                  <button id='student-start' className='survey-btn' onClick={startStudentSurvey}>START STUDENT SURVEY</button>
                  </div>
                  <div>
                  <button id='instructor-finish' className='survey-btn' onClick={finishInstructorSurvey}>FINISH INSTRUCTOR SURVEY</button>
                  <button id='student-finish' className='survey-btn' onClick={finishStudentSurvey}>FINISH STUDENT SURVEY</button>
                  </div>
                 </div>
              </section>
          </div>}

          <div>

              <div >
                {!spinning ? (
                  <div style={styles}>
                    <ReactLoading type= {"spin"} color={"black"}/>
                  </div>
                  ) 
                  : (
                    <div>
                      {facStartHidden && 
                      <div>
                        <b style={{textAlign:'left', margin:'20px'}}>
                        Instructor Survey Output: 
                        </b>
                        <div className="output-box">
                          <div>
                            <a href= {facQualtric} target="_blank" rel="noopener noreferrer">{facQualtric}</a>
                            {copyFacHidden && 
                            <CopyToClipboard text={facQualtric} 
                            onCopy={() => setFacCopied(true)}>
                              <button className='btn7'>Copy</button> 
                            </CopyToClipboard>}

                            {facCopied ? <span style={{color:'red', margin: '10px'}}>Copied !</span> : null}
                          </div>
                        </div>
                      </div>
                      }
                    </div>
                  )}
                </div>

                <div >
                {!spinning ? (
                  <div style={styles}>
                    <ReactLoading type= {"spin"} color={"black"}/>
                  </div>
                  ) 
                  : (
                    <div>
                      {stuStartHidden && 
                      <div>
                        <b style={{textAlign:'left', margin:'20px'}}>
                        Student Survey Output: 
                        </b>
                        <div className="output-box">
                          <div>
                            <a href= {stuStartMessage} target="_blank" rel="noopener noreferrer">{stuStartMessage}</a>
                            {copyStuHidden && 
                            <CopyToClipboard text={stuStartMessage} 
                            onCopy={() => setStuCopied(true)}>
                              <button className='btn7'>Copy</button> 
                            </CopyToClipboard>}

                            {stuCopied ? <span style={{color:'red', margin: '10px'}}>Copied !</span> : null}
                          </div>
                        </div>
                      </div>
                      }
                    </div>
                  )}
                </div>
      

                {/* <div >
                {!spinning ? (
                  <div style={styles}>
                    <ReactLoading type= {"spin"} color={"black"}/>
                  </div>
                  ) 
                  : (
                    <div>
                      {facHidden &&
                      <div>
                        <b style={{textAlign:'left', margin:'20px'}}>
                          Finish Instructor Survey Output: 
                        </b>
                        <div className="output-box">
                          <div>
                            {facMessage}
                          </div>
                        </div>
                      </div>
                      }
                    </div>
                  )}
                  </div> */}

                
                
                
          </div>
        </div>
  );
};

export default Survey

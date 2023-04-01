import React, { useState } from "react";
import CourseService from "../services/course.service";
import './coursestyle.css'

const UploadFile = ({setLoaded, setData}) => {
    const [state, setState] = useState({
      selectedFile: undefined,
      currentFile: undefined,
      progress: 0,
      message: ''
    })
  

  /**selectFile() method helps us to get the selected Files 
   * from <input type="file" > element later */
  const selectFile = (event) => {
    setState({
        ...state,
        selectedFile: event.target.files,
    })
    console.log('selected a file')
  }

  const upload = () => {

    console.log('Clicked upload')
    let currentFile = state.selectedFile[0];

    setState({
      ...state,
        progress: 0,
        currentFile: currentFile
    });

    //call upload service to start uploading the file to server and with a callback
    CourseService.upload_course(currentFile, (event) => {

        setState({
          ...state,
            progress: Math.round((100 * event.loaded) / event.total)
        });
    }).then((response) => {
        setState({
          ...state,
          //message: response.data,
        });
        //console.log(response.data)
        setData(response.data)
        setLoaded(true)

    }).catch(() => {
        setState({
          ...state,
            progress: 0,
            message: "Could not upload the file!",
            currentFile: undefined
        });
    });

    setState({
      ...state,
      selectedFile: undefined
    })
  }

  return (
    <div> 
      <div class="flexbox-container" style={{display: "inline-flex"}}>
        {state.currentFile && (
          <div className="progress">
            <div
              className="progress-bar progress-bar-info progress-bar-striped"
              role="progressbar"
              aria-valuenow={state.progress}
              aria-valuemin="0"
              aria-valuemax="100"
              style={{ width: 100, 
                        backgroundColor: 'pink' }}
            >
              {state.progress}%
            </div>
          </div>
        )}

        <label className="btn btn-default">
          <input type="file" onChange={(selectFile)} />
        </label>

        <button className="btn btn-success"
          disabled={!state.selectedFile}
          onClick={upload}
        >
          Upload file
        </button>
      </div>

      <div className="alert">
          {state.message}
      </div>
    </div>
    );

}

export default UploadFile;
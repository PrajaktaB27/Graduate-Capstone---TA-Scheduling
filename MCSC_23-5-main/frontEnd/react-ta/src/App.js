import './App.css';
import React from "react";
import { Routes, Route } from "react-router-dom";

import Home from "./Pages/HomePage";
import AssignmentTable from "./Pages/AssignmentTablePage/AssignmentTable";
import EditAssignmentTable from './Pages/AssignmentTablePage/EditAssignmentTable';
import UploadCourse from './Pages/CoursePage/UploadCourseData';
import StudentWorker from './Pages/StudentWorkerPage/StudentWorker';
import Survey from './Pages/SurveyPage/Survey';
import NavBar from './Components/NavBar';
import Error from './Components/ErrorPage';
import ExportFile from './Pages/AssignmentTablePage/AssignmentExport'

function App() {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={ <Home /> }/>
        <Route path="/survey" element={ <Survey /> }/>
        <Route path="/upload-course" element={ <UploadCourse /> }/>
        <Route path="/assignment-table" element={ <AssignmentTable /> }/>
        <Route path="/assignment-table/edit-assignment-table/:id" element={ <EditAssignmentTable /> }/>
        <Route path="/assignment-table/export" element={ <ExportFile /> }/>
        <Route path="/assignment-table/edit-assignment-table/:id/student-worker/:id" element={ <StudentWorker /> }/>
        <Route path="*" element={ <Error /> }/>
      </Routes>

    </>
  );
}

export default App;
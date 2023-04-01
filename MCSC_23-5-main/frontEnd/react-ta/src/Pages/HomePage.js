import React, { Component } from 'react';
import { useNavigate } from 'react-router-dom';
import './home.css'


const Home = () => {
    const navigate = useNavigate();

        return (
        <div>
        <div className="Home">
        <h1>Welcome</h1>
        <h2>The Seattle University TA Scheduler Application</h2>
        <div className="horizontal-center">
            <button className="btn" id='survey-btn' onClick= {() => navigate('survey')}>Survey</button>
            <button className="btn" id='upload-btn' onClick= {() => navigate('upload-course')}>Upload Course</button>
            <button className="btn" id='assignment-btn' onClick= {() => navigate('assignment-table')}>Assignment Table</button>
            {/* <button className="btn" onClick= {() => navigate('assignment-table/assignment-table-history')}>History</button> */}
        </div>
        </div>
    </div>

    );
    
}

export default Home;
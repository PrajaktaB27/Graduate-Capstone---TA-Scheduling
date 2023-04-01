import React from 'react';
import { useNavigate } from 'react-router-dom';
import './navBar.css';

const NavBar = () => {
   const navigate = useNavigate();

 return (
         <div className='navBar'>
            <button className="btn-nav" onClick= {() => navigate('/')}>Home</button>
            <button className="btn-nav" onClick= {() => navigate('survey')}>Survey</button>
            <button className="btn-nav" onClick= {() => navigate('upload-course')}>Upload Course</button>
            <button className="btn-nav" onClick= {() => navigate('assignment-table')}>Assignment Table</button>
         </div>
 );
};

export default NavBar;
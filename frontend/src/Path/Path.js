import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Error from '../Error/Error';
import Calibration from '../Calibration/Calibration';
import Principal from '../Principal/Principal';
import Historical from '../Historical/Historical';
import reportWebVitals from '../Default/reportWebVitals';
import NavBar from './NavBar';


const Path = () => {
  return (
    <Router>
        <NavBar />
        <Routes>
            <Route path="/" element={<Principal />} />
            <Route path="/error" element={<Error />} />
            <Route path="/calibration" element={<Calibration />} />
            <Route path="/historical" element={<Historical />} />
        </Routes>
    </Router>
  );
}

reportWebVitals();

export default Path;

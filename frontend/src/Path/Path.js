import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Error from '../Error/Error';
import Calibration from '../Calibration/Calibration';
import Principal from '../Principal/Principal';
import Historic from '../Historic/Historic';
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
            <Route path="/historic" element={<Historic />} />
        </Routes>
    </Router>
  );
}

reportWebVitals();

export default Path;

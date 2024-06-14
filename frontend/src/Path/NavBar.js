import React from 'react';
import { useLocation } from 'react-router-dom';
import './NavBar.css';
import UMA from '../images/uma.jpg';

const Navbar = () => {
    const location = useLocation();
    const ubicacion = location.pathname.substring(1);

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <a className="navbar-brand" href="/">TFG</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav me-auto">
                        <li className="nav-item" style={{marginLeft: "20px"}}>
                            <a className={ubicacion === 'error' ? 'nav-link active' : 'nav-link'} href="/error">Error</a>
                        </li>
                        <li className="nav-item" style={{marginLeft: "20px"}}>
                            <a className={ubicacion === 'calibration' ? 'nav-link active' : 'nav-link'} href="/calibration">Calibration</a>
                        </li>
                        <li className="nav-item" style={{marginLeft: "20px"}}>
                            <a className={ubicacion === 'historical' ? 'nav-link active' : 'nav-link'} href="/historical">Historical</a>
                        </li>
                    </ul>
                    <ul className="navbar-nav ms-auto">
                        <li className="nav-item">
                            <a href="https://www.uma.es/">
                                <img className="img-small" src={UMA} alt="Logo de la UMA" />
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;

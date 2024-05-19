// src/components/Navbar.js
import React from 'react';
import { useLocation } from 'react-router-dom';
import './NavBar.css'; // Para tus estilos personalizados
import UMA from '../images/uma.jpg'

const Navbar = () => {
    const location = useLocation();
    const ubicacion = location.pathname.substring(1); // Para obtener la ruta actual sin el "/"

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <a className="navbar-brand" href="/">TFG</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav ml-auto">
                        <li className="nav-item" style={{marginLeft: "20px"}}>
                            <a className={ubicacion === 'error' ? 'nav-link active' : 'nav-link'} href="/error">Error</a>
                        </li>
                        <li className="nav-item" style={{marginLeft: "20px"}}>
                            <a className={ubicacion === 'calibration' ? 'nav-link active' : 'nav-link'} href="/calibration">Calibration</a>
                        </li>
                        <li className="nav-item" style={{marginLeft: "20px"}}>
                            <a className={ubicacion === 'historical' ? 'nav-link active' : 'nav-link'} href="/historical">Historical</a>
                        </li>
                        <li>
                        <a href="https://www.uma.es/">
                            <img class="img-small" src={UMA} alt="Descripción de la imagen" />
                        </a>
                        </li>


                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;

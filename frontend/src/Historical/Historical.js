import React, { useState, useEffect } from "react";
import Graph from '../Graph/Graph'; // Importa el componente de la gráfica

function Historical() {
    const [showCalibrationGraphsQubits, setShowCalibrationGraphsQubits] = useState(false);
    const [calibrationQubits, setCalibrationQubits] = useState([]);

    const handleButtonCalibrationQubits = () => {
        setShowCalibrationGraphsQubits(!showCalibrationGraphsQubits); // Cambiar el estado de visibilidad
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://localhost:8000/historical', {
                    method: 'GET',
                    headers: {
                      'Content-Type': 'application/json'
                    }
                  })
                const data = await response.json();
                
                setCalibrationQubits(data.historical);
                console.log(data.historical[0].qubits)
            } catch (error) {
                console.error("Error fetching calibration data:", error);
            }
        };

        fetchData();
    }, []); // El segundo argumento del useEffect indica que solo se ejecutará una vez, al cargar el componente

    return (
        <div className="container">
            <div className="bar">
                <h1 className="title">Historical</h1>
            </div>

            <div className="container-button">
                <button onClick={handleButtonCalibrationQubits} className="button">
                    {showCalibrationGraphsQubits ? "Hide Qubit Calibration Charts" : "Show Qubit Calibration Charts"}
                </button>
            </div>

            {/* Aquí puedes renderizar tus gráficos de calibración si showCalibrationGraphsQubits es true */}
            {showCalibrationGraphsQubits && calibrationQubits && (
                <div>
                    <div style={{ marginBottom: '40px' }}>
                        <h2>Predicciones T1:</h2>
                        <Graph predictions={calibrationQubits[0].qubits} type={'T1'} />
                    </div>
                    <div style={{ marginBottom: '40px' }}>
                        <h2>Predicciones T2:</h2>
                        <Graph predictions={calibrationQubits[0].qubits} type={'T2'} />
                    </div>
                    <div style={{ marginBottom: '40px' }}>
                        <h2>Predicciones Prob0:</h2>
                        <Graph predictions={calibrationQubits[0].qubits} type={'probMeas0Prep1'} />
                    </div>
                    <div style={{ marginBottom: '40px' }}>
                        <h2>Predicciones Prob1:</h2>
                        <Graph predictions={calibrationQubits[0].qubits} type={'probMeas1Prep0'} />
                    </div>
                    <div style={{ marginBottom: '40px' }}>
                        <h2>Predicciones readout_error:</h2>
                        <Graph predictions={calibrationQubits[0].qubits} type={'readout_error'} />
                    </div>
                </div>
            )}
        </div>
    );
}

export default Historical;

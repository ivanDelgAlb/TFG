import React, { useState, useEffect } from "react";
import Graph from '../Graph/Graph'; // Importa el componente de la gráfica

function Historical() {
    const [showCalibrationGraphsQubits, setShowCalibrationGraphsQubits] = useState(false);
    const [showCalibrationGraphsGates, setShowCalibrationGraphsGates] = useState(false);
    const [calibration, setCalibration] = useState([]);
    const [machine, setMachine] = useState("");
    const [option, setOption] = useState("");
    const [error, setError] = useState(null);

    const handleButtonCalibration = () => {
        setError(null)
        if(!machine){
            setError("You must select a machine")
            return;
        }else if(!option){
            setError("You must select an option")
            return;
        }
        if(option === "Qubits"){
            setShowCalibrationGraphsQubits(!showCalibrationGraphsQubits);
            setShowCalibrationGraphsGates(false);
        }else{
            setShowCalibrationGraphsGates(!showCalibrationGraphsGates);
            setShowCalibrationGraphsQubits(false);
        }
    };

    const handleChangeMachine = (event) => {
        setMachine(event.target.value);
    };

    const handleChangeOption = (event) => {
        setOption(event.target.value);
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
                
                setCalibration(data.historical);
                console.log(data.historical)

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
            <div className="selectors-row">
                <div className="machine-selector">
                    <select value={machine} onChange={handleChangeMachine} className="selector-option-select">
                        <option value="">Choose a machine</option>
                        <option value="ibm Brisbane">ibm Brisbane</option>
                        <option value="ibm Kyoto">ibm Kyoto</option>
                        <option value="ibm Osaka">ibm Osaka</option>
                    </select>
                </div>
                <div className="option-selector">
                    <select value={option} onChange={handleChangeOption} className="selector-option-select">
                        <option value="">Choose an option</option>
                        <option value="Qubits">Qubits</option>
                        <option value="Gates">Gates</option>
                    </select>
                </div>
            </div>

            {error && <p className="error-message">{error}</p>}

            <div className="container-button">
                <button onClick={handleButtonCalibration} className="button">
                    {showCalibrationGraphsQubits || showCalibrationGraphsGates ? "Hide Calibration Charts" : "Show Calibration Charts"}
                </button>
            </div>

            {/* Aquí puedes renderizar tus gráficos de calibración si showCalibrationGraphsQubits es true */}
            {showCalibrationGraphsQubits && calibration && (
                <div>
                    <div style={{ marginBottom: '40px' }}>
                        <h2>Historical T1:</h2>
                        <Graph predictions={calibration[0].qubits} type={'T1'} historical={true} />
                    </div>
                    <div style={{ marginBottom: '40px' }}>
                        <h2>Historical T2:</h2>
                        <Graph predictions={calibration[0].qubits} type={'T2'} historical={true} />
                    </div>
                    <div style={{ marginBottom: '40px' }}>
                        <h2>Historical Prob0:</h2>
                        <Graph predictions={calibration[0].qubits} type={'probMeas0Prep1'} historical={true} />
                    </div>
                    <div style={{ marginBottom: '40px' }}>
                        <h2>Historical Prob1:</h2>
                        <Graph predictions={calibration[0].qubits} type={'probMeas1Prep0'} historical={true} />
                    </div>
                    <div style={{ marginBottom: '40px' }}>
                        <h2>Historical readout_error:</h2>
                        <Graph predictions={calibration[0].qubits} type={'readout_error'} historical={true} />
                    </div>
                </div>
            )}
            {showCalibrationGraphsGates && calibration && (
                <div>
                    <div style={{ marginBottom: '40px' }}>
                        <h2>Historical Gate error of one-qubit input:</h2>
                        <Graph predictions={calibration[1].gates} type={'gate_error_one_qubit'} historical={true} />
                    </div>
                    <div style={{ marginBottom: '40px' }}>
                        <h2>Historical Gate error of two-qubit input:</h2>
                        <Graph predictions={calibration[1].gates} type={'gate_error_two_qubit'} historical={true} />
                    </div>
                </div>
            )}
        </div>
    );
}

export default Historical;

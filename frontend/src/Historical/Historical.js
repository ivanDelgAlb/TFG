import React, { useEffect, useState } from "react";
import Graph from '../Graph/Graph';
import './Historical.css';

const urlLocal = process.env.REACT_APP_URL_LOCALHOST;
const urlDesploy = process.env.REACT_APP_URL_DEPLOYMENT;
const deployment = process.env.REACT_APP_DEPLOYMENT;

function Historical() {
    const [calibration, setCalibration] = useState([]);
    const [selectedMachine, setSelectedMachine] = useState("");
    const [option, setOption] = useState("");
    const [error, setError] = useState(null);
    const [showCalibrationGraphs, setShowCalibrationGraphs] = useState(false);
    const [loading, setLoading] = useState(false);

    const machines = ["ibm Brisbane", "ibm Kyoto", "ibm Osaka"];

    const handleButtonCalibration = () => {
        setError(null);
        
        if (!selectedMachine) {
            setError("You must select a machine");
            setLoading(false);
            return;
        } else {
            setShowCalibrationGraphs(prev => !prev);
        }
    };

    const handleChangeOption = (event) => {
        setLoading(true);
        setOption(event.target.value);
    };

    const handleTabChange = async (machine) => {
        console.log(machine);
        setSelectedMachine(machine);
        setOption("");
        setShowCalibrationGraphs(false);
        setError(null);
        setCalibration([]);

        try {
            const params = new URLSearchParams({machine: machine})
            let url = urlLocal

            if (deployment !== 'localhost') url = urlDesploy

            console.log(deployment)
            const response = await fetch(url + `historical?${params.toString()}`, {
                method: 'GET',
                headers: {
                  'Content-Type': 'application/json'
                }
            });

            const data = await response.json();
            console.log(data);
            setCalibration(data.historical);
            console.log(data.historical[0].qubits);
        } catch (error) {
            console.error("Error fetching calibration data:", error);
        } finally {
            setLoading(false);
            setShowCalibrationGraphs(true)
        }
    };

    useEffect(() => {
        console.log("Calibration state:", calibration);
    }, [calibration]);

    return (
        <div className="container">
            <div className="bar">
                <h1 className="title">Historical</h1>
            </div>

            <div className="tabs">
                {machines.map((machine) => (
                    <button 
                        key={machine}
                        className={`tab ${selectedMachine === machine ? "active" : ""}`} 
                        onClick={() => handleTabChange(machine)}
                    >
                        {machine}
                    </button>
                ))}
            </div>

            {selectedMachine && calibration.length > 0 &&(
                <div>
                    <div className="option-selector">
                        <select 
                            value={option} 
                            onChange={handleChangeOption} 
                            className={`option-selector-select ${'selected'}`}
                            aria-label="Select an option"
                        >
                            <option value="">All the historical data</option>
                            <option value="Qubits">Qubits</option>
                            <option value="Gates">Gates</option>
                        </select>
                        <label htmlFor="nQubitsInput" className="select-label">Option selected:</label>
                    </div>

                    {error && <p className="error-message">{error}</p>}

                    <div className="container-button">
                        <button onClick={handleButtonCalibration} className="button">
                            {showCalibrationGraphs ? "Hide Calibration Charts" : "Show Calibration Charts"}
                        </button>
                    </div>

                    {(option === "" || option === "Qubits" ) && calibration.length > 0 && showCalibrationGraphs && (
                        <div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical T1:</h2>
                                <Graph predictions={calibration[0].qubits} type={'T1'} historical={true} calibraciones={true} colors={1}/>
                            </div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical T2:</h2>
                                <Graph predictions={calibration[0].qubits} type={'T2'} historical={true} calibraciones={true} colors={2}/>
                            </div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical Prob_Meas0_Prep1:</h2>
                                <Graph predictions={calibration[0].qubits} type={'Prob0'} historical={true} calibraciones={true} colors={3}/>
                            </div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical Prob_Meas1_Prep0:</h2>
                                <Graph predictions={calibration[0].qubits} type={'Prob1'} historical={true} calibraciones={true} colors={4}/>
                            </div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical Readout_error:</h2>
                                <Graph predictions={calibration[0].qubits} type={'Error'} historical={true} calibraciones={true}colors={5}/>
                            </div>
                        </div>
                    )}

                    {(option === "" || option === "Gates") && calibration.length > 0 && showCalibrationGraphs &&(
                        <div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical Gate error of one-qubit input:</h2>
                                <Graph predictions={calibration[1].gates} type={'gate_error_1'} historical={true} calibraciones={true} colors={6}/>
                            </div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical Gate error of two-qubit input:</h2>
                                <Graph predictions={calibration[1].gates} type={'gate_error_2'} historical={true} calibraciones={true} colors={0}/>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default Historical;

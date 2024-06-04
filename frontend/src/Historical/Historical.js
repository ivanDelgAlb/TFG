import React, { useEffect, useState } from "react";
import Graph from '../Graph/Graph'; // Importa el componente de la gráfica
import './Historical.css'; // Asegúrate de crear este archivo CSS para los estilos

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
        setOption(""); // Reset the selected option
        setShowCalibrationGraphs(false); // Hide graphs
        setError(null);
        setCalibration([]); // Clear calibration data

        try {
            const response = await fetch('https://tfgprueba-1.onrender.com/historical', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    machine: machine
                })
            });

            const data = await response.json();
            console.log(data);
            setCalibration(data.historical);
            console.log(data.historical[0].qubits);
        } catch (error) {
            console.error("Error fetching calibration data:", error);
        } finally {
            setLoading(false);
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
                        <select value={option} onChange={handleChangeOption} className="selector-option-select">
                            <option value="">Choose an option</option>
                            <option value="Qubits">Qubits</option>
                            <option value="Gates">Gates</option>
                            <option value="ErrorQubits">Error Qubits</option>
                            <option value="ErrorGates">Error Gates</option>
                        </select>
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
                                <Graph predictions={calibration[0].qubits} type={'T1'} historical={true} color={'#1f77b4'}/>
                            </div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical T2:</h2>
                                <Graph predictions={calibration[0].qubits} type={'T2'} historical={true} color={'#660066'}/>
                            </div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical Prob_Meas0_Prep1:</h2>
                                <Graph predictions={calibration[0].qubits} type={'Prob0'} historical={true} color={'#006600'}/>
                            </div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical Prob_Meas1_Prep0:</h2>
                                <Graph predictions={calibration[0].qubits} type={'Prob1'} historical={true} color={'#000099'}/>
                            </div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical Readout_error:</h2>
                                <Graph predictions={calibration[0].qubits} type={'Error'} historical={true} color={'#ff6600'}/>
                            </div>
                        </div>
                    )}

                    {(option === "" || option === "Gates") && calibration.length > 0 && showCalibrationGraphs &&(
                        <div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical Gate error of one-qubit input:</h2>
                                <Graph predictions={calibration[1].gates} type={'gate_error_1'} historical={true} color={'#e6e600'}/>
                            </div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical Gate error of two-qubit input:</h2>
                                <Graph predictions={calibration[1].gates} type={'gate_error_2'} historical={true} color={'#2f4f4f'}/>
                            </div>
                        </div>
                    )}

                    {(option === "" || option === "ErrorQubits") && calibration.length > 0 && showCalibrationGraphs &&(
                        <div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical error Jensen of qubits:</h2>
                                <Graph predictions={calibration[2].errorQubits} type={'jensen_error'} historical={false} color={'#e6e600'}/>
                            </div>
                        </div>
                    )}

                    {(option === "" || option === "ErrorGates") && calibration.length > 0 && showCalibrationGraphs &&(
                        <div>
                            <div style={{ marginBottom: '40px' }}>
                                <h2>Historical error Jensen of gates:</h2>
                                <div style={{ width: '100%', maxWidth: '1200px', margin: '0 auto' }}>
                                    <Graph predictions={calibration[3].errorGates} type={'jensen_error'} historical={false} color={'#e6e600'} />
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default Historical;

import React, { useState } from 'react';
import './Calibration.css'

function Calibration() {
  const [machine, setMachine] = useState(""); 
  const [t1, setT1] = useState(null); 
  const [t2, setT2] = useState(null); 
  const [prob0, setProb0] = useState(null); 
  const [prob1, setProb1] = useState(null); 
  const [readoutError, setReadoutError] = useState(null); 
  const [prediction, setPrediction] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [depth, setDepth] = useState("");
  const [selection, setSelection] = useState("");
  const [gate_error_1, setgate1] = useState(null); 
  const [gate_error_2, setgate2] = useState(null); 


  const handleChangeSelection = (event) => {
    setSelection(event.target.value);
  };

  const handleChangeGate1 = (event) => {
    setgate1(event.target.value);
  };

  const handleChangeGate2 = (event) => {
    setgate2(event.target.value);
  };

  const handleChangeOption = (event) => {
    setMachine(event.target.value);
  };

  const handleChangeT1 = (event) => {
    setT1(event.target.value);
  };

  const handleChangeT2 = (event) => {
    setT2(event.target.value);
  };

  const handleChangeProb0 = (event) => {
    setProb0(event.target.value);
  };

  const handleChangeProb1 = (event) => {
    setProb1(event.target.value);
  };

  const handleChangeReadoutError = (event) => {
    setReadoutError(event.target.value);
  };

  const handleChangeDepth = (event) => {
    setDepth(event.target.value);
  };

  const handleButtonClick = async () => {
    setError("")
    setLoading(true); 
    if (!machine || !selection) {
      setError("All the field must be filled");
      setLoading(false)
      return;
    }

    if(selection === 'Qubits' && (!t1 || !t2 || !prob0 || !prob1 || !readoutError || !depth)){
      setError("All the field must be filled");
      setLoading(false)
      return;
    }

    if(selection === 'Gates' && (!gate_error_1 || !gate_error_2)){
      setError("All the field must be filled");
      setLoading(false)
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/predictCalibration', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          machine: machine, 
          selection: selection,
          t1: t1,
          t2: t2,
          prob0: prob0,
          prob1: prob1,
          readout_error: readoutError,
          depth: depth,
          gate_error_1: gate_error_1,
          gate_error_2: gate_error_2
        })
      });
      const data = await response.json();
      console.log(data.prediction[0].divergence)
      if (data.prediction && data.prediction.length > 0) {
        console.log(data)
        setPrediction(data.prediction[0].divergence);
        setError(null);
      } else {
        setError('No se encontraron predicciones válidas');
      }
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }finally {
      setLoading(false); // Ocultar el spinner al finalizar
    }
  };

  return (

    <div className="container">

      <div className="bar">
        <h1 className="title">Noise prediction of a calibration</h1>
      </div>

      <div className="selectors-row">
        <div className="selector-option">
          <select value={machine} onChange={handleChangeOption} className="selector-option-select">
            <option value="">Choose a machine</option>
            <option value="ibm Brisbane">ibm Brisbane</option>
            <option value="ibm Kyoto">ibm Kyoto</option>
            <option value="ibm Osaka">ibm Osaka</option>
          </select>
        </div>

        <div className="option-selector">
          <select value={selection} onChange={handleChangeSelection} className="option-selector-select">
            <option value="">Select an option</option>
            <option value="Qubits">Qubits</option>
            <option value="Gates">Gates</option>
          </select>
        </div>

        </div>

        
        {selection === 'Qubits' && 
          <>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              <div className="depth-selector">
                <select value={depth} onChange={handleChangeDepth} className="selector-option-select">
                  <option value="">Choose a depth</option>
                  <option value="5">5</option>
                  <option value="10">10</option>
                  <option value="15">15</option>
                </select>
              </div>
              <div className="input-container" >
                <label>T1:</label>
                <input type="number" value={t1 || ""} onChange={handleChangeT1} />
              </div>

              <div className="input-container">
                <label>T2:</label>
                <input type="number" value={t2 || ""} onChange={handleChangeT2} />
              </div>

              <div className="input-container">
                <label>Prob_meas0_prep1:</label>
                <input type="number" value={prob0 || ""} onChange={handleChangeProb0} />
              </div>

              <div className="input-container">
                <label>Prob_meas1_prep0:</label>
                <input type="number" value={prob1 || ""} onChange={handleChangeProb1} />
              </div>

              <div className="input-container">
                <label>Readout Error:</label>
                <input type="number" value={readoutError || ""} onChange={handleChangeReadoutError} />
              </div>
            </div>
          </>
        }


        {selection === 'Gates' && 
          <>
              <div className="input-container">
                <label>Gate error 1:</label>
                <input type="number" value={gate_error_1 || ""} onChange={handleChangeGate1} />
              </div>

              <div className="input-container">
                <label>Gate error 2:</label>
                <input type="number" value={gate_error_2 || ""} onChange={handleChangeGate2} />
              </div>
          </>
        }
      

      {error && 
        <p className="error-message">{error}</p>
      }

      <div className="container-button">
        <button onClick={handleButtonClick} className="button">Submit</button>
      </div>

      {loading && ( // Mostrar el spinner si está cargando
        <div className="loading">
          <h2>Cargando...</h2>
          <div>
            <div className="spinner"></div>
          </div>
        </div>
      )}

      {prediction.length !== 0  && !loading &&
        (
          <div>
            <h1>Quantum Noise Prediction</h1>
            <p>Prediction: {prediction}</p>
          </div>
        )
      }

    </div>
  );
}

export default Calibration;

import React, { useState } from 'react';
import './Calibration.css'

function Calibration() {
  const [machine, setMachine] = useState(""); 
  const [t1, setT1] = useState(""); 
  const [t2, setT2] = useState(""); 
  const [prob0, setProb0] = useState(""); 
  const [prob1, setProb1] = useState(""); 
  const [readoutError, setReadoutError] = useState(""); 
  const [prediction, setPrediction] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false); // Estado para controlar la visibilidad del spinner
  const [depth, setDepth] = useState(""); // Estado para almacenar la profundidad seleccionada

  const handleChangeOpcion = (event) => {
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
    setLoading(true); 
    if (!machine || !t1 || !t2 || !prob0 || !prob1 || !readoutError || !depth) {
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
          t1: t1,
          t2: t2,
          prob0: prob0,
          prob1: prob1,
          readout_error: readoutError,
          depth: depth
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
          <select value={machine} onChange={handleChangeOpcion} className="selector-option-select">
            <option value="">Choose a machine</option>
            <option value="ibm Brisbane">ibm Brisbane</option>
            <option value="ibm Kyoto">ibm Kyoto</option>
            <option value="ibm Osaka">ibm Osaka</option>
          </select>
        </div>

        <div className="depth-selector">
          <select value={depth} onChange={handleChangeDepth} className="option-selector-select">
            <option value="">Choose a depth</option>
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="15">15</option>
          </select>
          </div>
        </div>

        <div className="inputs-row">
          <div className="input-container">
            <label>T1:</label>
            <input type="number" value={t1} onChange={handleChangeT1} />
          </div>

          <div className="input-container">
            <label>T2:</label>
            <input type="number" value={t2} onChange={handleChangeT2} />
          </div>

          <div className="input-container">
            <label>Prob_meas0_prep1:</label>
            <input type="number" value={prob0} onChange={handleChangeProb0} />
          </div>

          <div className="input-container">
            <label>Prob_meas1_prep0:</label>
            <input type="number" value={prob1} onChange={handleChangeProb1} />
          </div>

          <div className="input-container">
            <label>Readout Error:</label>
            <input type="number" value={readoutError} onChange={handleChangeReadoutError} />
          </div>
        </div>

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
            <h1>Quantum Prediction</h1>
            <p>Prediction: {prediction}</p>
          </div>
        )
      }

    </div>
  );
}

export default Calibration;

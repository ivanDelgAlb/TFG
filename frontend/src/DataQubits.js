import React, { useState } from 'react';

function App() {
  const [machine, setMachine] = useState(""); 
  const [t1, setT1] = useState(""); 
  const [t2, setT2] = useState(""); 
  const [prob0, setProb0] = useState(""); 
  const [prob1, setProb1] = useState(""); 
  const [readoutError, setReadoutError] = useState(""); 
  const [fecha, setFecha] = useState(new Date()); 
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

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

  const handleButtonClick = async () => {
    if (!machine || !t1 || !t2 || !prob0 || !prob1 || !readoutError) {
      setError("Todos los campos son obligatorios");
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/predict', {
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
          date: fecha 
        })
      });
      const data = await response.json();
      setPrediction(data.prediction);
      setError(null); // Reiniciar el estado de error
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }
  };

  return (
    <div className="lila-franja">
      <div className="App">
        <h1 className="titulo">Mi TFG</h1>
        <div className="contenedor-selector">
          <div className="selector-option">
            <select value={machine} onChange={handleChangeOpcion} className="selector-option-select">
              <option value="">Selecciona una opción</option>
              <option value="ibm Brisbane">ibm Brisbane</option>
              <option value="ibm Kyoto">ibm Kyoto</option>
              <option value="ibm Osaka">ibm Osaka</option>
              {/* Agrega más opciones según sea necesario */}
            </select>
          </div>

          <div className="input-container">
            <label>T1:</label>
            <input type="number" value={t1} onChange={handleChangeT1} />
          </div>

          <div className="input-container">
            <label>T2:</label>
            <input type="number" value={t2} onChange={handleChangeT2} />
          </div>

          <div className="input-container">
            <label>Prob0:</label>
            <input type="number" value={prob0} onChange={handleChangeProb0} />
          </div>

          <div className="input-container">
            <label>Prob1:</label>
            <input type="number" value={prob1} onChange={handleChangeProb1} />
          </div>

          <div className="input-container">
            <label>Readout Error:</label>
            <input type="number" value={readoutError} onChange={handleChangeReadoutError} />
          </div>
        </div>

        {error && <p className="error-message">{error}</p>}

        <div className="contenedor-boton">
          <button onClick={handleButtonClick} className="boton">Submit</button>
        </div>

        <h1>Quantum Prediction</h1>
        <p>Prediction: {prediction}</p>
      </div>
    </div>
  );
}

export default App;

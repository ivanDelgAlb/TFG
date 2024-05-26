import React, { useState, useRef } from 'react';
import './Calibration.css'

function Calibration() {
  const [prediction, setPrediction] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [depth, setDepth] = useState("");
  const [nQubits, setNQubits] = useState("");
  const [tGates, setTGates] = useState("");
  const [phaseGates, setPhaseGates] = useState("");
  const [hGates, setHGates] = useState("");
  const [cNotGates, setCNotGates] = useState("");
  const [selection, setSelection] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);


  const handleChangeSelection = (event) => {
    setSelection(event.target.value);
  };

  const handleChangeDepth = (event) => {
    setDepth(event.target.value);
  };

  const handleChangeQubits = (event) => {
    setNQubits(event.target.value);
  };

  const handleChangeTGates = (event) => {
    setTGates(event.target.value);
  }

  const handleChangePhaseGates = (event) => {
    setPhaseGates(event.target.value);
  }

  const handleChangeHGates = (event) => {
    setHGates(event.target.value);
  }

  const handleChangeCNotGates = (event) => {
    setCNotGates(event.target.value);
  }

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if(file){
      const fileExtension = file.name.split('.').pop()
      if(fileExtension !== 'json'){

        setError("The configuration file must be a JSON")
        setSelectedFile(null)

        if(fileInputRef.current){
          fileInputRef.current.value = null;
        }
      }else{
        setError("")
        setSelectedFile(file);
      }
    }
    setSelectedFile(event.target.files[0]);
  }

  const handleFileRemove = () => {
    setSelectedFile(null);
    if(fileInputRef.current){
        fileInputRef.current.value = null
    }
  }

  const handleButtonClick = async () => {
    setError("")
    setLoading(true); 
    if (!selection) {
      setError("All the field must be filled");
      setLoading(false)
      return;
    }

    if(selectedFile === null){
        setError("You must submit a configuration file")
        setLoading(false)
        return;
    }

    try {
        const formData = new FormData()
        formData.append('selection', selection)
        formData.append('depth', depth)
        formData.append('file', selectedFile)
        formData.append('nQubits', nQubits)
        formData.append('tGates', tGates)
        formData.append('phaseGates', phaseGates)
        formData.append('hGates', hGates)
        formData.append('cNotGates', cNotGates)

        const response = await fetch('http://localhost:8000/predictCalibration/file', {
            method: 'POST',
            body: formData
        })

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
            <div style={{ display: 'flex', flexDirection: 'column', marginBottom: '10px'}}>
              <div className="depth-selector">
                <select value={depth} onChange={handleChangeDepth} className="selector-option-select">
                  <option value="">Choose a depth</option>
                  <option value="5">5</option>
                  <option value="10">10</option>
                  <option value="15">15</option>
                </select>
              </div>
            </div>
          </>
        }

        <h5>Introduce the number of gates of the circuit to be executed:</h5>

        <table style={{borderCollapse: 'separate', borderSpacing: '10px', marginBottom: '10px'}}>
          <tr>
            <td><label>Number of qubits:</label></td>
            <td><input className='input-gates' type="number" value={nQubits || ""} onChange={handleChangeQubits} /></td>
          </tr>
          <tr>
            <td><label>Number of T gates:</label></td>
            <td><input className='input-gates' type="number" value={tGates || ""} onChange={handleChangeTGates} /></td>
          </tr>
          <tr>
            <td><label>Number of Phase gates:</label></td>
            <td><input className='input-gates' type="number" value={phaseGates || ""} onChange={handleChangePhaseGates} /></td>
          </tr>
          <tr>
            <td><label>Number of Hadamard gates:</label></td>
            <td><input className='input-gates' type="number" value={hGates || ""} onChange={handleChangeHGates} /></td>
          </tr>
          <tr>
            <td><label>Number of C-Not gates:</label></td>
            <td><input className='input-gates' type="number" value={cNotGates || ""} onChange={handleChangeCNotGates} /></td>
          </tr>
        </table>

        <h5>Introduce a json file with the configuration of the machine (qiskit properties format):</h5>
        <input type="file" onChange={handleFileChange} ref={fileInputRef} style={{marginTop: '10px'}}/>
        {selectedFile && (
            <div>
                <button onClick={handleFileRemove} style={{marginTop: '10px'}}>Remove file</button>
            </div>
        )}

      {error && 
        <p className="error-message">{error}</p>
      }

      <div className="container-button">
        <button onClick={handleButtonClick} className="button" >Submit</button>
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

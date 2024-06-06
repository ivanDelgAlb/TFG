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
    const value = event.target.value;
    if(value < 0){
      return;
    }
    setNQubits(event.target.value);
  };

  const handleChangeTGates = (event) => {
    const value = event.target.value;
    if(value < 0){
      return;
    }
    setTGates(event.target.value);
  }

  const handleChangePhaseGates = (event) => {
    const value = event.target.value;
    if(value < 0){
      return;
    }
    setPhaseGates(event.target.value);
  }

  const handleChangeHGates = (event) => {
    const value = event.target.value;
    if(value < 0){
      return;
    }
    setHGates(event.target.value);
  }

  const handleChangeCNotGates = (event) => {
    const value = event.target.value;
    if(value < 0){
      return;
    }
    setCNotGates(event.target.value);
  }

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if(file){
      const fileExtension = file.name.split('.').pop()
      console.log(fileExtension)
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
    }else{
      setSelectedFile(null)
    }
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
      setError("You must select an option");
      setLoading(false)
      return;
    }

    if(selection === 'Qubits' && !depth){
      setError("You must select a depth")
      setLoading(false)
      return;
    }

    if(!nQubits){
      setError("You must select the number of qubits")
      setLoading(false)
      return;
    }

    if(!tGates){
      setError("You must select the number of T gates")
      setLoading(false)
      return;
    }

    if(!phaseGates){
      setError("You must select the number of phase gates")
      setLoading(false)
      return;
    }

    if(!hGates){
      setError("You must select the number of Hadamard gates")
      setLoading(false)
      return;
    }

    if(!cNotGates){
      setError("You must select the number of C-Not gates")
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
            setError('There was not any valid prediction');
        }
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }finally {
      setLoading(false);
    }
  };

  return (

    <div className="container">

      <div className="bar">
        <h1 className="title">Noise prediction of a calibration</h1>
      </div>

      <div className="selectors-row">

        <div className="option-selector">
          <select value={selection} onChange={handleChangeSelection} className="option-selector-select" aria-label='optionSelector'>
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
                <select value={depth} onChange={handleChangeDepth} className="selector-option-select" aria-label='depthSelector'>
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

        <table style={{borderCollapse: 'separate', borderSpacing: '10px', marginBottom: '10px', marginTop: '10px'}}>
          <tbody>
            <tr>
              <td><label>Number of qubits:</label></td>
              <td><input className='input-gates' type="number" value={nQubits || ""} onChange={handleChangeQubits} min={0} aria-label='nQubitsInput'/></td>
            </tr>
            <tr>
              <td><label>Number of T gates:</label></td>
              <td><input className='input-gates' type="number" value={tGates || ""} onChange={handleChangeTGates} min={0} aria-label='tGatesInput'/></td>
            </tr>
            <tr>
              <td><label>Number of Phase gates:</label></td>
              <td><input className='input-gates' type="number" value={phaseGates || ""} onChange={handleChangePhaseGates} min={0} aria-label='phaseGatesInput'/></td>
            </tr>
            <tr>
              <td><label>Number of Hadamard gates:</label></td>
              <td><input className='input-gates' type="number" value={hGates || ""} onChange={handleChangeHGates} min={0} aria-label='hGatesInput'/></td>
            </tr>
            <tr>
              <td><label>Number of C-Not gates:</label></td>
              <td><input className='input-gates' type="number" value={cNotGates || ""} onChange={handleChangeCNotGates} min={0} aria-label='cGatesInput'/></td>
            </tr>
          </tbody>
        </table>

        <h5>Introduce a json file with the configuration of the machine (qiskit properties format):</h5>
        <input type="file" onChange={handleFileChange} ref={fileInputRef} style={{marginTop: '10px'}} aria-label='fileInput' />
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

      {loading && (
        <div className="loading">
          <h2>Loading...</h2>
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

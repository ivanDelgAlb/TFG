import React, { useState, useRef } from 'react';
import './Calibration.css';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';

const MySwal = withReactContent(Swal);
const urlLocal = process.env.REACT_APP_URL_LOCALHOST;
const urlDesploy = process.env.REACT_APP_URL_DEPLOYMENT;
const deployment = process.env.REACT_APP_DEPLOYMENT;

function Calibration() {
  const [prediction, setPrediction] = useState("");
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
  const [model, setModel] = useState("");


  const handleChangeModel = (event) => {
    setModel(event.target.value);
  };

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
      setError("The number of T gates must be positive");
      return;
    }else if(!Number.isInteger(Number(value))){
      setError("The number of T gates must be an integer");
      return;
    }
    setError(null);
    setTGates(event.target.value);
  };

  const handleChangePhaseGates = (event) => {
    const value = event.target.value;
    if(value < 0){
      setError("The number of phase gates must be positive");
      return;
    }else if(!Number.isInteger(Number(value))){
      setError("The number of phase gates must be an integer");
      return;
    }
    setError(null);
    setPhaseGates(event.target.value);
  };

  const handleChangeHGates = (event) => {
    const value = event.target.value;
    if(value < 0){
      setError("The number of Hadamard gates must be positive");
      return;
    }else if(!Number.isInteger(Number(value))){
      setError("The number of Hadamard gates must be an integer");
      return;
    }
    setError(null);
    setHGates(event.target.value);
  };

  const handleChangeCNotGates = (event) => {
    const value = event.target.value;
    if(value < 0){
      setError("The number of C-Not gates must be positive");
      return;
    }else if(!Number.isInteger(Number(value))){
      setError("The number of C-Not gates must be an integer");
      return;
    }
    setError(null);
    setCNotGates(event.target.value);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if(file){
      const fileExtension = file.name.split('.').pop();
      if(fileExtension !== 'json'){
        setError("The configuration file must be a JSON");
        setSelectedFile(null);
        if(fileInputRef.current){
          fileInputRef.current.value = null;
        }
      }else{
        setError("");
        setSelectedFile(file);
      }
    }else{
      setSelectedFile(null);
    }
  };

  const handleFileRemove = () => {
    setSelectedFile(null);
    if(fileInputRef.current){
      fileInputRef.current.value = null;
    }
  };

  const popup = async () => {
    MySwal.fire({
      title: 'Prediction Result',
      text: `Prediction: ${"HELO"}`,
      icon: 'info',
    });
  }

  const handleButtonClick = async () => {
    setError("");
    setLoading(true);
    if (!selection) {
      setError("You must select an option");
      setLoading(false);
      return;
    }

    if(selection === 'Qubits' && !depth){
      setError("You must select a depth");
      setLoading(false);
      return;
    }

    if(!nQubits){
      setError("You must select the number of qubits");
      setLoading(false);
      return;
    }

    if(!tGates){
      setError("You must select the number of T gates");
      setLoading(false);
      return;
    }

    if(!phaseGates){
      setError("You must select the number of phase gates");
      setLoading(false);
      return;
    }

    if(!hGates){
      setError("You must select the number of Hadamard gates");
      setLoading(false);
      return;
    }

    if(!cNotGates){
      setError("You must select the number of C-Not gates");
      setLoading(false);
      return;
    }

    if(selectedFile === null){
      setError("You must submit a configuration file");
      setLoading(false);
      return;
    }

    try {
      const formData = new FormData();
      formData.append('selection', selection);
      formData.append('depth', depth);
      formData.append('model', model);
      formData.append('file', selectedFile);
      formData.append('nQubits', nQubits);
      formData.append('tGates', tGates);
      formData.append('phaseGates', phaseGates);
      formData.append('hGates', hGates);
      formData.append('cNotGates', cNotGates);

      const url = urlLocal

      if (deployment !== 'localhost') url = urlDesploy

      console.log(url)
      const response = await fetch( url + 'predictCalibration/', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log(data)
      if (data != null) {
        setError(null);
        console.log(data);
    
        let text = '';
    
        if (data['Perceptron']) {
          console.log("ENTRO")
            text += `Prediction Multilayer Perceptron: ${data['Perceptron'][0]['divergence']}`;
        }
    
        if (data['XgBoost']) {
          console.log("ENTRO")
            if (text !== '') {
                text += '<br>'; // Agregar un salto de línea si hay texto previo
            }
            text += `Prediction XGBoost: ${data['XgBoost'][0]['divergence']}`;
        }
    
        if (text !== '') {
            MySwal.fire({
                title: 'Prediction Result',
                html: text,
                icon: 'info',
            });
            setPrediction(data.prediction);
        } else {
            setError('There was not any valid prediction');
        }}
    
    } catch (error) {
      if(error.message.includes('400')){
        MySwal.fire({
          title: 'Error!',
          text: 'The JSON file provided is not valid',
          icon: 'error',
        });
      }else{
        console.error('Error fetching prediction:', error);
        MySwal.fire({
          title: 'Error!',
          text: 'An unexpected error occurred',
          icon: 'error',
        });
      }
    }finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="bar">
        <h1 className="title">Noise prediction of a calibration</h1>
      </div>

      <div className="selectors">
      <div className="option-selector">
          <select
            value={selection}
            onChange={handleChangeSelection}
            className={`option-selector-select ${selection ? 'selected' : ''}`}
            aria-label="Select an option"
          >
            <option value="">Select an option</option>
            <option value="Qubits">Qubits</option>
            <option value="Gates">Gates</option>
          </select>
          {selection && <label htmlFor="nQubitsInput" className="select-label">Option selected:</label>}
        </div>

        {selection === 'Qubits' && (
          <div className="depth-selector">
            <select
              value={depth}
              onChange={handleChangeDepth}
              className={`option-selector-select ${depth ? 'selected' : ''}`}
              aria-label="Select a depth"
            >
              <option value="">Select a depth</option>
              <option value="5">5</option>
              <option value="10">10</option>
              <option value="15">15</option>
            </select>
            {depth && <label htmlFor="nQubitsInput" className="select-label">Depth selected:</label>}
          </div>
        )}
          <div className="model-selector">
            <select
              value={model}
              onChange={handleChangeModel}
              className={`option-selector-select ${model ? 'selected' : ''}`}
              aria-label='Select a model'
            >
              <option value="">Select a model</option>
              <option value="Perceptron">Multilayer Perceptron</option>
              <option value="XgBoost">XgBoost</option>
              <option value="Perceptron-XgBoost">Both</option>
            </select>
            {model && <label htmlFor="nQubitsInput" className="select-label">Model selected:</label>}
          </div>
      </div>

          <div className="select-container">
          <select
            id="nQubitsInput"
            value={nQubits}
            onChange={handleChangeQubits}
            aria-label="nQubitsInput"
            className={`input-qubits ${nQubits ? 'selected' : ''}`}
          >
            <option value="">Select the number of qubits of the circuit</option>
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="15">15</option>
          </select>
         {nQubits &&  
          <label htmlFor="nQubitsInput" className="select-label">
            Select the number of qubits of the circuit
          </label>}
        </div>

      <h5>Introduce the number of gates of the circuit to be executed:</h5>

      <table style={{ borderCollapse: 'collapse', borderSpacing: '10px', marginBottom: '10px', marginTop: '10px'}}>
        <tbody>
          <tr>
            <td><label>Number of T gates:</label></td>
            <td><input className='input-gates' type="number" value={tGates || ""} onChange={handleChangeTGates} min={0} aria-label='tGatesInput' /></td>
          </tr>
          <tr>
            <td><label>Number of Phase gates:</label></td>
            <td><input className='input-gates' type="number" value={phaseGates || ""} onChange={handleChangePhaseGates} min={0} aria-label='phaseGatesInput' /></td>
          </tr>
          <tr>
            <td><label>Number of Hadamard gates:</label></td>
            <td><input className='input-gates' type="number" value={hGates || ""} onChange={handleChangeHGates} min={0} aria-label='hGatesInput' /></td>
          </tr>
          <tr>
            <td><label>Number of C-Not gates:</label></td>
            <td><input className='input-gates' type="number" value={cNotGates || ""} onChange={handleChangeCNotGates} min={0} aria-label='cGatesInput' /></td>
          </tr>
        </tbody>
      </table>

      <h5>Introduce a json file with the configuration of the machine (Qiskit properties format):</h5>
      <input type="file" onChange={handleFileChange} ref={fileInputRef} style={{ marginTop: '10px' }} aria-label='fileInput' />
      {selectedFile && (
        <div>
          <button onClick={handleFileRemove} style={{ marginTop: '10px' }}>Remove file</button>
        </div>
      )}

      {error && <p className="error-message">{error}</p>}

      <div className="container-button">
        <div className='button-loading'>
          <button onClick={handleButtonClick} disabled={loading} className={loading ? "button-disabled" : "button-enabled"}>
            {loading ? "Loading..." : "Predict Error"}
          </button>
        </div>

        <div>
          {prediction && 
          <button onClick={popup} disabled={loading} className={loading ? "button-disabled" : "button-enabled"}>
            Show Prediction
          </button>
        }
        </div>
      </div>

      

      {loading && <div className="loading"><div className="spinner"></div></div>}
    </div>
  );
}

export default Calibration;

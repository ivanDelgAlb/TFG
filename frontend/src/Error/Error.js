import React, { useState } from 'react';
import './Error.css';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCalendar } from '@fortawesome/free-solid-svg-icons';
import Graph from '../Graph/Graph';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';

const MySwal = withReactContent(Swal);

const CustomDateTimePickerInput = React.forwardRef(({ value, onClick }, ref) => (
  <div className="custom-datepicker-input" onClick={onClick} ref={ref} aria-label='selected date'>
    <span>{value}</span>
    <FontAwesomeIcon icon={faCalendar} className="icono-calendario" />
  </div>
));

const DateTimePicker = ({ selectedDateTime, onChange }) => (
  <DatePicker
    selected={selectedDateTime}
    onChange={onChange}
    showTimeSelect
    timeFormat="HH:mm"
    timeIntervals={60}
    dateFormat="dd/MM/yyyy HH:mm"
    customInput={<CustomDateTimePickerInput />}
  />
);

function Error() {
  const [machine, setMachine] = useState("");
  const [date, setDate] = useState(new Date());
  const [selection, setSelection] = useState("");
  const [depth, setDepth] = useState("");
  const [prediction, setPrediction] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showCalibrationGraphs, setShowCalibrationGraphs] = useState(false);

  const [nQubits, setNQubits] = useState(null); 
  const [tGates, setTGates] = useState(null); 
  const [phaseGates, setPhaseGates] = useState(null); 
  const [hGates, setHGates] = useState(null); 
  const [cnotGates, setCnotGates] = useState(null); 
  const [model, setModel] = useState("");


  const handleChangeModel = (event) => {
    setModel(event.target.value);
  };

  const handleChangeNQubits = (event) => {
    const value = event.target.value;
    if(value < 0){
      return;
    }
    setNQubits(event.target.value);
  };

  const handleChangeTGates = (event) => {
    const value = event.target.value;
    if(value < 0){
      setError("The number of T gates must be positive")
      return;
    }else if(!Number.isInteger(Number(value))){
      setError("The number of T gates must be an integer")
      return;
    }
    setError(null)
    setTGates(event.target.value);
  };

  const handleChangePhaseGates = (event) => {
    const value = event.target.value;
    if(value < 0){
      setError("The number of phase gates must be positive")
      return;
    }else if(!Number.isInteger(Number(value))){
      setError("The number of phase gates must be an integer")
      return;
    }
    setError(null)
    setPhaseGates(event.target.value);
  };

  const handleChangeHGates = (event) => {
    const value = event.target.value;
    if(value < 0){
      setError("The number of Hadamard gates must be positive")
      return;
    }else if(!Number.isInteger(Number(value))){
      setError("The number of Hadamard gates must be an integer")
      return;
    }
    setError(null)
    setHGates(event.target.value);
  };

  const handleChangeCnotGates = (event) => {
    const value = event.target.value;
    if(value < 0){
      setError("The number of C-Not gates must be positive")
      return;
    }else if(!Number.isInteger(Number(value))){
      setError("The number of C-Not gates must be an integer")
      return;
    }
    setError(null)
    setCnotGates(event.target.value);
  };

  const handleChangeMachine = (event) => {
    setMachine(event.target.value);
  };

  const handleChangeSelection = (event) => {
    setSelection(event.target.value);
    setShowCalibrationGraphs(false);
    setPrediction([]);
  };

  const handleChangeDepth = (event) => {
    setDepth(event.target.value);
  };

  const handleButtonClick = async () => {
    setError(null);
    setLoading(true);
    setPrediction([])

    if (!machine) {
      setError("You must select a machine");
      setLoading(false);
      return;
    }

    if(!selection){
      setError("You must select an option")
      setLoading(false);
      return;
    }

    if(!model){
      setError("You must select a model")
      setLoading(false);
      return;
    }

    if (selection === 'Qubits' && depth === '') {
      setError("You must select a depth");
      setLoading(false);
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

    if(!cnotGates){
      setError("You must select the number of C-Not gates")
      setLoading(false)
      return;
    }

    const currentDate = new Date();

    if (date < currentDate) {
      setError("Selected date must be after the current date");
      setLoading(false);
      return;
    }

    const isoDate = date.toISOString();

    try {
      MySwal.fire({
        title: 'Warning',
        text: 'The prediction may take some time to execute.',
        icon: 'info',
      });
      const response = await fetch('http://localhost:8000/predictError', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          machine: machine,
          date: isoDate,
          selection: selection,
          depth: depth,
          nQubits: nQubits,
          tGates: tGates,
          hGates: hGates,
          phaseGates: phaseGates,
          cnotGates: cnotGates,
          model: model
        })
      });
      const data = await response.json();
      const hasValidPredictions = Object.values(data).some(arr => Array.isArray(arr) && arr.length > 0);

      if (data) {
        console.log(data)
        setPrediction(data);
        setError(null);
        setShowCalibrationGraphs(true);
      } else {
        setError('No valid predictions found');
      }
    } catch (error) {
      console.error('Error fetching prediction:', error);
    } finally {
      setLoading(false);
    }
  };


  return (
    <>
      <div className="container">
        <div className="bar">
          <h1 className="title">Prediction within a Date Range</h1>
        </div>
        
        <div className="selectors">
          <div className="machine-selector">
          <select
            value={machine}
            onChange={handleChangeMachine}
            aria-label="Select a Select"
            className={`option-selector-select ${machine ? 'selected' : ''}`}
          >
            <option value="">Select a machine</option>
            <option value="ibm Brisbane">ibm Brisbane</option>
            <option value="ibm Kyoto">ibm Kyoto</option>
            <option value="ibm Osaka">ibm Osaka</option>
            <option value="All">All of the options</option>
          </select>
          {machine && <label htmlFor="nQubitsInput" className="select-label">Machine selected:</label>}
        </div>

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
          
          <div className="date-selector">
            <DateTimePicker selectedDateTime={date} onChange={setDate} />
          </div>
        </div>

        <div className="select-container">
          <select
            id="nQubitsInput"
            value={nQubits}
            onChange={handleChangeNQubits}
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


        

        <div className="table-container">
          <table>
            <tbody>
              <tr>
                <td><label>Number of T gates:</label></td>
                <td><input className='input-gates' type="number" value={tGates || ""} onChange={handleChangeTGates} min={0} aria-label='tGatesInput'/></td>
              </tr>
              <tr>
                <td><label>Number of phase gates:</label></td>
                <td><input className='input-gates' type="number" value={phaseGates || ""} onChange={handleChangePhaseGates} min={0} aria-label='phaseGatesInput'/></td>
              </tr>
              <tr>
                <td><label>Number of Hadamard gates:</label></td>
                <td><input className='input-gates' type="number" value={hGates || ""} onChange={handleChangeHGates} min={0} aria-label='hGatesInput'/></td>
              </tr>
              <tr>
                <td><label>Number of C-Not gates:</label></td>
                <td><input className='input-gates' type="number" value={cnotGates || ""} onChange={handleChangeCnotGates} min={0} aria-label='cnotGatesInput'/></td>
              </tr>
            </tbody>
          </table>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="container-button">
          <button onClick={handleButtonClick} disabled={loading} className={loading ? "button-disabled" : "button-enabled"}>
            {loading ? "Loading..." : "Predict Error"}
          </button>
        </div>

        {loading && <div className="loading"><div className="spinner"></div></div>}
        

        {!loading && showCalibrationGraphs && prediction && (
          <div className="graph-container" aria-label='graph-container'>
            <h2>Error Predictions:</h2>
            <Graph predictions={prediction} type={'divergence'}/>

            {selection === "Qubits" && showCalibrationGraphs && (
              <div>
                <div style={{ marginBottom: '40px' }}>
                  <h2>Historical T1:</h2>
                  <Graph predictions={prediction} type={'T1'} historical={true} calibraciones={false}/>
                </div>
                <div style={{ marginBottom: '40px' }}>
                  <h2>Historical T2:</h2>
                  <Graph predictions={prediction} type={'T2'} historical={true} calibraciones={false}/>
                </div>
                <div style={{ marginBottom: '40px' }}>
                  <h2>Historical Prob_Meas0_Prep1:</h2>
                  <Graph predictions={prediction} type={'Prob0'} historical={true} calibraciones={false}/>
                </div>
                <div style={{ marginBottom: '40px' }}>
                  <h2>Historical Prob_Meas1_Prep0:</h2>
                  <Graph predictions={prediction} type={'Prob1'} historical={true} calibraciones={false}/>
                </div>
                <div style={{ marginBottom: '40px' }}>
                  <h2>Historical Readout_error:</h2>
                  <Graph predictions={prediction} type={'Error'} historical={true}calibraciones={false}/>
                </div>
              </div>
            )}

            {selection === "Gates" && showCalibrationGraphs && (
              <div>
                <div style={{ marginBottom: '40px' }}>
                  <h2>Historical Gate error of one-qubit input:</h2>
                  <Graph predictions={prediction} type={'error_gate_1_qubit'} historical={true} calibraciones={false}/>
                </div>
                <div style={{ marginBottom: '40px' }}>
                  <h2>Historical Gate error of two-qubit input:</h2>
                  <Graph predictions={prediction} type={'error_gate_2_qubit'} historical={true} calibraciones={false}/>
                </div>
              </div>
            )}

          </div>
        )}
      </div>
    </>
  );
}

export default Error;

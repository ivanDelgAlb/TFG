import React, { useState } from 'react';
import './Error.css';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCalendar } from '@fortawesome/free-solid-svg-icons';
import Graph from '../Graph/Graph';

const CustomDateTimePickerInput = React.forwardRef(({ value, onClick }, ref) => (
  <div className="custom-datepicker-input" onClick={onClick} ref={ref}>
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

  const handleChangeNQubits = (event) => {
    setNQubits(event.target.value);
  };

  const handleChangeTGates = (event) => {
    setTGates(event.target.value);
  };

  const handleChangePhaseGates = (event) => {
    setPhaseGates(event.target.value);
  };

  const handleChangeHGates = (event) => {
    setHGates(event.target.value);
  };

  const handleChangeCnotGates = (event) => {
    setCnotGates(event.target.value);
  };


  const handleButtonCalibration = () => {
    setShowCalibrationGraphs(!showCalibrationGraphs);
  };

  const handleChangeMachine = (event) => {
    setMachine(event.target.value);
  };

  const handleChangeSelection = (event) => {
    setSelection(event.target.value);
    setShowCalibrationGraphs(false); // Ocultar la gráfica al cambiar la selección
    setPrediction([]); // Borrar los datos de predicción al cambiar la selección
  };

  const handleChangeDepth = (event) => {
    setDepth(event.target.value);
  };

  const handleButtonClick = async () => {
    setError(null);
    setLoading(true);

    if (!machine || !selection || !date) {
      setError("All fields are required");
      setLoading(false);
      return;
    }

    if (selection === 'Qubits' && (depth === '' || !nQubits || !tGates || !hGates || !phaseGates || !cnotGates)) {
      setError("All fields are required");
      setLoading(false);
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
          cnotGates: cnotGates
        })
      });
      const data = await response.json();
      console.log(data.prediction);
      if (data.prediction && data.prediction.length > 0) {
        setPrediction(data.prediction);
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
          <select value={machine} onChange={handleChangeMachine}>
            <option value="">Select a machine</option>
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

        <div className="date-selector">
          <DateTimePicker selectedDateTime={date} onChange={setDate} />
        </div>

      </div>

       {selection === 'Qubits' && 

        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <div className="depth-selector">
            <select value={depth} onChange={handleChangeDepth} className="option-selector-select">
              <option value="">Select a depth</option>
              <option value="5">5</option>
              <option value="10">10</option>
              <option value="15">15</option>
            </select>
          </div>
          </div>
        } 

        <table style={{borderCollapse: 'separate', borderSpacing: '10px', marginBottom: '10px', marginTop: '10px'}}>
          <tr>
            <td><label>Number of nQubitsubits:</label></td>
            <td><input className='input-gates' type="number" value={nQubits || ""} onChange={handleChangeNQubits} /></td>
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
            <td><input className='input-gates' type="number" value={cnotGates || ""} onChange={handleChangeCnotGates} /></td>
          </tr>
        </table>

      {error && <p className="error-message">{error}</p>}

      <div className="container-button">
        <button onClick={handleButtonClick} className="button">Submit</button>
      </div>

      {loading && (
        <div className="loading">
          <h2>Loading...</h2>
          <div>
            <div className="spinner"></div>
          </div>
        </div>
      )}
      
      {prediction.length !== 0 && !loading && (
        <>
        <div className="container-button">
          <button onClick={handleButtonCalibration} className="button">
            {showCalibrationGraphs ? "Hide Calibration Charts" : "Show Calibration Charts"}
          </button>
        </div>
          {showCalibrationGraphs && prediction && (
            <div className="graph-container">
              <h2>Error Predictions:</h2>
              <Graph predictions={prediction} type={'divergence'} color={'#ff0000'}/>

              {selection === "Qubits" && showCalibrationGraphs && (
                <div>
                  <div style={{ marginBottom: '40px' }}>
                    <h2>Historical T1:</h2>
                    <Graph predictions={prediction} type={'T1'} historical={true} color={'#1f77b4'}/>
                  </div>
                  <div style={{ marginBottom: '40px' }}>
                    <h2>Historical T2:</h2>
                    <Graph predictions={prediction} type={'T2'} historical={true} color={'#660066'}/>
                  </div>
                  <div style={{ marginBottom: '40px' }}>
                    <h2>Historical Prob_Meas0_Prep1:</h2>
                    <Graph predictions={prediction} type={'Prob0'} historical={true} color={'#006600'}/>
                  </div>
                  <div style={{ marginBottom: '40px' }}>
                    <h2>Historical Prob_Meas1_Prep0:</h2>
                    <Graph predictions={prediction} type={'Prob1'} historical={true} color={'#000099'}/>
                  </div>
                  <div style={{ marginBottom: '40px' }}>
                    <h2>Historical Readout_error:</h2>
                    <Graph predictions={prediction} type={'Error'} historical={true} color={'#ff6600'}/>
                  </div>
                </div>
              )}

              {selection === "Gates" && showCalibrationGraphs && (
                <div>
                  <div style={{ marginBottom: '40px' }}>
                    <h2>Historical Gate error of one-qubit input:</h2>
                    <Graph predictions={prediction} type={'gate_error_1'} historical={true} color={'#e6e600'}/>
                  </div>
                  <div style={{ marginBottom: '40px' }}>
                    <h2>Historical Gate error of two-qubit input:</h2>
                    <Graph predictions={prediction} type={'gate_error_2'} historical={true} color={'#2f4f4f'}/>
                  </div>
                  {/* Rest of historical graphs */}
                </div>
              )}

            </div>
          )}
        </>
      )}

      
    </div>
    </>
  );
}

export default Error;

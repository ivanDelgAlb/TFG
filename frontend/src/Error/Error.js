import React, { useState } from 'react';
import './Error.css';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCalendar } from '@fortawesome/free-solid-svg-icons';
import Graph from '../Graph/Graph'; // Importa el componente de la gráfica

// Define DateTimePicker component outside of App
const CustomDateTimePickerInput = ({ value, onClick }) => (
  <div className="custom-datepicker-input" onClick={onClick}>
    <span>{value}</span>
    <FontAwesomeIcon icon={faCalendar} className="icono-calendario" />
  </div>
);

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
  const [machine, setMachine] = useState(""); // Estado para almacenar la máquina seleccionada
  const [date, setDate] = useState(new Date()); // Estado para almacenar la fecha seleccionada
  const [selection, setSelection] = useState(""); // Estado para almacenar la selección de qubits o puertas
  const [depth, setDepth] = useState(""); // Estado para almacenar la profundidad seleccionada
  const [prediction, setPrediction] = useState([]);
  const [loading, setLoading] = useState(false); // Estado para controlar la visibilidad del spinner
  const [error, setError] = useState(null);

  const [showCalibrationGraphs, setShowCalibrationGraphs] = useState(false);

  const handleButtonCalibration = () => {
    setShowCalibrationGraphs(!showCalibrationGraphs); // Cambiar el estado de visibilidad
  };

  const handleChangeMachine = (event) => {
    setMachine(event.target.value);
  };

  const handleChangeSelection = (event) => {
    setSelection(event.target.value);
  };

  const handleChangeDepth = (event) => {
    setDepth(event.target.value);
  };

  const handleButtonClick = async () => {
    setError(null)
    setLoading(true); // Mostrar el spinner al inicio de la carga

    if (!machine || !selection || !date || !depth) {
      setError("Todos los campos son obligatorios");
      setLoading(false); // Ocultar el spinner al finalizar
      return;
    }

    // Get current date
    const currentDate = new Date();

    // Check if selected date is earlier than current date
    if (date < currentDate) {
        setError("La fecha seleccionada debe ser posterior a la fecha actual");
        setLoading(false); // Ocultar el spinner al finalizar
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
          depth: depth
        })
      })
      const data = await response.json();
      console.log(data.prediction)
      if (data.prediction && data.prediction.length > 0) {
        console.log(data.prediction)
        setPrediction(data.prediction);
        setError(null);
      } else {
        setError('No se encontraron predicciones válidas');
      }
    } catch (error) {
      console.error('Error fetching prediction:', error);
    } finally {
      setLoading(false); // Ocultar el spinner al finalizar
    }
  };

  return (
    <>
    <div className="container">
      <div className="bar">
        <h1 className="title">Predicción dado un rango de fechas</h1>
      </div>
      
      <div className="selectors">
        <div className="machine-selector">
          <select value={machine} onChange={handleChangeMachine}>
            <option value="">Selecciona una máquina</option>
            <option value="ibm Brisbane">ibm Brisbane</option>
            <option value="ibm Kyoto">ibm Kyoto</option>
            <option value="ibm Osaka">ibm Osaka</option>
          </select>
        </div>
        
        <div className="option-selector">
          <select value={selection} onChange={handleChangeSelection} className="option-selector-select">
            <option value="">Selecciona una opción</option>
            <option value="Qubits">Qubits</option>
            <option value="Puertas">Puertas</option>
          </select>
        </div>

        <div className="depth-selector">
          <select value={depth} onChange={handleChangeDepth} className="option-selector-select">
            <option value="">Selecciona una profundidad</option>
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="15">15</option>
          </select>
        </div>

        <div className="date-selector">
          <DateTimePicker selectedDateTime={date} onChange={setDate} />
        </div>
      </div>

      {error && <p className="error-message">{error}</p>}

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

      {prediction.length !== 0 && !loading && ( // Mostrar la gráfica si hay datos y no está cargando
        <div className="graph-container">
          <h2>Predicciones del error:</h2>
          <Graph predictions={prediction} type={'divergence'} /> {/* Mostrar la gráfica */}
          <div className="container-button">
            <button onClick={handleButtonCalibration} className="button">
              {showCalibrationGraphs ? "Ocultar Gráficas de Calibraciones" : "Ver Gráficas de Calibraciones"}
            </button>
          </div>
          {showCalibrationGraphs && (
            <div>
              <div style={{ marginBottom: '40px' }}>
                <h2>Predicciones T1:</h2>
                <Graph predictions={prediction} type={'T1'} />
              </div>
              <div style={{ marginBottom: '40px' }}>
                <h2>Predicciones T2:</h2>
                <Graph predictions={prediction} type={'T2'} />
              </div>
              <div style={{ marginBottom: '40px' }}>
                <h2>Predicciones Prob0:</h2>
                <Graph predictions={prediction} type={'Prob0'} />
              </div>
              <div style={{ marginBottom: '40px' }}>
                <h2>Predicciones Prob1:</h2>
                <Graph predictions={prediction} type={'Prob1'} />
              </div>
              <div style={{ marginBottom: '40px' }}>
                <h2>Predicciones Error length:</h2>
                <Graph predictions={prediction} type={'Error'} />
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

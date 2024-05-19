import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import './Graph.css'

const Graph = ({ predictions, type, historical }) => {
  const getRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  };

  
  const chartRef = useRef(null);
  const [minTypeDates, setMinTypeDates] = useState([]);
  const [minType, setMinType] = useState(null);
  const [isRange, setIsRange] = useState(false);

  useEffect(() => {
    if (predictions.length === 0) return;

    // Obtener fechas y datos del tipo especificado
    const dates = predictions.map(prediction => prediction.Date);
    const typeData = predictions.map(prediction => prediction[type]);

    // Calcular el valor mínimo del tipo especificado
    
    const minTypeValue = Math.min(...typeData);
    // Obtener todas las fechas correspondientes al valor mínimo del tipo especificado
    const minTypeDates = predictions
      .filter(prediction => prediction[type] === minTypeValue)
      .map(prediction => prediction.Date);

    setMinTypeDates(minTypeDates);
    setMinType(minTypeValue);
    setIsRange(minTypeDates.length > 1);

    const margin = (Math.max(...typeData) - minTypeValue) * 0.1; // Margen del 10%
    const minY = minTypeValue - margin;
    const maxY = Math.max(...typeData) + margin;

    const cursorColor = getRandomColor();

    const chartData = {
      labels: dates,
      datasets: [
        {
          label: type,
          data: typeData,
          borderColor: cursorColor, // Color aleatorio para el borde
          backgroundColor: cursorColor, // Color aleatorio para el fondo
          pointBackgroundColor: dates.map(date => minTypeDates.includes(date) ? cursorColor : 'rgba(255, 99, 132, 0.2)'), // Usar el mismo color aleatorio para los puntos
          pointRadius: dates.map(date => minTypeDates.includes(date) ? 5 : 3),
        }
      ],
    };

    const chartOptions = {
      scales: {
        y: {
          beginAtZero: false,
          min: minY,
          max: maxY,
        },
        x: {
          ticks: {
            maxTicksLimit: 5, // Limitar el número máximo de etiquetas del eje X
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: (context) => {
              const label = context.dataset.label || '';
              if (context.parsed.y === minTypeValue) {
                return [`Type: ${type}`, `Min value: ${minTypeValue}`];
              }
              return `${type}: ${context.parsed.y}`;
            }
          }
        }
      },
      legend: {
        position: 'right', // Ajusta la posición de la leyenda a la derecha
      }
    };

    const canvas = chartRef.current;
    const myChart = new Chart(canvas, {
      type: 'line',
      data: chartData,
      options: chartOptions,
    });

    const resizeChart = () => {
      myChart.resize();
    };

    resizeChart();

    window.addEventListener('resize', resizeChart);

    return () => {
      myChart.destroy();
      window.removeEventListener('resize', resizeChart);
    };
  }, [predictions, type, isRange]);

  return (
    <div className='graph' style={{ display: 'flex', justifyContent: 'space-between', width: '70%', margin: 'auto' }}>
      <canvas ref={chartRef} width={400} height={200}></canvas>
      {!historical && minTypeDates.length > 0 && (
        <div className="best-result" style={{margin: '20px'}}>
          <p>
            <span style={{ fontWeight: 'bold'}}>Best Result:</span> {type} of <span style={{ fontWeight: 'bold' , color: '#64ace8' }}>{minType}</span> at <span style={{ fontWeight: 'bold', color: 'rgb(182, 182, 182)' }}>{minTypeDates.join(', ')}</span>
          </p>
        </div>
      )}
    </div>
  );
};

export default Graph;

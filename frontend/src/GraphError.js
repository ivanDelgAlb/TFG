import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';

const Graph = ({ predictions }) => {
  const chartRef = useRef(null);
  const [minDivergenceDates, setMinDivergenceDates] = useState([]);
  const [minDivergence, setMinDivergence] = useState(null);
  const [isRange, setIsRange] = useState(false);

  useEffect(() => {
    if (predictions.length === 0) return;

    // Obtener fechas y divergencias de los datos
    const dates = predictions.map(prediction => prediction.Date);
    const divergences = predictions.map(prediction => prediction.divergence);

    // Calcular el valor mínimo de divergencia
    const minDivergenceValue = Math.min(...divergences);

    // Obtener todas las fechas correspondientes al valor mínimo de divergencia
    const minDivergenceDates = predictions
      .filter(prediction => prediction.divergence === minDivergenceValue)
      .map(prediction => prediction.Date);

    setMinDivergenceDates(minDivergenceDates);
    setMinDivergence(minDivergenceValue);
    setIsRange(minDivergenceDates.length > 1);

    const margin = (Math.max(...divergences) - minDivergenceValue) * 0.1; // Margen del 10%
    const minY = minDivergenceValue - margin;
    const maxY = Math.max(...divergences) + margin;

    const chartData = {
      labels: dates,
      datasets: [
        {
          label: 'Divergence',
          data: divergences,
          borderColor: 'rgba(255, 99, 132, 1)',
          backgroundColor: (context) => {
            if (minDivergenceDates.includes(dates[context.dataIndex])) {
              return 'rgba(0, 0, 0, 1)'; // Cambia el color a negro para los valores mínimos
            } else {
              return 'rgba(255, 99, 132, 0.2)';
            }
          },
        },
        // Dataset adicional para mostrar el valor mínimo en la leyenda
        {
          label: `Min Value (${minDivergence})`, // Etiqueta personalizada para el valor mínimo
          backgroundColor: 'rgba(0, 0, 0, 1)', // Color negro para el valor mínimo
          borderColor: 'rgba(0, 0, 0, 1)', // Color de borde negro
          fill: false, // Sin relleno
          hidden: false, // Mostrar en la leyenda
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
              if (context.parsed.y === minDivergence) {
                return [`Divergence: ${context.parsed.y}`, `Min value: ${context.parsed.y}`];
              }
              return `Divergence: ${context.parsed.y}`;
            }
          }
        }
      },
      legend: {
        position: 'right', // Ajusta la posición de la leyenda a la derecha
      }
    };

    const canvas = chartRef.current;
    const context = canvas.getContext('2d');
    const gradient = context.createLinearGradient(0, 0, 0, canvas.clientHeight);
    gradient.addColorStop(0, isRange ? 'rgba(54, 162, 235, 0.2)' : 'rgba(255, 99, 132, 0.2)');
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');

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
  }, [predictions, isRange]);

  return (
    <div className='graph' style={{ display: 'flex', justifyContent: 'space-between', width: '70%', margin: 'auto' }}>
      <canvas ref={chartRef} width={400} height={200}></canvas>
      {minDivergenceDates.length > 0 && (
        <p>
          Best Result: An error of {minDivergence} at {minDivergenceDates.join(', ')}
        </p>
      )}
    </div>
  );
};

export default Graph;

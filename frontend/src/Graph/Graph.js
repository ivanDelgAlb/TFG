import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import './Graph.css'

const Graph = ({ predictions, type, historical }) => {
  const getRandomColor = () => {
    /*
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    */
    const colors = ['#1f77b4', '#006699', '#e60000', '#006600', '#ff0000']
    const color = colors[Math.floor(Math.random() * colors.length)]
    return color;
  };

  
  const chartRef = useRef(null);

  useEffect(() => {
    if (predictions.length === 0) return;

    const dates = predictions.map(prediction => prediction.Date);
    const typeData = predictions.map(prediction => prediction[type]);

    const margin = (Math.max(...typeData) - Math.min(...typeData)) * 0.1; // Margen del 10%
    const minY = Math.min(...typeData) - margin;
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
          pointBackgroundColor: cursorColor, // Usar el mismo color aleatorio para los puntos
          pointRadius: 3,
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
  }, [predictions, type]);

  return (
    <div className='graph' style={{ display: 'flex', justifyContent: 'space-between', width: '70%', margin: 'auto' }}>
      <canvas ref={chartRef} width={400} height={200}></canvas>
      {!historical && (
        <div className="best-result" style={{margin: '20px'}}>
          <p>
            <span style={{ fontWeight: 'bold'}}>Best Result:</span> {type} of <span style={{ fontWeight: 'bold' , color: '#64ace8' }}>{Math.min(...predictions.map(prediction => prediction[type]))}</span>
          </p>
        </div>
      )}
    </div>
  );
};

export default Graph;

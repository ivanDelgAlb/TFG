import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import './Graph.css';

const Graph = ({ predictions, type, historical, color }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (predictions.length === 0) {
      console.log("No predictions provided.");
      return;
    }

    const dates = predictions.map(prediction => prediction.Date);
    const typeData = predictions.map(prediction => prediction[type]);

    console.log("Dates:", dates);
    console.log(`${type} Data:`, typeData);

    const allEqual = typeData.every(val => val === typeData[0]);
    const cursorColor = color;

    const margin = (Math.max(...typeData) - Math.min(...typeData)) * 0.1;
    const minY = allEqual ? typeData[0] - 1 : Math.min(...typeData) - margin;
    const maxY = allEqual ? typeData[0] + 1 : Math.max(...typeData) + margin;

    const chartData = {
      labels: dates,
      datasets: [
        {
          label: historical ? type : getBestResultLabel(predictions, type),
          data: typeData,
          borderColor: cursorColor,
          backgroundColor: cursorColor,
          pointBackgroundColor: cursorColor,
          pointRadius: historical ? 3 : 6, // Tamaño del punto más grande si no es historical
        }
      ],
    };

    const chartOptions = {
      scales: {
        y: {
          beginAtZero: !allEqual,
          min: minY,
          max: maxY,
        },
        x: {
          ticks: {
            maxTicksLimit: 5,
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
        position: 'right',
      }
    };

    const canvas = chartRef.current;
    if (canvas) {
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
    } else {
      console.log("Canvas element is not found.");
    }
  }, [predictions, type, color, historical]);

  // Función para obtener la etiqueta del mejor resultado
  const getBestResultLabel = (predictions, type) => {
    const bestResult = Math.min(...predictions.map(prediction => prediction[type]));
    return `${type} (Best Result: ${bestResult})`;
  };

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

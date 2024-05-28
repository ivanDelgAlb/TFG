import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import './Graph.css';

const Graph = ({ predictions, type, historical }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!predictions || Object.keys(predictions).length === 0) {
      console.log("No predictions provided.");
      return;
    }

    const datasets = [];
    const palette = ['#FF6B6B', '#78c2ad', '#FFE66D', '#7A92FF', '#FF9F80']; // Paleta de colores más bonitos

    let index = 0;
    for (const machine in predictions) {
      if (predictions.hasOwnProperty(machine)) {
        const machinePredictions = predictions[machine];

        if (machinePredictions.length === 0) {
          console.log(`No prediction data found for ${machine}.`);
          continue;
        }

        const dates = machinePredictions.map(prediction => prediction.Date);
        const typeData = machinePredictions.map(prediction => prediction[type]);

        console.log(`Dates for ${machine}:`, dates);
        console.log(`${type} Data for ${machine}:`, typeData);

        const allEqual = typeData.every(val => val === typeData[0]);

        datasets.push({
          label: historical ? `${machine} ${type}` : `${machine} (${type} Best Result: ${Math.min(...typeData)})`,
          data: typeData,
          borderColor: palette[index % palette.length], // Asignar un color único para cada máquina
          backgroundColor: palette[index % palette.length],
          pointBackgroundColor: palette[index % palette.length],
          pointRadius: historical ? 3 : 6,
        });

        index++;
      }
    }

    const chartData = {
      labels: Object.values(predictions)[0].map(prediction => prediction.Date),
      datasets: datasets,
    };

    const chartOptions = {
      scales: {
        y: {
          beginAtZero: false,
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
              return `${label}: ${context.parsed.y}`;
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
  }, [predictions, type, historical]);

  return (
    <div className='graph' style={{ display: 'flex', justifyContent: 'space-between', width: '70%', margin: 'auto' }}>
      <canvas ref={chartRef} width={400} height={200}></canvas>
    </div>
  );
};

export default Graph;

import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import './Graph.css';

const Graph = ({ predictions, type, historical, calibraciones, colors }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!predictions || Object.keys(predictions).length === 0) {
      console.log("No predictions provided.");
      return;
    }

    const datasets = [];
    const palette = ['#FF6B6B', '#78c2ad', '#FFE66D', '#7A92FF', '#B5EAEA', '#FFB6C1'];


    let index = 0;

    const processPredictions = (model, machine, machinePredictions) => {
      if (machinePredictions.length === 0) {
        console.log(`No prediction data found for ${machine}.`);
        return;
      }

      const dates = machinePredictions.map(prediction => prediction.Date);
      const typeData = machinePredictions.map(prediction => prediction[type]);

      const bestResultIndex = typeData.indexOf(Math.min(...typeData));

      datasets.push({
        label: historical ? `${model ? model + ' ' : ''}${machine} ${type}` : `${model ? model + ' ' : ''}${machine} (${type} Best Result: ${Math.min(...typeData)})`,
        data: typeData,
        borderColor: calibraciones ? palette[colors] : palette[index % palette.length],
        backgroundColor: calibraciones ? palette[colors] : palette[index % palette.length],
        pointBackgroundColor: calibraciones ? palette[colors] : palette[index % palette.length],
        pointRadius: !historical ? typeData.map((_, i) => (i === bestResultIndex ? 6 : 2)) : 3,
      });

      index++;
    };

    if (Array.isArray(predictions)) {
      processPredictions(null, "Data", predictions);
    } else {
      for (const model in predictions) {
        if (predictions.hasOwnProperty(model)) {
          for (const machine in predictions[model]) {
            if (predictions[model].hasOwnProperty(machine)) {
              processPredictions(model, machine, predictions[model][machine]);
            }
          }
        }
      }
    }

    const chartData = {
      labels: Array.isArray(predictions) ? predictions.map(prediction => prediction.Date) : Object.values(predictions)[0][Object.keys(predictions[Object.keys(predictions)[0]])[0]].map(prediction => prediction.Date),
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
    <div className='graph' style={{ display: 'flex', justifyContent: 'space-between', width: '100%', maxWidth: '1200px', margin: 'auto' }}>
      <div style={{ overflowX: 'auto', width: '100%' }}>
        <canvas ref={chartRef} width={2000} height={400}></canvas>
      </div>
    </div>
  );
};

export default Graph;
import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import './Graph.css';

const Graph = ({ predictions, type, historical }) => {
  const chartRef = useRef(null);
  const [startIdx, setStartIdx] = useState(0);
  const [endIdx, setEndIdx] = useState(200); // Mostrar los primeros 200 datos inicialmente

  useEffect(() => {
    if (!predictions || predictions.length === 0) {
      console.log("No predictions provided.");
      return;
    }

    const datasets = [];
    const palette = ['#FF6B6B', '#78c2ad', '#FFE66D', '#7A92FF', '#FF9F80'];
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
        borderColor: palette[index % palette.length],
        backgroundColor: palette[index % palette.length],
        pointBackgroundColor: palette[index % palette.length],
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
      labels: predictions.map(prediction => prediction.Date).slice(startIdx, endIdx),
      datasets: datasets,
    };

    const chartOptions = {
      scales: {
        y: {
          beginAtZero: false,
        },
        x: {
          ticks: {
            maxTicksLimit: 10,
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
  }, [predictions, type, historical, startIdx, endIdx]);

  const handleScroll = (e) => {
    const container = e.target;
    const scrollLeft = container.scrollLeft;
    const scrollWidth = container.scrollWidth;
    const clientWidth = container.clientWidth;

    // Verificar si estamos cerca del final y hay más datos para mostrar
    if (scrollLeft + clientWidth >= scrollWidth && endIdx < predictions.length) {
      const newStartIdx = Math.max(startIdx - 50, 0);
      setStartIdx(newStartIdx);
      setEndIdx(Math.min(newStartIdx + 200, predictions.length));
    }
  };

  return (
    <div className='graph-container' style={{ overflowX: 'auto' }} onScroll={handleScroll}>
      <canvas ref={chartRef}></canvas>
    </div>
  );
};

export default Graph;

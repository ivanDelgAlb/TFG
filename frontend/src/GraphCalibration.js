import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

const Graph = ({ predictions }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (predictions.length === 0) return;

    const chartData = {
      labels: predictions.map((_, index) => `Prediction ${index}`),
      datasets: [
        {
          label: 'T1',
          data: predictions.map(prediction => prediction.T1),
          borderColor: 'rgba(255, 99, 132, 1)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
        },
        {
          label: 'T2',
          data: predictions.map(prediction => prediction.T2),
          borderColor: 'rgba(54, 162, 235, 1)',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
        },
        {
          label: 'Prob0',
          data: predictions.map(prediction => prediction.Prob0),
          borderColor: 'rgba(255, 206, 86, 1)',
          backgroundColor: 'rgba(255, 206, 86, 0.2)',
        },
        {
          label: 'Prob1',
          data: predictions.map(prediction => prediction.Prob1),
          borderColor: 'rgba(75, 192, 192, 1)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
        },
        {
          label: 'Error',
          data: predictions.map(prediction => prediction.Error),
          borderColor: 'rgba(153, 102, 255, 1)',
          backgroundColor: 'rgba(153, 102, 255, 0.2)',
        },
      ],
    };

    const chartOptions = {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    };

    const resizeChart = () => {
      const canvas = chartRef.current;
      canvas.style.width = '70vw';
      canvas.style.height = '70vh';
    };

    const myChart = new Chart(chartRef.current, {
      type: 'line',
      data: chartData,
      options: chartOptions,
    });

    resizeChart();

    window.addEventListener('resize', resizeChart);

    return () => {
      myChart.destroy();
      window.removeEventListener('resize', resizeChart);
    };
  }, [predictions]);

  return <canvas ref={chartRef}></canvas>;
};

export default Graph;

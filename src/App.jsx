// src/App.jsx

import React from 'react';
import FlowChartComponent from './components/FlowChartComponent';
import data from './data/data';

export default function App() {
  return (
    <div>
      <FlowChartComponent data={data} />
    </div>
  );
}

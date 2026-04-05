import React from 'react';
import AddTrailJunction from './components/AddTrailJunction';
import Map from './components/Map';
import GraphMap from './components/GraphMap';
import './App.css'

function App() {
  return (
    <div>
      <h1>Trail Network</h1>
      {/* <AddTrailJunction /> */}
      {/* <Map /> */}
      <GraphMap />
    </div>
  );
}

export default App;

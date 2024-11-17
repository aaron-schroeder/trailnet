// src/components/Map.js
// Originally created to talk to the postgis db

import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { getTrailSegments } from '../services/api';

const Map = () => {
    const [segments, setSegments] = useState([]);

    useEffect(() => {
        const fetchSegments = async () => {
            // const data = await getTrailSegments();
            // HACK to mock this function (comment out the code above):
            const data = [
                {
                    "id": 1,
                    "name": "Sample Trail Segment",
                    "coordinates": [[32.233, -110.852], [32.234, -110.85], [32.236, -110.848]]
                    // "geometry": "SRID=4326;LINESTRING (-110.852 32.233, -110.85 32.234, -110.848 32.236)"
                }
            ];
            setSegments(data);
        };
        fetchSegments();
    }, []);

    return (
        <div id='container'>
        <MapContainer center={[32.233, -110.852]} zoom={16} >
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {segments.map(segment => (
                <Polyline
                    key={segment.id}
                    // positions={segment.geometry.coordinates.map(coord => [coord[1], coord[0]])} // Leaflet expects [lat, lng]
                    positions={segment.coordinates}
                    color="blue"
                />
            ))}
        </MapContainer>
        </div>
    );
};

export default Map;

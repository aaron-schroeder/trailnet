// src/components/Map.js
// Originally created to talk to the postgis db

import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polyline } from 'react-leaflet';
import { getTrailSegments } from '../services/api';

const Map = () => {
    const [segments, setSegments] = useState([]);

    useEffect(() => {
        const fetchSegments = async () => {
            const data = await getTrailSegments();
            // HACK to mock this function (comment out the code above):
            // const data = [
            //     {
            //         "id": 1,
            //         "name": "Sample Trail Segment",
            //         "geometry": "SRID=4326;LINESTRING (-110.852 32.233, -110.85 32.234, -110.848 32.236)"
            //     }
            // ];
            setSegments(data);
        };
        fetchSegments();
    }, []);

    return (
        <MapContainer center={[0, 0]} zoom={2} style={{ height: '100vh', width: '100%' }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {segments.map(segment => (
                <Polyline
                    key={segment.id}
                    positions={segment.geometry.coordinates.map(coord => [coord[1], coord[0]])} // Leaflet expects [lat, lng]
                    color="blue"
                />
            ))}
        </MapContainer>
    );
};

export default Map;

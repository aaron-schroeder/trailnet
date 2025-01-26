// src/components/Map.js
// Originally created to talk to the postgis db

import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { getTrailSegments, getRoutes } from '../services/api';

const Map = () => {
    const [segments, setSegments] = useState(null);

    useEffect(() => {
        const fetchSegments = async () => {
            const data = await getTrailSegments();
            // HACK to mock this function (comment out the code above):
            // const data = {
            //     "type": "FeatureCollection",
            //     "features": [
            //         {
            //             "id": 1,
            //             "type": "Feature",
            //             "geometry": {
            //                 "type": "LineString",
            //                 "coordinates": [
            //                     [
            //                         -110.852,
            //                         32.233
            //                     ],
            //                     [
            //                         -110.85,
            //                         32.234
            //                     ],
            //                     [
            //                         -110.848,
            //                         32.236
            //                     ]
            //                 ]
            //             },
            //             "properties": {
            //                 "name": "Sample Trail Segment"
            //             }
            //         }
            //     ]
            // }
            setSegments(data);
        };
        fetchSegments();
    }, []);

    const [routes, setRoutes] = useState(null);
    useEffect(() => {
        const fetchRoutes = async () => {
            const data = await getRoutes();
            setRoutes(data);
        };
        fetchRoutes();
    }, []);

    return (
        <div id='container'>
        <MapContainer center={[32.233, -110.852]} zoom={16} >
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {segments !== null && 
                segments.features.map(segment => (
                    <Polyline
                        key={`segment-${segment.id}`}
                        positions={segment.geometry.coordinates.map(coord => [coord[1], coord[0]])}
                        color="blue"
                    />
                ))
            }
            {routes !== null &&
                routes.features.map(route => (
                    <Polyline
                        key={`route-${route.id}`}
                        positions={route.geometry.coordinates.map(line =>
                            line.map(coord => [coord[1], coord[0]])
                        )}
                        color="red"
                    />
                ))
            }
        </MapContainer>
        </div>
    );
};

export default Map;

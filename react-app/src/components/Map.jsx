// src/components/Map.js
// Originally created to talk to the postgis db

import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polyline, Tooltip, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { getLines } from '../services/api';

const FitBounds = ({ bounds }) => {
    const map = useMap();
    if (bounds) map.fitBounds(bounds, { padding: [50, 50] });
    return null;
};

const getBoundsFromFeatures = (features) => {
    const allCoords = features.flatMap(feature =>
        feature.geometry.coordinates.map(coord => [coord[1], coord[0]])
    );
    return L.latLngBounds(allCoords);
};

const Map = () => {
    const [segments, setSegments] = useState(null);
    const [bounds, setBounds] = useState(null);

    useEffect(() => {
        const fetchSegments = async () => {
            const data = await getLines();
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

            const bounds = getBoundsFromFeatures(data.features);
            setBounds(bounds);
        };
        fetchSegments();
    }, []);


    if (!segments) return <div>Loading map...</div>;

    return (
        <div id='container'>
        <MapContainer 
            center={[32.233, -110.852]}
            zoom={16}
            //style={{ height: '100vh', width: '100%' }}
        >
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />

            <FitBounds bounds={bounds} />

            {segments !== null && 
                segments.features.map(segment => (
                    <Polyline
                        key={`segment-${segment.id}`}
                        positions={segment.geometry.coordinates.map(coord => [coord[1], coord[0]])}
                        color="blue"
                    >
                        <Tooltip direction="top" permanent={false} sticky>
                            Segment: {segment.properties.name}
                        </Tooltip>
                    </Polyline>

                ))
            }
        </MapContainer>
        </div>
    );
};

export default Map;

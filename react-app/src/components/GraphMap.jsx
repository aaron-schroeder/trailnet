import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polyline, CircleMarker, Tooltip } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const API_URL = import.meta.env.VITE_REACT_APP_BACKEND_URL || 'http://localhost:8000/postgis/';

function junctionColor(junctionId) {
    if (!junctionId) return '#999999';
    let hash = 0;
    for (let i = 0; i < junctionId.length; i++) {
        hash = junctionId.charCodeAt(i) + ((hash << 5) - hash);
    }
    const hue = Math.abs(hash) % 360;
    return `hsl(${hue}, 80%, 45%)`;
}

const GraphMap = () => {
    const [segments, setSegments] = useState([]);
    const [lines, setLines] = useState([]);
    const [activeSegments, setActiveSegments] = useState({});

    useEffect(() => {
        fetch(`${API_URL}graph/`)
            .then(r => r.json())
            .then(data => setSegments(data.segments));

        fetch(`${API_URL}lines/`)
            .then(r => r.json())
            .then(data => setLines(data.features));
    }, []);

    // build a lookup from line_id -> coordinates for polyline rendering
    const lineCoords = {};
    lines.forEach(feature => {
        lineCoords[feature.id] = feature.geometry.coordinates.map(
            ([lon, lat]) => [lat, lon]
        );
    });

    const toggleSegment = (unique_id) => {
        setActiveSegments(prev => ({
            ...prev,
            [unique_id]: !prev[unique_id]
        }));
    };

    return (
        <MapContainer center={[33.34, -112.07]} zoom={13}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; OpenStreetMap contributors'
            />

            {segments.map(seg => {
                const coords = lineCoords[seg.line_id];
                if (!coords) return null;

                const isActive = activeSegments[seg.unique_id] ?? true;

                const lineColor = isActive ? '#3388ff' : '#cccccc'; // blue when active, grey when inactive
                const startColor = isActive
                    ? junctionColor(seg.start_junction)
                    : '#aaaaaa';
                const endColor = isActive
                    ? junctionColor(seg.end_junction)
                    : '#aaaaaa';


                return (
                    <React.Fragment key={seg.unique_id}>
                        <Polyline
                            positions={coords}
                            pathOptions={{ color: lineColor, weight: 2 }}
                            eventHandlers={{
                                click: () => toggleSegment(seg.unique_id)
                            }}
                        >
                            <Tooltip sticky>{seg.unique_id} ({seg.name})</Tooltip>
                        </Polyline>

                        <CircleMarker
                            center={[seg.start_coord.lat, seg.start_coord.lon]}
                            radius={6}
                            pathOptions={{
                                color: startColor,
                                fillColor: startColor,
                                fillOpacity: 1,
                            }}
                            eventHandlers={{
                                click: () => toggleSegment(seg.unique_id)
                            }}
                        >
                            <Tooltip>{seg.start_junction} ({seg.unique_id})</Tooltip>
                        </CircleMarker>

                        <CircleMarker
                            center={[seg.end_coord.lat, seg.end_coord.lon]}
                            radius={6}
                            pathOptions={{
                                color: endColor,
                                fillColor: endColor,
                                fillOpacity: 1,
                            }}
                            eventHandlers={{
                                click: () => toggleSegment(seg.unique_id)
                            }}
                        >
                            <Tooltip>{seg.end_junction} ({seg.unique_id})</Tooltip>
                        </CircleMarker>
                    </React.Fragment>
                );
            })}
        </MapContainer>
    );
};

export default GraphMap;
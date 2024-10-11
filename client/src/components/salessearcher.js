import React, { useState } from 'react';

// Define the Download icon as a component
const Download = ({ size = 24, color = "#000000" }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5" />
    </svg>
);

function SalesSearcher() {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = () => {
        setResults([{ id: 1, name: 'Result 1' }, { id: 2, name: 'Result 2' }]); // Dummy data
    };

    const downloadCSV = () => {
        console.log('Download CSV');
    };

    return (
        <div className="sales-searcher">
            <div className="table-controls">
                <input
                    type="text"
                    placeholder="Search..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="search-input"
                />
                <button className="download-btn" onClick={downloadCSV}>
                    <Download size={24} color="#FFFFFF" /> {/* Use your custom SVG here */}
                </button>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                    </tr>
                </thead>
                <tbody>
                    {results.map((result) => (
                        <tr key={result.id}>
                            <td>{result.id}</td>
                            <td>{result.name}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default SalesSearcher;
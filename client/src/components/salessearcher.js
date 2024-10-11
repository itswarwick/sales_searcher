import React, { useState } from 'react';

// Define the Download icon as a component
const Download = ({ size = 24, color = "#000000" }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5" />
    </svg>
);

// Define the CheckCircle icon as a component
const CheckCircle = ({ size = 24, color = "#000000" }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
    </svg>
);

function SalesSearcher() {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);
    const [isDownloaded, setIsDownloaded] = useState(false);

    const handleSearch = () => {
        setResults([{ id: 1, name: 'Result 1' }, { id: 2, name: 'Result 2' }]); // Dummy data
    };

    const downloadCSV = () => {
        console.log('Download CSV');
        setIsDownloaded(true);

        // Transition back to the download icon after 0.5 seconds
        setTimeout(() => {
            setIsDownloaded(false);
        }, 500);
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
                    {isDownloaded ? <CheckCircle size={24} color="#FFFFFF" /> : <Download size={24} color="#FFFFFF" />}
                </button>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Customer Name</th>
                        <th>Customer Email</th>
                        <th># of Purchases</th>
                        <th>Total $ Spent</th>
                        <th>Date of Last Purchase</th>
                    </tr>
                </thead>
                <tbody>
                    {results.map((result) => (
                        <tr key={result.id}>
                            <td>{result.customerName}</td>
                            <td>{result.customerEmail}</td>
                            <td>{result.numPurchases}</td>
                            <td>{result.totalSpent}</td>
                            <td>{result.lastPurchaseDate}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default SalesSearcher;
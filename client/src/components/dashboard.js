import React, { useState } from 'react';
import SalesSearcher from './salessearcher';

function Dashboard() {
    const [activeTab, setActiveTab] = useState('salessearcher');

    const renderContent = () => {
        switch (activeTab) {
            case 'salessearcher':
                return <SalesSearcher />;
            case 'oosspotter':
                return <div>OOS Spotter is coming soon.</div>;
            case 'ordersync':
                return <div>Order Sync is coming soon.</div>;
            default:
                return null;
        }
    };

    return (
        <div className="dashboard-container">
            <h1>Dashboard</h1>
            <div className="nav-buttons">
                <button
                    className={activeTab === 'salessearcher' ? 'active' : ''}
                    onClick={() => setActiveTab('salessearcher')}
                >
                    Sales Searcher
                </button>
                <button
                    className={activeTab === 'oosspotter' ? 'active' : ''}
                    onClick={() => setActiveTab('oosspotter')}
                >
                    OOS Spotter
                </button>
                <button
                    className={activeTab === 'ordersync' ? 'active' : ''}
                    onClick={() => setActiveTab('ordersync')}
                >
                    Order Sync
                </button>
            </div>
            <div className="dashboard-content">
                {renderContent()}
            </div>
        </div>
    );
}

export default Dashboard;
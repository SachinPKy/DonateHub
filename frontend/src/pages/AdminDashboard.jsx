import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/api';
import './auth.css';

const AdminDashboard = () => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await api.get('/admin/stats/');
                setStats(response.data);
            } catch (err) {
                setError('Failed to fetch dashboard data. Make sure you have admin privileges.');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchStats();
    }, []);

    if (loading) return (
        <div className="admin-wrapper d-flex align-items-center justify-content-center min-vh-100 bg-dark">
            <div className="spinner-border text-primary" style={{ width: '3rem', height: '3rem' }}></div>
        </div>
    );

    const statCards = [
        { label: 'Total Donations', value: stats?.total, icon: 'bi-box-seam-fill', color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.1)' },
        { label: 'Pending Reviews', value: stats?.pending, icon: 'bi-hourglass-split', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)' },
        { label: 'Approved Today', value: stats?.approved, icon: 'bi-check-all', color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)' },
        { label: 'Completed', value: stats?.completed, icon: 'bi-trophy-fill', color: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.1)' }
    ];

    return (
        <div className="admin-wrapper py-5 min-vh-100">
            <div className="container">
                <header className="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-5 gap-3">
                    <div>
                        <h1 className="display-5 fw-bold text-white mb-2">Systems Overview</h1>
                        <p className="text-secondary mb-0 fw-medium">
                            <i className="bi bi-shield-check me-2 text-primary"></i>
                            DonateHub Administrative Control Panel
                        </p>
                    </div>
                    <div className="d-flex gap-3">
                        <a href="http://localhost:8000/admin/" target="_blank" rel="noopener noreferrer" className="btn btn-premium-secondary d-flex align-items-center gap-2">
                            <i className="bi bi-gear-fill"></i> Django Backend
                        </a>
                    </div>
                </header>

                {error && (
                    <div className="alert alert-danger border-0 shadow-lg mb-5 rounded-4 p-3 d-flex align-items-center gap-3">
                        <i className="bi bi-exclamation-octagon-fill fs-4"></i>
                        <div>{error}</div>
                    </div>
                )}

                {/* Stat Grid */}
                <div className="row g-4 mb-5">
                    {statCards.map((stat, idx) => (
                        <div key={idx} className="col-md-3">
                            <div className="glass-card h-100 p-4">
                                <div className="d-flex justify-content-between align-items-start mb-3">
                                    <div className="stat-icon" style={{ backgroundColor: stat.bg, color: stat.color }}>
                                        <i className={`bi ${stat.icon} fs-4`}></i>
                                    </div>
                                    <span className="badge-pulse">Live</span>
                                </div>
                                <h6 className="text-uppercase text-secondary ls-1 small fw-bold mb-1">{stat.label}</h6>
                                <h2 className="display-6 fw-bold text-white mb-0">{stat.value || 0}</h2>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Content Area */}
                <div className="row g-4">
                    <div className="col-lg-12">
                        <div className="glass-card p-0 overflow-hidden">
                            <div className="p-4 border-bottom border-light border-opacity-10 d-flex justify-content-between align-items-center bg-white bg-opacity-5">
                                <h5 className="mb-0 fw-bold text-white">Recent Activity Log</h5>
                                <button className="btn btn-sm btn-link text-primary text-decoration-none fw-bold">View Archive</button>
                            </div>
                            <div className="table-responsive">
                                <table className="table table-custom mb-0">
                                    <thead>
                                        <tr>
                                            <th>ID & Receipt</th>
                                            <th>Contributor</th>
                                            <th>Classification</th>
                                            <th>Status State</th>
                                            <th>Timestamp</th>
                                            <th className="text-end">Management</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {stats?.recent?.map((dn) => (
                                            <tr key={dn.id}>
                                                <td>
                                                    <div className="fw-bold text-white">#{dn.id}</div>
                                                    <div className="small text-secondary">{dn.receipt_number}</div>
                                                </td>
                                                <td>
                                                    <div className="d-flex align-items-center gap-2">
                                                        <div className="avatar-sm">{dn.donor_username?.charAt(0) || 'A'}</div>
                                                        <span className="text-white-50">{dn.donor_username || 'Anonymous'}</span>
                                                    </div>
                                                </td>
                                                <td><span className="text-primary fw-medium">{dn.category}</span></td>
                                                <td>
                                                    <span className={`status-dot ${dn.status === 'DELIVERED' ? 'bg-success' : 'bg-warning'}`}></span>
                                                    <span className="ms-2 small text-uppercase fw-bold text-secondary">{dn.status_display}</span>
                                                </td>
                                                <td className="text-secondary small">
                                                    {new Date(dn.created_at).toLocaleDateString()}
                                                </td>
                                                <td className="text-end">
                                                    <Link to={`/tracking/${dn.id}`} className="btn btn-action-sm">
                                                        <i className="bi bi-eye"></i>
                                                    </Link>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <style>{`
                .admin-wrapper {
                    background: radial-gradient(circle at top right, #1e293b, #0f172a);
                    color: white;
                }
                .glass-card {
                    background: rgba(255, 255, 255, 0.03);
                    backdrop-filter: blur(20px);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 24px;
                    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                }
                .glass-card:hover {
                    transform: translateY(-8px);
                    background: rgba(255, 255, 255, 0.05);
                    border-color: rgba(255, 255, 255, 0.15);
                }
                .stat-icon {
                    width: 52px;
                    height: 52px;
                    border-radius: 16px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .ls-1 { letter-spacing: 1px; }
                .badge-pulse {
                    font-size: 10px;
                    text-transform: uppercase;
                    background: rgba(16, 185, 129, 0.1);
                    color: #10b981;
                    padding: 4px 10px;
                    border-radius: 20px;
                    font-weight: 800;
                    display: flex;
                    align-items: center;
                    gap: 5px;
                }
                .badge-pulse::before {
                    content: '';
                    width: 6px;
                    height: 6px;
                    background: #10b981;
                    border-radius: 50%;
                    animation: pulse 1.5s infinite;
                }
                @keyframes pulse {
                    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
                    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
                    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
                }
                .table-custom { border-collapse: separate; border-spacing: 0 8px; }
                .table-custom thead th { 
                    border: none; 
                    color: #64748b; 
                    font-size: 11px; 
                    text-transform: uppercase; 
                    letter-spacing: 1.5px;
                    padding: 15px 25px;
                }
                .table-custom tbody tr { 
                    background: rgba(255, 255, 255, 0.02);
                    transition: all 0.2s ease;
                }
                .table-custom tbody tr:hover { 
                    background: rgba(255, 255, 255, 0.05);
                    transform: scale(1.005);
                }
                .table-custom td { padding: 20px 25px; vertical-align: middle; border-top: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05); }
                .avatar-sm { width: 32px; height: 32px; background: #3b82f6; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px; }
                .status-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; }
                .btn-premium-secondary {
                    background: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    color: white;
                    padding: 10px 20px;
                    border-radius: 12px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                }
                .btn-premium-secondary:hover {
                    background: white;
                    color: #0f172a;
                }
                .btn-action-sm {
                    width: 36px;
                    height: 36px;
                    border-radius: 10px;
                    background: rgba(59, 130, 246, 0.1);
                    color: #3b82f6;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    border: none;
                    transition: all 0.2s ease;
                }
                .btn-action-sm:hover {
                    background: #3b82f6;
                    color: white;
                }
            `}</style>
        </div>
    );
};

export default AdminDashboard;

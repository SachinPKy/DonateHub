import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/api';

const MyDonations = () => {
    const [donations, setDonations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [downloading, setDownloading] = useState(false);
    const [error, setError] = useState(null);
    const [selectedImage, setSelectedImage] = useState(null);

    useEffect(() => {
        const fetchDonations = async () => {
            try {
                const response = await api.get('/donations/');
                setDonations(response.data);
            } catch (err) {
                console.error('Error fetching donations:', err);
                setError('Failed to load donations. Please try again later.');
            } finally {
                setLoading(false);
            }
        };
        fetchDonations();
    }, []);

    const handleDownloadReceipt = async (donationId, receiptNumber) => {
        setDownloading(true);
        try {
            const response = await api.get(`/receipt/${donationId}/pdf/`, {
                responseType: 'blob',
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `receipt_${receiptNumber}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        } catch (err) {
            console.error('Error downloading receipt:', err);
            alert('Failed to download receipt. Please try again later.');
        } finally {
            setDownloading(false);
        }
    };

    const getStatusBadge = (status) => {
        switch (status) {
            case "SUBMITTED":
                return <span className="badge bg-warning status-badge">Submitted</span>;
            case "CONFIRMED":
                return <span className="badge bg-info status-badge">Confirmed</span>;
            case "PICKUP_SCHEDULED":
                return <span className="badge bg-primary status-badge">Pickup Scheduled</span>;
            case "PICKED_UP":
                return <span className="badge bg-secondary status-badge">Picked Up</span>;
            case "IN_TRANSIT":
                return <span className="badge bg-dark status-badge">In Transit</span>;
            case "DELIVERED":
            case "COMPLETED":
                return <span className="badge bg-success status-badge">Completed</span>;
            case "CANCELLED":
                return <span className="badge bg-danger status-badge">Cancelled</span>;
            default:
                return <span className="badge bg-secondary status-badge">{status}</span>;
        }
    };

    return (
        <>
            <style>
                {`
          .dashboard-wrapper {
            background: #f4f6f9;
            min-height: calc(100vh - 130px);
            padding-top: 50px;
            padding-bottom: 50px;
            color: black;
          }
          .dashboard-title {
            font-weight: bold;
          }
          .status-badge {
            font-size: 0.85rem;
            padding: 6px 12px;
          }
          .tracking-btn {
            font-size: 0.75rem;
            padding: 4px 8px;
          }
          .donation-thumb {
            width: 50px;
            height: 50px;
            object-fit: cover;
            border-radius: 6px;
            border: 1px solid #dee2e6;
            cursor: pointer;
          }
          .image-cell {
            text-align: center;
            min-width: 60px;
          }
          .gallery-image {
            max-height: 500px;
            object-fit: contain;
            width: 100%;
          }
          @media (max-width: 576px) {
            table { font-size: 0.85rem; }
            th, td { white-space: nowrap; }
          }

          /* Modal custom styling to mimic bootstrap if using native dialogs */
          .modal-backdrop {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 1040;
            display: flex;
            align-items: center;
            justify-content: center;
          }
          .modal-custom {
            background: white;
            border-radius: 8px;
            width: 90%;
            max-width: 600px;
            z-index: 1050;
            overflow: hidden;
            color: black;
          }
          .modal-header-custom {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            border-bottom: 1px solid #dee2e6;
          }
          .modal-body-custom {
            padding: 1rem;
            text-align: center;
          }
        `}
            </style>

            <div className="dashboard-wrapper">
                <div className="container">
                    <h2 className="dashboard-title text-primary mb-4">My Donations</h2>

                    {loading ? (
                        <div className="text-center py-5">
                            <div className="spinner-border text-primary" role="status">
                                <span className="visually-hidden">Loading...</span>
                            </div>
                        </div>
                    ) : error ? (
                        <div className="alert alert-danger text-center">{error}</div>
                    ) : donations && donations.length > 0 ? (
                        <div className="table-responsive">
                            <table className="table table-bordered table-hover bg-white shadow">
                                <thead className="table-dark text-center">
                                    <tr>
                                        <th>#</th>
                                        <th>Images</th>
                                        <th>Category</th>
                                        <th>Location</th>
                                        <th>Pickup Date</th>
                                        <th>Status</th>
                                        <th>Tracking</th>
                                        <th>Receipt</th>
                                        <th>Submitted</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {donations.map((donation, index) => (
                                        <tr key={donation.id}>
                                            <td className="text-center">{index + 1}</td>

                                            <td className="image-cell">
                                                {donation.main_image ? (
                                                    <img
                                                        src={`http://localhost:8000${donation.main_image}`}
                                                        alt="thumb"
                                                        className="donation-thumb"
                                                        onClick={() => setSelectedImage({ url: `http://localhost:8000${donation.main_image}`, title: donation.category })}
                                                    />
                                                ) : (
                                                    <span className="text-muted">-</span>
                                                )}
                                            </td>

                                            <td>
                                                <strong>{donation.category}</strong>
                                                <br />
                                                <small className="text-muted">
                                                    {donation.description.length > 50 ? `${donation.description.substring(0, 50)}...` : donation.description}
                                                </small>
                                            </td>

                                            <td>
                                                {donation.area && `${donation.area}, `}
                                                {donation.district && donation.district}
                                                <br />
                                                <small className="text-muted">{donation.state}</small>
                                            </td>

                                            <td>{donation.pickup_date}</td>

                                            <td className="text-center">
                                                {getStatusBadge(donation.status)}
                                            </td>

                                            <td className="text-center">
                                                <Link to={`/tracking/${donation.id}`} className="btn btn-sm btn-outline-primary tracking-btn">
                                                    Track
                                                </Link>
                                            </td>

                                            <td className="text-center">
                                                <button
                                                    className="btn btn-sm btn-outline-success"
                                                    onClick={() => handleDownloadReceipt(donation.id, donation.receipt_number)}
                                                    disabled={downloading}
                                                >
                                                    {downloading ? (
                                                        <span className="spinner-border spinner-border-sm me-1"></span>
                                                    ) : (
                                                        <i className="bi bi-download me-1"></i>
                                                    )}
                                                    Download
                                                </button>
                                            </td>

                                            <td>{donation.created_at}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    ) : (
                        <div className="alert alert-info text-center">
                            You have not made any donations yet.
                            <Link to="/add" className="alert-link ms-1">Add a donation</Link>
                        </div>
                    )}
                </div>
            </div>

            {/* Image Modal Component embedded */}
            {selectedImage && (
                <div className="modal-backdrop" onClick={() => setSelectedImage(null)}>
                    <div className="modal-custom" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header-custom">
                            <h5 className="mb-0">{selectedImage.title}</h5>
                            <button type="button" className="btn-close" onClick={() => setSelectedImage(null)}></button>
                        </div>
                        <div className="modal-body-custom">
                            <img src={selectedImage.url} className="gallery-image" alt="Donation" />
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

export default MyDonations;

import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api/api';
import './tracking.css';

const DonationTracking = () => {
  const { id } = useParams();
  const [donation, setDonation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    const fetchDonation = async () => {
      try {
        const response = await api.get(`/donations/${id}/`);
        setDonation(response.data);
      } catch (err) {
        console.error('Error fetching donation tracking:', err);
        setError('Donation not found or access denied.');
      } finally {
        setLoading(false);
      }
    };
    fetchDonation();
  }, [id]);

  const handleDownloadReceipt = async () => {
    setDownloading(true);
    try {
      const response = await api.get(`/receipt/${id}/pdf/`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `receipt_${donation.receipt_number}.pdf`);
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

  if (loading) {
    return (
      <div className="tracking-wrapper d-flex align-items-center justify-content-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="tracking-wrapper container py-5">
        <div className="alert alert-danger text-center shadow-lg border-0">{error}</div>
        <div className="text-center mt-3">
          <Link to="/my-donations" className="btn btn-primary px-4">Back to My Donations</Link>
        </div>
      </div>
    );
  }

  const getStatusStepStatus = (stepName) => {
    const statusOrder = ['SUBMITTED', 'CONFIRMED', 'PICKUP_SCHEDULED', 'PICKED_UP', 'IN_TRANSIT', 'DELIVERED', 'COMPLETED'];
    const currentIdx = statusOrder.indexOf(donation.status);
    const stepIdx = statusOrder.indexOf(stepName);

    if (stepIdx < currentIdx) return 'completed';
    if (stepIdx === currentIdx) return 'current';
    return '';
  };

  const statusSteps = [
    { key: 'SUBMITTED', label: 'Submitted', icon: 'bi-send-fill' },
    { key: 'CONFIRMED', label: 'Confirmed', icon: 'bi-patch-check-fill' },
    { key: 'PICKUP_SCHEDULED', label: 'Scheduled', icon: 'bi-calendar-event-fill' },
    { key: 'PICKED_UP', label: 'Picked Up', icon: 'bi-truck' },
    { key: 'DELIVERED', label: 'Delivered', icon: 'bi-house-heart-fill' }
  ];

  return (
    <div className="tracking-wrapper">
      <div className="container py-5">
        <div className="d-flex justify-content-between align-items-center mb-5">
          <Link to="/my-donations" className="text-white text-decoration-none opacity-75 hover-opacity-100 transition">
            <i className="bi bi-arrow-left me-2"></i> My Donations
          </Link>
          <button
            onClick={handleDownloadReceipt}
            className="btn btn-primary d-flex align-items-center gap-2 px-4 rounded-pill shadow-lg"
            disabled={downloading}
          >
            {downloading ? (
              <span className="spinner-border spinner-border-sm"></span>
            ) : (
              <i className="bi bi-file-earmark-pdf-fill fs-5"></i>
            )}
            Download Receipt
          </button>
        </div>

        <div className="row g-4">
          <div className="col-lg-8">
            <div className="donation-card p-4 p-md-5 mb-4">
              <div className="d-flex justify-content-between align-items-start mb-4">
                <div>
                  <h3 className="fw-bold mb-1">Tracking Receipt</h3>
                  <p className="text-primary fw-bold mb-0">{donation.receipt_number}</p>
                </div>
                <span className={`status-badge ${donation.status === 'DELIVERED' ? 'bg-success' : 'bg-primary'
                  } bg-opacity-25 text-${donation.status === 'DELIVERED' ? 'success' : 'primary'
                  }`}>
                  {donation.status_display}
                </span>
              </div>

              <div className="row g-4 border-top border-light border-opacity-10 pt-4">
                <div className="col-sm-6">
                  <div className="info-item">
                    <label className="small text-muted text-uppercase ls-1">Category</label>
                    <p className="fw-bold mb-0">{donation.category}</p>
                  </div>
                </div>
                <div className="col-sm-6">
                  <div className="info-item">
                    <label className="small text-muted text-uppercase ls-1">Pickup Date</label>
                    <p className="fw-bold mb-0">{donation.pickup_date}</p>
                  </div>
                </div>
                <div className="col-sm-6">
                  <div className="info-item">
                    <label className="small text-muted text-uppercase ls-1">Location</label>
                    <p className="fw-bold mb-0">{donation.area}, {donation.district}</p>
                  </div>
                </div>
                <div className="col-sm-6">
                  <div className="info-item">
                    <label className="small text-muted text-uppercase ls-1">Submission Date</label>
                    <p className="fw-bold mb-0">{new Date(donation.created_at).toLocaleDateString(undefined, { dateStyle: 'long' })}</p>
                  </div>
                </div>
              </div>

              <div className="mt-5">
                <label className="small text-muted text-uppercase ls-1 mb-2">Description</label>
                <div className="bg-white bg-opacity-5 p-3 rounded-lg border border-light border-opacity-10">
                  <p className="mb-0 text-white-50">{donation.description}</p>
                </div>
              </div>
            </div>

            <div className="donation-card p-4 p-md-5">
              <h5 className="fw-bold mb-4 d-flex align-items-center gap-2">
                <i className="bi bi-activity text-primary"></i>
                Journey Timeline
              </h5>
              <div className="tracking-list">
                {statusSteps.map((step, index) => (
                  <div key={index} className={`tracking-item ${getStatusStepStatus(step.key)}`}>
                    <div className="tracking-icon">
                      <i className={`bi ${step.icon} fs-5`}></i>
                    </div>
                    <div className="tracking-content">
                      <h6 className="mb-1">{step.label}</h6>
                      <p className="mb-0">
                        {getStatusStepStatus(step.key) === 'completed' ? 'This stage is completed' :
                          getStatusStepStatus(step.key) === 'current' ? 'You are currently at this stage' : 'Awaiting this stage'}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="col-lg-4">
            <div className="donation-card p-4 mb-4">
              <h5 className="fw-bold mb-4">Donated Items</h5>
              {donation.images && donation.images.length > 0 ? (
                <div className="row g-3">
                  {donation.images.map((img, idx) => (
                    <div key={idx} className="col-6">
                      <div className="gallery-img-wrapper position-relative" onClick={() => setSelectedImage(img.image)}>
                        <img
                          src={img.image}
                          alt="donation"
                          className="img-fluid rounded-lg cursor-pointer hover-scale transition"
                          style={{ height: '120px', width: '100%', objectFit: 'cover' }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-4 bg-white bg-opacity-5 rounded-lg">
                  <i className="bi bi-images fs-2 text-muted mb-2 d-block"></i>
                  <p className="text-muted small mb-0">No photos available</p>
                </div>
              )}
            </div>

            <div className="donation-card p-4">
              <h5 className="fw-bold mb-4">Need Assistance?</h5>
              <p className="text-white-50 small mb-4">Our dedicated team is ready to help you with any queries regarding your donation.</p>
              <div className="d-grid gap-3">
                <a
                  href="https://wa.me/919846088219"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-outline-primary py-2 rounded-lg d-flex align-items-center justify-content-center gap-2"
                >
                  <i className="bi bi-chat-dots-fill"></i> Support Chat
                </a>
                <a
                  href="tel:+919846088219"
                  className="btn btn-outline-light py-2 rounded-lg d-flex align-items-center justify-content-center gap-2"
                >
                  <i className="bi bi-telephone-fill"></i> Call Helpline
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Modal for Lightbox */}
      {selectedImage && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.9)', backdropFilter: 'blur(10px)' }} onClick={() => setSelectedImage(null)}>
          <div className="modal-dialog modal-lg modal-dialog-centered">
            <div className="modal-content border-0 bg-transparent">
              <div className="text-end mb-2">
                <button className="btn btn-link text-white p-0 text-decoration-none fs-3">&times;</button>
              </div>
              <img src={selectedImage} className="img-fluid rounded shadow-2xl" alt="Enlarged view" />
            </div>
          </div>
        </div>
      )}

      <style>{`
        .ls-1 { letter-spacing: 1px; }
        .transition { transition: all 0.3s ease; }
        .hover-scale:hover { transform: scale(1.05); }
        .hover-opacity-100:hover { opacity: 1 !important; }
      `}</style>
    </div>
  );
};

export default DonationTracking;

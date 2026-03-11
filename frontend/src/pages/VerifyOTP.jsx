import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import api from '../api/api';
import { useAuth } from '../context/AuthContext';
import './auth.css';

const VerifyOTP = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [otp, setOtp] = useState('');
  const [donation, setDonation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const donationId = searchParams.get('id');
  const isDeliveryAgent = user?.is_staff || user?.is_superuser;

  useEffect(() => {
    if (donationId) {
      const fetchDonation = async () => {
        try {
          const response = await api.get(`/donations/${donationId}/`);
          setDonation(response.data);
        } catch (err) {
          setError('Failed to fetch donation details.');
        }
      };
      fetchDonation();
    }
  }, [donationId]);

  const handleSendOTP = async () => {
    setLoading(true);
    setError('');
    setMessage('');
    try {
      const response = await api.post(`/donations/${donationId}/send-otp/`);
      setMessage(response.data.message);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send OTP.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');
    try {
      const response = await api.post(`/donations/${donationId}/verify-otp/`, { otp });
      setMessage(response.data.message);
      setTimeout(() => navigate(`/tracking/${donationId}`), 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Invalid OTP.');
    } finally {
      setLoading(false);
    }
  };

  if (!donationId) return <div className="container mt-5 alert alert-warning">No donation ID provided.</div>;

  return (
    <div className="auth-wrapper d-flex align-items-center justify-content-center min-vh-100 bg-dark text-white">
      <div className="auth-card p-5 rounded-4 shadow-lg border border-light border-opacity-10" style={{ maxWidth: '450px', width: '95%' }}>
        <h2 className="text-center fw-bold mb-4">OTP Verification</h2>

        {donation && (
          <div className="donation-preview mb-4 p-3 rounded-3 bg-secondary bg-opacity-25 border border-light border-opacity-10">
            <p className="mb-1 small text-white opacity-75 text-uppercase fw-bold">Receipt Number</p>
            <p className="mb-2 fw-bold text-primary">{donation.receipt_number}</p>
            <div className="d-flex justify-content-between">
              <div>
                <p className="mb-0 small text-white opacity-75">Category</p>
                <p className="mb-0 small">{donation.category}</p>
              </div>
              <div className="text-end">
                <p className="mb-0 small text-white opacity-75">Status</p>
                <p className="mb-0 small">{donation.status_display}</p>
              </div>
            </div>
          </div>
        )}

        {message && <div className="alert alert-success py-2 small mb-3">{message}</div>}
        {error && <div className="alert alert-danger py-2 small mb-3">{error}</div>}

        {isDeliveryAgent && (
          <button
            onClick={handleSendOTP}
            className="btn btn-outline-primary w-100 mb-4 py-2"
            disabled={loading}
          >
            {loading ? 'Sending...' : 'Send OTP to Donor Email'}
          </button>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="form-label small fw-bold text-uppercase opacity-50">Enter 6-Digit OTP</label>
            <input
              type="text"
              className="form-control bg-transparent text-white border-light border-opacity-25 py-3 rounded-3 text-center fs-4 ls-lg"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              maxLength="6"
              placeholder="000000"
              required
            />
          </div>
          <button type="submit" className="btn btn-primary w-100 py-3 fw-bold rounded-3" disabled={loading || !otp}>
            {loading ? <span className="spinner-border spinner-border-sm me-2"></span> : null}
            Verify & Complete Delivery
          </button>
        </form>

        <p className="text-center mt-4 mb-0 small text-white opacity-75">
          The donor should have received the OTP on their registered email.
        </p>
      </div>

      <style>{`
                .ls-lg { letter-spacing: 0.5em; padding-left: 0.5em; }
            `}</style>
    </div>
  );
};

export default VerifyOTP;

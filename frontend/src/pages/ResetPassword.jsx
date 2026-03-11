import React, { useState } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import api from '../api/api';
import './auth.css';

const ResetPassword = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const uid = searchParams.get('uid');
    const token = searchParams.get('token');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        setLoading(true);
        setError('');
        setMessage('');

        try {
            const response = await api.post('/auth/reset-password/', {
                uid,
                token,
                password
            });
            setMessage(response.data.message);
            setTimeout(() => navigate('/login'), 3000);
        } catch (err) {
            setError(err.response?.data?.error || 'Invalid or expired link.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page d-flex align-items-center justify-content-center min-vh-100">
            <div className="auth-card p-5" style={{ maxWidth: '450px', width: '90%' }}>
                <h2 className="text-center auth-title mb-4">New Password</h2>
                <p className="auth-subtitle text-center mb-4">Please enter your new password below to secure your account.</p>

                {message && <div className="alert alert-success">{message}</div>}
                {error && <div className="alert alert-danger">{error}</div>}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="mb-4">
                        <label className="form-label text-dark fw-bold">NEW PASSWORD</label>
                        <input
                            type="password"
                            className="form-control"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Min 8 characters"
                            required
                        />
                    </div>
                    <div className="mb-4">
                        <label className="form-label text-dark fw-bold">CONFIRM PASSWORD</label>
                        <input
                            type="password"
                            className="form-control"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder="Repeat your password"
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-primary btn-login w-100 mb-4" disabled={loading}>
                        {loading ? <span className="spinner-border spinner-border-sm me-2"></span> : null}
                        Update Password
                    </button>
                    <div className="text-center">
                        <Link to="/login" className="auth-link-primary">Back to Login</Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ResetPassword;

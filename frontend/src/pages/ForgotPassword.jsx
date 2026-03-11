import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/api';
import './auth.css';

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setMessage('');

        try {
            const response = await api.post('/auth/forgot-password/', { email });
            setMessage(response.data.message);
        } catch (err) {
            setError(err.response?.data?.error || 'Something went wrong. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page d-flex align-items-center justify-content-center min-vh-100">
            <div className="auth-card p-5" style={{ maxWidth: '450px', width: '90%' }}>
                <h2 className="text-center auth-title mb-4">Reset Password</h2>
                <p className="auth-subtitle text-center mb-4">Enter your email and we'll send you a link to reset your password and recover your account.</p>

                {message && <div className="alert alert-success">{message}</div>}
                {error && <div className="alert alert-danger">{error}</div>}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="mb-4">
                        <label className="form-label text-dark fw-bold">EMAIL ADDRESS</label>
                        <input
                            type="email"
                            className="form-control"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            placeholder="Enter your registered email"
                        />
                    </div>
                    <button type="submit" className="btn btn-primary btn-login w-100 mb-4" disabled={loading}>
                        {loading ? <span className="spinner-border spinner-border-sm me-2"></span> : null}
                        Send Reset Link
                    </button>
                    <div className="text-center">
                        <Link to="/login" className="auth-link-primary">Back to Login</Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ForgotPassword;

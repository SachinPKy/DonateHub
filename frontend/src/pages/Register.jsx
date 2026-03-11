import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './auth.css';

const Register = () => {
    const navigate = useNavigate();
    const { register } = useAuth();

    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (formData.password !== formData.confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        setLoading(true);
        try {
            const result = await register(formData.username, formData.email, formData.password);
            if (result.success) {
                alert("Registration successful! Please login.");
                navigate('/login');
            } else {
                // Formatting error message if it's an object
                const errMsg = typeof result.error === 'object'
                    ? Object.values(result.error).flat().join(' ')
                    : result.error;
                setError(errMsg || "Registration failed. Please try again.");
            }
        } catch (err) {
            setError("An unexpected error occurred.");
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleSignup = () => {
        window.location.href = "http://localhost:8000/accounts/google/login/?next=/api/social-callback/";
    };

    return (
        <div className="auth-wrapper">
            <style>{`
                .auth-wrapper {
                    min-vh-100;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: rgba(26, 26, 46, 0.4);
                    backdrop-filter: blur(10px);
                    padding: 40px 20px;
                    min-height: 100vh;
                }
                .auth-card {
                    background: rgba(255, 255, 255, 0.05);
                    backdrop-filter: blur(20px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 24px;
                    padding: 48px;
                    width: 100%;
                    max-width: 500px;
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                    color: white;
                }
                .auth-title {
                    font-size: 2rem;
                    font-weight: 800;
                    margin-bottom: 8px;
                    background: linear-gradient(to right, #fff, #94a3b8);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                .auth-subtitle {
                    color: #cbd5e1; /* Increased contrast from #94a3b8 */
                    margin-bottom: 32px;
                }
                .form-control {
                    background: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    color: white;
                    padding: 12px 16px;
                    border-radius: 12px;
                    transition: all 0.3s ease;
                }
                .form-control:focus {
                    background: rgba(255, 255, 255, 0.1);
                    border-color: #3b82f6;
                    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
                    color: white;
                }
                .btn-primary {
                    background: #3b82f6;
                    border: none;
                    padding: 14px;
                    border-radius: 12px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                }
                .btn-primary:hover {
                    background: #2563eb;
                    transform: translateY(-1px);
                }
                .btn-google {
                    background: white;
                    color: #1a1a2e;
                    border: none;
                    padding: 12px;
                    border-radius: 12px;
                    font-weight: 600;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                    margin-bottom: 24px;
                    transition: all 0.3s ease;
                }
                .divider {
                    display: flex;
                    align-items: center;
                    text-align: center;
                    margin: 24px 0;
                    color: #94a3b8; /* Increased contrast from #475569 */
                }
                .divider::before, .divider::after {
                    content: '';
                    flex: 1;
                    border-bottom: 1px solid #334155;
                }
                .divider span { padding: 0 12px; font-size: 0.875rem; }
            `}</style>
            <div className="auth-card">
                <div className="text-center">
                    <h2 className="auth-title">Create Account</h2>
                    <p className="auth-subtitle">Be the change you want to see</p>
                </div>

                <button onClick={handleGoogleSignup} className="btn btn-google w-100">
                    <i className="bi bi-google"></i>
                    Sign up with Google
                </button>

                <div className="divider">
                    <span>OR USE YOUR EMAIL</span>
                </div>

                {error && (
                    <div className="alert alert-danger py-2 border-0 bg-danger bg-opacity-10 text-danger mb-4" role="alert">
                        <i className="bi bi-exclamation-circle me-2"></i>
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    <div className="row">
                        <div className="col-md-6 mb-3">
                            <label className="form-label small fw-bold text-uppercase opacity-50">Username</label>
                            <input
                                type="text"
                                className="form-control"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                placeholder="Unique Name"
                                required
                            />
                        </div>
                        <div className="col-md-6 mb-3">
                            <label className="form-label small fw-bold text-uppercase opacity-50">Email</label>
                            <input
                                type="email"
                                className="form-control"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                placeholder="name@email.com"
                                required
                            />
                        </div>
                    </div>

                    <div className="mb-3">
                        <label className="form-label small fw-bold text-uppercase opacity-50">Password</label>
                        <div className="password-wrapper">
                            <input
                                type={showPassword ? "text" : "password"}
                                className="form-control"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                placeholder="Create Password"
                                required
                            />
                            <button
                                type="button"
                                className="toggle-password"
                                onClick={() => setShowPassword(!showPassword)}
                                aria-label={showPassword ? "Hide password" : "Show password"}
                            >
                                <i className={`bi ${showPassword ? 'bi-eye-slash' : 'bi-eye'}`}></i>
                            </button>
                        </div>
                    </div>

                    <div className="mb-4">
                        <label className="form-label small fw-bold text-uppercase opacity-50">Confirm Password</label>
                        <div className="password-wrapper">
                            <input
                                type={showConfirmPassword ? "text" : "password"}
                                className="form-control"
                                name="confirmPassword"
                                value={formData.confirmPassword}
                                onChange={handleChange}
                                placeholder="Repeat Password"
                                required
                            />
                            <button
                                type="button"
                                className="toggle-password"
                                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                aria-label={showConfirmPassword ? "Hide password" : "Show password"}
                            >
                                <i className={`bi ${showConfirmPassword ? 'bi-eye-slash' : 'bi-eye'}`}></i>
                            </button>
                        </div>
                    </div>

                    <button type="submit" className="btn btn-primary w-100 mb-4" disabled={loading}>
                        {loading ? <span className="spinner-border spinner-border-sm me-2"></span> : null}
                        Join DonateHub
                    </button>
                </form>

                <div className="text-center">
                    <p className="mb-0 text-white opacity-75">
                        Already joined? {' '}
                        <Link to="/login" className="text-white text-decoration-none fw-bold hover-underline">Sign In</Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Register;

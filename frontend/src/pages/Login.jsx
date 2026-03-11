import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './auth.css';

const Login = () => {
    const navigate = useNavigate();
    const { login } = useAuth();

    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const result = await login(formData.username, formData.password);
            if (result.success) {
                navigate('/');
            } else {
                setError(result.error || 'Invalid username or password');
            }
        } catch (err) {
            setError('An unexpected error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleLogin = () => {
        // Redirect to Django Allauth Google Login
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
                    padding: 20px;
                    min-height: 100vh;
                }
                .auth-card {
                    background: rgba(255, 255, 255, 0.05);
                    backdrop-filter: blur(20px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 24px;
                    padding: 48px;
                    width: 100%;
                    max-width: 450px;
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
                    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
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
                .btn-google:hover {
                    background: #f1f5f9;
                    transform: translateY(-1px);
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
                .divider span {
                    padding: 0 12px;
                    font-size: 0.875rem;
                }
                .divider span {
                    padding: 0 12px;
                    font-size: 0.875rem;
                }
            `}</style>

            <div className="auth-card">
                <div className="text-center">
                    <h2 className="auth-title">Welcome Back</h2>
                    <p className="auth-subtitle">Elevating the art of giving</p>
                </div>

                <button onClick={handleGoogleLogin} className="btn btn-google w-100">
                    <i className="bi bi-google"></i>
                    Continue with Google
                </button>

                <div className="divider">
                    <span>OR CONTINUE WITH EMAIL</span>
                </div>

                {error && (
                    <div className="alert alert-danger py-2 border-0 bg-danger bg-opacity-10 text-danger mb-4" role="alert">
                        <i className="bi bi-exclamation-circle me-2"></i>
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label small fw-bold text-uppercase opacity-50">Username</label>
                        <input
                            type="text"
                            className="form-control"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            placeholder="Your unique ID"
                            required
                        />
                    </div>

                    <div className="mb-4">
                        <label className="form-label small fw-bold text-uppercase opacity-50">Password</label>
                        <div className="password-wrapper">
                            <input
                                type={showPassword ? "text" : "password"}
                                className="form-control"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                placeholder="••••••••"
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
                        <div className="text-end mt-2">
                            <Link to="/forgot-password" style={{ color: '#3b82f6', textDecoration: 'none', fontSize: '0.85rem', fontWeight: '500' }}>
                                Forgot Password?
                            </Link>
                        </div>
                    </div>

                    <button type="submit" className="btn btn-primary w-100 mb-4" disabled={loading}>
                        {loading ? (
                            <span className="spinner-border spinner-border-sm me-2"></span>
                        ) : null}
                        Sign In to DonateHub
                    </button>
                </form>

                <div className="text-center">
                    <p className="mb-0 text-white opacity-75">
                        New to the hub? {' '}
                        <Link to="/register" className="text-white text-decoration-none fw-bold hover-underline">Create Account</Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login;

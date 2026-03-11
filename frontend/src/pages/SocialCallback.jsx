import React, { useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const SocialCallback = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const { setTokens } = useAuth();

    useEffect(() => {
        const access = searchParams.get('access');
        const refresh = searchParams.get('refresh');

        if (access && refresh) {
            setTokens(access, refresh)
                .then(() => {
                    navigate('/');
                })
                .catch((err) => {
                    console.error("Social login processing failed", err);
                    navigate('/login?error=social_failed');
                });
        } else {
            navigate('/login');
        }
    }, [searchParams, navigate, setTokens]);

    return (
        <div className="d-flex justify-content-center align-items-center min-vh-100 bg-dark text-white">
            <div className="text-center">
                <div className="spinner-border text-primary mb-3" role="status"></div>
                <h4>Completing secure login...</h4>
                <p className="text-muted">You will be redirected in a moment.</p>
            </div>
        </div>
    );
};

export default SocialCallback;

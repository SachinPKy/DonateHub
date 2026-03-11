import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
    const navigate = useNavigate();
    const { user, logout, isAuthenticated } = useAuth();

    // Mocking superuser for now, can be checked via user.is_superuser if added to serializer
    const isSuperuser = user?.is_superuser || false;

    const handleLogout = (e) => {
        e.preventDefault();
        logout();
        navigate('/login');
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark bg-opacity-75">
            <div className="container">
                <Link className="navbar-brand fw-bold" to="/">DonateHub</Link>

                {/* MOBILE TOGGLER */}
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarMenu">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse justify-content-end" id="navbarMenu">
                    <ul className="navbar-nav align-items-lg-center">
                        {isAuthenticated && isSuperuser ? (
                            <>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/admin">Admin Dashboard</Link>
                                </li>
                                <li className="nav-item ms-lg-2">
                                    <form onSubmit={handleLogout}>
                                        <button type="submit" className="btn btn-outline-light btn-sm mt-2 mt-lg-0">
                                            Logout
                                        </button>
                                    </form>
                                </li>
                            </>
                        ) : isAuthenticated ? (
                            <>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/add">Add Donation</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/my-donations">My Donations</Link>
                                </li>
                                <li className="nav-item ms-lg-2">
                                    <form onSubmit={handleLogout}>
                                        <button type="submit" className="btn btn-outline-light btn-sm mt-2 mt-lg-0">
                                            Logout
                                        </button>
                                    </form>
                                </li>
                            </>
                        ) : (
                            <>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/login">Login</Link>
                                </li>
                                <li className="nav-item ms-lg-2">
                                    <Link className="btn btn-outline-light btn-sm mt-2 mt-lg-0" to="/register">
                                        Register
                                    </Link>
                                </li>
                            </>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;

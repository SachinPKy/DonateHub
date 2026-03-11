import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Home = () => {
    const { isAuthenticated, user } = useAuth();
    const isSuperuser = user?.is_superuser || false;

    return (
        <>
            <style>
                {`
          /* HERO */
          .hero {
              padding: 120px 0;
          }

          .hero-title {
              font-size: 3.2rem;
              font-weight: bold;
              color: #ffffff;
          }

          .hero-subtitle {
              font-size: 1.3rem;
              color: #ffffff;
          }

          /* CARDS */
          .card {
              background-color: rgba(255, 255, 255, 0.1);
              backdrop-filter: blur(10px);
              color: white;
              border: 1px solid rgba(255, 255, 255, 0.2);
              border-radius: 15px;
          }

          h2 {
              color: white;
          }

          /* ===== MOBILE RESPONSIVE ===== */
          @media (max-width: 576px) {
              .hero {
                  padding: 70px 15px;
              }

              .hero-title {
                  font-size: 2rem;
              }

              .hero-subtitle {
                  font-size: 1rem;
              }

              .btn-lg {
                  font-size: 1rem;
                  padding: 10px 18px;
              }
          }
        `}
            </style>

            {/* ================= HERO SECTION ================= */}
            <section className="hero text-center">
                <div className="container">
                    <h1 className="hero-title">
                        Give What You Can. Change a Life.
                    </h1>

                    <p className="hero-subtitle mt-4">
                        DonateHub is a centralized platform connecting donors and NGOs
                        to ensure reusable items reach those who need them most.
                    </p>

                    {isAuthenticated && !isSuperuser ? (
                        <Link to="/add" className="btn btn-primary btn-lg mt-4">
                            Donate Now
                        </Link>
                    ) : !isAuthenticated && (
                        <Link to="/register" className="btn btn-success btn-lg mt-4">
                            Get Started
                        </Link>
                    )}
                </div>
            </section>

            {/* ================= HOW TO USE / MERITS OF DONATING ================= */}
            {!isAuthenticated ? (
                <section className="container my-5">
                    <h2 className="text-center mb-4">How DonateHub Works</h2>

                    <div className="row text-center">
                        <div className="col-md-3 mb-4">
                            <div className="card p-4 shadow h-100">
                                <h5 className="text-white">Register</h5>
                                <p>Create an account to start donating securely.</p>
                            </div>
                        </div>

                        <div className="col-md-3 mb-4">
                            <div className="card p-4 shadow h-100">
                                <h5 className="text-white">Login</h5>
                                <p>Access your dashboard and donation features.</p>
                            </div>
                        </div>

                        <div className="col-md-3 mb-4">
                            <div className="card p-4 shadow h-100">
                                <h5 className="text-white">Donate</h5>
                                <p>Add donation details with AI-powered assistance.</p>
                            </div>
                        </div>

                        <div className="col-md-3 mb-4">
                            <div className="card p-4 shadow h-100">
                                <h5 className="text-white">Track</h5>
                                <p>View and track all your donations easily.</p>
                            </div>
                        </div>
                    </div>
                </section>
            ) : (
                <section className="container my-5">
                    <h2 className="text-center mb-4">Merits of Donating</h2>

                    <div className="row text-center">
                        <div className="col-md-3 mb-4">
                            <div className="card p-4 shadow h-100">
                                <h5 className="text-white">Make a Difference</h5>
                                <p>Your donations directly impact lives and create positive change in communities.</p>
                            </div>
                        </div>

                        <div className="col-md-3 mb-4">
                            <div className="card p-4 shadow h-100">
                                <h5 className="text-white">Tax Benefits</h5>
                                <p>Charitable donations may qualify for tax deductions, reducing your taxable income.</p>
                            </div>
                        </div>

                        <div className="col-md-3 mb-4">
                            <div className="card p-4 shadow h-100">
                                <h5 className="text-white">Personal Fulfillment</h5>
                                <p>Experience the joy and satisfaction that comes from helping others in need.</p>
                            </div>
                        </div>

                        <div className="col-md-3 mb-4">
                            <div className="card p-4 shadow h-100">
                                <h5 className="text-white">Build Community</h5>
                                <p>Strengthen social bonds and inspire others to contribute to worthy causes.</p>
                            </div>
                        </div>
                    </div>
                </section>
            )}
        </>
    );
};

export default Home;

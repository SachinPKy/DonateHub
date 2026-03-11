import React from 'react';
import { Link } from 'react-router-dom';

const Success = () => {
    return (
        <>
            <style>
                {`
          .success-wrapper {
            min-height: calc(100vh - 130px);
            background: linear-gradient(to right, #e8f5e9, #ffffff);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 15px;
            color: black;
          }

          .success-card {
            width: 100%;
            max-width: 600px;
            padding: 40px;
            border-radius: 15px;
            background: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            text-align: center;
          }

          .success-icon {
            font-size: 70px;
            color: #28a745;
          }

          .btn-custom {
            margin: 8px;
          }

          @media (max-width: 576px) {
            .success-card {
              padding: 25px;
            }
            .success-icon {
              font-size: 55px;
            }
            h2 {
              font-size: 1.5rem;
            }
            .lead {
              font-size: 1rem;
            }
            .btn {
              width: 100%;
              margin: 6px 0;
            }
          }
        `}
            </style>

            <div className="success-wrapper">
                <div className="success-card">
                    <div className="success-icon">✔</div>

                    <h2 className="text-success mt-3">Donation Added Successfully!</h2>

                    <p className="lead mt-3">
                        Thank you for your generosity. Your donation has been recorded and will
                        be processed by our team.
                    </p>

                    <hr />

                    <p>
                        You can track the status of your donation or continue helping by adding
                        more donations.
                    </p>

                    <div className="mt-4">
                        <Link to="/my-donations" className="btn btn-primary btn-custom">
                            View My Donations
                        </Link>

                        <Link to="/add" className="btn btn-outline-success btn-custom">
                            Add Another Donation
                        </Link>
                    </div>

                    <br />

                    <Link to="/" className="btn btn-link"> Back to Home </Link>
                </div>
            </div>
        </>
    );
};

export default Success;

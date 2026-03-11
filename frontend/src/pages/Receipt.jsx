import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const Receipt = () => {
    // Mock receipt data
    const donation = {
        receipt_number: 'DON-20251025-001',
        category: 'Clothes',
        description: 'Used winter clothes in good condition',
        pickup_date: '25 Oct 2025',
        amount: 1500.00,
        statusDisplay: 'In Transit',
        donor: {
            username: 'User123',
            email: 'user123@example.com'
        },
        area: 'Technopark',
        district: 'Thiruvananthapuram',
        state: 'Kerala',
        pickup_address: 'Building A, Apartment 101'
    };

    const generated_date = new Date().toLocaleString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });

    return (
        <>
            <style>
                {`
          .receipt-wrapper {
            background: #f5f5f5;
            padding: 40px 15px;
            color: #222;
            min-height: calc(100vh - 130px);
          }

          .receipt-card {
            max-width: 800px;
            margin: auto;
            background: #ffffff;
            padding: 40px;
            border: 1px solid #ddd;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
          }

          /* HEADER */
          .receipt-header {
            text-align: center;
            margin-bottom: 30px;
          }

          .receipt-header h1 {
            margin: 0;
            font-size: 28px;
            letter-spacing: 0.5px;
            color: #212529;
          }

          .receipt-header p {
            margin-top: 6px;
            font-size: 13px;
            color: #666;
          }

          .receipt-title {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 25px 0 35px;
            color: #2e7d32;
          }

          /* SECTION TITLE */
          .receipt-section-title {
            font-size: 13px;
            font-weight: bold;
            text-transform: uppercase;
            color: #555;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 6px;
            margin-bottom: 15px;
            margin-top: 25px;
          }

          .receipt-section-title:first-of-type {
            margin-top: 0;
          }

          /* TABLE */
          .receipt-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
          }

          .receipt-table td {
            padding: 8px 6px;
            vertical-align: top;
            font-size: 14px;
          }

          .receipt-table td.label {
            width: 35%;
            color: #555;
          }

          .receipt-table td.value {
            width: 65%;
            font-weight: 500;
            color: #111;
          }

          /* STATUS */
          .receipt-status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            color: #fff;
            background: #17a2b8; /* Default for SUBMITTED */
          }

          /* LOCATION BOX */
          .receipt-location-box {
            background: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
          }

          .receipt-location-box .label {
            font-size: 11px;
            color: #666;
            text-transform: uppercase;
          }

          .receipt-location-box .value {
            font-size: 15px;
            font-weight: 600;
            color: #333;
            margin-top: 5px;
          }

          /* FOOTER */
          .receipt-footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            font-size: 13px;
            color: #555;
          }

          .back-btn {
            display: block;
            text-align: center;
            margin-top: 20px;
            text-decoration: none;
            color: #0d6efd;
          }

          @media print {
            .receipt-wrapper {
              background: white;
              padding: 0;
            }
            .receipt-card {
              border: none;
              box-shadow: none;
            }
            .back-btn, .navbar, .footer {
              display: none !important;
            }
          }
        `}
            </style>

            <div className="receipt-wrapper">
                <div className="receipt-card">
                    <div className="receipt-header">
                        <h1>DonateHub</h1>
                        <p>Making a Difference, One Donation at a Time</p>
                    </div>

                    <div className="receipt-title">Donation Receipt</div>

                    <div className="receipt-section-title">Receipt Information</div>
                    <table className="receipt-table">
                        <tbody>
                            <tr>
                                <td className="label">Receipt Number</td>
                                <td className="value">{donation.receipt_number}</td>
                            </tr>
                            <tr>
                                <td className="label">Generated Date</td>
                                <td className="value">{generated_date}</td>
                            </tr>
                        </tbody>
                    </table>

                    <div className="receipt-section-title">Donor Information</div>
                    <table className="receipt-table">
                        <tbody>
                            <tr>
                                <td className="label">Donor Name</td>
                                <td className="value">{donation.donor.username}</td>
                            </tr>
                            <tr>
                                <td className="label">Email</td>
                                <td className="value">{donation.donor.email}</td>
                            </tr>
                        </tbody>
                    </table>

                    <div className="receipt-section-title">Donation Details</div>
                    <table className="receipt-table">
                        <tbody>
                            <tr>
                                <td className="label">Category</td>
                                <td className="value">{donation.category}</td>
                            </tr>
                            <tr>
                                <td className="label">Description</td>
                                <td className="value">{donation.description}</td>
                            </tr>
                            <tr>
                                <td className="label">Pickup Date</td>
                                <td className="value">{donation.pickup_date}</td>
                            </tr>
                            <tr>
                                <td className="label">Donation Value</td>
                                <td className="value">₹{donation.amount.toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td className="label">Status</td>
                                <td className="value">
                                    <span className="receipt-status">
                                        {donation.statusDisplay}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <div className="receipt-section-title">Pickup Location</div>
                    <div className="receipt-location-box">
                        <div className="label">Full Address</div>
                        <div className="value">
                            {donation.area && <>{donation.area}<br /></>}
                            {donation.district && <>{donation.district}<br /></>}
                            {donation.state} - India
                        </div>
                        {donation.pickup_address && (
                            <div className="value" style={{ marginTop: '10px', fontWeight: 'normal' }}>
                                {donation.pickup_address}
                            </div>
                        )}
                    </div>

                    <div className="receipt-footer">
                        Thank you for your generous donation.<br />
                        This is a system-generated receipt.<br /><br />
                        <strong>DonateHub</strong> - Kerala's Trusted Donation Platform
                    </div>
                </div>

                <Link to="/my-donations" className="back-btn">← Back to My Donations</Link>
                <div className="text-center mt-3">
                    <button className="btn btn-outline-secondary btn-sm" onClick={() => window.print()}>
                        🖨️ Print Receipt
                    </button>
                </div>
            </div>
        </>
    );
};

export default Receipt;

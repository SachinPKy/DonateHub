import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import './index.css';

// Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Pages
import Home from './pages/Home';
import AddDonation from './pages/AddDonation';
import MyDonations from './pages/MyDonations';
import DonationTracking from './pages/DonationTracking';
import Login from './pages/Login';
import Register from './pages/Register';
import Success from './pages/Success';
import VerifyOTP from './pages/VerifyOTP';
import Receipt from './pages/Receipt';
import SocialCallback from './pages/SocialCallback';
import AdminDashboard from './pages/AdminDashboard';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';

function App() {
  return (
    <Router>
      <div className="d-flex flex-column min-vh-100">
        <Navbar />
        <main className="flex-grow-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/add" element={<AddDonation />} />
            <Route path="/my-donations" element={<MyDonations />} />
            <Route path="/tracking/:id" element={<DonationTracking />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/success" element={<Success />} />
            <Route path="/verify-otp" element={<VerifyOTP />} />
            <Route path="/receipt" element={<Receipt />} />
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route path="/social-callback" element={<SocialCallback />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;

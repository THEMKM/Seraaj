import { Route, Routes, Navigate } from 'react-router-dom';
import Landing from './pages/Landing';
import Signup from './pages/Signup';
import Login from './pages/Login';
import VolunteerDashboard from './pages/VolunteerDashboard';
import Opportunities from './pages/Opportunities';
import OpportunityDetail from './pages/OpportunityDetail';
import OrgDashboard from './pages/OrgDashboard';
import OpportunityForm from './pages/OpportunityForm';
import ApplicantReview from './pages/ApplicantReview';
import SuperadminSettings from './pages/SuperadminSettings';
import ThemeToggle from './components/ThemeToggle';
import ProtectedRoute from './components/ProtectedRoute';

export default function App() {
  return (
    <>
    <div className="fixed top-2 right-2 z-10"><ThemeToggle /></div>
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<ProtectedRoute><VolunteerDashboard /></ProtectedRoute>} />
      <Route path="/opportunities" element={<ProtectedRoute><Opportunities /></ProtectedRoute>} />
      <Route path="/opportunity/:id" element={<ProtectedRoute><OpportunityDetail /></ProtectedRoute>} />
      <Route path="/org/dashboard" element={<ProtectedRoute><OrgDashboard /></ProtectedRoute>} />
      <Route path="/org/opportunity/new" element={<ProtectedRoute><OpportunityForm /></ProtectedRoute>} />
      <Route path="/org/opportunity/:id/applicants" element={<ProtectedRoute><ApplicantReview /></ProtectedRoute>} />
      <Route path="/settings" element={<ProtectedRoute><SuperadminSettings /></ProtectedRoute>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
    </>
  );
}

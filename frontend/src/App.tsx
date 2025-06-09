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

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<VolunteerDashboard />} />
      <Route path="/opportunities" element={<Opportunities />} />
      <Route path="/opportunity/:id" element={<OpportunityDetail />} />
      <Route path="/org/dashboard" element={<OrgDashboard />} />
      <Route path="/org/opportunity/new" element={<OpportunityForm />} />
      <Route path="/org/opportunity/:id/applicants" element={<ApplicantReview />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

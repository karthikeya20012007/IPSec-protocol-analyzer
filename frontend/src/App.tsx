import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import { Shell } from './components/layout/Shell';
import { Captures } from './pages/Captures';
import { Overview } from './pages/Overview';
import { Traffic } from './pages/Traffic';
import { IPsec } from './pages/IPsec';
import { Security } from './pages/Security';
import { Reports } from './pages/Reports';
import { LandingPage } from './pages/LandingPage';

function App() {
  return (
    <BrowserRouter>
      <AppProvider>
        <Routes>
          {/* Landing Page */}
          <Route path="/" element={<LandingPage />} />

          {/* Analyzer Application */}
          <Route path="/app" element={<Shell><Captures /></Shell>} />
          <Route path="/app/overview" element={<Shell><Overview /></Shell>} />
          <Route path="/app/traffic" element={<Shell><Traffic /></Shell>} />
          <Route path="/app/ipsec" element={<Shell><IPsec /></Shell>} />
          <Route path="/app/security" element={<Shell><Security /></Shell>} />
          <Route path="/app/reports" element={<Shell><Reports /></Shell>} />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppProvider>
    </BrowserRouter>
  );
}

export default App;

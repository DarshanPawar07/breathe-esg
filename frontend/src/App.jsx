import {
  Routes,
  Route,
  Navigate
} from 'react-router-dom'

import Sidebar from './components/layout/Sidebar'

import Navbar from './components/layout/Navbar'

import Dashboard from './pages/Dashboard'

import UploadPage from './pages/UploadPage'

import ReviewPage from './pages/ReviewPage'

import FailedRows from './pages/FailedRows'

import EmissionDetails from './pages/EmissionDetails'

import NotFound from './pages/NotFound'


function App() {

  return (

    <div className="app-shell">

      {/* Sidebar */}

      <Sidebar />

      {/* Main Content */}

      <div className="main-wrapper">

        {/* Navbar */}

        <Navbar />

        {/* Page Content */}

        <main className="page-content">

          <Routes>

            {/* Dashboard */}

            <Route
              path="/"
              element={<Dashboard />}
            />

            {/* Upload */}

            <Route
              path="/upload"
              element={<UploadPage />}
            />

            {/* Review Queue */}

            <Route
              path="/review"
              element={<ReviewPage />}
            />

            {/* Failed Rows */}

            <Route
              path="/failed"
              element={<FailedRows />}
            />

            {/* Emission Details */}

            <Route
              path="/emissions/:id"
              element={<EmissionDetails />}
            />

            {/* Redirect */}

            <Route
              path="/dashboard"
              element={
                <Navigate to="/" />
              }
            />

            {/* 404 */}

            <Route
              path="*"
              element={<NotFound />}
            />

          </Routes>

        </main>

      </div>

    </div>
  )
}

export default App
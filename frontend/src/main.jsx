import React from 'react'

import ReactDOM from 'react-dom/client'

import { BrowserRouter } from 'react-router-dom'

import { Toaster } from 'react-hot-toast'

import App from './App'

import './styles/globals.css'

import './styles/layout.css'

import './styles/dashboard.css'

import './styles/tables.css'

import './styles/forms.css'


ReactDOM.createRoot(
  document.getElementById('root')
).render(

  <React.StrictMode>

    <BrowserRouter>

      <Toaster
        position="top-right"
      />

      <App />

    </BrowserRouter>

  </React.StrictMode>
)
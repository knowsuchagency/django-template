import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import './index.css'
import App from './App.tsx'

// Detect if we're running through Django by checking if the current path starts with /app
// In development, we're at /static/ but still want root routing
const isServedByDjango = window.location.pathname.startsWith('/app')
const basename = isServedByDjango ? '/app' : '/static'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter basename={basename}>
      <App />
    </BrowserRouter>
  </StrictMode>,
)

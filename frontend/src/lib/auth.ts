import { AllauthClient } from '@knowsuchagency/allauth-fetch'

const isDevelopment = import.meta.env.DEV

export const allauthClient = new AllauthClient(
  isDevelopment ? 'http://localhost:8000' : '',
  '/api/v1/csrf-token',
  'browser'
)

// Create a fetch wrapper that includes CSRF token
export const allauthFetch = async (url: string, options: RequestInit = {}) => {
  const csrfToken = await allauthClient.fetchCSRFToken()
  
  const headers = {
    ...options.headers,
    ...(csrfToken && options.method !== 'GET' ? { 'X-CSRFToken': csrfToken } : {})
  }
  
  const fullUrl = isDevelopment && url.startsWith('/') ? `http://localhost:8000${url}` : url
  
  return fetch(fullUrl, {
    ...options,
    headers,
    credentials: 'include',
  })
}
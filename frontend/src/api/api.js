import axios from 'axios'

import toast from 'react-hot-toast'


// ─────────────────────────────────────
// AXIOS INSTANCE
// ─────────────────────────────────────

const api = axios.create({

  baseURL:
    import.meta.env.VITE_API_BASE_URL,

  headers: {

    'Content-Type': 'application/json',
  },
})


// ─────────────────────────────────────
// REQUEST INTERCEPTOR
// ─────────────────────────────────────

api.interceptors.request.use(

  (config) => {

    return config
  },

  (error) => {

    return Promise.reject(error)
  }
)


// ─────────────────────────────────────
// RESPONSE INTERCEPTOR
// ─────────────────────────────────────

api.interceptors.response.use(

  (response) => {

    return response
  },

  (error) => {

    console.error(
      'API Error:',
      error
    )

    const message = (

      error?.response?.data?.error ||

      error?.response?.data?.message ||

      'Something went wrong'
    )

    toast.error(message)

    return Promise.reject(error)
  }
)


// ─────────────────────────────────────
// DASHBOARD APIS
// ─────────────────────────────────────

export const fetchDashboardSummary =
  async (params = {}) => {

    const response = await api.get(
      '/dashboard/',
      {
        params
      }
    )

    return response.data
  }


// ─────────────────────────────────────
// EMISSION RECORD APIS
// ─────────────────────────────────────

export const fetchEmissionRecords =
  async (params = {}) => {

    const response = await api.get(
      '/emission-records/',
      {
        params
      }
    )

    return response.data
  }


export const fetchPendingRecords =
  async () => {

    const response = await api.get(
      '/emission-records/pending/'
    )

    return response.data
  }


export const fetchApprovedRecords =
  async () => {

    const response = await api.get(
      '/emission-records/approved/'
    )

    return response.data
  }


// ─────────────────────────────────────
// REVIEW ACTIONS
// ─────────────────────────────────────

export const approveRecord =
  async (recordId) => {

    const response = await api.post(
      `/review/${recordId}/approve/`,
      {
        reviewer_email:
          'sarah@breatheesg.com'
      }
    )

    toast.success(
      'Record approved'
    )

    return response.data
  }


export const flagRecord =
  async (
    recordId,
    reason = 'Suspicious values detected'
  ) => {

    const response = await api.post(
      `/review/${recordId}/flag/`,
      {
        reviewer_email:
          'sarah@breatheesg.com',

        reason,
      }
    )

    toast.success(
      'Record flagged'
    )

    return response.data
  }


export const lockRecord =
  async (recordId) => {

    const response = await api.post(
      `/review/${recordId}/lock/`
    )

    toast.success(
      'Record locked'
    )

    return response.data
  }


// ─────────────────────────────────────
// FILE UPLOAD APIS
// ─────────────────────────────────────

export const uploadSAPFile =
  async (
    file,
    tenantId = 1
  ) => {

    const formData = new FormData()

    formData.append('file', file)

    formData.append(
      'tenant_id',
      tenantId
    )

    const response = await api.post(
      '/upload/sap/',
      formData,
      {
        headers: {
          'Content-Type':
            'multipart/form-data',
        },
      }
    )

    toast.success(
      'SAP file uploaded successfully'
    )

    return response.data
  }


export const uploadUtilityFile =
  async (
    file,
    tenantId = 1
  ) => {

    const formData = new FormData()

    formData.append('file', file)

    formData.append(
      'tenant_id',
      tenantId
    )

    const response = await api.post(
      '/upload/utility/',
      formData,
      {
        headers: {
          'Content-Type':
            'multipart/form-data',
        },
      }
    )

    toast.success(
      'Utility file uploaded successfully'
    )

    return response.data
  }


export const uploadTravelFile =
  async (
    file,
    tenantId = 1
  ) => {

    const formData = new FormData()

    formData.append('file', file)

    formData.append(
      'tenant_id',
      tenantId
    )

    const response = await api.post(
      '/upload/travel/',
      formData,
      {
        headers: {
          'Content-Type':
            'multipart/form-data',
        },
      }
    )

    toast.success(
      'Travel file uploaded successfully'
    )

    return response.data
  }


// ─────────────────────────────────────
// EXPORT INSTANCE
// ─────────────────────────────────────

export default api

export const ingestTravelData = async (
  payload
) => {

  const response = await api.post(

    '/ingest/travel/',

    payload
  )

  return response
}
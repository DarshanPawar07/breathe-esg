import { useEffect, useState } from 'react'

import {

  fetchDashboardSummary,

  fetchEmissionRecords

} from '../api/api'


const useDashboard = () => {

  const [summary, setSummary] =
    useState(null)

  const [records, setRecords] =
    useState([])

  const [loading, setLoading] =
    useState(true)

  const [filters, setFilters] =
    useState({

      facility: '',

      status: '',

      source_type: '',

      scope: '',
    })


  // ─────────────────────────────
  // LOAD DASHBOARD
  // ─────────────────────────────

  const loadDashboard = async () => {

    try {

      setLoading(true)

      const dashboardData =
        await fetchDashboardSummary(
          filters
        )

      const emissionData =
        await fetchEmissionRecords(
          filters
        )

      setSummary(dashboardData)

      setRecords(emissionData)

    } catch (error) {

      console.error(
        'Dashboard load failed',
        error
      )

    } finally {

      setLoading(false)
    }
  }


  // ─────────────────────────────
  // INITIAL LOAD
  // ─────────────────────────────

  useEffect(() => {

    loadDashboard()

  }, [filters])


  // ─────────────────────────────
  // RETURN
  // ─────────────────────────────

  return {

    summary,

    records,

    loading,

    filters,

    setFilters,

    reload: loadDashboard,
  }
}

export default useDashboard
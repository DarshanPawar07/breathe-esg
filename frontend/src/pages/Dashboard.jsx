import { useMemo, useState } from 'react'

import PageContainer from '../components/layout/PageContainer'

import DashboardHeader from '../components/dashboard/DashboardHeader'

import KPISection from '../components/dashboard/KPISection'

import FiltersBar from '../components/dashboard/FiltersBar'

import StatusTabs from '../components/dashboard/StatusTabs'

import AnalystTable from '../components/dashboard/AnalystTable'

import QuickStats from '../components/dashboard/QuickStats'

import EmptyState from '../components/dashboard/EmptyState'

import Loader from '../components/shared/Loader'

import useDashboard from '../hooks/useDashboard'


function Dashboard() {

  const {

    summary,

    records,

    loading,

    filters,

    setFilters,

    reload

  } = useDashboard()

  const [activeTab, setActiveTab] =
    useState('all')


  // ─────────────────────────────
  // SAFE RECORDS
  // ─────────────────────────────

  const safeRecords = useMemo(() => {

    if (Array.isArray(records)) {

      return records
    }

    if (records?.results) {

      return records.results
    }

    return []

  }, [records])


  // ─────────────────────────────
  // FILTER BY STATUS TAB
  // ─────────────────────────────

  const filteredRecords = useMemo(() => {

    if (activeTab === 'all') {

      return safeRecords
    }

    return safeRecords.filter((record) =>

      record.status === activeTab
    )

  }, [safeRecords, activeTab])


  // ─────────────────────────────
  // LOADING STATE
  // ─────────────────────────────

  if (loading) {

    return (
      <Loader text="Loading dashboard..." />
    )
  }


  // ─────────────────────────────
  // UI
  // ─────────────────────────────

  return (

    <PageContainer

      title="Breathe ESG"

      subtitle="Enterprise ESG analyst dashboard"
    >

      <DashboardHeader />

      <KPISection
        summary={summary?.summary}
      />

      <QuickStats
        records={filteredRecords}
      />

      <FiltersBar

        filters={filters}

        setFilters={setFilters}

        facilities={
          summary?.filters?.facilities || []
        }
      />

      <StatusTabs

        activeTab={activeTab}

        setActiveTab={setActiveTab}
      />

      {filteredRecords.length === 0 ? (

        <EmptyState />

      ) : (

        <AnalystTable

          records={filteredRecords}

          reloadDashboard={reload}
        />
      )}

    </PageContainer>
  )
}

export default Dashboard
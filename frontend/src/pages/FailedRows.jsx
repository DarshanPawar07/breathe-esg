import { useMemo } from 'react'

import PageContainer from '../components/layout/PageContainer'

import AnalystTable from '../components/dashboard/AnalystTable'

import Loader from '../components/shared/Loader'

import EmptyState from '../components/dashboard/EmptyState'

import useDashboard from '../hooks/useDashboard'


function FailedRows() {

  const {

    records,

    loading,

    reload

  } = useDashboard()


  const failedRecords = useMemo(() => {

    return records.filter((record) =>

      record.status === 'flagged'
    )

  }, [records])


  if (loading) {

    return (
      <Loader text="Loading failed rows..." />
    )
  }

  return (

    <PageContainer

      title="Failed / Flagged Rows"

      subtitle="Suspicious or invalid emission records"
    >

      {failedRecords.length === 0 ? (

        <EmptyState

          title="No failed rows"

          subtitle="No suspicious emissions detected"
        />

      ) : (

        <AnalystTable

          records={failedRecords}

          reloadDashboard={reload}
        />
      )}

    </PageContainer>
  )
}

export default FailedRows
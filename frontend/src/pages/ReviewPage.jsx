import { useMemo } from 'react'

import PageContainer from '../components/layout/PageContainer'

import ReviewTable from '../components/review/ReviewTable'

import Loader from '../components/shared/Loader'

import EmptyState from '../components/dashboard/EmptyState'

import useDashboard from '../hooks/useDashboard'


function ReviewPage() {

  const {

    records,

    loading,

    reload

  } = useDashboard()


  const pendingRecords = useMemo(() => {

    return records.filter((record) =>

      record.status === 'pending' ||

      record.status === 'flagged'
    )

  }, [records])


  if (loading) {

    return (
      <Loader text="Loading review queue..." />
    )
  }

  return (

    <PageContainer

      title="Review Queue"

      subtitle="Approve, flag or lock emission records"
    >

      {pendingRecords.length === 0 ? (

        <EmptyState

          title="No pending reviews"

          subtitle="All records are already reviewed"
        />

      ) : (

        <ReviewTable

          records={pendingRecords}

          reloadDashboard={reload}
        />
      )}

    </PageContainer>
  )
}

export default ReviewPage
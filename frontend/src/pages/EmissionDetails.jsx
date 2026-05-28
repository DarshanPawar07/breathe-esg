import { useEffect, useState } from 'react'

import {

  useNavigate,

  useParams

} from 'react-router-dom'

import PageContainer from '../components/layout/PageContainer'

import ReviewModal from '../components/review/ReviewModal'

import Loader from '../components/shared/Loader'

import EmptyState from '../components/dashboard/EmptyState'

import {

  fetchEmissionRecords

} from '../api/api'


function EmissionDetails() {

  const { id } = useParams()

  const navigate = useNavigate()

  const [record, setRecord] =
    useState(null)

  const [loading, setLoading] =
    useState(true)


  // ─────────────────────────────
  // LOAD RECORD
  // ─────────────────────────────

  useEffect(() => {

    const loadRecord = async () => {

      try {

        setLoading(true)

        const records =
          await fetchEmissionRecords()

        const selectedRecord =
          records.find((item) =>

            String(item.id) ===
            String(id)
          )

        setRecord(selectedRecord)

      } catch (error) {

        console.error(
          'Failed to load emission record',
          error
        )

      } finally {

        setLoading(false)
      }
    }

    loadRecord()

  }, [id])


  // ─────────────────────────────
  // LOADING
  // ─────────────────────────────

  if (loading) {

    return (

      <Loader text="Loading emission details..." />
    )
  }


  // ─────────────────────────────
  // NOT FOUND
  // ─────────────────────────────

  if (!record) {

    return (

      <PageContainer

        title="Emission Record"

        subtitle="Record details"
      >

        <EmptyState

          title="Record not found"

          subtitle="This emission record does not exist"
        />

      </PageContainer>
    )
  }


  // ─────────────────────────────
  // PAGE
  // ─────────────────────────────

  return (

    <PageContainer

      title="Emission Record"

      subtitle="Detailed ESG emission record"
    >

      <ReviewModal

        record={record}

        onClose={() =>
          navigate('/')
        }
      />

    </PageContainer>
  )
}

export default EmissionDetails
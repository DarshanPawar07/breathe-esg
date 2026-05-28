import { useState } from 'react'

import {

  approveRecord,

  flagRecord,

  lockRecord

} from '../api/api'


const useReviewActions = () => {

  const [loading, setLoading] =
    useState(false)


  // ─────────────────────────────
  // APPROVE
  // ─────────────────────────────

  const approve = async (
    recordId
  ) => {

    try {

      setLoading(true)

      return await approveRecord(
        recordId
      )

    } finally {

      setLoading(false)
    }
  }


  // ─────────────────────────────
  // FLAG
  // ─────────────────────────────

  const flag = async (
    recordId,
    reason
  ) => {

    try {

      setLoading(true)

      return await flagRecord(
        recordId,
        reason
      )

    } finally {

      setLoading(false)
    }
  }


  // ─────────────────────────────
  // LOCK
  // ─────────────────────────────

  const lock = async (
    recordId
  ) => {

    try {

      setLoading(true)

      return await lockRecord(
        recordId
      )

    } finally {

      setLoading(false)
    }
  }


  return {

    loading,

    approve,

    flag,

    lock,
  }
}

export default useReviewActions
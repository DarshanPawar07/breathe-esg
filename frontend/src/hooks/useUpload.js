import { useState } from 'react'

import api from '../api/api'


function useUpload() {

  const [uploading, setUploading] =
    useState(false)

  const [uploadResult, setUploadResult] =
    useState({

      created: 0,

      failed: 0,

      flagged: 0,
    })


  // ─────────────────────────────
  // UPLOAD FILE
  // ─────────────────────────────

  const uploadFile = async (

    sourceType,

    file,

    tenantId = 1
  ) => {

    try {

      setUploading(true)

      const formData =
        new FormData()

      formData.append(
        'file',
        file
      )

      formData.append(
        'tenant_id',
        tenantId
      )


      // API ENDPOINT

      let endpoint = ''

      if (sourceType === 'SAP') {

        endpoint =
          '/upload/sap/'
      }

      else if (
        sourceType === 'Utility'
      ) {

        endpoint =
          '/upload/utility/'
      }

      else {

        endpoint =
          '/upload/travel/'
      }


      // REQUEST

      const response =
        await api.post(

          endpoint,

          formData,

          {

            headers: {

              'Content-Type':
                'multipart/form-data',
            },
          }
        )


      // RESPONSE DATA

      const result =
        response.data


      // UPDATE STATE

      setUploadResult({

        created:
          result.created || 0,

        failed:
          result.failed || 0,

        flagged:
          result.flagged || 0,
      })


      return result

    } catch (error) {

      console.error(error)

      throw error

    } finally {

      setUploading(false)
    }
  }


  return {

    uploading,

    uploadResult,

    uploadFile,
  }
}

export default useUpload
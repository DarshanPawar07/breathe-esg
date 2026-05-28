import { useState } from 'react'

import axios from 'axios'


const API_BASE =
  'http://127.0.0.1:8000/api'


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


      // API URL

      let endpoint = ''

      if (sourceType === 'SAP') {

        endpoint =
          `${API_BASE}/upload/sap/`
      }

      else if (
        sourceType === 'Utility'
      ) {

        endpoint =
          `${API_BASE}/upload/utility/`
      }

      else {

        endpoint =
          `${API_BASE}/upload/travel/`
      }


      // REQUEST

      const response =
        await axios.post(

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
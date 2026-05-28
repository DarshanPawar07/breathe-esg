import { useState } from 'react'

import UploadDropzone from './UploadDropzone'
import UploadProgress from './UploadProgress'

import useUpload from '../../hooks/useUpload'


function UploadCard() {

  // ─────────────────────────────
  // STATE
  // ─────────────────────────────

  const [sourceType, setSourceType] =
    useState('SAP')

  const [file, setFile] =
    useState(null)

  const [successMessage, setSuccessMessage] =
    useState('')

  const [errorMessage, setErrorMessage] =
    useState('')


  // ─────────────────────────────
  // HOOK
  // ─────────────────────────────

  const {

    uploading,

    uploadResult,

    uploadFile

  } = useUpload()


  // ─────────────────────────────
  // HANDLE UPLOAD
  // ─────────────────────────────

  const handleUpload = async () => {

    try {

      setSuccessMessage('')

      setErrorMessage('')

      if (!file) {

        setErrorMessage(
          'Please select a CSV file'
        )

        return
      }

      // ONLY CSV

      if (
        !file.name.endsWith('.csv')
      ) {

        setErrorMessage(
          'Only CSV files are supported'
        )

        return
      }

      // Upload API

      const response =
        await uploadFile(

          sourceType,

          file,

          1 // tenant id
        )

      // Success

      setSuccessMessage(

        `${sourceType} file uploaded successfully`
      )

      console.log(
        'Upload Response:',
        response
      )

      // Reset file

      setFile(null)

    } catch (error) {

      console.error(error)

      setErrorMessage(

        error?.response?.data?.message ||

        'Upload failed'
      )
    }
  }


  // ─────────────────────────────
  // UI
  // ─────────────────────────────

  return (

    <div className="upload-card">

      {/* Header */}

      <div
        style={{
          marginBottom: '24px',
        }}
      >

        <h2
          style={{
            marginBottom: '8px',
          }}
        >
          ESG File Upload
        </h2>

        <p
          style={{
            color: '#8d8d8d',
          }}
        >
          Upload SAP, Utility or Travel CSV files
        </p>

      </div>


      {/* Source Type */}

      <div className="form-group">

        <label>
          Source Type
        </label>

        <select

          className="form-control"

          value={sourceType}

          onChange={(e) =>

            setSourceType(
              e.target.value
            )
          }
        >

          <option value="SAP">
            SAP
          </option>

          <option value="Utility">
            Utility
          </option>

          <option value="Travel">
            Travel
          </option>

        </select>

      </div>


      {/* Upload Dropzone */}

      <UploadDropzone

        file={file}

        setFile={setFile}
      />


      {/* Messages */}

      {successMessage && (

        <div
          style={{

            marginTop: '18px',

            padding: '14px',

            borderRadius: '12px',

            background: '#122617',

            border:
              '1px solid #2f6b3c',

            color: '#7be495',
          }}
        >

          {successMessage}

        </div>
      )}


      {errorMessage && (

        <div
          style={{

            marginTop: '18px',

            padding: '14px',

            borderRadius: '12px',

            background: '#331616',

            border:
              '1px solid #7c2e2e',

            color: '#ff9c9c',
          }}
        >

          {errorMessage}

        </div>
      )}


      {/* Upload Button */}

      <div
        style={{
          marginTop: '24px',
        }}
      >

        <button

          className="primary-button"

          onClick={handleUpload}

          disabled={uploading}
        >

          {

            uploading
              ? 'Uploading...'
              : `Upload ${sourceType} File`
          }

        </button>

      </div>


      {/* Upload Progress */}

      <UploadProgress

        uploading={uploading}

        uploadResult={uploadResult}
      />

    </div>
  )
}

export default UploadCard
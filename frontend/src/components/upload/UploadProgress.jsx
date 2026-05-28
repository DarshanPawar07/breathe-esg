function UploadProgress({

  uploading,

  uploadResult,
}) {

  // ─────────────────────────────
  // LOADING
  // ─────────────────────────────

  if (uploading) {

    return (

      <div
        className="upload-progress"
      >

        <div
          style={{
            marginBottom: '12px',
          }}
        >
          Uploading file...
        </div>

        <div
          style={{

            height: '10px',

            background: '#1d1d1d',

            borderRadius: '999px',

            overflow: 'hidden',
          }}
        >

          <div
            style={{

              width: '100%',

              height: '100%',

              background: 'white',

              animation:
                'pulse 1.5s infinite',
            }}
          />

        </div>

      </div>
    )
  }


  // ─────────────────────────────
  // NO DATA YET
  // ─────────────────────────────

  const hasData =

    uploadResult &&
    (

      uploadResult.created > 0 ||

      uploadResult.failed > 0 ||

      uploadResult.flagged > 0
    )


  if (!hasData) {

    return null
  }


  // ─────────────────────────────
  // SUMMARY
  // ─────────────────────────────

  return (

    <div
      className="upload-summary"
    >

      <h3
        style={{
          marginBottom: '18px',
        }}
      >
        Upload Summary
      </h3>

      <div
        style={{

          display: 'grid',

          gridTemplateColumns:
            'repeat(3, 1fr)',

          gap: '16px',
        }}
      >

        {/* Created */}

        <div
          className="summary-box"
        >

          <div
            className="summary-value"
          >
            {
              uploadResult.created
            }
          </div>

          <div
            className="summary-label"
          >
            Created
          </div>

        </div>


        {/* Failed */}

        <div
          className="summary-box"
        >

          <div
            className="summary-value"
          >
            {
              uploadResult.failed
            }
          </div>

          <div
            className="summary-label"
          >
            Failed
          </div>

        </div>


        {/* Flagged */}

        <div
          className="summary-box"
        >

          <div
            className="summary-value"
          >
            {
              uploadResult.flagged
            }
          </div>

          <div
            className="summary-label"
          >
            Flagged
          </div>

        </div>

      </div>

    </div>
  )
}

export default UploadProgress
import { useEffect, useState } from 'react'

import axios from 'axios'


function UploadHistory() {

  const [uploads, setUploads] =
    useState([])


  // ─────────────────────────────
  // FETCH HISTORY
  // ─────────────────────────────

  useEffect(() => {

    fetchHistory()

  }, [])


  const fetchHistory = async () => {

    try {

      const response =
        await axios.get(

          '/upload-history/'
        )

      setUploads(response.data)

    } catch (error) {

      console.error(error)
    }
  }


  return (

    <div className="history-card">

      <h3
        style={{
          marginBottom: '20px',
        }}
      >
        Upload History
      </h3>

      <table className="data-table">

        <thead>

          <tr>

            <th>File</th>

            <th>Source</th>

            <th>Uploaded At</th>

            <th>Status</th>

          </tr>

        </thead>

        <tbody>

          {

            uploads.length === 0

            ? (

              <tr>

                <td
                  colSpan="4"
                  style={{
                    textAlign: 'center',
                  }}
                >
                  No uploads yet
                </td>

              </tr>
            )

            : (

              uploads.map((item) => (

                <tr key={item.id}>

                  <td>
                    {item.file_name}
                  </td>

                  <td>
                    {item.source_type}
                  </td>

                  <td>

                    {

                      new Date(
                        item.created_at
                      ).toLocaleString()
                    }

                  </td>

                  <td>
                    {item.status}
                  </td>

                </tr>
              ))
            )
          }

        </tbody>

      </table>

    </div>
  )
}

export default UploadHistory
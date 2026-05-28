import {

  formatDate

} from '../../utils/formatDate'

import {

  formatCO2

} from '../../utils/formatNumber'

import {

  statusColors

} from '../../utils/statusColors'

import useReviewActions from '../../hooks/useReviewActions'


function AnalystTable({

  records = [],

  reloadDashboard

}) {

  const {

    approve,

    flag,

    lock

  } = useReviewActions()


  const handleApprove =
    async (recordId) => {

      await approve(recordId)

      reloadDashboard()
    }


  const handleFlag =
    async (recordId) => {

      await flag(recordId)

      reloadDashboard()
    }


  const handleLock =
    async (recordId) => {

      await lock(recordId)

      reloadDashboard()
    }


  return (

    <div className="table-wrapper">

      <table className="data-table">

        <thead>

          <tr>

            <th>
              Source
            </th>

            <th>
              Date
            </th>

            <th>
              Activity
            </th>

            <th>
              Facility
            </th>

            <th>
              Original
            </th>

            <th>
              Normalized
            </th>

            <th>
              Scope
            </th>

            <th>
              CO₂e kg
            </th>

            <th>
              Status
            </th>

            <th>
              Actions
            </th>

          </tr>

        </thead>

        <tbody>

          {records.map((record) => {

            const statusStyle =
              statusColors[
                record.status
              ]

            return (

              <tr key={record.id}>

                <td>
                  {record.source_type}
                </td>

                <td>
                  {
                    formatDate(
                      record.activity_date
                    )
                  }
                </td>

                <td>
                  {
                    record.activity_type
                  }
                </td>

                <td>
                  {
                    record.facility_name ||
                    '-'
                  }
                </td>

                <td>

                  {
                    record.original_quantity
                  }

                  {' '}

                  {
                    record.original_unit
                  }

                </td>

                <td>

                  {
                    record.normalized_quantity
                  }

                  {' '}

                  {
                    record.normalized_unit
                  }

                </td>

                <td>
                  {record.scope}
                </td>

                <td>

                  {
                    formatCO2(
                      record.co2e_kg
                    )
                  }

                </td>

                <td>

                  <span

                    className="status-badge"

                    style={{

                      background:
                        statusStyle.background,

                      color:
                        statusStyle.color,

                      border:
                        `1px solid ${statusStyle.border}`,
                    }}
                  >

                    {record.status}

                  </span>

                </td>

                <td>

                  <div className="table-actions">

                    <button

                      className="action-button approve"

                      onClick={() =>
                        handleApprove(
                          record.id
                        )
                      }
                    >

                      Approve

                    </button>

                    <button

                      className="action-button flag"

                      onClick={() =>
                        handleFlag(
                          record.id
                        )
                      }
                    >

                      Flag

                    </button>

                    <button

                      className="action-button lock"

                      onClick={() =>
                        handleLock(
                          record.id
                        )
                      }
                    >

                      Lock

                    </button>

                  </div>

                </td>

              </tr>
            )
          })}

        </tbody>

      </table>

    </div>
  )
}

export default AnalystTable
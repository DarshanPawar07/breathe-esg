import {

  formatDate

} from '../../utils/formatDate'

import {

  formatCO2

} from '../../utils/formatNumber'


function ReviewModal({

  record,

  onClose

}) {

  if (!record) {

    return null
  }

  return (

    <div
      style={{
        position: 'fixed',

        inset: 0,

        background:
          'rgba(0,0,0,0.75)',

        display: 'flex',

        alignItems: 'center',

        justifyContent: 'center',

        zIndex: 999,
      }}
    >

      <div
        style={{
          width: '700px',

          background: '#121212',

          border:
            '1px solid #2b2b2b',

          borderRadius: '18px',

          padding: '28px',
        }}
      >

        <div
          style={{
            display: 'flex',

            justifyContent:
              'space-between',

            marginBottom: '24px',
          }}
        >

          <h2>
            Emission Record Detail
          </h2>

          <button
            onClick={onClose}
          >
            Close
          </button>

        </div>

        <div
          style={{
            display: 'grid',

            gridTemplateColumns:
              '1fr 1fr',

            gap: '18px',
          }}
        >

          <div>

            <p>
              <strong>
                Source:
              </strong>
              {' '}
              {record.source_type}
            </p>

            <p>
              <strong>
                Activity:
              </strong>
              {' '}
              {record.activity_type}
            </p>

            <p>
              <strong>
                Scope:
              </strong>
              {' '}
              {record.scope}
            </p>

            <p>
              <strong>
                Date:
              </strong>
              {' '}
              {
                formatDate(
                  record.activity_date
                )
              }
            </p>

          </div>

          <div>

            <p>
              <strong>
                Original:
              </strong>
              {' '}
              {
                record.original_quantity
              }
              {' '}
              {
                record.original_unit
              }
            </p>

            <p>
              <strong>
                Normalized:
              </strong>
              {' '}
              {
                record.normalized_quantity
              }
              {' '}
              {
                record.normalized_unit
              }
            </p>

            <p>
              <strong>
                CO₂e:
              </strong>
              {' '}
              {
                formatCO2(
                  record.co2e_kg
                )
              }
            </p>

            <p>
              <strong>
                Status:
              </strong>
              {' '}
              {record.status}
            </p>

          </div>

        </div>

      </div>

    </div>
  )
}

export default ReviewModal
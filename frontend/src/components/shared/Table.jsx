function Table({

  columns = [],

  data = [],

  renderRow,

}) {

  return (

    <div className="table-wrapper">

      <table className="data-table">

        <thead>

          <tr>

            {columns.map((column) => (

              <th key={column}>

                {column}

              </th>
            ))}

          </tr>

        </thead>

        <tbody>

          {data.length === 0 && (

            <tr>

              <td
                colSpan={
                  columns.length
                }
                style={{
                  textAlign: 'center',
                }}
              >

                No records found

              </td>

            </tr>
          )}

          {data.map((item) =>

            renderRow(item)
          )}

        </tbody>

      </table>

    </div>
  )
}

export default Table
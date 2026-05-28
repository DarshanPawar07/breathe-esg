function QuickStats({

  records = []

}) {

  const totalCO2 = records.reduce(

    (acc, item) => {

      return (
        acc +
        Number(item.co2e_kg || 0)
      )
    },

    0
  )

  return (

    <div
      style={{
        marginBottom: '24px',

        display: 'flex',

        gap: '18px',

        flexWrap: 'wrap',
      }}
    >

      <div className="kpi-card">

        <h3>
          Total CO₂e
        </h3>

        <h2>
          {
            totalCO2.toLocaleString()
          } kg
        </h2>

      </div>

      <div className="kpi-card">

        <h3>
          Records Loaded
        </h3>

        <h2>
          {records.length}
        </h2>

      </div>

    </div>
  )
}

export default QuickStats
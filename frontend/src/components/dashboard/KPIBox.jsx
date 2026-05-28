function KPIBox({

  title,

  value

}) {

  return (

    <div className="kpi-card">

      <h3>
        {title}
      </h3>

      <h2>
        {value}
      </h2>

    </div>
  )
}

export default KPIBox
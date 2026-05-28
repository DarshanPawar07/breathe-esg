import KPIBox from './KPIBox'


function KPISection({

  summary

}) {

  if (!summary) {

    return null
  }

  return (

    <div className="kpi-grid">

      <KPIBox
        title="Total Rows"
        value={
          summary.total_rows
        }
      />

      <KPIBox
        title="Pending"
        value={
          summary.pending
        }
      />

      <KPIBox
        title="Approved"
        value={
          summary.approved
        }
      />

      <KPIBox
        title="Failed / Flagged"
        value={
          summary.flagged
        }
      />

      <KPIBox
        title="Scope 1"
        value={
          summary.scope_1_total
        }
      />

      <KPIBox
        title="Scope 2"
        value={
          summary.scope_2_total
        }
      />

      <KPIBox
        title="Scope 3"
        value={
          summary.scope_3_total
        }
      />

    </div>
  )
}

export default KPISection
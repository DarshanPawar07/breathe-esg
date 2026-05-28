import AnalystTable from '../dashboard/AnalystTable'


function ReviewTable({

  records,

  reloadDashboard

}) {

  return (

    <AnalystTable

      records={records}

      reloadDashboard={
        reloadDashboard
      }
    />
  )
}

export default ReviewTable
import {

  statusColors

} from '../../utils/statusColors'


function StatusBadge({

  status

}) {

  const style =
    statusColors[status]

  return (

    <span

      className="status-badge"

      style={{

        background:
          style?.background,

        color:
          style?.color,

        border:
          `1px solid ${style?.border}`,
      }}
    >

      {status}

    </span>
  )
}

export default StatusBadge
import emptyState from '../../assets/empty-state.svg'


function EmptyState({

  title = 'No records found',

  subtitle = (
    'Try changing filters or uploading new files'
  )

}) {

  return (

    <div
      style={{
        padding: '60px 20px',

        textAlign: 'center',
      }}
    >

      <img
        src={emptyState}
        alt="Empty"
        style={{
          width: '220px',
          marginBottom: '20px',
        }}
      />

      <h2
        style={{
          marginBottom: '10px',
        }}
      >
        {title}
      </h2>

      <p
        style={{
          color: '#8d8d8d',
        }}
      >
        {subtitle}
      </p>

    </div>
  )
}

export default EmptyState
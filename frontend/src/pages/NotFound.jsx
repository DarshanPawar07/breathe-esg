import { Link } from 'react-router-dom'


function NotFound() {

  return (

    <div
      style={{

        minHeight: '100vh',

        display: 'flex',

        flexDirection: 'column',

        alignItems: 'center',

        justifyContent: 'center',

        background: '#0b0b0b',

        color: 'white',
      }}
    >

      <h1
        style={{
          fontSize: '72px',
          marginBottom: '16px',
        }}
      >
        404
      </h1>

      <p
        style={{
          color: '#8d8d8d',
          marginBottom: '28px',
        }}
      >
        Page not found
      </p>

      <Link
        to="/"
        className="primary-button"
      >
        Go to Dashboard
      </Link>

    </div>
  )
}

export default NotFound
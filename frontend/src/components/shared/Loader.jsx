function Loader({

  text = 'Loading...'

}) {

  return (

    <div
      style={{

        display: 'flex',

        flexDirection: 'column',

        alignItems: 'center',

        justifyContent: 'center',

        padding: '60px',
      }}
    >

      <div
        style={{

          width: '46px',

          height: '46px',

          border:
            '4px solid #2d2d2d',

          borderTop:
            '4px solid white',

          borderRadius: '50%',

          animation:
            'spin 1s linear infinite',

          marginBottom: '18px',
        }}
      />

      <p
        style={{
          color: '#9d9d9d',
        }}
      >
        {text}
      </p>

      <style>

        {`

          @keyframes spin {

            from {
              transform: rotate(0deg);
            }

            to {
              transform: rotate(360deg);
            }
          }
        `}

      </style>

    </div>
  )
}

export default Loader
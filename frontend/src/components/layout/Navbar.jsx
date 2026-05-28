function Navbar() {

  return (

    <header className="navbar">

      {/* Left */}

      <div>

        <h2
          style={{
            fontSize: '20px',
            marginBottom: '4px',
          }}
        >
          Emission Records Dashboard
        </h2>

        <p
          style={{
            color: '#8e8e8e',
            fontSize: '13px',
          }}
        >
          Enterprise ESG analyst workflow
        </p>

      </div>

      {/* Right */}

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
        }}
      >

        <div
          style={{
            background: '#161616',

            border: '1px solid #2a2a2a',

            padding: '10px 14px',

            borderRadius: '12px',

            color: '#d2d2d2',
          }}
        >
          Tata Motors
        </div>

      </div>

    </header>
  )
}

export default Navbar
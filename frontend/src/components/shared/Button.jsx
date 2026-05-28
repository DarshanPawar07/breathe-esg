function Button({

  children,

  onClick,

  type = 'button',

  variant = 'primary',

  disabled = false,

  fullWidth = false,

}) {

  const styles = {

    primary: {

      background: 'white',

      color: 'black',
    },

    secondary: {

      background: '#181818',

      color: 'white',

      border: '1px solid #2c2c2c',
    },

    danger: {

      background: '#3a1717',

      color: '#ff9c9c',
    },
  }

  return (

    <button

      type={type}

      onClick={onClick}

      disabled={disabled}

      style={{

        padding: '12px 18px',

        borderRadius: '12px',

        fontWeight: '600',

        fontSize: '14px',

        width: fullWidth
          ? '100%'
          : 'auto',

        opacity: disabled
          ? 0.6
          : 1,

        transition: '0.2s ease',

        ...styles[variant],
      }}
    >

      {children}

    </button>
  )
}

export default Button
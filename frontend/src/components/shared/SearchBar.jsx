function SearchBar({

  value,

  onChange,

  placeholder = 'Search...'

}) {

  return (

    <input

      type="text"

      value={value}

      onChange={(e) =>
        onChange(
          e.target.value
        )
      }

      placeholder={placeholder}

      style={{

        width: '100%',

        maxWidth: '340px',

        background: '#151515',

        border:
          '1px solid #2a2a2a',

        color: 'white',

        padding: '14px 16px',

        borderRadius: '12px',

        fontSize: '14px',
      }}
    />
  )
}

export default SearchBar
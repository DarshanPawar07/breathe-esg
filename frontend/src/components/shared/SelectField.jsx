function SelectField({

  label,

  value,

  onChange,

  options = [],

  placeholder = 'Select option'

}) {

  return (

    <div className="form-group">

      {label && (

        <label>
          {label}
        </label>
      )}

      <select

        className="form-control"

        value={value}

        onChange={(e) =>
          onChange(
            e.target.value
          )
        }
      >

        <option value="">
          {placeholder}
        </option>

        {options.map((option) => (

          <option

            key={option.value}

            value={option.value}
          >

            {option.label}

          </option>
        ))}

      </select>

    </div>
  )
}

export default SelectField
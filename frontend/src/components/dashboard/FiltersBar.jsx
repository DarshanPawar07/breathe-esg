function FiltersBar({

  filters,

  setFilters,

  facilities = []

}) {

  const handleChange = (
    key,
    value
  ) => {

    setFilters((prev) => ({

      ...prev,

      [key]: value,
    }))
  }

  return (

    <div className="filters-bar">

      {/* Facility */}

      <select

        value={filters.facility}

        onChange={(e) =>
          handleChange(
            'facility',
            e.target.value
          )
        }
      >

        <option value="">
          All Facilities
        </option>

        {facilities.map(
          (facility) => (

            <option
              key={facility.id}
              value={facility.id}
            >

              {
                facility.facility_code
              }
              {' '}
              {
                facility.facility_name
              }

            </option>
          )
        )}

      </select>

      {/* Status */}

      <select

        value={filters.status}

        onChange={(e) =>
          handleChange(
            'status',
            e.target.value
          )
        }
      >

        <option value="">
          All Status
        </option>

        <option value="pending">
          Pending
        </option>

        <option value="approved">
          Approved
        </option>

        <option value="flagged">
          Flagged
        </option>

        <option value="locked">
          Locked
        </option>

      </select>

      {/* Scope */}

      <select

        value={filters.scope}

        onChange={(e) =>
          handleChange(
            'scope',
            e.target.value
          )
        }
      >

        <option value="">
          All Scopes
        </option>

        <option value="Scope 1">
          Scope 1
        </option>

        <option value="Scope 2">
          Scope 2
        </option>

        <option value="Scope 3">
          Scope 3
        </option>

      </select>

    </div>
  )
}

export default FiltersBar
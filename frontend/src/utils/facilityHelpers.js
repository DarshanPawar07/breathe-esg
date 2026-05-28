export const getFacilityDisplay = (
  facility
) => {

  if (!facility) {

    return 'Unknown Facility'
  }

  const code = (
    facility.facility_code || ''
  )

  const name = (
    facility.facility_name || ''
  )

  return `${code} ${name}`
}


export const groupByFacility = (
  records = []
) => {

  const grouped = {}

  records.forEach((record) => {

    const facilityName = (
      record.facility_name ||
      'Unknown Facility'
    )

    if (!grouped[facilityName]) {

      grouped[facilityName] = []
    }

    grouped[facilityName].push(
      record
    )
  })

  return grouped
}
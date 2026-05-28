export const formatNumber = (
  value
) => {

  if (
    value === null ||
    value === undefined
  ) {

    return '0'
  }

  return Number(value)
    .toLocaleString(
      'en-IN',
      {

        maximumFractionDigits: 2,
      }
    )
}


export const formatCO2 = (
  value
) => {

  return (
    `${formatNumber(value)} kg`
  )
}
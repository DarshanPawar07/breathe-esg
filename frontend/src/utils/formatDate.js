export const formatDate = (
  dateValue
) => {

  if (!dateValue) {

    return '-'
  }

  try {

    const date = new Date(
      dateValue
    )

    return date.toLocaleDateString(
      'en-IN',
      {

        year: 'numeric',

        month: 'short',

        day: 'numeric',
      }
    )

  } catch (error) {

    return dateValue
  }
}
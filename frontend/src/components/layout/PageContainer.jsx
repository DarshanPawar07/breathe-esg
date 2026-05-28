function PageContainer({

  title,

  subtitle,

  children

}) {

  return (

    <div className="dashboard-page">

      {/* Header */}

      <div
        className="dashboard-header"
      >

        <div
          className="dashboard-title"
        >

          <h1>
            {title}
          </h1>

          <p>
            {subtitle}
          </p>

        </div>

      </div>

      {/* Content */}

      {children}

    </div>
  )
}

export default PageContainer
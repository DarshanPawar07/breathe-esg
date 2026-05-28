function StatusTabs({

  activeTab,

  setActiveTab

}) {

  const tabs = [

    'all',

    'pending',

    'approved',

    'flagged',

    'locked',
  ]

  return (

    <div className="status-tabs">

      {tabs.map((tab) => (

        <button

          key={tab}

          className={

            activeTab === tab
              ? 'status-tab active'
              : 'status-tab'
          }

          onClick={() =>
            setActiveTab(tab)
          }
        >

          {tab}

        </button>
      ))}

    </div>
  )
}

export default StatusTabs
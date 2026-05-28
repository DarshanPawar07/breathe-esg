import { NavLink } from 'react-router-dom'

import logo from '../../assets/logo.svg'

import sidebarLinks from '../../data/sidebarLinks'


function Sidebar() {

  return (

    <aside className="sidebar">

      <div className="sidebar-top">

        {/* Logo */}

        <img

          src={logo}

          alt="Breathe ESG"

          style={{
            width: '160px',
          }}
        />

        {/* Navigation */}

        <div className="sidebar-links">

          {sidebarLinks.map((item) => {

            const Icon = item.icon

            return (

              <NavLink

                key={item.path}

                to={item.path}

                className={({ isActive }) =>

                  isActive
                    ? 'sidebar-link active'
                    : 'sidebar-link'
                }
              >

                <div
                  style={{
                    display: 'flex',

                    alignItems: 'center',

                    gap: '12px',
                  }}
                >

                  <Icon />

                  <span>
                    {item.label}
                  </span>

                </div>

              </NavLink>
            )
          })}

        </div>

      </div>

      {/* Analyst */}

      <div
        style={{

          borderTop:
            '1px solid #232323',

          paddingTop: '20px',
        }}
      >

        <div
          style={{

            display: 'flex',

            alignItems: 'center',

            gap: '14px',
          }}
        >

          <div
            style={{

              width: '42px',

              height: '42px',

              borderRadius: '50%',

              background: 'white',

              color: 'black',

              display: 'flex',

              alignItems: 'center',

              justifyContent: 'center',

              fontWeight: '700',
            }}
          >
            S
          </div>

          <div>

            <div
              style={{
                fontWeight: '600',
              }}
            >
              Sarah
            </div>

            <div
              style={{

                color: '#8c8c8c',

                fontSize: '13px',
              }}
            >
              ESG Analyst
            </div>

          </div>

        </div>

      </div>

    </aside>
  )
}

export default Sidebar
import {

  FiHome,

  FiUploadCloud,

  FiAlertTriangle,

  FiCheckSquare,

  FiFileText

} from 'react-icons/fi'


const sidebarLinks = [

  {
    label: 'Dashboard',

    path: '/',

    icon: FiHome,
  },

  {
    label: 'Upload Center',

    path: '/upload',

    icon: FiUploadCloud,
  },

  {
    label: 'Review Queue',

    path: '/review',

    icon: FiCheckSquare,
  },

  {
    label: 'Failed Rows',

    path: '/failed',

    icon: FiAlertTriangle,
  },

  {
    label: 'Emissions',

    path: '/emissions/1',

    icon: FiFileText,
  },
]

export default sidebarLinks
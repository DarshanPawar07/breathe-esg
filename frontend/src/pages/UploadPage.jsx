import PageContainer from '../components/layout/PageContainer'

import UploadCard from '../components/upload/UploadCard'

import UploadHistory from '../components/upload/UploadHistory'


function UploadPage() {

  return (

    <PageContainer

      title="Upload Center"

      subtitle="Upload SAP, utility and travel files"
    >

      <UploadCard />

      <UploadHistory
        uploads={[]}
      />

    </PageContainer>
  )
}

export default UploadPage
import { FiUploadCloud } from 'react-icons/fi'


function UploadDropzone({

  file,

  setFile

}) {

  const handleFileChange = (
    event
  ) => {

    const selectedFile =
      event.target.files[0]

    if (selectedFile) {

      setFile(selectedFile)
    }
  }

  return (

    <div className="upload-dropzone">

      <FiUploadCloud
        size={42}
        style={{
          marginBottom: '14px',
        }}
      />

      <h3
        style={{
          marginBottom: '10px',
        }}
      >
        Upload ESG Source File
      </h3>

      <p
        style={{
          marginBottom: '18px',
          color: '#8c8c8c',
        }}
      >
        Drag and drop CSV file or browse manually
      </p>

      <input

        type="file"

        accept=".csv"

        onChange={handleFileChange}
      />

      {file && (

        <div
          style={{
            marginTop: '16px',
            color: '#d0d0d0',
          }}
        >

          Selected:
          {' '}
          {file.name}

        </div>
      )}

    </div>
  )
}

export default UploadDropzone
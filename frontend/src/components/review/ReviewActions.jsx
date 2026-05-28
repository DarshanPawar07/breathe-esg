function ReviewActions({

  onApprove,

  onFlag,

  onLock

}) {

  return (

    <div className="table-actions">

      <button

        className="action-button approve"

        onClick={onApprove}
      >

        Approve

      </button>

      <button

        className="action-button flag"

        onClick={onFlag}
      >

        Flag

      </button>

      <button

        className="action-button lock"

        onClick={onLock}
      >

        Lock

      </button>

    </div>
  )
}

export default ReviewActions
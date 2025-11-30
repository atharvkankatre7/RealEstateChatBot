import { useState } from 'react'

function ChatInput({ onSend, disabled }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim() && !disabled) {
      onSend(query)
      setQuery('')
    }
  }

  return (
    <div className="card shadow-sm">
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <input
              type="text"
              className="form-control"
              placeholder="Ask something... (e.g., 'Analyze Wakad' or 'Compare Aundh and Akurdi')"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              disabled={disabled}
            />
            <button
              className="btn btn-primary"
              type="submit"
              disabled={disabled || !query.trim()}
            >
              {disabled ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Sending...
                </>
              ) : (
                'Send'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ChatInput


import ChartResult from './ChartResult'
import TableResult from './TableResult'
import { downloadData } from '../api'

function ChatMessage({ message }) {
  const isUser = message.type === 'user'

  const handleDownload = async (format) => {
    if (!message.tableData || message.tableData.length === 0) {
      alert('No data available to download')
      return
    }

    try {
      await downloadData(message.tableData, format)
    } catch (error) {
      alert(`Error downloading data: ${error.message}`)
    }
  }

  return (
    <div className={`mb-4 ${isUser ? 'text-end' : ''}`}>
      <div className={`d-inline-block ${isUser ? 'bg-primary text-white' : 'bg-light'} rounded p-3`} style={{ maxWidth: '80%' }}>
        <div className="d-flex justify-content-between align-items-center mb-2">
          <div className="fw-bold">
            {isUser ? 'You' : '🤖 Bot'}
          </div>
          {!isUser && message.tableData && message.tableData.length > 0 && (
            <div className="btn-group btn-group-sm" role="group">
              <button
                type="button"
                className="btn btn-outline-primary btn-sm"
                onClick={() => handleDownload('csv')}
                title="Download as CSV"
              >
                📥 CSV
              </button>
              <button
                type="button"
                className="btn btn-outline-primary btn-sm"
                onClick={() => handleDownload('json')}
                title="Download as JSON"
              >
                📥 JSON
              </button>
            </div>
          )}
        </div>
        <div style={{ whiteSpace: 'pre-wrap' }}>
          {message.content}
        </div>
      </div>

      {/* Chart and Table for bot messages */}
      {!isUser && message.chartData && (
        <div className="mt-3">
          <ChartResult
            chartData={message.chartData}
            localities={message.localities}
            metrics={message.metrics}
            queryType={message.queryType}
          />
        </div>
      )}

      {!isUser && message.tableData && message.tableData.length > 0 && (
        <div className="mt-3">
          <TableResult data={message.tableData} />
        </div>
      )}
    </div>
  )
}

export default ChatMessage


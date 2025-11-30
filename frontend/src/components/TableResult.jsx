function TableResult({ data }) {
  if (!data || data.length === 0) {
    return null
  }

  // Get all unique keys from the data
  const columns = Object.keys(data[0])

  // Format cell value
  const formatValue = (value) => {
    if (value === null || value === undefined) return '-'
    if (typeof value === 'number') {
      // Format large numbers with commas
      if (value >= 1000) {
        return value.toLocaleString('en-IN')
      }
      // Format decimals to 2 places
      if (value % 1 !== 0) {
        return value.toFixed(2)
      }
      return value.toString()
    }
    return String(value)
  }

  // Format column name
  const formatColumnName = (col) => {
    return col
      .replace(/\s+/g, ' ')
      .replace(/-/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  return (
    <div className="card shadow-sm mb-3">
      <div className="card-header">
        <h6 className="mb-0">📊 Data Table</h6>
      </div>
      <div className="card-body p-0">
        <div style={{ maxHeight: '400px', overflowY: 'auto', overflowX: 'auto' }}>
          <table className="table table-striped table-hover table-sm mb-0">
            <thead className="table-light sticky-top">
              <tr>
                {columns.map((col, idx) => (
                  <th key={idx} scope="col" style={{ whiteSpace: 'nowrap' }}>
                    {formatColumnName(col)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIdx) => (
                <tr key={rowIdx}>
                  {columns.map((col, colIdx) => (
                    <td key={colIdx} style={{ whiteSpace: 'nowrap' }}>
                      {formatValue(row[col])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default TableResult


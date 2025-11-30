import { useEffect, useRef } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line, Bar } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

function ChartResult({ chartData, localities, metrics, queryType }) {
  const chartRef = useRef(null)

  if (!chartData || !chartData.years || chartData.years.length === 0) {
    return null
  }

  const isComparison = queryType === 'comparison' && localities && localities.length > 1

  // Prepare datasets based on metrics and type
  const datasets = []

  if (isComparison) {
    // Comparison mode - multiple localities
    if (metrics.includes('price') && chartData.prices_by_locality) {
      Object.entries(chartData.prices_by_locality).forEach(([locality, prices], index) => {
        datasets.push({
          label: `${locality} - Price (₹/sqft)`,
          data: prices,
          borderColor: `hsl(${index * 60}, 70%, 50%)`,
          backgroundColor: `hsla(${index * 60}, 70%, 50%, 0.1)`,
          tension: 0.4,
          fill: false,
        })
      })
    }

    if (metrics.includes('demand') && chartData.demand_by_locality) {
      Object.entries(chartData.demand_by_locality).forEach(([locality, demands], index) => {
        datasets.push({
          label: `${locality} - Demand (units)`,
          data: demands,
          borderColor: `hsl(${index * 60 + 30}, 70%, 50%)`,
          backgroundColor: `hsla(${index * 60 + 30}, 70%, 50%, 0.1)`,
          tension: 0.4,
          fill: false,
          yAxisID: 'y1',
        })
      })
    }
  } else {
    // Single locality mode
    if (metrics.includes('price') && chartData.prices) {
      datasets.push({
        label: 'Price (₹/sqft)',
        data: chartData.prices,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.4,
        fill: true,
      })
    }

    if (metrics.includes('demand') && chartData.demand) {
      datasets.push({
        label: 'Demand (units sold)',
        data: chartData.demand,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.4,
        fill: true,
        yAxisID: 'y1',
      })
    }
  }

  if (datasets.length === 0) {
    return null
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: isComparison
          ? `Comparison: ${localities.join(' vs ')}`
          : `${localities?.[0] || 'Locality'} Analysis`,
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Year',
        },
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: {
          display: true,
          text: metrics.includes('price') ? 'Price (₹/sqft)' : 'Units',
        },
      },
      ...(metrics.includes('demand') && metrics.includes('price') && {
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: 'Demand (units)',
          },
          grid: {
            drawOnChartArea: false,
          },
        },
      }),
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false,
    },
  }

  const chartDataConfig = {
    labels: chartData.years,
    datasets: datasets,
  }

  return (
    <div className="card shadow-sm mb-3">
      <div className="card-body">
        <div style={{ height: '400px', position: 'relative' }}>
          <Line ref={chartRef} data={chartDataConfig} options={chartOptions} />
        </div>
      </div>
    </div>
  )
}

export default ChartResult


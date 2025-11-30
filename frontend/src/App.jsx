import { useState, useEffect, useRef } from 'react'
import ChatInput from './components/ChatInput'
import ChatMessage from './components/ChatMessage'
import ChartResult from './components/ChartResult'
import TableResult from './components/TableResult'
import { queryAnalysis, getLocalities } from './api'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

function App() {
  const [messages, setMessages] = useState([])
  const [localities, setLocalities] = useState([])
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const chatContainerRef = useRef(null)

  useEffect(() => {
    // Load available localities on mount
    getLocalities()
      .then(data => {
        setLocalities(data.localities || [])
      })
      .catch(err => {
        console.error('Error loading localities:', err)
      })
  }, [])

  const handleQuery = async (query) => {
    if (!query.trim()) return

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: query,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])
    setLoading(true)

    try {
      const response = await queryAnalysis(query)
      
      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.summary,
        chartData: response.chartData,
        tableData: response.tableData,
        localities: response.localities,
        metrics: response.metrics,
        queryType: response.type,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, botMessage])
      
      // Scroll to bottom after message is added
      setTimeout(() => {
        scrollToBottom()
      }, 100)
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: `Error: ${error.message || 'Failed to process query'}`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
      
      // Scroll to bottom after error message
      setTimeout(() => {
        scrollToBottom()
      }, 100)
    } finally {
      setLoading(false)
    }
  }

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
    }
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }

  useEffect(() => {
    // Scroll to bottom when messages change
    scrollToBottom()
  }, [messages])

  return (
    <div className="container-fluid p-0">
      {/* Header */}
      <nav className="navbar navbar-light bg-white shadow-sm mb-4">
        <div className="container">
          <span className="navbar-brand mb-0 h1">🏠 Real Estate Analysis Chatbot</span>
          <span className="text-muted small">
            {localities.length > 0 && `Available: ${localities.join(', ')}`}
          </span>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container">
        <div className="row">
          <div className="col-lg-8 mx-auto">
            {/* Chat Messages */}
            <div 
              ref={chatContainerRef}
              className="card shadow-sm mb-4" 
              style={{ minHeight: '500px', maxHeight: '70vh', overflowY: 'auto' }}
            >
              <div className="card-body">
                {messages.length === 0 ? (
                  <div className="text-center text-muted py-5">
                    <h5>Welcome! 👋</h5>
                    <p>Ask me about real estate data for any locality.</p>
                    <p className="small">Try: "Analyze Wakad" or "Compare Ambegaon Budruk and Aundh"</p>
                  </div>
                ) : (
                  <>
                    {messages.map(message => (
                      <ChatMessage key={message.id} message={message} />
                    ))}
                    <div ref={messagesEndRef} />
                  </>
                )}
                {loading && (
                  <div className="d-flex justify-content-center py-3">
                    <div className="spinner-border text-primary" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Chat Input */}
            <ChatInput onSend={handleQuery} disabled={loading} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App


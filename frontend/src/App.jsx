import { useState, useEffect } from 'react'
import axios from 'axios'
import './index.css'

// Configure Axios base URL
axios.defaults.baseURL = 'http://localhost:5000';

function App() {
  const [comment, setComment] = useState('')
  const [stats, setStats] = useState({ angel_power: 0, devil_power: 0 })
  const [recentComments, setRecentComments] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchStats = async () => {
    try {
      const res = await axios.get('/api/stats')
      setStats(res.data)
    } catch (error) {
      console.error("Error fetching stats:", error)
    }
  }

  const fetchComments = async () => {
    try {
      const res = await axios.get('/api/comments')
      setRecentComments(res.data)
    } catch (error) {
      console.error("Error fetching comments:", error)
    }
  }

  useEffect(() => {
    fetchStats()
    fetchComments()

    // Poll for updates every 5 seconds
    const interval = setInterval(() => {
      fetchStats()
      fetchComments()
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!comment.trim()) return

    setLoading(true)
    try {
      await axios.post('/api/comments', { text: comment })
      setComment('')
      fetchStats()
      fetchComments()
    } catch (error) {
      console.error("Error submitting comment:", error)
      alert("Failed to submit comment")
    } finally {
      setLoading(false)
    }
  }

  // Calculate percentages for the bars
  const total = stats.angel_power + stats.devil_power
  const angelHeight = total === 0 ? 50 : (stats.angel_power / total) * 100
  const devilHeight = total === 0 ? 50 : (stats.devil_power / total) * 100

  // Normalize heights to ensure they fit in the container but show relative difference
  // If one is much larger, it should dominate. 
  // Let's just map them to px or % directly but cap at 100%

  // Better visualization logic:
  // Max height is 100%. 
  // If total is 0, both 0.
  // Else, calculate percentage relative to total.

  return (
    <div className="container">
      <h1>Angel vs Devil</h1>

      <div className="card">
        <div className="power-meter-container">
          <div
            className="power-bar angel-bar"
            style={{ height: `${total === 0 ? 10 : (stats.angel_power / (total || 1)) * 100}%` }}
          >
            <span>{stats.angel_power.toFixed(1)}</span>
          </div>

          <div className="vs-text">VS</div>

          <div
            className="power-bar devil-bar"
            style={{ height: `${total === 0 ? 10 : (stats.devil_power / (total || 1)) * 100}%` }}
          >
            <span>{stats.devil_power.toFixed(1)}</span>
          </div>
        </div>
      </div>

      <div className="card">
        <form onSubmit={handleSubmit}>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            maxLength={300}
            placeholder="Write your comment here... (Max 300 chars)"
            rows={4}
          />
          <div style={{ textAlign: 'right', color: '#666', marginBottom: '1rem' }}>
            {comment.length}/300
          </div>
          <button type="submit" disabled={loading || !comment.trim()}>
            {loading ? 'Analyzing...' : 'Submit Comment'}
          </button>
        </form>
      </div>

      <div className="card comment-list">
        <h3>Recent Comments</h3>
        {recentComments.map(c => (
          <div key={c.id} className="comment-item">
            <span>{c.text}</span>
            <span className={`comment-score ${c.sentiment_score > 0 ? 'score-positive' : c.sentiment_score < 0 ? 'score-negative' : 'score-neutral'}`}>
              {c.sentiment_score > 0 ? 'Angel' : c.sentiment_score < 0 ? 'Devil' : 'Neutral'}
              ({c.sentiment_score.toFixed(2)})
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App

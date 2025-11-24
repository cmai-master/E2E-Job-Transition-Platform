import { useEffect, useState } from 'react'
import browser from 'webextension-polyfill'

interface Stats {
  enabled: boolean
  points: number
  contributionsToday: number
}

export default function Popup() {
  const [stats, setStats] = useState<Stats>({
    enabled: true,
    points: 0,
    contributionsToday: 0,
  })

  useEffect(() => {
    // Load stats from storage
    browser.storage.sync.get(['enabled', 'points', 'contributionsToday']).then((data) => {
      setStats({
        enabled: data.enabled ?? true,
        points: data.points ?? 0,
        contributionsToday: data.contributionsToday ?? 0,
      })
    })
  }, [])

  const toggleEnabled = async () => {
    const newEnabled = !stats.enabled
    await browser.storage.sync.set({ enabled: newEnabled })
    setStats((prev) => ({ ...prev, enabled: newEnabled }))
  }

  return (
    <div className="popup-container">
      <header className="popup-header">
        <h1>CareerNavigator</h1>
        <p className="version">v0.1.0</p>
      </header>

      <div className="popup-content">
        <div className="stats-card">
          <div className="stat-item">
            <span className="stat-label">Your Points</span>
            <span className="stat-value">{stats.points}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Today's Contributions</span>
            <span className="stat-value">{stats.contributionsToday}</span>
          </div>
        </div>

        <div className="toggle-section">
          <label className="toggle-label">
            <input
              type="checkbox"
              checked={stats.enabled}
              onChange={toggleEnabled}
            />
            <span>Auto-contribute job data</span>
          </label>
        </div>

        <div className="info-section">
          <p className="info-text">
            Browse job listings on LinkedIn, Indeed, or 사람인 to automatically
            contribute data and earn points!
          </p>
        </div>

        <button
          className="dashboard-button"
          onClick={() => {
            browser.tabs.create({ url: 'http://localhost:3000/dashboard' })
          }}
        >
          Open Dashboard
        </button>
      </div>

      <footer className="popup-footer">
        <a href="#" onClick={() => browser.runtime.openOptionsPage()}>
          Settings
        </a>
      </footer>
    </div>
  )
}

/**
 * Background Service Worker
 * Handles extension lifecycle and message passing
 */

import browser from 'webextension-polyfill'

// Extension installed/updated
browser.runtime.onInstalled.addListener((details) => {
  console.log('CareerNavigator Extension installed:', details.reason)

  if (details.reason === 'install') {
    // Set default settings
    browser.storage.sync.set({
      enabled: true,
      autoContribute: false,
      points: 0,
    })
  }
})

// Handle messages from content scripts
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Background received message:', message)

  if (message.type === 'JOB_DATA_EXTRACTED') {
    // Handle job data extraction
    handleJobDataSubmission(message.data)
      .then((result) => sendResponse({ success: true, result }))
      .catch((error) => sendResponse({ success: false, error: error.message }))

    return true // Keep message channel open for async response
  }

  return false
})

/**
 * Submit job data to backend API
 */
async function handleJobDataSubmission(jobData: any) {
  const API_URL = process.env.VITE_API_URL || 'http://localhost:8000'

  try {
    const response = await fetch(`${API_URL}/api/v1/contributions/jobs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jobData),
    })

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`)
    }

    const result = await response.json()

    // Update points
    if (result.points) {
      const { points } = await browser.storage.sync.get('points')
      await browser.storage.sync.set({
        points: (points || 0) + result.points,
      })
    }

    return result
  } catch (error) {
    console.error('Failed to submit job data:', error)
    throw error
  }
}

console.log('CareerNavigator Background Service Worker loaded')

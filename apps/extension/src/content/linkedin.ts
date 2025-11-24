/**
 * LinkedIn Job Page Content Script
 * Extracts job data from LinkedIn job postings
 */

import browser from 'webextension-polyfill'

console.log('CareerNavigator: LinkedIn content script loaded')

interface JobData {
  source: string
  source_url: string
  title: string
  company: string
  location: string
  description: string
  posted_date: string
  extracted_at: string
}

/**
 * Extract job data from LinkedIn job page
 */
function extractJobData(): JobData | null {
  try {
    // Check if we're on a job detail page
    const jobTitle = document.querySelector('.job-details-jobs-unified-top-card__job-title')
    if (!jobTitle) {
      return null
    }

    // Extract data
    const title = jobTitle.textContent?.trim() || ''
    const company =
      document
        .querySelector('.job-details-jobs-unified-top-card__company-name')
        ?.textContent?.trim() || ''
    const location =
      document
        .querySelector('.job-details-jobs-unified-top-card__primary-description-container')
        ?.textContent?.trim() || ''
    const description =
      document.querySelector('.jobs-description-content__text')?.textContent?.trim() || ''

    // Get posted date
    const postedElement = document.querySelector('.jobs-unified-top-card__posted-date')
    const posted_date = postedElement?.textContent?.trim() || ''

    const jobData: JobData = {
      source: 'linkedin',
      source_url: window.location.href,
      title,
      company,
      location,
      description,
      posted_date,
      extracted_at: new Date().toISOString(),
    }

    return jobData
  } catch (error) {
    console.error('Error extracting job data:', error)
    return null
  }
}

/**
 * Send job data to background script
 */
async function sendJobData(jobData: JobData) {
  try {
    const response = await browser.runtime.sendMessage({
      type: 'JOB_DATA_EXTRACTED',
      data: jobData,
    })

    if (response.success) {
      console.log('Job data submitted successfully:', response.result)
      showSuccessNotification()
    } else {
      console.error('Failed to submit job data:', response.error)
    }
  } catch (error) {
    console.error('Error sending job data:', error)
  }
}

/**
 * Show success notification
 */
function showSuccessNotification() {
  const notification = document.createElement('div')
  notification.textContent = '✓ Job data contributed! +10 points'
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #10b981;
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 10000;
    animation: slideIn 0.3s ease-out;
  `

  document.body.appendChild(notification)

  setTimeout(() => {
    notification.remove()
  }, 3000)
}

/**
 * Check if user wants to contribute this job
 */
async function checkAndExtract() {
  const { enabled } = await browser.storage.sync.get('enabled')
  if (!enabled) {
    return
  }

  const jobData = extractJobData()
  if (jobData) {
    console.log('Extracted job data:', jobData)
    await sendJobData(jobData)
  }
}

// Wait for page to load, then extract
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    setTimeout(checkAndExtract, 2000)
  })
} else {
  setTimeout(checkAndExtract, 2000)
}

// Also listen for URL changes (SPA navigation)
let lastUrl = location.href
new MutationObserver(() => {
  const url = location.href
  if (url !== lastUrl) {
    lastUrl = url
    setTimeout(checkAndExtract, 2000)
  }
}).observe(document, { subtree: true, childList: true })

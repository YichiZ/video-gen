import { useState, useEffect } from 'react'
import { videoAPI } from '../api/client'
import VideoPlayer from './VideoPlayer'
import './VideoGenerator.css'

function VideoGenerator() {
  const [prompt, setPrompt] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [operationId, setOperationId] = useState(null)
  const [status, setStatus] = useState(null)
  const [videoBlob, setVideoBlob] = useState(null)
  const [error, setError] = useState(null)
  const [pollingInterval, setPollingInterval] = useState(null)

  useEffect(() => {
    // Cleanup polling on unmount
    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval)
      }
    }
  }, [pollingInterval])

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt')
      return
    }

    setIsGenerating(true)
    setError(null)
    setStatus(null)
    setVideoBlob(null)
    setOperationId(null)

    try {
      const response = await videoAPI.generateVideo(prompt)
      setOperationId(response.operation_id)
      setStatus(response.status)

      // Start polling for status
      startPolling(response.operation_id)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to generate video')
      setIsGenerating(false)
    }
  }

  const startPolling = (opId) => {
    const interval = setInterval(async () => {
      try {
        const statusResponse = await videoAPI.getStatus(opId)
        setStatus(statusResponse.status)

        if (statusResponse.status === 'completed') {
          clearInterval(interval)
          setPollingInterval(null)
          setIsGenerating(false)
          // Download the video
          await downloadVideo(opId)
        } else if (statusResponse.status === 'failed') {
          clearInterval(interval)
          setPollingInterval(null)
          setIsGenerating(false)
          setError(statusResponse.message || 'Video generation failed')
        }
      } catch (err) {
        console.error('Error polling status:', err)
        clearInterval(interval)
        setPollingInterval(null)
        setIsGenerating(false)
        setError('Error checking status: ' + (err.message || 'Unknown error'))
      }
    }, 3000) // Poll every 3 seconds

    setPollingInterval(interval)
  }

  const downloadVideo = async (opId) => {
    try {
      const blob = await videoAPI.downloadVideo(opId)
      setVideoBlob(blob)
    } catch (err) {
      setError('Failed to download video: ' + (err.message || 'Unknown error'))
    }
  }

  const handleDownload = () => {
    if (!videoBlob || !operationId) return

    const url = URL.createObjectURL(videoBlob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${operationId}.mp4`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const handleReset = () => {
    setPrompt('')
    setIsGenerating(false)
    setOperationId(null)
    setStatus(null)
    setVideoBlob(null)
    setError(null)
    if (pollingInterval) {
      clearInterval(pollingInterval)
      setPollingInterval(null)
    }
  }

  return (
    <div className="video-generator">
      <div className="generator-card">
        <div className="input-section">
          <label htmlFor="prompt-input">Enter your video prompt:</label>
          <textarea
            id="prompt-input"
            className="prompt-input"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="A close up of two people staring at a cryptic drawing on a wall, torchlight flickering..."
            rows={4}
            disabled={isGenerating}
          />
          <div className="button-group">
            <button
              className="btn btn-primary"
              onClick={handleGenerate}
              disabled={isGenerating || !prompt.trim()}
            >
              {isGenerating ? 'Generating...' : 'Generate Video'}
            </button>
            {(status === 'completed' || error) && (
              <button className="btn btn-secondary" onClick={handleReset}>
                New Video
              </button>
            )}
          </div>
        </div>

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {status && (
          <div className="status-section">
            <div className={`status-badge status-${status}`}>
              Status: {status}
            </div>
            {operationId && (
              <div className="operation-id">
                Operation ID: <code>{operationId}</code>
              </div>
            )}
          </div>
        )}

        {videoBlob && (
          <div className="video-section">
            <VideoPlayer videoBlob={videoBlob} />
            <button className="btn btn-download" onClick={handleDownload}>
              Download Video
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default VideoGenerator

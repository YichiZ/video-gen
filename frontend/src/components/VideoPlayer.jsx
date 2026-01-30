import { useRef, useEffect } from 'react'
import './VideoPlayer.css'

function VideoPlayer({ videoBlob }) {
  const videoRef = useRef(null)

  useEffect(() => {
    if (videoBlob && videoRef.current) {
      const url = URL.createObjectURL(videoBlob)
      videoRef.current.src = url

      return () => {
        URL.revokeObjectURL(url)
      }
    }
  }, [videoBlob])

  if (!videoBlob) {
    return null
  }

  return (
    <div className="video-player-container">
      <video
        ref={videoRef}
        className="video-player"
        controls
        playsInline
        preload="metadata"
      >
        Your browser does not support the video tag.
      </video>
    </div>
  )
}

export default VideoPlayer

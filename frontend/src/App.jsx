import { useState } from 'react'
import VideoGenerator from './components/VideoGenerator'
import './App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Video Generation with Veo3</h1>
        <p>Generate videos using AI-powered text prompts</p>
      </header>
      <main className="app-main">
        <VideoGenerator />
      </main>
    </div>
  )
}

export default App

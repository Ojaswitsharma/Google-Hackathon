"use client";

import { useState, useRef, useEffect } from 'react'
import { Mic, MicOff, Send, Loader2, Play, Download, Eye } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useSafeWorldGeneration, useSessionStatus, useAPIHealth } from '@/hooks/useSafeWorlds'
import { getEmotionColor, formatDuration } from '@/lib/api'
import Link from "next/link"

export default function Home() {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [duration, setDuration] = useState<'short' | 'medium' | 'long'>('medium')
  const recognitionRef = useRef<any>(null)

  // API hooks
  const { data, loading, error, progress, generateWorld, reset } = useSafeWorldGeneration()
  const { status: sessionStatus } = useSessionStatus(data?.session_id || null)
  const { isHealthy } = useAPIHealth()

  useEffect(() => {
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      const recognition = new (window as any).webkitSpeechRecognition()
      recognition.continuous = true
      recognition.interimResults = true
      recognition.lang = 'en-US'

      recognition.onresult = (event: any) => {
        let finalTranscript = ''
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript
          }
        }
        if (finalTranscript) {
          setTranscript(prev => prev + finalTranscript)
        }
      }

      recognition.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error)
        setIsListening(false)
      }

      recognition.onend = () => {
        setIsListening(false)
      }

      recognitionRef.current = recognition
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
    }
  }, [])

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop()
      setIsListening(false)
    } else {
      recognitionRef.current?.start()
      setIsListening(true)
    }
  }

  const handleSubmit = async () => {
    if (!transcript.trim()) return
    
    try {
      await generateWorld({
        user_input: transcript.trim(),
        include_media: true,
        duration_preference: duration
      })
    } catch (error) {
      console.error('Failed to generate safe world:', error)
    }
  }

  const handleQuickGenerate = async () => {
    if (!transcript.trim()) return
    
    try {
      await generateWorld({
        user_input: transcript.trim(),
        include_media: false,
        duration_preference: duration
      }, false)
    } catch (error) {
      console.error('Failed to generate quick world:', error)
    }
  }

  const clearTranscript = () => {
    setTranscript('')
    reset()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-green-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-green-200">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-green-800">Safe Worlds</h1>
          <div className="flex items-center gap-4">
            {/* API Health Status */}
            <div className={`w-3 h-3 rounded-full ${isHealthy ? 'bg-green-500' : 'bg-red-500'}`} 
                 title={isHealthy ? 'API Connected' : 'API Offline'} />
            <Link href="/">
              <Button variant="outline" size="sm">Sign Out</Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto p-4 space-y-6">
        {/* Input Section */}
        <Card>
          <CardHeader>
            <CardTitle className="text-green-800">Share Your Feelings</CardTitle>
            <CardDescription>
              Use your voice or type to describe how you're feeling today.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Voice Input */}
            <div className="flex items-center gap-4">
              <Button
                onClick={toggleListening}
                variant={isListening ? "destructive" : "default"}
                size="lg"
                className={isListening ? "" : "bg-green-600 hover:bg-green-700"}
              >
                {isListening ? <MicOff className="w-5 h-5 mr-2" /> : <Mic className="w-5 h-5 mr-2" />}
                {isListening ? 'Stop Listening' : 'Start Speaking'}
              </Button>
              
              {/* Duration Preference */}
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">Duration:</span>
                {(['short', 'medium', 'long'] as const).map((dur) => (
                  <Button
                    key={dur}
                    variant={duration === dur ? "default" : "outline"}
                    size="sm"
                    onClick={() => setDuration(dur)}
                    className={duration === dur ? "bg-green-600 hover:bg-green-700" : ""}
                  >
                    {dur}
                  </Button>
                ))}
              </div>
            </div>

            {/* Text Area */}
            <div className="space-y-2">
              <textarea
                value={transcript}
                onChange={(e) => setTranscript(e.target.value)}
                placeholder="Tell me how you're feeling... (or use voice input above)"
                className="w-full h-32 p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              
              {/* Controls */}
              <div className="flex gap-2 justify-between">
                <Button
                  onClick={clearTranscript}
                  variant="outline"
                  size="sm"
                  disabled={!transcript.trim()}
                >
                  Clear
                </Button>
                
                <div className="flex gap-2">
                  <Button
                    onClick={handleQuickGenerate}
                    variant="outline"
                    disabled={!transcript.trim() || loading}
                    className="border-green-600 text-green-600 hover:bg-green-50"
                  >
                    {loading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Send className="w-4 h-4 mr-2" />}
                    Quick Story
                  </Button>
                  
                  <Button
                    onClick={handleSubmit}
                    disabled={!transcript.trim() || loading}
                    className="bg-green-600 hover:bg-green-700"
                  >
                    {loading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Send className="w-4 h-4 mr-2" />}
                    Create World
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Progress Section */}
        {loading && (
          <Card>
            <CardContent className="pt-6">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">{progress}</span>
                  <Loader2 className="w-4 h-4 animate-spin" />
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-green-600 h-2 rounded-full transition-all duration-500" 
                       style={{ width: loading ? '60%' : '0%' }} />
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Error Display */}
        {error && (
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <div className="text-red-800">
                <strong>Error:</strong> {error}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Results Section */}
        {data && (
          <div className="space-y-4">
            {/* World Info */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  Your Safe World
                  <div 
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: getEmotionColor(data.emotion) }}
                  />
                </CardTitle>
                <CardDescription>
                  Generated on {new Date(data.created_at).toLocaleString()}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-semibold text-green-800">Emotion Detected</h4>
                    <p className="text-gray-700 capitalize">{data.emotion}</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-green-800">World Type</h4>
                    <p className="text-gray-700">{data.world_type}</p>
                  </div>
                </div>
                
                {data.keywords.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-green-800 mb-2">Key Themes</h4>
                    <div className="flex flex-wrap gap-2">
                      {data.keywords.map((keyword, idx) => (
                        <span key={idx} 
                              className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                <div>
                  <h4 className="font-semibold text-green-800 mb-2">Your Story</h4>
                  <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                    {data.narrative}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Media Controls */}
            {data.media_content && (
              <Card>
                <CardHeader>
                  <CardTitle>Generated Media</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-4">
                    {data.media_content.audio_path && (
                      <div className="flex items-center gap-2">
                        <audio controls className="w-64">
                          <source src={`http://localhost:8004/media/audio/${data.session_id}`} type="audio/mpeg" />
                        </audio>
                        {data.media_content.audio_duration && (
                          <span className="text-sm text-gray-600">
                            ({formatDuration(data.media_content.audio_duration)})
                          </span>
                        )}
                      </div>
                    )}
                    
                    {data.media_content.video_path && (
                      <div className="w-full">
                        <video controls className="w-full max-w-lg rounded-lg">
                          <source src={`http://localhost:8004/media/video/${data.session_id}`} type="video/mp4" />
                        </video>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Session Status */}
            {sessionStatus && (
              <Card>
                <CardHeader>
                  <CardTitle>Processing Status</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span>Audio Ready:</span>
                      <span className={sessionStatus.audio_ready ? 'text-green-600' : 'text-yellow-600'}>
                        {sessionStatus.audio_ready ? '✓' : '⏳'}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Video Ready:</span>
                      <span className={sessionStatus.video_ready ? 'text-green-600' : 'text-yellow-600'}>
                        {sessionStatus.video_ready ? '✓' : '⏳'}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

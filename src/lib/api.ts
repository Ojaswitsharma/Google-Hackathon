// API utilities for Safe Worlds backend integration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8004';

export interface SafeWorldRequest {
  user_input: string;
  include_media?: boolean;
  duration_preference?: 'short' | 'medium' | 'long';
}

export interface MediaContent {
  story_text?: string;
  audio_path?: string;
  video_path?: string;
  video_url?: string;
  audio_duration?: number;
  story_json_path?: string;
}

export interface SafeWorldResponse {
  emotion: string;
  keywords: string[];
  interactive_elements: string[];
  narrative: string;
  video_prompt: string;
  music_prompt: string;
  world_type: string;
  generated_story?: string;
  media_content?: MediaContent;
  session_id: string;
  created_at: string;
}

export interface SessionStatus {
  status: string;
  audio_ready?: boolean;
  video_ready?: boolean;
  audio_url?: string;
  video_url?: string;
}

class SafeWorldsAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Generate a complete safe world with media
   */
  async generateSafeWorld(request: SafeWorldRequest): Promise<SafeWorldResponse> {
    const response = await fetch(`${this.baseUrl}/generate_safe_world`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Generate a quick safe world without media (faster)
   */
  async generateQuickWorld(request: SafeWorldRequest): Promise<SafeWorldResponse> {
    const response = await fetch(`${this.baseUrl}/generate_safe_world_quick`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...request,
        include_media: false,
      }),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Check the status of a session's media generation
   */
  async getSessionStatus(sessionId: string): Promise<SessionStatus> {
    const response = await fetch(`${this.baseUrl}/session/${sessionId}/status`);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get the audio file URL for a session
   */
  getAudioUrl(sessionId: string): string {
    return `${this.baseUrl}/media/audio/${sessionId}`;
  }

  /**
   * Get the video file URL for a session
   */
  getVideoUrl(sessionId: string): string {
    return `${this.baseUrl}/media/video/${sessionId}`;
  }

  /**
   * Check if the API is healthy
   */
  async healthCheck(): Promise<{ status: string; service: string }> {
    const response = await fetch(`${this.baseUrl}/health`);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get API information
   */
  async getApiInfo(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/`);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }
}

// Export singleton instance
export const safeWorldsAPI = new SafeWorldsAPI();

// Utility functions
export const formatDuration = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
};

export const getEmotionColor = (emotion: string): string => {
  const colors: Record<string, string> = {
    anxiety: '#FF6B6B',
    sadness: '#4ECDC4',
    anger: '#FF8E53',
    joy: '#FFD93D',
    overwhelm: '#6BCF7F',
    lonely: '#A8E6CF',
    excited: '#FFB3BA',
    neutral: '#C7C7C7'
  };
  
  return colors[emotion.toLowerCase()] || colors.neutral;
};

export default SafeWorldsAPI;

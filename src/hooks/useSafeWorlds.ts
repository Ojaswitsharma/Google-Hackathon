// React hooks for Safe Worlds API integration
import { useState, useCallback, useEffect } from 'react';
import { safeWorldsAPI, SafeWorldRequest, SafeWorldResponse, SessionStatus } from '../lib/api';

export interface UseGenerationState {
  data: SafeWorldResponse | null;
  loading: boolean;
  error: string | null;
  progress: string;
}

export interface UseSessionState {
  status: SessionStatus | null;
  loading: boolean;
  error: string | null;
}

/**
 * Hook for generating safe worlds
 */
export const useSafeWorldGeneration = () => {
  const [state, setState] = useState<UseGenerationState>({
    data: null,
    loading: false,
    error: null,
    progress: '',
  });

  const generateWorld = useCallback(async (request: SafeWorldRequest, withMedia: boolean = true) => {
    setState(prev => ({
      ...prev,
      loading: true,
      error: null,
      progress: 'Starting generation...',
    }));

    try {
      setState(prev => ({ ...prev, progress: 'Analyzing your input...' }));
      
      const response = withMedia 
        ? await safeWorldsAPI.generateSafeWorld(request)
        : await safeWorldsAPI.generateQuickWorld(request);

      setState({
        data: response,
        loading: false,
        error: null,
        progress: 'Complete!',
      });

      return response;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      setState({
        data: null,
        loading: false,
        error: errorMessage,
        progress: '',
      });
      throw error;
    }
  }, []);

  const reset = useCallback(() => {
    setState({
      data: null,
      loading: false,
      error: null,
      progress: '',
    });
  }, []);

  return {
    ...state,
    generateWorld,
    reset,
  };
};

/**
 * Hook for monitoring session status
 */
export const useSessionStatus = (sessionId: string | null) => {
  const [state, setState] = useState<UseSessionState>({
    status: null,
    loading: false,
    error: null,
  });

  const checkStatus = useCallback(async () => {
    if (!sessionId) return;

    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const status = await safeWorldsAPI.getSessionStatus(sessionId);
      setState({
        status,
        loading: false,
        error: null,
      });
      return status;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to check status';
      setState({
        status: null,
        loading: false,
        error: errorMessage,
      });
    }
  }, [sessionId]);

  // Auto-refresh status for active sessions
  useEffect(() => {
    if (!sessionId) return;

    checkStatus();
    
    const interval = setInterval(checkStatus, 3000); // Check every 3 seconds
    
    return () => clearInterval(interval);
  }, [sessionId, checkStatus]);

  return {
    ...state,
    checkStatus,
  };
};

/**
 * Hook for API health monitoring
 */
export const useAPIHealth = () => {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  const [checking, setChecking] = useState(false);

  const checkHealth = useCallback(async () => {
    setChecking(true);
    try {
      await safeWorldsAPI.healthCheck();
      setIsHealthy(true);
    } catch (error) {
      setIsHealthy(false);
    } finally {
      setChecking(false);
    }
  }, []);

  useEffect(() => {
    checkHealth();
    
    // Check health every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    
    return () => clearInterval(interval);
  }, [checkHealth]);

  return {
    isHealthy,
    checking,
    checkHealth,
  };
};

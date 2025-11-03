/**
 * API service layer for backend communication.
 * 
 * Provides typed API calls with error handling and SSE streaming support.
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import type { 
  ChatRequest, 
  ChatResponse, 
  StreamChunk, 
  DocumentInfo,
  HealthCheckResponse,
  ApiError 
} from '@/types';

/**
 * Base API configuration
 */
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

/**
 * Create axios instance with default configuration
 */
const createApiClient = (): AxiosInstance => {
  const client = axios.create({
    baseURL: API_BASE,
    timeout: 30000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Request interceptor
  client.interceptors.request.use(
    (config) => {
      // Add auth token if available
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response interceptor
  client.interceptors.response.use(
    (response) => response,
    (error: AxiosError<ApiError>) => {
      if (error.response?.status === 401) {
        // Handle unauthorized - redirect to login if needed
        console.error('Unauthorized access');
      }
      
      // Extract error message
      const apiError: ApiError = error.response?.data || {
        error: 'NetworkError',
        message: 'Không thể kết nối với server. Vui lòng thử lại.',
        timestamp: new Date().toISOString(),
      };
      
      return Promise.reject(apiError);
    }
  );

  return client;
};

/**
 * API client instance
 */
export const api = createApiClient();

/**
 * Chat API methods
 */
export const chatAPI = {
  /**
   * Send a chat message (non-streaming)
   */
  sendMessage: async (message: string): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/chat/simple', {
      message,
      stream: false,
    } as ChatRequest);
    
    return response.data;
  },

  /**
   * Stream a chat message via Server-Sent Events
   * 
   * Usage:
   * ```ts
   * for await (const chunk of chatAPI.streamMessage(message)) {
   *   console.log(chunk.text);
   *   if (chunk.done) break;
   * }
   * ```
   */
  streamMessage: async function* (message: string): AsyncGenerator<StreamChunk, void, unknown> {
    const response = await fetch(`${API_BASE}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        stream: true,
      } as ChatRequest),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('Response body is not readable');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          break;
        }

        // Decode chunk and add to buffer
        buffer += decoder.decode(value, { stream: true });

        // Split by newlines and process complete lines
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // Keep incomplete line in buffer

        for (const line of lines) {
          if (line.trim().startsWith('data: ')) {
            const data = line.trim().slice(6); // Remove 'data: ' prefix
            
            if (data === '[DONE]') {
              yield { text: '', done: true };
              return;
            }

            try {
              const chunk: StreamChunk = JSON.parse(data);
              yield chunk;
              
              if (chunk.done) {
                return;
              }
            } catch (e) {
              console.error('Failed to parse SSE data:', data, e);
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  },
};

/**
 * Documents API methods
 */
export const documentsAPI = {
  /**
   * Upload a document file
   */
  upload: async (file: File): Promise<{ document_id: string; filename: string; status: string }> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  /**
   * Get list of all documents
   */
  list: async (): Promise<{ documents: DocumentInfo[]; total: number }> => {
    const response = await api.get('/documents/list');
    return response.data;
  },

  /**
   * Delete a document by ID
   */
  delete: async (documentId: string): Promise<{ document_id: string; status: string }> => {
    const response = await api.delete(`/documents/${documentId}`);
    return response.data;
  },
};

/**
 * Health check API
 */
export const healthAPI = {
  /**
   * Check API health
   */
  check: async (): Promise<HealthCheckResponse> => {
    const response = await api.get<HealthCheckResponse>('/health');
    return response.data;
  },
};


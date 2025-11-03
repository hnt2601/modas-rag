/**
 * TypeScript type definitions for the RAG system.
 * 
 * All types are strictly typed with no 'any' usage.
 */

/**
 * Message role type
 */
export type MessageRole = 'user' | 'assistant' | 'system';

/**
 * Message status type
 */
export type MessageStatus = 'sending' | 'sent' | 'error' | 'streaming';

/**
 * Chat message interface
 */
export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  status?: MessageStatus;
  error?: string;
}

/**
 * Chat request payload
 */
export interface ChatRequest {
  message: string;
  stream?: boolean;
}

/**
 * Chat response from API
 */
export interface ChatResponse {
  answer: string;
  sources?: Array<{
    filename: string;
    chunk_index: number;
    content: string;
    score: number;
  }>;
  metadata?: {
    retrieval_time?: number;
    generation_time?: number;
    total_time?: number;
  };
}

/**
 * Streaming chunk from SSE
 */
export interface StreamChunk {
  text: string;
  done: boolean;
}

/**
 * Document metadata
 */
export interface DocumentMetadata {
  filename: string;
  file_type: string;
  file_size: number;
  upload_time: string;
  chunk_count?: number;
}

/**
 * Document info
 */
export interface DocumentInfo {
  document_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  chunk_count: number;
  upload_time: string;
}

/**
 * API error response
 */
export interface ApiError {
  error: string;
  message: string;
  detail?: string;
  timestamp: string;
}

/**
 * Health check response
 */
export interface HealthCheckResponse {
  status: string;
  checks: {
    api: string;
    qdrant?: string;
    fpt_cloud?: string;
  };
  timestamp: string;
}


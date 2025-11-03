/**
 * Custom hook for chat functionality with streaming support.
 * 
 * Manages chat state, message sending, and SSE streaming.
 */

import { useState, useCallback, useRef } from 'react';
import { message as antdMessage } from 'antd';
import { chatAPI } from '@/services/api';
import type { Message } from '@/types';

/**
 * Hook return type
 */
interface UseChatReturn {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  sendMessage: (content: string, stream?: boolean) => Promise<void>;
  clearMessages: () => void;
  retryLastMessage: () => Promise<void>;
}

/**
 * Custom hook for chat functionality
 * 
 * @returns Chat state and methods
 * 
 * @example
 * ```tsx
 * const { messages, isLoading, sendMessage } = useChat();
 * 
 * const handleSend = async () => {
 *   await sendMessage(inputValue, true); // with streaming
 * };
 * ```
 */
export const useChat = (): UseChatReturn => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const lastUserMessageRef = useRef<string>('');

  /**
   * Add a message to the chat
   */
  const addMessage = useCallback((message: Message) => {
    setMessages((prev) => [...prev, message]);
  }, []);

  /**
   * Update the last message (for streaming)
   */
  const updateLastMessage = useCallback((updates: Partial<Message>) => {
    setMessages((prev) => {
      if (prev.length === 0) return prev;
      
      const updated = [...prev];
      const lastIndex = updated.length - 1;
      updated[lastIndex] = { ...updated[lastIndex], ...updates };
      
      return updated;
    });
  }, []);

  /**
   * Send a message with optional streaming
   */
  const sendMessage = useCallback(async (content: string, stream: boolean = true) => {
    if (!content.trim()) {
      antdMessage.warning('Vui lòng nhập tin nhắn');
      return;
    }

    // Store for retry
    lastUserMessageRef.current = content;

    // Reset error
    setError(null);
    setIsLoading(true);

    // Add user message
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
      status: 'sent',
    };
    addMessage(userMessage);

    // Create assistant message placeholder
    const assistantMessage: Message = {
      id: `assistant-${Date.now()}`,
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      status: stream ? 'streaming' : 'sending',
    };
    addMessage(assistantMessage);

    try {
      if (stream) {
        // Streaming mode
        let fullContent = '';
        
        for await (const chunk of chatAPI.streamMessage(content)) {
          if (chunk.done) {
            updateLastMessage({
              status: 'sent',
            });
            break;
          }
          
          fullContent += chunk.text;
          updateLastMessage({
            content: fullContent,
            status: 'streaming',
          });
        }
      } else {
        // Non-streaming mode
        const response = await chatAPI.sendMessage(content);
        
        updateLastMessage({
          content: response.answer,
          status: 'sent',
        });
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Đã xảy ra lỗi khi gửi tin nhắn';
      
      setError(errorMessage);
      updateLastMessage({
        content: 'Xin lỗi, đã xảy ra lỗi. Vui lòng thử lại.',
        status: 'error',
        error: errorMessage,
      });
      
      antdMessage.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, [addMessage, updateLastMessage]);

  /**
   * Clear all messages
   */
  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
    lastUserMessageRef.current = '';
  }, []);

  /**
   * Retry the last message
   */
  const retryLastMessage = useCallback(async () => {
    if (!lastUserMessageRef.current) {
      antdMessage.warning('Không có tin nhắn để thử lại');
      return;
    }

    // Remove last two messages (user + assistant error)
    setMessages((prev) => prev.slice(0, -2));
    
    // Resend
    await sendMessage(lastUserMessageRef.current, true);
  }, [sendMessage]);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
    retryLastMessage,
  };
};


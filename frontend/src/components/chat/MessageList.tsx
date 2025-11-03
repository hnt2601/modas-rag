/**
 * MessageList component for displaying chat messages.
 * 
 * Handles message rendering with auto-scroll and accessibility.
 */

import React, { useEffect, useRef } from 'react';
import { Empty } from 'antd';
import { MessageBubble } from './MessageBubble';
import type { Message } from '@/types';

interface MessageListProps {
  messages: Message[];
  onRetry?: () => void;
  style?: React.CSSProperties;
}

/**
 * MessageList component
 * 
 * Features:
 * - Auto-scroll to bottom on new messages
 * - Empty state
 * - Virtualization for large message lists (future enhancement)
 * - Accessibility with proper ARIA labels
 * 
 * @param props - Component props
 */
export const MessageList: React.FC<MessageListProps> = ({
  messages,
  onRetry,
  style,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  /**
   * Auto-scroll to bottom when new messages arrive
   */
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'end',
      });
    }
  }, [messages]);

  /**
   * Empty state
   */
  if (messages.length === 0) {
    return (
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
          ...style,
        }}
        role="region"
        aria-label="Danh sách tin nhắn trống"
      >
        <Empty
          description="Chưa có tin nhắn nào. Hãy bắt đầu cuộc trò chuyện!"
          image={Empty.PRESENTED_IMAGE_SIMPLE}
        />
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      style={{
        flex: 1,
        overflowY: 'auto',
        overflowX: 'hidden',
        padding: '16px',
        ...style,
      }}
      role="log"
      aria-live="polite"
      aria-label="Danh sách tin nhắn"
      aria-atomic="false"
    >
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          message={message}
          onRetry={message.status === 'error' ? onRetry : undefined}
        />
      ))}
      
      {/* Invisible element for auto-scroll anchor */}
      <div
        ref={messagesEndRef}
        aria-hidden="true"
        style={{ height: 1 }}
      />
    </div>
  );
};


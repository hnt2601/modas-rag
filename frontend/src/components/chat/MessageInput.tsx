/**
 * MessageInput component for chat input.
 * 
 * Provides accessible text input with send functionality.
 */

import React, { useState, useRef, KeyboardEvent } from 'react';
import { Input, Button, Space } from 'antd';
import { SendOutlined, LoadingOutlined } from '@ant-design/icons';

const { TextArea } = Input;

interface MessageInputProps {
  onSend: (message: string) => void;
  isLoading?: boolean;
  disabled?: boolean;
  placeholder?: string;
}

/**
 * MessageInput component
 * 
 * Features:
 * - Auto-resizing textarea
 * - Send on Enter (new line on Shift+Enter)
 * - Loading state
 * - Keyboard shortcuts
 * - Accessibility with ARIA labels
 * 
 * @param props - Component props
 */
export const MessageInput: React.FC<MessageInputProps> = ({
  onSend,
  isLoading = false,
  disabled = false,
  placeholder = 'Nhập câu hỏi của bạn...',
}) => {
  const [message, setMessage] = useState('');
  const textAreaRef = useRef<any>(null);

  /**
   * Handle send message
   */
  const handleSend = (): void => {
    if (!message.trim() || isLoading || disabled) {
      return;
    }

    onSend(message.trim());
    setMessage('');
    
    // Focus back to textarea
    setTimeout(() => {
      textAreaRef.current?.focus();
    }, 0);
  };

  /**
   * Handle Enter key press
   * - Enter: Send message
   * - Shift+Enter: New line
   */
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>): void => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Space.Compact
      style={{ width: '100%' }}
      role="form"
      aria-label="Form gửi tin nhắn"
    >
      <TextArea
        ref={textAreaRef}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        autoSize={{ minRows: 2, maxRows: 6 }}
        disabled={disabled || isLoading}
        maxLength={2000}
        showCount
        style={{ resize: 'none' }}
        aria-label="Nhập tin nhắn"
        aria-describedby="send-hint"
      />
      
      <Button
        type="primary"
        size="large"
        icon={isLoading ? <LoadingOutlined spin /> : <SendOutlined />}
        onClick={handleSend}
        disabled={disabled || isLoading || !message.trim()}
        loading={isLoading}
        aria-label="Gửi tin nhắn"
        aria-keyshortcuts="Enter"
        style={{
          height: 'auto',
          minHeight: 64,
        }}
      >
        {isLoading ? 'Đang gửi...' : 'Gửi'}
      </Button>
      
      {/* Screen reader hint */}
      <span id="send-hint" style={{ display: 'none' }}>
        Nhấn Enter để gửi, Shift+Enter để xuống dòng
      </span>
    </Space.Compact>
  );
};


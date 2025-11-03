/**
 * MessageBubble component with WCAG 2.0 accessibility compliance.
 * 
 * Displays individual chat messages with proper styling and accessibility features.
 */

import React from 'react';
import { Card, Typography, Space, Tag, Tooltip, Button } from 'antd';
import { UserOutlined, RobotOutlined, CopyOutlined, ReloadOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import dayjs from 'dayjs';
import type { Message } from '@/types';

const { Text } = Typography;

interface MessageBubbleProps {
  message: Message;
  onRetry?: () => void;
}

/**
 * MessageBubble component
 * 
 * Features:
 * - WCAG 2.0 compliant with proper contrast ratios
 * - ARIA labels for screen readers
 * - Keyboard navigation support
 * - Markdown rendering for AI responses
 * - Copy to clipboard functionality
 * - Retry on error
 * 
 * @param props - Component props
 */
export const MessageBubble: React.FC<MessageBubbleProps> = ({ message, onRetry }) => {
  const isUser = message.role === 'user';
  const isError = message.status === 'error';
  const isStreaming = message.status === 'streaming';

  /**
   * Copy message content to clipboard
   */
  const handleCopy = async (): Promise<void> => {
    try {
      await navigator.clipboard.writeText(message.content);
      // Could use antd message here, but keeping component pure
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  /**
   * Get status badge
   */
  const getStatusBadge = (): React.ReactNode => {
    if (isStreaming) {
      return <Tag color="processing">Đang nhận...</Tag>;
    }
    if (isError) {
      return <Tag color="error">Lỗi</Tag>;
    }
    return null;
  };

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        marginBottom: 16,
      }}
      role="article"
      aria-label={`${isUser ? 'Tin nhắn của bạn' : 'Tin nhắn từ AI'} lúc ${dayjs(message.timestamp).format('HH:mm')}`}
    >
      <Card
        size="small"
        style={{
          maxWidth: '70%',
          minWidth: '200px',
          backgroundColor: isUser ? '#e6f7ff' : '#ffffff',
          borderColor: isError ? '#ff4d4f' : isUser ? '#1890ff' : '#d9d9d9',
          borderWidth: isError ? 2 : 1,
        }}
        styles={{
          body: {
            padding: '12px 16px',
          },
        }}
      >
        {/* Message Header */}
        <Space style={{ marginBottom: 8, width: '100%', justifyContent: 'space-between' }}>
          <Space size="small">
            {isUser ? (
              <UserOutlined aria-label="Người dùng" style={{ color: '#1890ff' }} />
            ) : (
              <RobotOutlined aria-label="Trợ lý AI" style={{ color: '#52c41a' }} />
            )}
            <Text strong style={{ fontSize: 12 }}>
              {isUser ? 'Bạn' : 'Trợ lý AI'}
            </Text>
            {getStatusBadge()}
          </Space>
          
          <Text type="secondary" style={{ fontSize: 11 }}>
            {dayjs(message.timestamp).format('HH:mm')}
          </Text>
        </Space>

        {/* Message Content */}
        <div
          style={{
            wordBreak: 'break-word',
            lineHeight: 1.6,
          }}
        >
          {isUser ? (
            // Plain text for user messages
            <Text>{message.content}</Text>
          ) : (
            // Markdown rendering for AI messages
            <ReactMarkdown
              components={{
                // Custom styles for markdown elements
                p: ({ children }) => (
                  <p style={{ margin: '0 0 8px 0' }}>{children}</p>
                ),
                code: ({ children, className }) => {
                  const isInline = !className;
                  return isInline ? (
                    <code
                      style={{
                        backgroundColor: '#f5f5f5',
                        padding: '2px 6px',
                        borderRadius: 3,
                        fontSize: '0.9em',
                      }}
                    >
                      {children}
                    </code>
                  ) : (
                    <pre
                      style={{
                        backgroundColor: '#f5f5f5',
                        padding: 12,
                        borderRadius: 6,
                        overflow: 'auto',
                      }}
                    >
                      <code>{children}</code>
                    </pre>
                  );
                },
              }}
            >
              {message.content || (isStreaming ? '...' : '')}
            </ReactMarkdown>
          )}
        </div>

        {/* Error Message */}
        {isError && message.error && (
          <div style={{ marginTop: 8 }}>
            <Text type="danger" style={{ fontSize: 12 }}>
              {message.error}
            </Text>
          </div>
        )}

        {/* Action Buttons */}
        <Space size="small" style={{ marginTop: 8 }}>
          {message.content && (
            <Tooltip title="Sao chép">
              <Button
                type="text"
                size="small"
                icon={<CopyOutlined />}
                onClick={handleCopy}
                aria-label="Sao chép nội dung tin nhắn"
                style={{ padding: '0 4px' }}
              />
            </Tooltip>
          )}
          
          {isError && onRetry && (
            <Tooltip title="Thử lại">
              <Button
                type="text"
                size="small"
                icon={<ReloadOutlined />}
                onClick={onRetry}
                aria-label="Thử lại tin nhắn"
                style={{ padding: '0 4px' }}
              />
            </Tooltip>
          )}
        </Space>
      </Card>
    </div>
  );
};


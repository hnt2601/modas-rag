/**
 * ChatInterface - Main chat component with Ant Design.
 * 
 * Integrates all chat sub-components with Layout and Card.
 */

import React from 'react';
import { Layout, Card, Typography, Space, Button, Tooltip } from 'antd';
import { DeleteOutlined, QuestionCircleOutlined } from '@ant-design/icons';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { useChat } from '@/hooks/useChat';

const { Content } = Layout;
const { Title, Text } = Typography;

/**
 * ChatInterface component
 * 
 * Features:
 * - Ant Design Layout and Card components
 * - Streaming message support via SSE
 * - Message history
 * - Clear chat functionality
 * - Loading states
 * - Error handling
 * - Accessibility compliance (WCAG 2.0)
 * 
 * @example
 * ```tsx
 * <ChatInterface />
 * ```
 */
export const ChatInterface: React.FC = () => {
  const {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
    retryLastMessage,
  } = useChat();

  /**
   * Handle send message with streaming
   */
  const handleSend = async (content: string): Promise<void> => {
    await sendMessage(content, true); // Enable streaming
  };

  return (
    <Layout
      style={{
        height: '100vh',
        backgroundColor: '#f5f5f5',
      }}
    >
      <Content
        style={{
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          maxWidth: 1200,
          margin: '0 auto',
          width: '100%',
        }}
      >
        <Card
          style={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          }}
          styles={{
            body: {
              flex: 1,
              display: 'flex',
              flexDirection: 'column',
              padding: 0,
            },
          }}
          role="main"
          aria-label="Giao diện chat"
        >
          {/* Header */}
          <div
            style={{
              padding: '20px 24px',
              borderBottom: '1px solid #f0f0f0',
              backgroundColor: '#ffffff',
            }}
            role="banner"
          >
            <Space
              style={{
                width: '100%',
                justifyContent: 'space-between',
              }}
            >
              <Space direction="vertical" size={0}>
                <Title level={3} style={{ margin: 0 }}>
                  Trợ lý AI RAG
                </Title>
                <Text type="secondary" style={{ fontSize: 13 }}>
                  Hệ thống tìm kiếm và trả lời thông minh với mô hình AI tiếng Việt
                </Text>
              </Space>
              
              <Space>
                <Tooltip title="Hướng dẫn sử dụng">
                  <Button
                    type="text"
                    icon={<QuestionCircleOutlined />}
                    aria-label="Hướng dẫn sử dụng"
                  />
                </Tooltip>
                
                <Tooltip title="Xóa lịch sử chat">
                  <Button
                    type="text"
                    danger
                    icon={<DeleteOutlined />}
                    onClick={clearMessages}
                    disabled={messages.length === 0}
                    aria-label="Xóa lịch sử chat"
                  />
                </Tooltip>
              </Space>
            </Space>
          </div>

          {/* Message List */}
          <MessageList
            messages={messages}
            onRetry={retryLastMessage}
            style={{
              flex: 1,
              backgroundColor: '#fafafa',
            }}
          />

          {/* Error Banner */}
          {error && (
            <div
              style={{
                padding: '12px 24px',
                backgroundColor: '#fff2f0',
                borderTop: '1px solid #ffccc7',
                borderBottom: '1px solid #ffccc7',
              }}
              role="alert"
              aria-live="assertive"
            >
              <Text type="danger">
                ⚠️ {error}
              </Text>
            </div>
          )}

          {/* Input Area */}
          <div
            style={{
              padding: '16px 24px',
              borderTop: '1px solid #f0f0f0',
              backgroundColor: '#ffffff',
            }}
          >
            <MessageInput
              onSend={handleSend}
              isLoading={isLoading}
              placeholder="Nhập câu hỏi của bạn... (Enter để gửi, Shift+Enter để xuống dòng)"
            />
          </div>
        </Card>
      </Content>
    </Layout>
  );
};


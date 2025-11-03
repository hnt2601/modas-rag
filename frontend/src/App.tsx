/**
 * Main App component with Ant Design ConfigProvider.
 * 
 * Sets up theme, locale, and routing for the application.
 */

import React from 'react';
import { ConfigProvider, App as AntApp } from 'antd';
import viVN from 'antd/locale/vi_VN';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { theme } from '@/theme/antd-theme';
import { ChatInterface } from '@/components/chat/ChatInterface';

/**
 * Create React Query client
 */
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

/**
 * Main App component
 * 
 * Features:
 * - Ant Design ConfigProvider with Vietnamese locale
 * - Custom theme configuration
 * - React Query setup
 * - Global error boundary (via AntApp)
 * - WCAG 2.0 accessibility
 */
function App(): React.ReactElement {
  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider
        theme={theme}
        locale={viVN}
      >
        <AntApp>
          <ChatInterface />
        </AntApp>
      </ConfigProvider>
    </QueryClientProvider>
  );
}

export default App;


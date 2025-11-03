/**
 * Ant Design theme configuration.
 * 
 * Follows WCAG 2.0 accessibility standards with proper contrast ratios.
 */

import type { ThemeConfig } from 'antd';

export const theme: ThemeConfig = {
  token: {
    // Brand Colors
    colorPrimary: '#1890ff',
    colorSuccess: '#52c41a',
    colorWarning: '#faad14',
    colorError: '#ff4d4f',
    colorInfo: '#1890ff',
    colorLink: '#1890ff',
    
    // Typography
    fontSize: 14,
    fontSizeHeading1: 38,
    fontSizeHeading2: 30,
    fontSizeHeading3: 24,
    fontSizeHeading4: 20,
    fontSizeHeading5: 16,
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    
    // Spacing
    marginXS: 8,
    marginSM: 12,
    margin: 16,
    marginMD: 20,
    marginLG: 24,
    marginXL: 32,
    marginXXL: 48,
    
    // Border Radius
    borderRadius: 6,
    borderRadiusLG: 8,
    borderRadiusSM: 4,
    
    // Line Height (for accessibility)
    lineHeight: 1.5715,
    lineHeightHeading1: 1.21,
    lineHeightHeading2: 1.35,
    
    // Control Heights
    controlHeight: 40,
    controlHeightLG: 48,
    controlHeightSM: 32,
  },
  
  components: {
    // Button customization
    Button: {
      controlHeight: 40,
      controlHeightLG: 48,
      controlHeightSM: 32,
      fontSize: 14,
      borderRadius: 6,
      primaryShadow: '0 2px 0 rgba(5, 145, 255, 0.1)',
    },
    
    // Input customization
    Input: {
      controlHeight: 40,
      controlHeightLG: 48,
      controlHeightSM: 32,
      fontSize: 14,
      borderRadius: 6,
    },
    
    // Card customization
    Card: {
      borderRadius: 8,
      boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02)',
    },
    
    // Typography customization
    Typography: {
      fontSize: 14,
      fontSizeHeading1: 38,
      fontSizeHeading2: 30,
      fontSizeHeading3: 24,
      fontSizeHeading4: 20,
      fontSizeHeading5: 16,
    },
    
    // Layout customization
    Layout: {
      headerBg: '#ffffff',
      headerHeight: 64,
      headerPadding: '0 24px',
      bodyBg: '#f5f5f5',
      siderBg: '#ffffff',
    },
    
    // Message customization (for MessageBubble)
    Message: {
      contentBg: '#ffffff',
      contentPadding: '10px 16px',
    },
  },
};

/**
 * Vietnamese locale configuration
 */
export const getVietnameseLocale = () => {
  return {
    locale: 'vi',
    // Ant Design will use Vietnamese locale from 'antd/locale/vi_VN'
  };
};


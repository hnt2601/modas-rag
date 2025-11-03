# RAG System Frontend

Professional React frontend with Ant Design 5.x for the RAG system.

## Features

✅ **React 18+ with TypeScript** - Strict mode, no 'any' types
✅ **Ant Design 5.x** - Enterprise UI design system  
✅ **Streaming Chat** - SSE support for real-time responses
✅ **WCAG 2.0 Compliant** - Full accessibility support
✅ **Vietnamese Locale** - Built-in Vietnamese language support
✅ **Custom Theme** - Branded color scheme and components
✅ **React Query** - Efficient data fetching and caching
✅ **Markdown Rendering** - Rich text display for AI responses

## Quick Start

### Prerequisites

- Node.js 18+ 
- pnpm (recommended) or npm

### Installation

```bash
cd frontend

# Install dependencies
pnpm install

# Copy environment template
cp .env.example .env

# Start development server
pnpm dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
# Build
pnpm build

# Preview build
pnpm preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── chat/
│   │       ├── ChatInterface.tsx    # Main chat component
│   │       ├── MessageList.tsx      # Message list
│   │       ├── MessageBubble.tsx    # Individual message
│   │       └── MessageInput.tsx     # Input field
│   ├── hooks/
│   │   └── useChat.ts              # Chat state management
│   ├── services/
│   │   └── api.ts                  # API calls with SSE
│   ├── theme/
│   │   └── antd-theme.ts           # Ant Design theme
│   ├── types/
│   │   └── index.ts                # TypeScript types
│   ├── App.tsx                     # Main app
│   ├── main.tsx                    # Entry point
│   └── index.css                   # Global styles
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Components

### ChatInterface

Main chat component with Layout and Card from Ant Design.

**Features:**
- Layout with header and content area
- Message list with auto-scroll
- Input area with send button
- Loading states
- Error handling
- Clear chat functionality

### MessageBubble

Individual message display with accessibility.

**Features:**
- User and AI message distinction
- Markdown rendering for AI responses
- Copy to clipboard
- Retry on error
- Status indicators (sending, streaming, error)
- ARIA labels for screen readers

### MessageList

Scrollable message container.

**Features:**
- Auto-scroll to latest message
- Empty state
- Smooth scrolling
- Accessible region with ARIA

### MessageInput

Text input with send functionality.

**Features:**
- Auto-resizing textarea
- Send on Enter (new line on Shift+Enter)
- Character count (max 2000)
- Loading state
- Keyboard shortcuts
- Accessible form

## Hooks

### useChat

Custom hook for chat state management.

```tsx
const {
  messages,        // Array of messages
  isLoading,       // Loading state
  error,           // Error message
  sendMessage,     // Send message function
  clearMessages,   // Clear chat
  retryLastMessage // Retry failed message
} = useChat();
```

**Features:**
- Message state management
- Streaming support via SSE
- Error handling
- Retry functionality
- Auto-retry on failure

## API Service

### chatAPI

Methods for chat communication:

```typescript
// Non-streaming
const response = await chatAPI.sendMessage(message);

// Streaming (SSE)
for await (const chunk of chatAPI.streamMessage(message)) {
  console.log(chunk.text);
  if (chunk.done) break;
}
```

### documentsAPI

Methods for document management:

```typescript
// Upload document
await documentsAPI.upload(file);

// List documents
const { documents } = await documentsAPI.list();

// Delete document
await documentsAPI.delete(documentId);
```

## Theme Configuration

Customizable Ant Design theme in `src/theme/antd-theme.ts`:

```typescript
export const theme: ThemeConfig = {
  token: {
    colorPrimary: '#1890ff',
    fontSize: 14,
    borderRadius: 6,
    // ... more tokens
  },
  components: {
    Button: { /* ... */ },
    Input: { /* ... */ },
    Card: { /* ... */ },
  },
};
```

## Accessibility (WCAG 2.0)

✅ **Keyboard Navigation** - All interactive elements accessible via keyboard
✅ **Screen Reader Support** - ARIA labels and roles throughout
✅ **Focus Management** - Visible focus indicators
✅ **Color Contrast** - Meets WCAG AA standards
✅ **Semantic HTML** - Proper heading hierarchy
✅ **Error Messaging** - Clear error states and messages

## TypeScript Configuration

Strict mode enabled with:
- `noImplicitAny: true`
- `strictNullChecks: true`
- `noUnusedLocals: true`
- `noUnusedParameters: true`

No `any` types allowed!

## Environment Variables

Create `.env` file:

```bash
# Backend API URL
VITE_API_BASE=http://localhost:8000

# Environment
VITE_ENV=development
```

## Scripts

```bash
# Development
pnpm dev              # Start dev server

# Build
pnpm build            # TypeScript check + build
pnpm preview          # Preview production build

# Linting
pnpm lint             # ESLint check
pnpm type-check       # TypeScript check only
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome)

## Dependencies

### Core
- `react` ^18.2.0
- `react-dom` ^18.2.0
- `antd` ^5.12.8
- `typescript` ^5.3.3

### State & Data
- `@tanstack/react-query` ^5.17.9
- `zustand` ^4.4.7
- `axios` ^1.6.5

### Utilities
- `react-markdown` ^9.0.1
- `dayjs` ^1.11.10
- `@ant-design/icons` ^5.2.6

## Development

### Code Style

- Follow Airbnb React style guide
- Use functional components with hooks
- Prefer const over let
- Use arrow functions
- Descriptive variable names

### Component Guidelines

1. One component per file
2. Props interface above component
3. Comprehensive JSDoc comments
4. Accessibility attributes
5. Error boundaries where needed

### Testing (TODO)

```bash
# Unit tests
pnpm test

# E2E tests
pnpm test:e2e
```

## Deployment

### Production Build

```bash
pnpm build
```

Output in `dist/` directory.

### Docker

```bash
# Build image
docker build -t rag-frontend:latest .

# Run container
docker run -p 80:80 rag-frontend:latest
```

## Troubleshooting

### Port Already in Use

Change port in `vite.config.ts`:

```typescript
server: {
  port: 3000, // or any other port
}
```

### API Connection Issues

Check `VITE_API_BASE` in `.env` and ensure backend is running.

### Type Errors

Run type check:

```bash
pnpm type-check
```

## Next Steps

- [ ] Add document upload UI
- [ ] Add settings page
- [ ] Add chat history persistence
- [ ] Add user authentication
- [ ] Add dark mode support
- [ ] Add unit tests
- [ ] Add E2E tests

## License

MIT


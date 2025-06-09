# ChatUI Artifact System Specification

**Version:** 1.0.0
**Status:** Draft Specification
**Purpose:** A production-ready, frontend-first streaming chat interface with extensible artifact support

## Table of Contents

1. [Introduction](#introduction)
2. [Problem Statement](#problem-statement)
3. [Architecture Overview](#architecture-overview)
4. [Core Concepts](#core-concepts)
5. [API Specifications](#api-specifications)
6. [Component Design](#component-design)
7. [Token Parsing Engine](#token-parsing-engine)
8. [Artifact System](#artifact-system)
9. [Panel-Based Artifacts](#panel-based-artifacts)
10. [State Management](#state-management)
11. [Implementation Guidelines](#implementation-guidelines)
12. [Extension Guide](#extension-guide)
13. [Usage Examples](#usage-examples)
14. [Performance Considerations](#performance-considerations)
15. [Security Considerations](#security-considerations)

## Introduction

The ChatUI Artifact System is a frontend-first solution for building streaming chat interfaces that can parse and render rich artifacts embedded in LLM responses. Unlike traditional approaches where the backend handles token classification, this system moves all display logic to the frontend, maintaining a clean separation of concerns.

### Key Principles

- **Frontend-First**: All display logic and token parsing happens in the browser
- **Streaming-First**: Designed for real-time token streaming with minimal latency
- **Extensible**: Easy to add new artifact types without backend changes
- **Type-Safe**: Full TypeScript support with comprehensive type definitions
- **Framework-Agnostic Backend**: Works with any backend that streams raw tokens
- **Performance-Optimized**: Efficient token buffering and parsing

## Problem Statement

Current chat implementations often suffer from:

1. **Backend Display Logic**: Servers parsing tokens for display purposes violates separation of concerns
2. **Tight Coupling**: Adding new artifact types requires coordinated backend/frontend changes
3. **Limited Flexibility**: Fixed artifact types determined by backend implementation
4. **Performance Overhead**: Redundant parsing and reconstruction of data structures
5. **Poor Developer Experience**: Complex coordination between backend and frontend teams

This specification addresses these issues by providing a clean, extensible architecture where the backend simply streams tokens and the frontend handles all presentation logic.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                          Frontend                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   ChatUI    │───▶│ TokenParser  │───▶│  Artifact    │  │
│  │  Component  │    │   Engine     │    │  Renderer    │  │
│  └─────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                     │         │
│         │                   │                     │         │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Message   │    │    Token     │    │   Artifact   │  │
│  │   Store     │    │   Buffer     │    │  Registry    │  │
│  └─────────────┘    └──────────────┘    └──────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Raw Token Stream
                              │
┌─────────────────────────────────────────────────────────────┐
│                          Backend                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌──────────────┐                      │
│  │     API     │───▶│     LLM      │                      │
│  │  Endpoint   │    │  Integration │                      │
│  └─────────────┘    └──────────────┘                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Core Concepts

### 1. Token Stream

A continuous stream of text tokens from the LLM, delivered via Server-Sent Events (SSE) or WebSocket.

```typescript
interface TokenEvent {
	token: string;
	// No classification or type information - just raw tokens
}
```

### 2. Artifact

A structured piece of content embedded within the chat stream, identified by delimiters.

```typescript
interface Artifact {
	id: string;
	type: string;
	content: string;
	metadata?: Record<string, any>;
	status: 'streaming' | 'complete' | 'error';
	renderLocation?: 'inline' | 'panel' | 'both'; // Where to render
}
```

### 3. Message Section

A portion of a message that can be either plain text or an artifact.

```typescript
type MessageSection = { type: 'text'; content: string } | { type: 'artifact'; artifact: Artifact };

interface Message {
	id: string;
	role: 'user' | 'assistant';
	sections: MessageSection[];
	timestamp: Date;
}
```

### 4. Artifact Parser

A parser that identifies and extracts artifacts from a token stream.

```typescript
interface ArtifactParser {
	name: string;
	startDelimiter: string | RegExp;
	endDelimiter: string | RegExp;
	parse: (content: string) => Partial<Artifact>;
}
```

## API Specifications

### Backend API

The backend should provide a simple streaming endpoint:

```typescript
// Request
POST /api/chat
Content-Type: application/json

{
  "messages": Message[],
  "options": {
    "model": string,
    "temperature": number,
    // ... other LLM options
  }
}

// Response (Server-Sent Events)
Content-Type: text/event-stream

data: {"token": "Hello"}
data: {"token": " "}
data: {"token": "world"}
data: {"token": "!"}
data: {"done": true}
```

### LLM Authentication & Provider Configuration

#### API Key Management

Different LLM providers require authentication via API keys. The backend should handle provider-specific authentication:

```typescript
// Environment variables for different providers
interface LLMProviderConfig {
	// OpenAI
	OPENAI_API_KEY?: string;

	// Anthropic
	ANTHROPIC_API_KEY?: string;

	// Google
	GOOGLE_API_KEY?: string;

	// Azure OpenAI
	AZURE_OPENAI_API_KEY?: string;
	AZURE_OPENAI_ENDPOINT?: string;

	// AWS Bedrock
	AWS_ACCESS_KEY_ID?: string;
	AWS_SECRET_ACCESS_KEY?: string;
	AWS_REGION?: string;

	// Cohere
	COHERE_API_KEY?: string;

	// Replicate
	REPLICATE_API_TOKEN?: string;
}
```

#### LiteLLM Integration Example

If using LiteLLM for multi-provider support:

```python
# Backend implementation example
import litellm
import os
from typing import AsyncGenerator

# Configure API keys
litellm.api_key = os.getenv("OPENAI_API_KEY")  # Default
litellm.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
litellm.cohere_key = os.getenv("COHERE_API_KEY")
# ... other provider keys

async def stream_chat_completion(
    messages: list,
    model: str = "gpt-4",
    **options
) -> AsyncGenerator[str, None]:
    """Stream tokens from LLM provider via LiteLLM"""

    try:
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            stream=True,
            **options
        )

        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:
        # Handle provider-specific errors
        yield f"Error: {str(e)}"
```

#### Model Configuration

The frontend can specify which model to use, but the backend validates available models:

```typescript
// Frontend request with model specification
{
  "messages": [...],
  "options": {
    "model": "claude-3-sonnet-20240229",  // Anthropic
    "temperature": 0.7,
    "max_tokens": 4000
  }
}

// Or OpenAI model
{
  "messages": [...],
  "options": {
    "model": "gpt-4-turbo-preview",  // OpenAI
    "temperature": 0.7
  }
}
```

#### Provider-Specific Configuration

```python
# Backend model validation and configuration
SUPPORTED_MODELS = {
    # OpenAI
    "gpt-4": {"provider": "openai", "requires": ["OPENAI_API_KEY"]},
    "gpt-4-turbo-preview": {"provider": "openai", "requires": ["OPENAI_API_KEY"]},
    "gpt-3.5-turbo": {"provider": "openai", "requires": ["OPENAI_API_KEY"]},

    # Anthropic
    "claude-3-opus-20240229": {"provider": "anthropic", "requires": ["ANTHROPIC_API_KEY"]},
    "claude-3-sonnet-20240229": {"provider": "anthropic", "requires": ["ANTHROPIC_API_KEY"]},
    "claude-3-haiku-20240307": {"provider": "anthropic", "requires": ["ANTHROPIC_API_KEY"]},

    # Google
    "gemini-pro": {"provider": "google", "requires": ["GOOGLE_API_KEY"]},

    # Local models (via Ollama, etc.)
    "llama2": {"provider": "ollama", "requires": []},
    "codellama": {"provider": "ollama", "requires": []},
}

def validate_model_access(model: str) -> bool:
    """Check if required API keys are available for the model"""
    if model not in SUPPORTED_MODELS:
        return False

    config = SUPPORTED_MODELS[model]
    required_keys = config.get("requires", [])

    return all(os.getenv(key) for key in required_keys)
```

#### Error Handling for Authentication

```typescript
// Backend error responses for authentication issues
data: {"error": "API key not configured for provider", "data_type": "error"}
data: {"error": "Invalid API key for OpenAI", "data_type": "error"}
data: {"error": "Rate limit exceeded", "data_type": "error"}
data: {"error": "Model not available", "data_type": "error"}
```

#### Security Considerations for API Keys

1. **Never expose API keys to the frontend**
2. **Use environment variables or secure key management**
3. **Implement rate limiting per API key**
4. **Monitor usage and costs**
5. **Rotate keys regularly**

```python
# Secure key management example
from cryptography.fernet import Fernet

class SecureKeyManager:
    def __init__(self):
        self.cipher = Fernet(os.getenv("ENCRYPTION_KEY"))

    def get_api_key(self, provider: str) -> str:
        encrypted_key = os.getenv(f"{provider.upper()}_API_KEY_ENCRYPTED")
        if encrypted_key:
            return self.cipher.decrypt(encrypted_key.encode()).decode()
        return os.getenv(f"{provider.upper()}_API_KEY")
```

### Frontend API

#### Main Component

```typescript
interface ChatUIProps {
	// Core props
	endpoint: string;
	headers?: Record<string, string>;

	// Artifact configuration
	parsers?: ArtifactParser[];
	artifactComponents?: Record<string, React.ComponentType<ArtifactProps>>;

	// UI customization
	className?: string;
	messageClassName?: string;
	inputClassName?: string;

	// Callbacks
	onMessage?: (message: Message) => void;
	onArtifact?: (artifact: Artifact) => void;
	onError?: (error: Error) => void;

	// Options
	autoScroll?: boolean;
	showTimestamps?: boolean;
	allowFileUploads?: boolean;
}
```

#### Token Parser Engine

```typescript
class TokenParserEngine {
	constructor(parsers: ArtifactParser[]);

	// Process incoming tokens
	processToken(token: string): ParseResult;

	// Get current parsing state
	getState(): ParserState;

	// Reset parser state
	reset(): void;
}

interface ParseResult {
	sections: MessageSection[];
	buffered: string;
	activeParser?: ArtifactParser;
}
```

## Component Design

### Component Hierarchy

```
<ChatUI>
  <MessageList>
    <Message>
      <MessageSection>
        <TextContent />
        <ArtifactRenderer>
          <CustomArtifactComponent />
        </ArtifactRenderer>
      </MessageSection>
    </Message>
  </MessageList>
  <InputArea>
    <TextInput />
    <SendButton />
    <FileUpload />
  </InputArea>
</ChatUI>
```

### Key Components

#### ChatUI (Main Container)

- Manages WebSocket/SSE connection
- Coordinates token parsing
- Handles message state
- Provides context to child components

#### TokenParserEngine

- Maintains parsing state
- Identifies artifact boundaries
- Buffers incomplete tokens
- Yields parsed sections

#### ArtifactRenderer

- Looks up appropriate component for artifact type
- Handles artifact lifecycle (streaming → complete)
- Provides error boundaries
- Manages artifact-specific state

## Token Parsing Engine

### Algorithm

```typescript
class TokenParserEngine {
	private buffer: string = '';
	private sections: MessageSection[] = [];
	private activeParser: ArtifactParser | null = null;
	private artifactContent: string = '';

	processToken(token: string): ParseResult {
		this.buffer += token;

		while (this.buffer.length > 0) {
			if (this.activeParser) {
				// Currently parsing an artifact
				const endMatch = this.findDelimiter(this.buffer, this.activeParser.endDelimiter);

				if (endMatch) {
					// Artifact complete
					this.artifactContent += this.buffer.slice(0, endMatch.index);
					this.completeArtifact();
					this.buffer = this.buffer.slice(endMatch.end);
				} else {
					// Continue buffering artifact content
					this.artifactContent += this.buffer;
					this.buffer = '';
				}
			} else {
				// Looking for artifact start
				const startMatch = this.findAnyStartDelimiter(this.buffer);

				if (startMatch) {
					// Found artifact start
					if (startMatch.index > 0) {
						// Add text before artifact
						this.addTextSection(this.buffer.slice(0, startMatch.index));
					}
					this.activeParser = startMatch.parser;
					this.buffer = this.buffer.slice(startMatch.end);
					this.startArtifact();
				} else if (this.canFlushBuffer()) {
					// No partial delimiters, flush as text
					this.addTextSection(this.buffer);
					this.buffer = '';
				} else {
					// Might be start of delimiter, keep buffering
					break;
				}
			}
		}

		return {
			sections: [...this.sections],
			buffered: this.buffer,
			activeParser: this.activeParser
		};
	}
}
```

### Buffer Management

The parser must handle partial delimiter matching:

```typescript
private canFlushBuffer(): boolean {
  // Check if buffer could be start of any delimiter
  for (const parser of this.parsers) {
    const delimiter = parser.startDelimiter.toString();
    if (delimiter.startsWith(this.buffer)) {
      return false; // Keep buffering
    }
  }
  return true; // Safe to flush
}
```

## Artifact System

### Built-in Artifact Types

#### Code Block

````typescript
const codeBlockParser: ArtifactParser = {
	name: 'code',
	startDelimiter: /```(\w*)\n/,
	endDelimiter: '\n```',
	parse: (content, metadata) => ({
		type: 'code',
		metadata: {
			language: metadata.groups?.[1] || 'plaintext'
		}
	})
};
````

#### Custom Tag

```typescript
const createTagParser = (tagName: string): ArtifactParser => ({
	name: tagName,
	startDelimiter: `<${tagName}>`,
	endDelimiter: `</${tagName}>`,
	parse: (content) => ({
		type: tagName,
		content: content.trim()
	})
});
```

### Artifact Component Interface

```typescript
interface ArtifactProps {
  artifact: Artifact;
  isStreaming: boolean;
  onUpdate?: (content: string) => void;
}

// Example implementation
const CodeArtifact: React.FC<ArtifactProps> = ({
  artifact,
  isStreaming
}) => {
  const language = artifact.metadata?.language || 'plaintext';

  return (
    <div className="artifact-code">
      {isStreaming && <StreamingIndicator />}
      <SyntaxHighlighter language={language}>
        {artifact.content}
      </SyntaxHighlighter>
    </div>
  );
};
```

## Panel-Based Artifacts

### Overview

In addition to inline artifacts (rendered within chat messages), the ChatUI system supports **panel artifacts** - artifacts that render in a separate panel beside the chat. This enables building interfaces where:

- Code editors persist alongside the conversation
- Documents can be viewed and edited while chatting
- Visualizations update in real-time based on chat interactions
- Multiple artifacts can be tabbed or stacked in the side panel

### Architecture for Panel Artifacts

```typescript
interface PanelArtifact extends Artifact {
	panelId: string;
	panelTitle?: string;
	panelPosition?: 'right' | 'left' | 'bottom';
	isPersistent?: boolean; // Stays open across messages
	isEditable?: boolean; // User can edit the artifact
}

interface ChatUIProps {
	// ... existing props ...

	// Panel configuration
	enableArtifactPanel?: boolean;
	panelPosition?: 'right' | 'left' | 'bottom';
	panelWidth?: string | number;
	onPanelArtifactUpdate?: (artifact: PanelArtifact, newContent: string) => void;
}
```

### Rendering Strategies

#### 1. Inline vs Panel Decision

Artifacts can specify their preferred rendering location:

```typescript
const createPanelTagParser = (tagName: string): ArtifactParser => ({
	name: tagName,
	startDelimiter: `<${tagName} panel="true">`,
	endDelimiter: `</${tagName}>`,
	parse: (content) => ({
		type: tagName,
		content: content.trim(),
		renderLocation: 'panel', // Key difference
		panelTitle: tagName.charAt(0).toUpperCase() + tagName.slice(1)
	})
});
```

#### 2. Hybrid Rendering

Some artifacts can render both inline (preview) and in panel (full):

````typescript
const codeBlockParser: ArtifactParser = {
	name: 'code',
	startDelimiter: /```(\w*)\s*(panel)?\n/,
	endDelimiter: '\n```',
	parse: (content, metadata) => ({
		type: 'code',
		content: content.trim(),
		renderLocation: metadata.groups?.[2] ? 'both' : 'inline',
		metadata: {
			language: metadata.groups?.[1] || 'plaintext'
		}
	})
};
````

### Panel Management

```typescript
interface ArtifactPanelState {
	activeArtifacts: PanelArtifact[];
	selectedArtifactId: string | null;
	panelOpen: boolean;
}

class ArtifactPanelStore {
	private state: ArtifactPanelState;

	// Add artifact to panel
	addPanelArtifact(artifact: PanelArtifact): void;

	// Update artifact content (for editable artifacts)
	updateArtifactContent(id: string, content: string): void;

	// Remove artifact from panel
	removeArtifact(id: string): void;

	// Select active artifact (for tabbed interface)
	selectArtifact(id: string): void;
}
```

### Component Structure for Panel Layout

```
<ChatUIContainer>
  <ChatSection>
    <ChatUI>
      <MessageList>
        <Message>
          <InlineArtifact />  <!-- Rendered in chat -->
          <PanelArtifactRef /> <!-- Shows "View in panel →" -->
        </Message>
      </MessageList>
      <InputArea />
    </ChatUI>
  </ChatSection>

  <ArtifactPanel position="right" width="50%">
    <ArtifactTabs>
      <ArtifactTab id="artifact1" title="Code" />
      <ArtifactTab id="artifact2" title="Diagram" />
    </ArtifactTabs>
    <ArtifactContent>
      <PanelArtifactRenderer artifact={selectedArtifact} />
    </ArtifactContent>
  </ArtifactPanel>
</ChatUIContainer>
```

### Example: Editable Code Artifact

```typescript
// Parser for editable code blocks
const editableCodeParser: ArtifactParser = {
  name: 'editor',
  startDelimiter: '<editor language="\\w+">',
  endDelimiter: '</editor>',
  parse: (content, metadata) => ({
    type: 'code-editor',
    content: content.trim(),
    renderLocation: 'panel',
    isEditable: true,
    panelTitle: 'Code Editor',
    metadata: {
      language: extractLanguageFromTag(metadata)
    }
  })
};

// Component for panel rendering
const CodeEditorArtifact: React.FC<PanelArtifactProps> = ({
  artifact,
  isStreaming,
  onUpdate
}) => {
  return (
    <MonacoEditor
      value={artifact.content}
      language={artifact.metadata?.language}
      onChange={(value) => onUpdate?.(value)}
      options={{
        readOnly: isStreaming || !artifact.isEditable
      }}
    />
  );
};
```

### Usage Examples

#### Basic Panel Artifact

```typescript
// In your LLM prompt/response:
"I'll create a React component for you:

<component panel='true'>
function HelloWorld() {
  return <h1>Hello, World!</h1>;
}
</component>

This component renders a simple greeting."

// Renders: inline reference in chat + full component in side panel
```

#### Editable Document

```typescript
// LLM response with editable artifact
"I've created a markdown document you can edit:

<document panel='true' editable='true'>
# Project README

## Overview
Your project description here...

## Installation
`npm install`

## Usage
Edit this document as needed!
</document>

Feel free to modify the document in the panel."
```

### State Synchronization

For editable panel artifacts, maintain synchronization between chat and panel:

```typescript
const ChatWithPanels: React.FC = () => {
  const [panelArtifacts, setPanelArtifacts] = useState<PanelArtifact[]>([]);

  const handleArtifact = (artifact: Artifact) => {
    if (artifact.renderLocation === 'panel' || artifact.renderLocation === 'both') {
      setPanelArtifacts(prev => [...prev, artifact as PanelArtifact]);
    }
  };

  const handlePanelUpdate = (artifactId: string, newContent: string) => {
    // Update artifact content
    setPanelArtifacts(prev =>
      prev.map(a => a.id === artifactId ? {...a, content: newContent} : a)
    );

    // Optionally send update back to chat/backend
    sendArtifactUpdate(artifactId, newContent);
  };

  return (
    <div className="chat-with-panels">
      <ChatUI
        onArtifact={handleArtifact}
        enableArtifactPanel={true}
      />
      <ArtifactPanel
        artifacts={panelArtifacts}
        onUpdate={handlePanelUpdate}
      />
    </div>
  );
};
```

### Panel Features

1. **Tab Management** - Multiple artifacts in tabs
2. **Resize Handle** - Adjustable panel width
3. **Maximize/Minimize** - Full screen artifact view
4. **Export/Download** - Save artifact content
5. **Diff View** - Show changes for editable artifacts
6. **Split View** - Multiple artifacts side by side

## State Management

### Message Store

```typescript
interface ChatState {
	messages: Message[];
	currentMessage: Partial<Message> | null;
	isStreaming: boolean;
	error: Error | null;
}

class MessageStore {
	private state: ChatState;
	private subscribers: Set<(state: ChatState) => void>;

	// Add user message
	addUserMessage(content: string): void;

	// Start assistant message
	startAssistantMessage(): void;

	// Update current message with new sections
	updateCurrentMessage(sections: MessageSection[]): void;

	// Complete current message
	completeCurrentMessage(): void;

	// Subscribe to state changes
	subscribe(callback: (state: ChatState) => void): () => void;
}
```

### Streaming State

```typescript
interface StreamingState {
	isConnected: boolean;
	isStreaming: boolean;
	reconnectAttempts: number;
	lastError: Error | null;
}
```

## Implementation Guidelines

### 1. Project Structure

```
chatui/
├── src/
│   ├── components/
│   │   ├── ChatUI.tsx
│   │   ├── Message.tsx
│   │   ├── MessageSection.tsx
│   │   ├── InputArea.tsx
│   │   └── artifacts/
│   │       ├── ArtifactRenderer.tsx
│   │       ├── CodeArtifact.tsx
│   │       └── index.ts
│   ├── parsers/
│   │   ├── TokenParserEngine.ts
│   │   ├── ArtifactParser.ts
│   │   └── defaultParsers.ts
│   ├── stores/
│   │   ├── MessageStore.ts
│   │   └── StreamingStore.ts
│   ├── hooks/
│   │   ├── useChat.ts
│   │   ├── useStreaming.ts
│   │   └── useArtifacts.ts
│   └── types/
│       └── index.ts
├── package.json
└── README.md
```

### 2. Package Dependencies

```json
{
	"name": "@your-org/chatui",
	"version": "1.0.0",
	"peerDependencies": {
		"react": "^18.0.0",
		"react-dom": "^18.0.0"
	},
	"dependencies": {
		"nanoid": "^4.0.0",
		"eventsource-parser": "^1.0.0"
	},
	"devDependencies": {
		"typescript": "^5.0.0",
		"@types/react": "^18.0.0",
		"vite": "^4.0.0"
	}
}
```

### 3. Core Implementation Steps

1. **Set up TypeScript types** - Define all interfaces and types
2. **Implement TokenParserEngine** - Core parsing logic with buffer management
3. **Create MessageStore** - State management for messages
4. **Build streaming connection** - SSE/WebSocket handling with reconnection
5. **Implement base components** - ChatUI, Message, MessageSection
6. **Add artifact system** - ArtifactRenderer and default artifacts
7. **Create React hooks** - useChat, useStreaming, useArtifacts
8. **Add error handling** - Comprehensive error boundaries and recovery
9. **Implement testing** - Unit tests for parser, integration tests for components
10. **Documentation** - API docs, usage examples, and guides

## Extension Guide

### Adding Custom Artifacts

````typescript
// 1. Define the parser
const mermaidParser: ArtifactParser = {
  name: 'mermaid',
  startDelimiter: '```mermaid\n',
  endDelimiter: '\n```',
  parse: (content) => ({
    type: 'mermaid',
    content: content.trim()
  })
};

// 2. Create the component
const MermaidArtifact: React.FC<ArtifactProps> = ({
  artifact,
  isStreaming
}) => {
  const [svg, setSvg] = useState<string>('');

  useEffect(() => {
    if (!isStreaming && artifact.content) {
      mermaid.render('mermaid-' + artifact.id, artifact.content)
        .then(result => setSvg(result.svg));
    }
  }, [artifact, isStreaming]);

  return (
    <div className="artifact-mermaid">
      {isStreaming ? (
        <div>Rendering diagram...</div>
      ) : (
        <div dangerouslySetInnerHTML={{ __html: svg }} />
      )}
    </div>
  );
};

// 3. Register with ChatUI
<ChatUI
  parsers={[mermaidParser]}
  artifactComponents={{
    mermaid: MermaidArtifact
  }}
/>
````

### Custom Styling

```typescript
// Via CSS classes
<ChatUI
  className="my-chat"
  messageClassName="my-message"
  inputClassName="my-input"
/>

// Via theme provider
<ChatUIThemeProvider theme={customTheme}>
  <ChatUI />
</ChatUIThemeProvider>
```

## Usage Examples

### Basic Usage

```typescript
import { ChatUI } from '@your-org/chatui';

function App() {
  return (
    <ChatUI
      endpoint="/api/chat"
      headers={{
        'Authorization': 'Bearer token'
      }}
    />
  );
}
```

### With Custom Artifacts

```typescript
import { ChatUI, createTagParser } from '@your-org/chatui';
import { SqlArtifact, ChartArtifact } from './artifacts';

function App() {
  return (
    <ChatUI
      endpoint="/api/chat"
      parsers={[
        createTagParser('sql'),
        createTagParser('chart')
      ]}
      artifactComponents={{
        sql: SqlArtifact,
        chart: ChartArtifact
      }}
      onArtifact={(artifact) => {
        console.log('New artifact:', artifact);
      }}
    />
  );
}
```

### Advanced Configuration

```typescript
import { ChatUI, MessageStore } from '@your-org/chatui';

function App() {
  const messageStore = new MessageStore({
    maxMessages: 100,
    persistKey: 'chat-history'
  });

  return (
    <ChatUI
      endpoint="/api/chat"
      messageStore={messageStore}
      reconnectOptions={{
        maxAttempts: 5,
        delay: 1000,
        backoff: 2
      }}
      streamingOptions={{
        parser: 'eventsource', // or 'websocket'
        timeout: 30000
      }}
    />
  );
}
```

## Performance Considerations

### 1. Token Buffering

- Use efficient string concatenation (avoid creating new strings unnecessarily)
- Implement circular buffer for large streams
- Clear buffers after parsing to prevent memory leaks

### 2. Rendering Optimization

- Use React.memo for Message components
- Implement virtual scrolling for long conversations
- Debounce rapid token updates
- Use CSS transforms for smooth scrolling

### 3. Parser Efficiency

- Pre-compile regular expressions
- Use early exit strategies in parsing loops
- Implement parser result caching
- Consider Web Workers for heavy parsing

### 4. Memory Management

```typescript
// Implement message pruning
const MAX_MESSAGES = 100;

function pruneMessages(messages: Message[]): Message[] {
	if (messages.length <= MAX_MESSAGES) return messages;
	return messages.slice(-MAX_MESSAGES);
}
```

## Security Considerations

### 1. Content Sanitization

```typescript
// Sanitize HTML in artifacts
import DOMPurify from 'dompurify';

const sanitizeContent = (content: string): string => {
	return DOMPurify.sanitize(content, {
		ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
		ALLOWED_ATTR: ['href']
	});
};
```

### 2. XSS Prevention

- Never use dangerouslySetInnerHTML with user content
- Sanitize all artifact content before rendering
- Use Content Security Policy headers
- Validate artifact types against whitelist

### 3. Connection Security

- Always use HTTPS for streaming endpoints
- Implement token refresh for long-running connections
- Validate server certificates
- Use secure WebSocket (wss://) connections

### 4. Rate Limiting

```typescript
// Client-side rate limiting
const rateLimiter = {
	attempts: 0,
	resetTime: Date.now(),

	canSend(): boolean {
		if (Date.now() - this.resetTime > 60000) {
			this.attempts = 0;
			this.resetTime = Date.now();
		}
		return this.attempts++ < 30; // 30 messages per minute
	}
};
```

## Conclusion

The ChatUI Artifact System provides a robust, extensible foundation for building sophisticated chat interfaces with rich content rendering. By moving all display logic to the frontend and maintaining a clean separation of concerns, it enables rapid development and easy customization while maintaining high performance and security standards.

This specification serves as a complete guide for implementing the system from scratch or integrating it into existing applications. The modular architecture ensures that teams can adopt it incrementally and extend it to meet their specific needs.

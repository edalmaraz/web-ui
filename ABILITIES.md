# Web UI Capabilities and Features

## Core Features

### User Interface
- **Gradio-based Web Interface**
  - Multiple theme support:
    - Default
    - Soft
    - Ocean
    - Citrus
    - Glass
    - Monochrome
    - Origin
  - Real-time streaming updates
  - Interactive UI elements
  - Configuration persistence

### Agent System
- **Multiple Agent Types**
  - Browser Agent
  - Organization Agent
  - Custom Agent
  - Research Agent

- **Agent Configuration**
  - Maximum steps control
  - Vision capability toggle
  - Maximum actions per step
  - Tool calling method selection
  - Custom prompts support
  - Agent state management
  - History tracking and persistence

## LLM Integration
The web UI supports multiple Large Language Models (LLMs) through a unified interface:

### Supported LLM Providers
- **OpenAI**
  - Support for GPT models
  - Configurable API endpoint and key
  - Temperature control for response variation

- **Azure OpenAI**
  - Enterprise-grade OpenAI deployment
  - Custom endpoint configuration
  - API version control

- **Google (Gemini)**
  - Access to Gemini models
  - Flash thinking experimental models
  - API key configuration

- **Anthropic**
  - Claude model support
  - Custom endpoint configuration

- **DeepSeek**
  - DeepSeek Chat models
  - DeepSeek-R1 models with custom implementation
  - Custom endpoint and API key support
  - Special R1 chat optimization

- **Mistral AI**
  - Access to Mistral models
  - Custom endpoint configuration

- **Ollama**
  - Local model deployment
  - Support for multiple model types including DeepSeek-R1
  - Custom endpoint configuration (default: localhost:11434)
  - Specialized DeepSeek-R1 Ollama integration

## Browser Automation Features

### Browser Configuration
- Custom Chrome path support
- User data directory configuration
- Debugging port and host settings
- Persistent session option
- Window size customization
- Security settings toggle
- Headless mode support

### Browser Capabilities
- **Custom Browser Integration**
  - Use your own Chrome browser
  - Maintain existing login sessions
  - Access to browser history
  - Support for custom user profiles
  - Chrome DevTools Protocol integration
  - Clipboard operations (copy/paste)
  - Main content extraction

- **Parallel Browser Sessions**
  - Multiple concurrent browser instances
  - Independent context for each session
  - Shared or isolated user data
  - Session persistence management

- **Vision Support**
  - Optional vision capabilities
  - Screen capture and analysis
  - Image-based interaction
  - Screenshot capture and saving
  - Base64 image encoding support

## Deep Research Capabilities
- **Automated Research**
  - Task-based research execution
  - UUID-based task tracking
  - Configurable search iterations
  - Multiple query support per iteration
  - Automatic save directory management

- **Research Output**
  - Report generation
  - PDF document handling
  - History information collection
  - Error handling and recovery
  - Custom browser integration for research

- **Search Configuration**
  - Maximum query number per iteration
  - Search iteration control
  - Custom save directory specification
  - Progress tracking and reporting

## Recording and Debugging
- **Session Recording**
  - Video recording of browser sessions
  - Configurable recording paths
  - Trace path saving
  - Agent history recording

- **Debugging Features**
  - Comprehensive logging system
    - Multiple log levels (debug, info, result)
    - Configurable logging verbosity
  - Playwright trace support
  - Error tracking and reporting

## File Management
- **Save Functionality**
  - Automatic directory creation
  - UUID-based file organization
  - Multiple file format support
  - Configuration file management

- **Configuration Management**
  - Default configuration settings
  - Configuration file loading/saving
  - Current configuration persistence
  - UI state synchronization

## Security Features
- **Authentication**
  - Secure API key management
  - Environment-based configuration
  - VNC password protection
  - Isolated browser contexts

- **Browser Security**
  - Optional security controls
  - Sandboxed execution
  - User data protection
  - Session isolation

## Integration Capabilities
- **Environment Management**
  - Environment variable support
  - Dotenv configuration
  - Custom endpoint configuration
  - Flexible API integration

- **External Tools**
  - Playwright integration
  - LangChain integration
  - JSON repair utilities
  - Base64 encoding support

## Testing Framework
- **Test Suites**
  - LLM API testing
  - Browser automation testing
  - Deep research testing
  - Playwright integration
  - Custom agent testing
  - Message handling tests

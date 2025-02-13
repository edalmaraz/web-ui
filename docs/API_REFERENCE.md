# API Reference

## Core Components

### BrowserContext
```typescript
interface BrowserContext {
    // Properties
    page: Page;
    context: Context;
    
    // Methods
    initialize(): Promise<void>;
    get_current_page(): Promise<Page>;
    new_page(): Promise<Page>;
    close(): Promise<void>;
}
```

### ActionResult
```typescript
interface ActionResult {
    extracted_content: string | object;
    error?: string;
    success: boolean;
}
```

### FunctionRegistry
```typescript
interface FunctionRegistry {
    // Properties
    functions: Map<string, Function>;
    
    // Methods
    register(name: string, requires_browser?: boolean): Function;
    get_function(name: string): Function;
    list_functions(): string[];
}
```

## Function Categories

### Browser Control

#### go_to_url
```typescript
async function go_to_url(
    browser: BrowserContext,
    url: string,
    options?: {
        timeout?: number;
        waitUntil?: 'load' | 'domcontentloaded' | 'networkidle';
    }
): Promise<ActionResult>
```

#### click_element
```typescript
async function click_element(
    browser: BrowserContext,
    selector: string,
    options?: {
        button?: 'left' | 'right' | 'middle';
        clickCount?: number;
        delay?: number;
    }
): Promise<ActionResult>
```

### Content Extraction

#### perform_ocr
```typescript
async function perform_ocr(
    browser: BrowserContext,
    selector?: string,
    options?: {
        lang?: string;
        preprocessing?: boolean;
        timeout?: number;
    }
): Promise<ActionResult>
```

#### extract_tables_from_image
```typescript
async function extract_tables_from_image(
    image_path: string,
    options?: {
        min_confidence?: number;
        preprocessing?: boolean;
    }
): Promise<ActionResult>
```

### Media Processing

#### convert_speech_to_text
```typescript
async function convert_speech_to_text(
    browser: BrowserContext,
    audio_selector: string,
    options?: {
        language?: string;
        model?: string;
    }
): Promise<ActionResult>
```

#### extract_faces
```typescript
async function extract_faces(
    browser: BrowserContext,
    selector?: string,
    options?: {
        min_confidence?: number;
        return_landmarks?: boolean;
    }
): Promise<ActionResult>
```

### AI Integration

#### image_to_text_with_gpt_vision
```typescript
async function image_to_text_with_gpt_vision(
    browser: BrowserContext,
    selector?: string,
    options?: {
        prompt?: string;
        max_tokens?: number;
        temperature?: number;
    }
): Promise<ActionResult>
```

## Events

### NetworkEvent
```typescript
interface NetworkEvent {
    type: 'request' | 'response';
    url: string;
    method: string;
    headers: Record<string, string>;
    body?: string;
    timestamp: number;
}
```

### BrowserEvent
```typescript
interface BrowserEvent {
    type: 'navigation' | 'domcontentloaded' | 'load';
    url: string;
    timestamp: number;
}
```

## Custom Types

### ImageProcessingOptions
```typescript
interface ImageProcessingOptions {
    preprocessing?: boolean;
    enhance_contrast?: boolean;
    denoise?: boolean;
    sharpen?: boolean;
    threshold?: number;
}
```

### BrowserProfile
```typescript
interface BrowserProfile {
    name: string;
    settings: {
        javascript_enabled?: boolean;
        cookies_enabled?: boolean;
        proxy?: string;
        user_agent?: string;
    };
}
```

### OCRResult
```typescript
interface OCRResult {
    text: string;
    confidence: number;
    bounding_box?: {
        x: number;
        y: number;
        width: number;
        height: number;
    };
}
```

## Error Types

### BrowserError
```typescript
class BrowserError extends Error {
    constructor(
        message: string,
        public readonly code: string,
        public readonly details?: object
    );
}
```

### FunctionError
```typescript
class FunctionError extends Error {
    constructor(
        message: string,
        public readonly function_name: string,
        public readonly details?: object
    );
}
```

## Configuration

### SystemConfig
```typescript
interface SystemConfig {
    browser: {
        executable_path?: string;
        default_viewport?: {
            width: number;
            height: number;
        };
        timeout: number;
    };
    ocr: {
        default_language: string;
        preprocessing: boolean;
    };
    ai: {
        openai_api_key?: string;
        default_model: string;
    };
}
```

## Utility Types

### Selector
```typescript
type Selector = string | {
    css?: string;
    xpath?: string;
    text?: string;
};
```

### TimeoutOptions
```typescript
interface TimeoutOptions {
    timeout?: number;
    interval?: number;
    max_tries?: number;
}
```

### CallbackFunction
```typescript
type CallbackFunction = (
    event: any,
    context?: any
) => Promise<void> | void;
```

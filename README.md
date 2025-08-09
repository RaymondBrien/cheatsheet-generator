# cheatsheet-generator

[![Tests](https://github.com/RaymondBrien/cheatsheet-generator/actions/workflows/tests.yml/badge.svg)](https://github.com/RaymondBrien/cheatsheet-generator/actions/workflows/tests.yml)

A dynamic cheatsheet generator which generates self-validating cheatsheets for tools specified in a topic-subtopic structure.

> [!TIP]
> To run via CLI:
> ```bash
> python cli.py --topic <TOPIC>
> ```

> [!IMPORTANT]
> **Environment Setup:**
> 1. Copy `.env.template` to `.env` (or create `.env` manually)
> 2. Add your Anthropic API key: `ANTHROPIC_API_KEY=sk-ant-...`
> 3. The system will automatically load your API key from `.env`

## Features:
- safe generated files
- configurable calls to different LLM clients
- robust environment variable loading with fallbacks
- automatic .env file detection and loading

## Design:
```mermaid
flowchart TD
    A[Start: main.py] --> B[Initialize Anthropic Client]
    B --> C[Load Prompt Configuration]
    C --> D[Load Topic YAML Files]

    D --> E[Parse Topic Structure]
    E --> F[Validate Topic/Subtopic]

    F --> G[Build Prompt with Context]
    G --> H[Configure API Parameters]
    H --> I[Make Claude API Call]

    I --> J{API Response Success?}
    J -->|Yes| K[Parse Response Content]
    J -->|No| L[Handle Error]

    K --> M[Validate Token Length]
    M --> N[Format Output]
    N --> O[Save to Output Directory]

    L --> P[Log Error & Retry]
    P --> I

    O --> Q[Generate Cheatsheet Files]
    Q --> R[End]

    subgraph "Configuration"
        C1[API_CONFIG.py] --> C
        C2[prompt_config.py] --> C
        C3[topics/*.yml] --> D
    end

    subgraph "Prompt Building"
        G1[Role Definition] --> G
        G2[Topic Context] --> G
        G3[Format Instructions] --> G
    end

    subgraph "Output Processing"
        O1[cheatsheets/] --> O
        O2[transcripts/] --> O
        O3[transcript-audio/] --> O
    end

    subgraph "Utilities"
        U1[parse_yaml.py] --> E
        U2[file_management.py] --> O
        U3[command_validator.py] --> F
        U4[api_calls.py] --> I
    end
```

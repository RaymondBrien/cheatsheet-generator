# TODO - Cheatsheet Generator Improvements

## 🚀 High Priority - Core Functionality
[ ] Templating: this will be helpful for cheatsheets but also for theoryhub very quick resource generation.

- seperate subrepo
- tests
- design
- components
- cookiecutter/copier?
- jinja
- first template
- make more abstract
- reduce deps
- make separate to add as dep for other projects


components:

general design:
- header
- footer
- colors
- logo

sections:
- title
- topic
- tagline
- dividers
- subtopic
- examples
- tables

data:
- date
- sources
- copyright
- version number




[ ] makefile create template topic card with subtopics - or cookiecutter
[ ] utils function for compressing all wav files, put in zip
[ ] try latest whisper open ai text to voice
[x] request a second response (or two parts of one response for single api call) which returns an accompanying voiceover-script
[ ] save transcript and voiecover recording in same designated subdir as cheatsheet, once validated
[ ] identify points to learn more about async and shared state protection
[ ] update docs for clear entry points, features and how to use
[ ] add async, with unit tests
[ ] each topic should have its own dir - requires some refactoring later
[ ] sort voiceoverscript subdir vs transcripts - is some code only expecting one and then writing it to voiceover-scripts instead? Just keep voiceover_scripts
[ ] trial template engines?: https://yte-template-engine.github.io/

## 🧪 Today's Testing Tasks
[ ] Write unit tests for api_utils functions
[ ] Add error handling for API failures
[ ] Test nightly? - how does that work?
[ ] build?

## 🏗️ Architecture & Design Improvements
[ ] Implement dependency injection pattern
[ ] Create service layer abstraction for API calls
[ ] Separate configuration management from business logic
[ ] Implement proper logging system with structured logging
[ ] Add health checks and monitoring endpoints
[x] Create abstract base classes for extensibility
[x] Refactor so that I don't need a topic file in order to call this, we could just have a string 'bash', and remove the irrelevant sections of the main prompt text
[ ] new cheatsheet for each subtopic - how are these enumerated? Or one cheatsheet per topic split into each subtopics.


## 🛡️ Error Handling & Resilience
[ ] Add retry mechanisms with exponential backoff for API calls
[ ] Create circuit breaker pattern for API failures
[ ] Add input validation and sanitization
[ ] Implement graceful degradation when services are unavailable

## ⚙️ Configuration & Environment Management
[ ] Create centralized configuration management
[ ] Add environment-specific configuration files
[ ] Implement secrets management for API keys
[ ] Add configuration validation
[ ] Create configuration hot-reloading capability

## 🧪 Testing & Quality Assurance
[ ] Add comprehensive unit tests with 90%+ coverage
[ ] Implement automated security testing

## 📊 Monitoring & Observability
[ ] Add structured logging with correlation IDs (blackboard with agents, messages carrying trace id's)
[ ] Implement metrics collection (API response times, success rates)
[ ] Add alerting for critical failures
[ ] Implement audit logging for compliance

## 🚀 Performance & Scalability
[ ] Add async/await for I/O operations
[ ] Implement connection pooling for API clients
[ ] Add rate limiting and throttling
[ ] Optimize memory usage for large responses
[ ] Add horizontal scaling capabilities

## 🔒 Security & Compliance
[ ] Implement secure API key management
[ ] Implement rate limiting to prevent abuse
[ ] Add audit trails for all operations
[ ] Implement least privilege access controls
[ ] Add security scanning in CI/CD

## 📦 DevOps & Deployment
[ ] test autoruns from gh workflows
[ ] run CI tests on each push
[ ] Add comprehensive CI/CD pipeline
[ ] Implement blue-green deployment strategy
[ ] Add automated dependency updates
[ ] Add automated rollback capabilities

## 📚 Documentation & Standards
[ ] Add comprehensive API documentation
[ ] Create architecture decision records (ADRs)
[ ] Add code documentation and examples
[ ] Create user guides and tutorials
[ ] Implement OpenAPI/Swagger documentation
[ ] Add contribution guidelines

## 🎯 Code Quality & Standards
[ ] Implement pre-commit hooks for ruff
[ ] Add code complexity analysis
[ ] Create coding standards document

## 🔄 Data Management
[ ] add a series of topic files 
[ ] Implement data validation schemas
[ ] Add data migration capabilities
[ ] Implement backup and recovery procedures
[ ] Add data versioning for topic files
[ ] Create data export/import functionality

## 🎨 User Experience
[ ] Add progress indicators for long-running operations
[ ] Implement user-friendly error messages
[ ] Add interactive CLI with rich formatting
[ ] Create web interface for non-technical users
[ ] Add export options (PDF, HTML, etc.)
[ ] Implement user preferences and customization

## 🔧 Maintenance & Technical Debt
[ ] Refactor main.py to follow single responsibility principle
[ ] Extract hardcoded values to configuration
[ ] Remove unused imports and dead code
[ ] Optimize imports and reduce startup time
[ ] Add code coverage reporting
[ ] Implement automated dependency vulnerability scanning


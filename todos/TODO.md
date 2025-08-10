# TODO - Cheatsheet Generator Improvements

## 🚀 High Priority - Core Functionality

[x] send basic prompt
[x] test api connection first
[x] send first request for bash cheatsheet
[x] save received response in outputs/cheatsheets (mocked up with yaml so do markdown version later, just save a file first)
[ ] makefile create template topic card with subtopics - or cookiecutter
[x] poetry for easier deps management
[x] validate each command?
[x] request a second response (or two parts of one response for single api call) which returns an accompanying voiceover-script
[ ] check cheatsheets are uploaded correctly and saved in correct location 
[ ] git commit and push cheatsheet pdf once completed
[x] local tool that renders an mp3 of text-to-voice recording of transcript?
[ ] save transcript and voiecover recording in same designated subdir as cheatsheet, once validated
[ ] identify points to learn more about async and shared state protection
[ ] start to make faster now!
[ ] update docs and add async testing
[ ] find all areas to reduce DRY, use async and speed up process, multithreading and multiprocessing could be good here: multithreading for API request whilst doing the prep of file names etc, multiprocessing to then make the files, move them and generate the audio after, as well as another thread to upload. Discover how to test timings so I can see if doing async/multi[thread/processing] makes an impact on timing. Also httpio async version (what's it called?) will help here possibly - op to learn!
[ ] each topic should have its own dir - requires some refactoring later
[ ] sort voiceoverscript subdir vs transcripts - is some code only expecting one and then writing it to voiceover-scripts instead? Just keep voiceover_scripts

## 🧪 Today's Testing Tasks
[x] Fix API error in main.py (client.responses.create doesn't exist)
[x] Add dry run validation for prompt content
[x] Create CLI interface for easier testing
[x] Test dry run mode to validate prompt content
[x] Test first live API call with bash topic
[x] Validate API response format and content
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
[ ] Implement comprehensive error handling with custom exceptions
[ ] Add retry mechanisms with exponential backoff for API calls
[ ] Create circuit breaker pattern for API failures
[ ] Add input validation and sanitization
[ ] Implement graceful degradation when services are unavailable
[ ] Add error reporting and alerting

## ⚙️ Configuration & Environment Management
[ ] Create centralized configuration management
[ ] Add environment-specific configuration files
[ ] Implement secrets management for API keys
[ ] Add configuration validation
[ ] Create configuration hot-reloading capability
[ ] Add feature flags for gradual rollouts

## 🧪 Testing & Quality Assurance
[ ] flesh out test cases
[ ] Add comprehensive unit tests with 90%+ coverage
[ ] Implement integration tests for API interactions
[ ] Add property-based testing for data validation
[ ] Create performance benchmarks
[ ] Add mutation testing for critical paths
[ ] Implement automated security testing

## 📊 Monitoring & Observability
[ ] Add structured logging with correlation IDs
[ ] Implement metrics collection (API response times, success rates)
[ ] Add distributed tracing for API calls
[ ] Create dashboards for system health
[ ] Add alerting for critical failures
[ ] Implement audit logging for compliance

## 🚀 Performance & Scalability
[ ] Implement caching layer for API responses
[ ] Add async/await for I/O operations
[ ] Implement connection pooling for API clients
[ ] Add rate limiting and throttling
[ ] Optimize memory usage for large responses
[ ] Add horizontal scaling capabilities

## 🔒 Security & Compliance
[ ] Implement secure API key management
[ ] Add input sanitization and validation
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
[ ] Create infrastructure as code
[ ] Add automated rollback capabilities

## 📚 Documentation & Standards
[ ] Add comprehensive API documentation
[ ] Create architecture decision records (ADRs)
[ ] Add code documentation and examples
[ ] Create user guides and tutorials
[ ] Implement OpenAPI/Swagger documentation
[ ] Add contribution guidelines

## 🎯 Code Quality & Standards
[ ] Add comprehensive type hints throughout codebase
[ ] Implement code formatting with black/isort
[ ] Add linting with flake8/pylint
[ ] Implement pre-commit hooks
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


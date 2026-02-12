# AgriSutra - System Design Document

## Architecture Overview

**Serverless RAG Pattern on AWS**

AgriSutra leverages a serverless architecture to ensure scalability, cost-efficiency, and minimal operational overhead while delivering real-time AI-powered agricultural guidance.

### Request Flow

```
User Voice Input
    ↓
AWS Transcribe (Speech-to-Text)
    ↓
API Gateway
    ↓
AWS Lambda (Request Router)
    ↓
AI Agent Orchestrator (Amazon Bedrock)
    ├─→ Resilience Sentry Agent
    ├─→ Economic Budgeting Agent
    ├─→ Equipment Translator Agent
    └─→ RAG Knowledge Retrieval (Vector DB)
    ↓
Governance Layer (Trust Engine Validation)
    ↓
AWS Lambda (Response Formatter)
    ↓
AWS Polly (Text-to-Speech)
    ↓
Voice Response to User
```

## Tech Stack

### Frontend
- **Framework**: React Native or Flutter
- **UI Paradigm**: Voice-first design with minimal visual elements
- **Components**:
  - Voice input button (primary interaction)
  - Visual feedback for transcription
  - Optional text display for literate users
  - Offline mode indicator
- **Local Storage**: SQLite for offline data caching

### AI & Language Processing

#### Speech-to-Text
- **Service**: AWS Transcribe
- **Features**: Custom vocabulary for agricultural terms, dialect recognition
- **Optimization**: Streaming transcription for low latency

#### Language Models & Agents
- **Service**: Amazon Bedrock
- **Models**: Claude 3 (Haiku for speed, Sonnet for complex reasoning)
- **Agent Framework**: Bedrock Agents with multi-agent orchestration
- **RAG Implementation**: Vector embeddings for agricultural knowledge base

#### Text-to-Speech
- **Service**: AWS Polly
- **Voices**: Neural voices for Hindi, Kannada, Tamil
- **Customization**: SSML for natural prosody and emphasis

### Compute Layer
- **API Gateway**: REST API for mobile client communication
- **AWS Lambda**: Serverless functions for:
  - Request routing and validation
  - Agent orchestration
  - Governance layer enforcement
  - Response formatting
- **Execution**: Python 3.11 runtime with AWS SDK

### Data Layer

#### Relational Data
- **Service**: Amazon RDS (PostgreSQL)
- **Schema**:
  - User profiles (farm size, location, crops)
  - Crop management records
  - Historical query logs
  - Economic transaction history

#### NoSQL Data
- **Service**: Amazon DynamoDB
- **Use Cases**:
  - Equipment translations (English ↔ Vernacular)
  - Common Q&A pairs for offline mode
  - User preferences and settings
  - Session state management

#### Caching Layer
- **Service**: Amazon ElastiCache (Redis)
- **Cached Data**:
  - Weather forecasts (hyper-local, 15-min refresh)
  - Market prices (hourly refresh)
  - Frequently accessed translations
  - Agent response templates

#### Vector Database
- **Service**: Amazon OpenSearch Service (with k-NN plugin) or Pinecone
- **Content**:
  - Agricultural research papers (embedded)
  - Government advisory documents
  - Crop management best practices
  - Pest/disease identification data
- **Retrieval**: Semantic search for RAG context

### Security & Authentication

#### User Authentication
- **Service**: AWS Cognito
- **Features**:
  - Phone number-based authentication (OTP)
  - Anonymous guest mode for first-time users
  - Multi-device sync with user consent

#### Access Control
- **IAM Roles**: Least-privilege access for Lambda functions
- **API Gateway Authorization**: JWT token validation
- **Secrets Management**: AWS Secrets Manager for API keys

#### Data Protection
- **Encryption**: 
  - At rest: RDS/DynamoDB encryption enabled
  - In transit: TLS 1.3 for all API calls
- **Voice Logs**: Anonymized and stored separately from user profiles
- **PII Handling**: Automatic redaction of sensitive information

## Component Details

### Governance Layer (Trust Engine)

**Purpose**: Validate AI-generated advice against safety and regulatory standards.

**Implementation**:
- Lambda function with rule-based validation
- Banned substance database (DynamoDB)
- Dosage limit checks for chemicals
- Government policy compliance rules
- Fallback to human expert review for edge cases

**Rules**:
- Block toxic pesticides (DDT, Endosulfan, etc.)
- Validate chemical dosages against regulatory limits
- Flag predatory financial products
- Ensure crop recommendations match regional climate

### Offline Mode

**Strategy**: Progressive Web App (PWA) capabilities + local caching

**Cached Assets**:
- 500 most common Q&A pairs (DynamoDB export)
- Last 7 days of weather data
- Equipment translation dictionary
- User's crop calendar and reminders

**Sync Mechanism**:
- Background sync when connectivity restored
- Conflict resolution for offline edits
- Delta updates to minimize bandwidth

## Deployment Architecture

### Regions
- **Primary**: ap-south-1 (Mumbai) - Lowest latency for Indian farmers
- **Backup**: ap-southeast-1 (Singapore) - Disaster recovery

### Scaling Strategy
- **Lambda**: Auto-scaling based on request volume
- **RDS**: Read replicas for query load distribution
- **DynamoDB**: On-demand capacity mode
- **ElastiCache**: Cluster mode for horizontal scaling

### Monitoring
- **AWS CloudWatch**: Metrics, logs, and alarms
- **AWS X-Ray**: Distributed tracing for latency analysis
- **Custom Metrics**: Voice response accuracy, user satisfaction scores

## Cost Optimization

- **Lambda**: Pay-per-invocation, no idle costs
- **Transcribe/Polly**: Batch processing for non-urgent requests
- **RDS**: Reserved instances for predictable workloads
- **S3 Intelligent-Tiering**: Automatic cost optimization for voice logs
- **CloudFront**: CDN for static assets to reduce data transfer costs

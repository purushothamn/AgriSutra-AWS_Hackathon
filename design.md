# AgriSutra - Design Document

## System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Mobile/Web Client                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Voice UI    │  │  Dashboard   │  │  Translator  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway (AWS)                       │
│              Authentication, Rate Limiting, Routing          │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Voice      │   │   Weather    │   │   Budget     │
│   Service    │   │   Service    │   │   Service    │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Translator  │   │  Governance  │   │   Database   │
│   Service    │   │    Layer     │   │   (RDS)      │
└──────────────┘   └──────────────┘   └──────────────┘
```

## Component Design

### 1. Vernacular Voice UI

#### Architecture
- **Frontend**: React Native with voice recording capabilities
- **Speech-to-Text**: AWS Transcribe with custom vocabulary for agricultural terms
- **Text-to-Speech**: AWS Polly with Neural voices for Indian languages
- **Dialect Models**: Fine-tuned models for regional variations

#### Data Flow
```
User Voice Input → Audio Capture → AWS Transcribe (with custom vocab) 
→ Text Processing → Intent Recognition → Response Generation 
→ AWS Polly → Audio Output
```

#### Key Components
- **AudioRecorder**: Captures voice with noise cancellation
- **TranscriptionManager**: Manages STT with dialect-specific models
- **SpeechSynthesizer**: Converts text responses to natural speech
- **DialectSelector**: User preference management

#### Storage
- Cached audio responses for common queries (reduce latency)
- User dialect preferences in local storage
- Offline fallback for basic commands

---

### 2. Disaster & Weather Alerts

#### Architecture
- **Weather APIs**: India Meteorological Department (IMD), OpenWeather API
- **Alert Engine**: AWS Lambda functions for real-time processing
- **Notification Service**: AWS SNS for push notifications
- **Caching**: Redis for weather data caching

#### Data Flow
```
Weather API (polling every 30 min) → Lambda Processor 
→ Alert Rules Engine → Governance Validation 
→ SNS → Push Notification → User Device
```

#### Alert Rules Engine
```javascript
{
  "rules": [
    {
      "condition": "rainfall > 100mm/day",
      "severity": "high",
      "action": "immediate_alert",
      "message_template": "heavy_rain_warning"
    },
    {
      "condition": "temperature > 40°C for 3 days",
      "severity": "medium",
      "action": "advisory",
      "message_template": "heatwave_precaution"
    }
  ]
}
```

#### Database Schema
```sql
CREATE TABLE weather_alerts (
    id UUID PRIMARY KEY,
    user_id UUID,
    location GEOGRAPHY(POINT),
    alert_type VARCHAR(50),
    severity VARCHAR(20),
    message TEXT,
    sent_at TIMESTAMP,
    acknowledged BOOLEAN
);

CREATE TABLE weather_cache (
    location_id VARCHAR(50) PRIMARY KEY,
    forecast_data JSONB,
    updated_at TIMESTAMP,
    expires_at TIMESTAMP
);
```

---

### 3. Economic Crop Budgeting Agent

#### Architecture
- **Backend**: Python FastAPI service
- **ML Model**: Crop price prediction using historical data
- **Database**: PostgreSQL for cost data, TimescaleDB for price trends
- **Calculation Engine**: Rule-based + ML hybrid approach

#### Core Modules

**Cost Calculator**
```python
class CropBudgetCalculator:
    def calculate_total_cost(self, crop_type, area, farming_method):
        # Seeds, fertilizers, labor, water, equipment
        return {
            "fixed_costs": {...},
            "variable_costs": {...},
            "total": float,
            "per_acre": float
        }
    
    def predict_revenue(self, crop_type, expected_yield, market_trends):
        # ML-based price prediction + yield estimation
        return {
            "expected_price": float,
            "revenue_range": (min, max),
            "confidence": float
        }
```

**Recommendation Engine**
```python
class CropRecommender:
    def recommend_crops(self, budget, location, season, soil_type):
        # Multi-criteria optimization
        # Returns ranked list of suitable crops
        return [
            {
                "crop": "wheat",
                "expected_profit": 45000,
                "risk_level": "low",
                "water_requirement": "medium"
            }
        ]
```

#### Database Schema
```sql
CREATE TABLE crop_costs (
    id UUID PRIMARY KEY,
    crop_type VARCHAR(50),
    region VARCHAR(50),
    season VARCHAR(20),
    seed_cost DECIMAL,
    fertilizer_cost DECIMAL,
    labor_cost DECIMAL,
    water_cost DECIMAL,
    equipment_cost DECIMAL,
    updated_at TIMESTAMP
);

CREATE TABLE market_prices (
    id UUID PRIMARY KEY,
    crop_type VARCHAR(50),
    market_location VARCHAR(100),
    price DECIMAL,
    recorded_at TIMESTAMP
);

CREATE TABLE user_budgets (
    id UUID PRIMARY KEY,
    user_id UUID,
    crop_type VARCHAR(50),
    planned_costs JSONB,
    actual_costs JSONB,
    season VARCHAR(20),
    created_at TIMESTAMP
);
```

---

### 4. English-to-Local Equipment Translator

#### Architecture
- **Translation Database**: DynamoDB for fast lookups
- **Search Engine**: Elasticsearch for fuzzy matching
- **Image Storage**: S3 with CloudFront CDN
- **Offline Support**: SQLite local database

#### Data Model
```json
{
  "equipment_id": "tractor_001",
  "english_term": "tractor",
  "translations": {
    "hindi": "ट्रैक्टर",
    "tamil": "டிராக்டர்",
    "telugu": "ట్రాక్టర్",
    "kannada": "ಟ್ರಾಕ್ಟರ್"
  },
  "category": "machinery",
  "images": [
    "https://cdn.agrisutra.com/equipment/tractor_001.jpg"
  ],
  "usage_instructions": {
    "hindi": "...",
    "tamil": "..."
  },
  "related_terms": ["plough", "cultivator"]
}
```

#### API Design
```
GET /api/v1/translate?term=tractor&from=en&to=hi
POST /api/v1/translate/batch
GET /api/v1/equipment/search?q=plough&lang=hi
GET /api/v1/equipment/{id}
```

#### Offline Sync Strategy
- Download translation database on first launch (compressed ~5MB)
- Incremental updates weekly
- Priority sync for user's selected dialect

---

### 5. Governance Layer for Safe Advice

#### Architecture
- **Rule Engine**: AWS Lambda with configurable rules
- **Content Validation**: ML-based safety classifier
- **Expert Review Queue**: Manual review dashboard
- **Audit System**: CloudWatch Logs + S3 archival

#### Governance Pipeline
```
User Query/Advice → Content Analysis → Safety Classification 
→ Rule Validation → Expert Review (if flagged) 
→ Approval/Rejection → Audit Log → User Response
```

#### Safety Rules
```yaml
safety_rules:
  - rule_id: "pesticide_limit"
    description: "Flag excessive pesticide recommendations"
    condition: "pesticide_quantity > regulatory_limit"
    action: "block"
    
  - rule_id: "water_conservation"
    description: "Ensure water-efficient practices"
    condition: "water_usage > sustainable_threshold"
    action: "warn"
    
  - rule_id: "organic_certification"
    description: "Validate organic farming advice"
    condition: "advice_type == 'organic' AND !certified_practice"
    action: "review"
```

#### ML Safety Classifier
```python
class SafetyClassifier:
    def classify_advice(self, text, context):
        # Categories: safe, needs_review, unsafe
        return {
            "classification": "safe",
            "confidence": 0.95,
            "flags": [],
            "recommendations": []
        }
```

#### Audit Schema
```sql
CREATE TABLE advice_audit (
    id UUID PRIMARY KEY,
    user_id UUID,
    advice_text TEXT,
    classification VARCHAR(20),
    flags JSONB,
    reviewed_by UUID,
    approved BOOLEAN,
    created_at TIMESTAMP,
    reviewed_at TIMESTAMP
);
```

---

## Technology Stack

### Frontend
- **Mobile**: React Native (iOS/Android)
- **Web**: Progressive Web App (PWA) with React
- **UI Framework**: React Native Paper (Material Design)
- **State Management**: Redux Toolkit
- **Offline Storage**: AsyncStorage + SQLite

### Backend
- **API Gateway**: AWS API Gateway
- **Compute**: AWS Lambda (serverless), ECS for long-running services
- **Voice Services**: AWS Transcribe, AWS Polly
- **Translation**: Custom NLP models + AWS Translate
- **Databases**: 
  - PostgreSQL (RDS) for relational data
  - DynamoDB for translations
  - Redis (ElastiCache) for caching
  - TimescaleDB for time-series data

### AI/ML
- **Frameworks**: TensorFlow, PyTorch
- **Deployment**: AWS SageMaker
- **Models**: 
  - Crop price prediction (LSTM)
  - Safety classification (BERT-based)
  - Dialect-specific ASR models

### Infrastructure
- **Cloud Provider**: AWS
- **CDN**: CloudFront
- **Monitoring**: CloudWatch, X-Ray
- **CI/CD**: GitHub Actions, AWS CodePipeline
- **IaC**: Terraform

---

## Security Design

### Authentication & Authorization
- **User Auth**: AWS Cognito with phone number verification
- **API Security**: JWT tokens with 24-hour expiry
- **Role-Based Access**: Farmer, Expert, Admin roles

### Data Protection
- **Encryption at Rest**: AES-256 for databases
- **Encryption in Transit**: TLS 1.3
- **PII Handling**: Tokenization for sensitive data
- **Data Retention**: 90-day retention for voice recordings

### Privacy
- **Location Data**: Coarse location only (district level)
- **Voice Data**: Opt-in recording for quality improvement
- **Data Deletion**: User-initiated account deletion

---

## Deployment Architecture

### Multi-Region Setup
- **Primary Region**: ap-south-1 (Mumbai)
- **DR Region**: ap-southeast-1 (Singapore)
- **CDN**: Global CloudFront distribution

### Scaling Strategy
- **Auto-scaling**: Based on CPU/memory metrics
- **Database**: Read replicas for query distribution
- **Caching**: Multi-tier (CloudFront → Redis → Database)

### Disaster Recovery
- **RTO**: 4 hours
- **RPO**: 1 hour
- **Backup**: Daily automated snapshots
- **Failover**: Automated DNS failover with Route 53

---

## User Interface Design

### Voice-First Interaction Flow
```
App Launch → Dialect Selection → Voice Prompt 
→ "How can I help you today?" 
→ User speaks query → Processing indicator 
→ Voice response + Visual summary
```

### Key Screens
1. **Home Dashboard**: Weather widget, alerts, quick actions
2. **Voice Assistant**: Waveform visualization, transcript display
3. **Budget Planner**: Cost breakdown, profit projections, charts
4. **Equipment Translator**: Search bar, image gallery, audio pronunciation
5. **Alerts**: Notification list, severity indicators, action buttons

### Accessibility
- Voice-only navigation option
- High contrast mode for outdoor use
- Large fonts (minimum 16sp)
- Haptic feedback for confirmations

---

## Testing Strategy

### Unit Testing
- Backend services: 80%+ coverage
- Frontend components: 70%+ coverage

### Integration Testing
- API contract testing
- End-to-end voice flow testing
- Weather alert pipeline testing

### User Testing
- Field testing with 100+ farmers across 5 states
- Dialect accuracy validation
- Usability testing with low-literacy users

### Performance Testing
- Load testing: 100K concurrent users
- Latency testing on 2G/3G networks
- Battery consumption profiling

---

## Monitoring & Observability

### Metrics
- Voice recognition accuracy per dialect
- API response times (p50, p95, p99)
- Alert delivery success rate
- User engagement metrics

### Logging
- Structured logging with correlation IDs
- Centralized log aggregation (CloudWatch)
- Error tracking (Sentry)

### Alerting
- PagerDuty for critical incidents
- Slack notifications for warnings
- Weekly health reports

---

## Rollout Plan

### Phase 1 (Months 1-3): MVP
- Voice UI (3 dialects: Hindi, Tamil, Telugu)
- Basic weather alerts
- Equipment translator (500 terms)

### Phase 2 (Months 4-6): Enhanced Features
- Crop budgeting agent
- Governance layer
- 6 additional dialects

### Phase 3 (Months 7-9): Scale & Optimize
- Performance optimization
- Offline mode enhancement
- Community features

### Phase 4 (Months 10-12): Advanced Features
- Crop disease detection
- Marketplace integration
- Livestock management

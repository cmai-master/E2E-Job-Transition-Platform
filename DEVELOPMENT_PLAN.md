# CareerNavigator 개발 계획서

**Version**: 1.0
**Date**: 2024-11-24
**Status**: Ready for Development

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [기술 스택 및 아키텍처](#2-기술-스택-및-아키텍처)
3. [프로젝트 구조](#3-프로젝트-구조)
4. [개발 환경 설정](#4-개발-환경-설정)
5. [데이터베이스 설계](#5-데이터베이스-설계)
6. [API 설계 원칙](#6-api-설계-원칙)
7. [Phase별 상세 개발 계획](#7-phase별-상세-개발-계획)
8. [Git Workflow](#8-git-workflow)
9. [테스트 전략](#9-테스트-전략)
10. [배포 전략](#10-배포-전략)
11. [마일스톤 및 KPI](#11-마일스톤-및-kpi)
12. [리스크 관리](#12-리스크-관리)

---

## 1. 프로젝트 개요

### 1.1 프로젝트 목표

CareerNavigator는 AI 기술을 활용한 이직 지원 플랫폼으로, 다음 핵심 가치를 제공합니다:

- **시간 절약**: 이직 준비 시간 60% 단축
- **매칭 정확도**: 적합 포지션 발견율 3배 향상
- **협상력 강화**: 평균 연봉 협상 15% 개선

### 1.2 핵심 차별화 요소

1. **User-Contributed Data Network**: Browser Extension을 통한 P2P 데이터 수집
2. **Multi-Agent Architecture**: 5개 전문 AI Agent 협업 시스템
3. **Knowledge Graph 기반 매칭**: Neo4j를 활용한 Semantic Matching
4. **Production-Ready RAG**: LightRAG 기반 Hybrid Search

### 1.3 MVP 범위 (6개월)

**목표 지표**:
- 1,000+ 활성 사용자
- 25,000+ 유니크 채용 공고
- 70% 사용자 활성화율
- NPS 50+

---

## 2. 기술 스택 및 아키텍처

### 2.1 전체 기술 스택

```yaml
# Backend
Language: Python 3.11+
Framework: FastAPI 0.104+
ORM: SQLAlchemy 2.0
Migration: Alembic

# Frontend
Framework: Next.js 14 (App Router)
Language: TypeScript 5.0
UI: Tailwind CSS 3.0, shadcn/ui
State: Zustand, React Query

# AI/ML
Orchestration: LangGraph, LangChain 0.1.0+
LLM: Claude Sonnet 4, GPT-4o, GPT-4o-mini
Embeddings: OpenAI text-embedding-3-large
Reranking: Cohere

# Data Layer
Graph DB: Neo4j 5.x (AuraDB)
Vector DB: Qdrant 1.7+
RDBMS: PostgreSQL 15+
Cache: Redis 7+

# Infrastructure
Cloud: Azure (AKS, Cosmos DB, Functions, Blob Storage)
Container: Docker, Kubernetes
CI/CD: GitHub Actions
IaC: Terraform

# Monitoring
LLM Tracing: LangSmith
Metrics: Prometheus + Grafana
APM: Azure Application Insights
Error: Sentry

# Browser Extension
Manifest: V3
Framework: React 18
Build: Vite
```

### 2.2 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Web App    │  │    Mobile    │  │  Extension   │      │
│  │  (Next.js)   │  │ (React Native)│ │  (Chrome)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   API Gateway (FastAPI)                      │
│            Rate Limiting, Auth, CORS, Logging                │
└─────────────────────────┬───────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼─────┐     ┌───▼────┐     ┌────▼─────┐
    │  Agent   │     │  Data  │     │   User   │
    │ Service  │     │Service │     │ Service  │
    └────┬─────┘     └───┬────┘     └────┬─────┘
         │               │                │
         │               │                │
    ┌────▼──────────────────────────┐    │
    │   LangGraph Orchestration     │    │
    │  ┌──────┐ ┌──────┐ ┌──────┐  │    │
    │  │Agent1│ │Agent2│ │Agent3│  │    │
    │  └──────┘ └──────┘ └──────┘  │    │
    └────┬──────────────────────────┘    │
         │                               │
┌────────▼───────────────────────────────▼─────┐
│           Context Management Layer            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Neo4j   │  │  Qdrant  │  │PostgreSQL│   │
│  │  (Graph) │  │ (Vector) │  │  (RDBMS) │   │
│  └──────────┘  └──────────┘  └──────────┘   │
└───────────────────────────────────────────────┘
```

### 2.3 Multi-Agent Architecture

5개 전문 Agent로 구성:

1. **Profile Analyzer Agent**: 이력서 파싱, 스킬 추출, 경력 분석
2. **Job Matcher Agent**: 채용 공고 매칭, 스코어링, 추천
3. **Application Assistant Agent**: 지원서 최적화, Cover Letter 생성
4. **Interview Coach Agent**: 모의 면접, 답변 피드백
5. **Negotiation Advisor Agent**: 오퍼 분석, 협상 전략

### 2.4 데이터 소싱 전략

**3-Tier Architecture**:

```
Tier 1 (PRIMARY): User-Contributed Data
├─ Browser Extension (Chrome/Edge/Firefox)
├─ 목표: 1,000 users → 10,000 jobs/day
└─ 법적 리스크: Zero

Tier 2 (SECONDARY): Official APIs
├─ Indeed API: 10,000 jobs
├─ 워크넷 API: 5,000 jobs
└─ ZipRecruiter API: 3,000 jobs (Phase 2)

Tier 3 (TERTIARY): Selective Web Scraping
├─ 사람인, 잡코리아: 8,000 jobs
├─ 대기업 채용 페이지: 1,000 jobs
└─ Rate-limited, robots.txt 준수
```

---

## 3. 프로젝트 구조

### 3.1 Monorepo 구조

```
careernavigator/
├── apps/
│   ├── backend/                 # FastAPI Backend
│   │   ├── app/
│   │   │   ├── api/            # API Routes
│   │   │   │   ├── v1/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── users.py
│   │   │   │   │   ├── jobs.py
│   │   │   │   │   ├── applications.py
│   │   │   │   │   └── agents.py
│   │   │   │   └── deps.py     # Dependencies
│   │   │   ├── agents/         # AI Agents
│   │   │   │   ├── base.py
│   │   │   │   ├── profile_analyzer.py
│   │   │   │   ├── job_matcher.py
│   │   │   │   ├── application_assistant.py
│   │   │   │   ├── interview_coach.py
│   │   │   │   └── negotiation_advisor.py
│   │   │   ├── core/           # Core Logic
│   │   │   │   ├── config.py
│   │   │   │   ├── security.py
│   │   │   │   └── logging.py
│   │   │   ├── db/             # Database
│   │   │   │   ├── models.py   # SQLAlchemy Models
│   │   │   │   ├── session.py
│   │   │   │   └── neo4j.py    # Neo4j Client
│   │   │   ├── schemas/        # Pydantic Schemas
│   │   │   │   ├── user.py
│   │   │   │   ├── job.py
│   │   │   │   └── application.py
│   │   │   ├── services/       # Business Logic
│   │   │   │   ├── auth.py
│   │   │   │   ├── job_service.py
│   │   │   │   ├── rag_service.py
│   │   │   │   └── crawler_service.py
│   │   │   ├── rag/            # RAG Pipeline
│   │   │   │   ├── lightrag.py
│   │   │   │   ├── retriever.py
│   │   │   │   └── reranker.py
│   │   │   └── main.py
│   │   ├── alembic/            # Migrations
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── pyproject.toml
│   │
│   ├── frontend/               # Next.js Frontend
│   │   ├── src/
│   │   │   ├── app/           # App Router
│   │   │   │   ├── (auth)/
│   │   │   │   │   ├── login/
│   │   │   │   │   └── signup/
│   │   │   │   ├── (dashboard)/
│   │   │   │   │   ├── jobs/
│   │   │   │   │   ├── applications/
│   │   │   │   │   ├── profile/
│   │   │   │   │   └── settings/
│   │   │   │   ├── api/       # API Routes
│   │   │   │   ├── layout.tsx
│   │   │   │   └── page.tsx
│   │   │   ├── components/    # React Components
│   │   │   │   ├── ui/        # shadcn/ui
│   │   │   │   ├── jobs/
│   │   │   │   ├── profile/
│   │   │   │   └── agent/
│   │   │   ├── lib/
│   │   │   │   ├── api.ts     # API Client
│   │   │   │   ├── auth.ts
│   │   │   │   └── utils.ts
│   │   │   ├── hooks/
│   │   │   ├── store/         # Zustand Store
│   │   │   └── types/
│   │   ├── public/
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── tailwind.config.ts
│   │
│   └── extension/             # Browser Extension
│       ├── src/
│       │   ├── background/    # Service Worker
│       │   │   └── index.ts
│       │   ├── content/       # Content Scripts
│       │   │   ├── linkedin.ts
│       │   │   ├── indeed.ts
│       │   │   └── saramin.ts
│       │   ├── popup/         # Extension Popup
│       │   │   ├── Popup.tsx
│       │   │   └── index.tsx
│       │   ├── options/       # Options Page
│       │   └── utils/
│       │       ├── api.ts
│       │       └── storage.ts
│       ├── public/
│       │   └── manifest.json
│       ├── package.json
│       └── vite.config.ts
│
├── packages/                  # Shared Packages
│   ├── types/                # Shared TypeScript Types
│   ├── utils/                # Shared Utilities
│   └── config/               # Shared Config
│
├── infra/                    # Infrastructure
│   ├── terraform/
│   ├── kubernetes/
│   └── docker/
│       └── docker-compose.yml
│
├── docs/                     # Documentation
│   ├── api/
│   ├── architecture/
│   └── guides/
│
├── scripts/                  # Utility Scripts
│   ├── seed-data.py
│   └── migration.sh
│
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       ├── frontend-ci.yml
│       └── extension-ci.yml
│
├── .gitignore
├── README.md
├── CareerNavigator_기획서_v1.0.md
└── DEVELOPMENT_PLAN.md (이 문서)
```

### 3.2 패키지 관리

- **Backend**: Poetry 또는 pip-tools
- **Frontend/Extension**: pnpm (Monorepo 지원)
- **Monorepo Tool**: Turborepo 또는 pnpm workspace

---

## 4. 개발 환경 설정

### 4.1 필수 도구

```bash
# 필수 설치 항목
- Python 3.11+
- Node.js 18+ (LTS)
- pnpm 8+
- Docker Desktop
- Docker Compose
- Git

# 추천 IDE
- VSCode
  - Extensions:
    - Python
    - Pylance
    - ESLint
    - Prettier
    - Tailwind CSS IntelliSense
    - Docker
```

### 4.2 로컬 개발 환경 구성

#### 4.2.1 Docker Compose

```yaml
# infra/docker/docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: careernavigator
      POSTGRES_USER: cnav
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  neo4j:
    image: neo4j:5.15-community
    environment:
      NEO4J_AUTH: neo4j/dev_password
      NEO4J_PLUGINS: '["apoc", "graph-data-science"]'
    ports:
      - "7474:7474"  # Browser
      - "7687:7687"  # Bolt
    volumes:
      - neo4j_data:/data

  qdrant:
    image: qdrant/qdrant:v1.7.4
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build:
      context: ../../apps/backend
      dockerfile: Dockerfile.dev
    volumes:
      - ../../apps/backend:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://cnav:dev_password@postgres:5432/careernavigator
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=dev_password
      - QDRANT_URL=http://qdrant:6333
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - neo4j
      - qdrant
      - redis
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ../../apps/frontend
      dockerfile: Dockerfile.dev
    volumes:
      - ../../apps/frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
    command: pnpm dev

volumes:
  postgres_data:
  neo4j_data:
  qdrant_data:
  redis_data:
```

#### 4.2.2 환경 변수 설정

```bash
# apps/backend/.env.example
# Database
DATABASE_URL=postgresql://cnav:dev_password@localhost:5432/careernavigator
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=dev_password
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379

# LLM APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
COHERE_API_KEY=...

# External APIs
INDEED_API_KEY=...
WORKNET_API_KEY=...
CRUNCHBASE_API_KEY=...
GLASSDOOR_API_KEY=...

# Auth
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Azure (Production)
AZURE_STORAGE_CONNECTION_STRING=...
AZURE_APPLICATION_INSIGHTS_KEY=...

# Monitoring
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=careernavigator-dev
SENTRY_DSN=...
```

```bash
# apps/frontend/.env.local.example
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

#### 4.2.3 개발 서버 실행

```bash
# 1. Docker Compose 실행 (DB 레이어)
cd infra/docker
docker-compose up -d

# 2. Backend 실행
cd apps/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head  # DB 마이그레이션
uvicorn app.main:app --reload

# 3. Frontend 실행
cd apps/frontend
pnpm install
pnpm dev

# 4. Extension 개발 (선택)
cd apps/extension
pnpm install
pnpm dev  # Watch mode
# Chrome: chrome://extensions/ → Load unpacked → dist/
```

---

## 5. 데이터베이스 설계

### 5.1 PostgreSQL Schema

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    location JSONB,  -- {city, country}
    linkedin_url VARCHAR(500),
    github_url VARCHAR(500),
    profile_vector VECTOR(1536),  -- pgvector extension
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Skills
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    skill_name VARCHAR(255) NOT NULL,
    category VARCHAR(50),  -- technical, domain, soft
    proficiency_level INTEGER CHECK (proficiency_level BETWEEN 1 AND 5),
    years_used DECIMAL(3, 1),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Career History
CREATE TABLE career_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    responsibilities TEXT[],
    achievements JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Companies
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    industry VARCHAR(100),
    size VARCHAR(50),
    founded_year INTEGER,
    headquarters JSONB,
    description TEXT,
    website VARCHAR(500),
    social_links JSONB,
    funding JSONB,
    tech_stack TEXT[],
    ratings JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Jobs
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source VARCHAR(50) NOT NULL,
    source_url VARCHAR(1000) NOT NULL,
    company_id UUID REFERENCES companies(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    requirements JSONB,
    responsibilities TEXT[],
    compensation JSONB,
    location JSONB,
    job_vector VECTOR(1536),
    posted_date TIMESTAMP NOT NULL,
    deadline TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    view_count INTEGER DEFAULT 0,
    apply_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_posted_date ON jobs(posted_date DESC);
CREATE INDEX idx_jobs_company_id ON jobs(company_id);

-- Applications
CREATE TABLE applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    applied_date TIMESTAMP DEFAULT NOW(),
    resume_version VARCHAR(255),
    cover_letter TEXT,
    timeline JSONB,
    interview_records JSONB,
    offer_details JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, job_id)
);

CREATE INDEX idx_applications_user_id ON applications(user_id);
CREATE INDEX idx_applications_status ON applications(status);

-- User Contributions (Extension)
CREATE TABLE user_contributions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    contribution_type VARCHAR(50),  -- job, salary, interview
    data JSONB NOT NULL,
    source VARCHAR(50),
    is_validated BOOLEAN DEFAULT FALSE,
    points_earned INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Gamification
CREATE TABLE user_points (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    total_points INTEGER DEFAULT 0,
    lifetime_points INTEGER DEFAULT 0,
    tier VARCHAR(20) DEFAULT 'free',  -- free, premium
    premium_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 5.2 Neo4j Schema (Cypher)

```cypher
// Node Constraints
CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE;
CREATE CONSTRAINT job_id IF NOT EXISTS FOR (j:Job) REQUIRE j.id IS UNIQUE;
CREATE CONSTRAINT company_id IF NOT EXISTS FOR (c:Company) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT skill_name IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE;

// Indexes
CREATE INDEX user_email IF NOT EXISTS FOR (u:User) ON (u.email);
CREATE INDEX job_title IF NOT EXISTS FOR (j:Job) ON (j.title);
CREATE INDEX company_name IF NOT EXISTS FOR (c:Company) ON (c.name);

// Relationships
// User -> Skill
(:User)-[:HAS_SKILL {proficiency: INT, years: FLOAT}]->(:Skill)

// User -> Company
(:User)-[:WORKED_AT {start_date: DATE, end_date: DATE, title: STRING}]->(:Company)

// User -> Job
(:User)-[:APPLIED_TO {date: DATETIME, status: STRING}]->(:Job)
(:User)-[:VIEWED {date: DATETIME}]->(:Job)
(:User)-[:SAVED {date: DATETIME}]->(:Job)

// User -> Preferences
(:User)-[:PREFERS {weight: FLOAT}]->(:Company)
(:User)-[:PREFERS {weight: FLOAT}]->(:Industry)
(:User)-[:PREFERS {weight: FLOAT}]->(:Location)

// Job -> Skill
(:Job)-[:REQUIRES {importance: STRING}]->(:Skill)  // required, preferred, nice-to-have

// Job -> Company
(:Job)-[:POSTED_BY]->(:Company)

// Job -> Job (Similarity)
(:Job)-[:SIMILAR_TO {similarity: FLOAT}]->(:Job)

// Company -> Skill
(:Company)-[:USES_TECH]->(:Skill)

// Company -> Industry
(:Company)-[:IN_INDUSTRY]->(:Industry)

// Company -> Company
(:Company)-[:COMPETES_WITH]->(:Company)

// Skill -> Skill
(:Skill)-[:RELATED_TO {similarity: FLOAT}]->(:Skill)
(:Skill)-[:PARENT_OF]->(:Skill)  // Taxonomy hierarchy
```

### 5.3 Qdrant Collections

```python
# Collection 1: User Profiles
user_collection = {
    "collection_name": "user_profiles",
    "vectors": {
        "size": 1536,
        "distance": "Cosine"
    },
    "payload_schema": {
        "user_id": "keyword",
        "skills": "keyword[]",
        "years_experience": "integer",
        "target_roles": "text[]",
        "location": "keyword"
    }
}

# Collection 2: Job Postings
job_collection = {
    "collection_name": "job_postings",
    "vectors": {
        "size": 1536,
        "distance": "Cosine"
    },
    "payload_schema": {
        "job_id": "keyword",
        "company_name": "keyword",
        "title": "text",
        "required_skills": "keyword[]",
        "salary_min": "float",
        "salary_max": "float",
        "location": "keyword",
        "posted_date": "datetime"
    }
}

# Collection 3: Companies
company_collection = {
    "collection_name": "companies",
    "vectors": {
        "size": 1536,
        "distance": "Cosine"
    },
    "payload_schema": {
        "company_id": "keyword",
        "name": "keyword",
        "industry": "keyword",
        "tech_stack": "keyword[]",
        "culture_values": "text[]"
    }
}
```

---

## 6. API 설계 원칙

### 6.1 RESTful API 규칙

- **Base URL**: `https://api.careernavigator.ai/v1`
- **인증**: Bearer Token (JWT)
- **응답 형식**: JSON
- **에러 처리**: RFC 7807 (Problem Details)

### 6.2 주요 엔드포인트

```
Authentication:
POST   /auth/signup              # 회원가입
POST   /auth/login               # 로그인
POST   /auth/refresh             # 토큰 갱신
POST   /auth/logout              # 로그아웃

Users:
GET    /users/me                 # 현재 사용자 정보
PUT    /users/me                 # 프로필 업데이트
POST   /users/me/resume          # 이력서 업로드
GET    /users/me/skills          # 스킬 목록
POST   /users/me/skills          # 스킬 추가

Jobs:
GET    /jobs                     # 채용 공고 목록 (필터링, 페이징)
GET    /jobs/{id}                # 채용 공고 상세
GET    /jobs/recommendations     # 추천 공고 (AI)
POST   /jobs/{id}/save           # 공고 저장
POST   /jobs/{id}/view           # 조회수 증가

Applications:
GET    /applications             # 지원 내역
POST   /applications             # 지원하기
GET    /applications/{id}        # 지원 상세
PUT    /applications/{id}        # 지원 상태 업데이트
DELETE /applications/{id}        # 지원 취소

Companies:
GET    /companies                # 회사 목록
GET    /companies/{id}           # 회사 상세
GET    /companies/{id}/jobs      # 회사 채용 공고
GET    /companies/{id}/reviews   # 회사 리뷰

Agents:
POST   /agents/profile-analyze   # 프로필 분석
POST   /agents/job-match         # Job 매칭
POST   /agents/resume-optimize   # 이력서 최적화
POST   /agents/interview-prep    # 면접 준비
POST   /agents/negotiate         # 협상 조언
GET    /agents/conversation/{id} # Agent 대화 이력

Contributions (Extension):
POST   /contributions/jobs       # Job 데이터 기여
POST   /contributions/salaries   # 연봉 데이터 기여
POST   /contributions/interviews # 면접 후기 기여
GET    /contributions/points     # 포인트 조회

Admin:
GET    /admin/stats              # 통계
GET    /admin/users              # 사용자 관리
POST   /admin/crawl              # 수동 크롤링 트리거
```

### 6.3 에러 응답 형식

```json
{
  "type": "https://api.careernavigator.ai/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "The request body is invalid",
  "instance": "/users/me/skills",
  "errors": [
    {
      "field": "skill_name",
      "message": "Skill name is required"
    }
  ]
}
```

---

## 7. Phase별 상세 개발 계획

### Phase 1: 프로젝트 기반 구조 (Week 1-2)

**목표**: 개발 환경 구축 및 기본 인프라 설정

#### Week 1: 프로젝트 초기화

**Tasks**:
- [ ] Monorepo 구조 생성 (pnpm workspace)
- [ ] Backend 프로젝트 초기화
  - FastAPI 프로젝트 구조
  - Poetry 또는 requirements.txt 설정
  - Dockerfile 작성
- [ ] Frontend 프로젝트 초기화
  - Next.js 14 프로젝트 생성
  - shadcn/ui 설치
  - Tailwind CSS 설정
- [ ] Extension 프로젝트 초기화
  - Vite + React 설정
  - Manifest V3 구성

**Deliverables**:
- 각 앱 디렉토리에서 "Hello World" 실행 가능
- Git repository 구조 확립

#### Week 2: 개발 환경 구성

**Tasks**:
- [ ] Docker Compose 작성
  - PostgreSQL
  - Neo4j
  - Qdrant
  - Redis
- [ ] Backend 기본 설정
  - Database 연결
  - Alembic 마이그레이션 설정
  - 기본 CRUD 엔드포인트
- [ ] Frontend 기본 설정
  - API 클라이언트 구성
  - 라우팅 설정
  - 기본 레이아웃
- [ ] CI/CD 파이프라인
  - GitHub Actions (Lint, Test)

**Deliverables**:
- `docker-compose up`으로 전체 스택 실행 가능
- Backend ↔ Frontend 통신 확인
- CI 파이프라인 작동

---

### Phase 2: 사용자 관리 및 인증 (Week 3-4)

**목표**: 사용자 인증 시스템 및 프로필 관리

#### Week 3: 인증 시스템

**Tasks**:
- [ ] JWT 기반 인증 구현
  - Signup, Login, Logout API
  - Access/Refresh Token
  - Password hashing (bcrypt)
- [ ] OAuth 통합 (Google, LinkedIn)
- [ ] Frontend 인증 UI
  - Login/Signup 페이지
  - Protected Routes
  - Auth Context

**Deliverables**:
- 회원가입 → 로그인 → 대시보드 접근 가능
- JWT 토큰 관리

#### Week 4: 프로필 관리 및 이력서 파싱

**Tasks**:
- [ ] User Profile CRUD API
- [ ] 이력서 업로드 (Azure Blob Storage)
- [ ] 이력서 파싱 MVP
  - PyPDF2, python-docx로 텍스트 추출
  - spaCy NER로 기본 정보 추출
- [ ] Frontend 프로필 페이지
  - 프로필 편집 폼
  - 이력서 업로드 UI
  - 스킬 입력 인터페이스

**Deliverables**:
- PDF 이력서 업로드 → 텍스트 추출 → 프로필 자동 입력

---

### Phase 3: Knowledge Graph 기반 구축 (Week 5-6)

**목표**: Neo4j 스키마 구현 및 데이터 시딩

#### Week 5: Neo4j 스키마 및 스킬 택소노미

**Tasks**:
- [ ] Neo4j 스키마 구현
  - Cypher 쿼리로 제약 조건 생성
  - 인덱스 생성
- [ ] 스킬 택소노미 데이터 수집
  - 500+ 기술 스킬
  - 스킬 간 관계 (RELATED_TO, PARENT_OF)
  - 카테고리: Programming, Cloud, Database, Framework, etc.
- [ ] Python Neo4j Driver 통합
  - Connection pool
  - 기본 CRUD 작업

**Data Sources**:
- GitHub Skills
- LinkedIn Skill Taxonomy
- Stack Overflow Tags

**Deliverables**:
- Neo4j에 500+ 스킬 노드 생성
- 스킬 검색 API

#### Week 6: 회사 데이터 시딩

**Tasks**:
- [ ] 회사 데이터 수집
  - Crunchbase API (100+ 스타트업)
  - Glassdoor API (리뷰, 평점)
  - 수동 큐레이션 (대기업)
- [ ] Company 노드 생성
- [ ] Company ↔ Skill 관계 구축
- [ ] Company ↔ Industry 관계

**Deliverables**:
- 100+ 회사 데이터 in Neo4j
- 회사 검색 및 상세 페이지

---

### Phase 4: 멀티소스 Job 수집 (Week 7-8)

**목표**: 15,000+ 채용 공고 수집 시스템 구축

#### Week 7: Official API 통합

**Tasks**:
- [ ] Indeed API 통합
  - API 키 발급
  - Job search endpoint
  - 일일 10,000 jobs 수집
  - 데이터 정규화
- [ ] 워크넷 API 통합
  - 공공 API 연동
  - 일일 5,000 jobs 수집
- [ ] Job 저장 파이프라인
  - PostgreSQL 저장
  - Embedding 생성 (GPT-4o-mini)
  - Qdrant 인덱싱

**Deliverables**:
- 매일 자동으로 15,000 jobs 수집
- Job 목록 API 및 UI

#### Week 8: 중복 제거 및 Extension MVP

**Tasks**:
- [ ] Job 중복 제거 파이프라인
  - Hash-based exact match
  - Fuzzy matching (fuzzywuzzy)
  - Semantic deduplication (embedding similarity)
- [ ] Browser Extension MVP
  - LinkedIn job page content script
  - Job 데이터 추출 로직
  - 사용자 동의 UI
  - Backend API 연동 (/contributions/jobs)
- [ ] 데이터 품질 검증
  - 필수 필드 체크
  - Spam detection

**Deliverables**:
- 중복 제거된 Job DB
- Chrome Extension 설치 → LinkedIn 검색 → 데이터 기여

---

### Phase 5: Profile Analyzer Agent (Week 9-10)

**목표**: 첫 번째 AI Agent 구현

#### Week 9: LangGraph 프레임워크

**Tasks**:
- [ ] LangGraph 설정
  - StateGraph 정의
  - Agent State 스키마
  - Checkpointing 설정
- [ ] Base Agent 클래스
  - Agent interface
  - LLM 통합 (Claude Sonnet 4)
  - Prompt templates
- [ ] Profile Analyzer Agent v1
  - 이력서 텍스트 → GPT-4로 구조화
  - 경력 연차 계산
  - 스킬 추출 (NER + LLM validation)

**Deliverables**:
- Agent 프레임워크 작동
- 이력서 → 구조화된 JSON

#### Week 10: 스킬 정규화 및 준비도 평가

**Tasks**:
- [ ] 스킬 정규화
  - "React.js" → "React" 매핑
  - 동의어 처리
  - Neo4j 스킬 매칭
- [ ] 이직 준비도 평가 알고리즘
  - 경력 연차 점수 (30%)
  - 스킬 적합도 점수 (40%)
  - 시장 타이밍 점수 (30%)
  - 최종 점수: 0-100
- [ ] Frontend Integration
  - 프로필 분석 결과 UI
  - 부족한 스킬 표시
  - 액션 아이템 제안

**Deliverables**:
- 프로필 → AI 분석 → 준비도 점수 + 개선 제안

---

### Phase 6: Job Matcher Agent (Week 11-12)

**목표**: Semantic Job Matching

#### Week 11: Embedding 및 Vector Search

**Tasks**:
- [ ] User Profile Embedding
  - 경력, 스킬, 선호도 → 텍스트 → embedding
  - Qdrant에 저장
- [ ] Job Embedding
  - Job description → embedding
  - 배치 처리 (기존 15,000 jobs)
- [ ] Qdrant Vector Search
  - Cosine similarity search
  - Filters (location, salary, etc.)
  - Top-K retrieval

**Deliverables**:
- User 로그인 → 추천 공고 (Vector similarity 기반)

#### Week 12: Multi-Factor Scoring

**Tasks**:
- [ ] 5개 차원 매칭 스코어링
  - Skill Match (35%): Cosine similarity
  - Experience Level (20%): Years match
  - Company Fit (20%): Culture, size preference
  - Location/Salary (15%)
  - Career Growth (10%)
- [ ] Explainable AI
  - 각 차원별 점수 및 근거 생성
  - "Python 90% match, AWS 80% match" 등
- [ ] Job Matcher Agent 완성
  - User profile → Top 10 matched jobs
  - 매칭 근거 설명

**Deliverables**:
- 개인화된 Job 추천 + 매칭 근거

---

### Phase 7: Browser Extension V2 (Week 13-14)

**목표**: Extension 확장 및 Gamification

#### Week 13: 멀티 플랫폼 지원

**Tasks**:
- [ ] Indeed extractor
- [ ] 사람인 extractor
- [ ] 잡코리아 extractor
- [ ] 배치 추출 (여러 페이지)
- [ ] 오프라인 큐 (네트워크 끊김 대응)

**Deliverables**:
- 4개 플랫폼에서 데이터 추출 가능

#### Week 14: Gamification

**Tasks**:
- [ ] 포인트 시스템 Backend
  - 기여당 포인트 계산
  - 마일스톤 보너스
  - Referral 보너스
- [ ] Premium 티어 관리
  - 포인트 → Premium 전환
  - Premium 기능 잠금
- [ ] Extension UI 개선
  - 포인트 표시
  - 리더보드
  - 배지 시스템
- [ ] Extension Store 준비
  - 아이콘, 스크린샷
  - 설명 작성

**Deliverables**:
- Gamification 시스템 작동
- 50명 베타 테스터 모집

---

### Phase 8: RAG 파이프라인 (Week 15-16)

**목표**: LightRAG 기반 Hybrid Search

#### Week 15: LightRAG 설정

**Tasks**:
- [ ] LightRAG 설치 및 설정
- [ ] Neo4j + Qdrant 통합
- [ ] Job descriptions 인덱싱
- [ ] Company reviews 인덱싱
- [ ] Hybrid retrieval
  - Graph query (Cypher)
  - Vector search (Qdrant)
  - 결과 병합

**Deliverables**:
- "Python backend jobs in Seoul" → Hybrid search 결과

#### Week 16: Reranking 및 데이터 품질

**Tasks**:
- [ ] Cohere Reranking API 통합
  - Retrieved docs → Rerank → Top-K
- [ ] Company Intelligence 통합
  - Glassdoor reviews
  - Crunchbase 펀딩 정보
- [ ] 데이터 품질 대시보드
  - Job freshness
  - Duplicate rate
  - User contribution stats

**Deliverables**:
- RAG 파이프라인 완성
- Admin 대시보드

---

### Phase 9: Application Assistant Agent (Week 17-18)

**목표**: 지원서 자동화

#### Week 17: Resume Optimizer

**Tasks**:
- [ ] Job-tailored Resume 생성
  - Job description 키워드 추출
  - 관련 경험 강조
  - ATS 최적화
- [ ] Cover Letter Generator
  - 템플릿 기반 생성
  - LLM으로 개인화
- [ ] Version Management
  - 공고별 이력서 저장

**Deliverables**:
- Job 클릭 → "맞춤 이력서 생성" 버튼 → PDF 다운로드

#### Week 18: Application Tracker

**Tasks**:
- [ ] Kanban Board UI
  - 지원 중, 서류 통과, 면접, 오퍼
  - Drag & drop
- [ ] 자동 리마인더
  - 지원 후 7일 (follow-up)
  - 면접 전 1일
- [ ] Statistics
  - 지원율, 응답률, 전환율

**Deliverables**:
- 지원 현황 대시보드

---

### Phase 10: Interview Coach Agent (Week 19-20)

**목표**: 면접 준비 시스템

#### Week 19: 면접 DB 및 Mock Interview

**Tasks**:
- [ ] 면접 질문 DB 구축
  - 100+ 기업별 질문 시드
  - 크라우드소싱 메커니즘
- [ ] Mock Interview (텍스트)
  - GPT-4가 면접관 역할
  - STAR 메소드 평가
  - 답변 피드백

**Deliverables**:
- 텍스트 기반 모의 면접

#### Week 20: Voice Interview

**Tasks**:
- [ ] Whisper STT 통합
- [ ] ElevenLabs TTS 통합
- [ ] Real-time voice interview
- [ ] 답변 분석
  - 구조 (STAR)
  - 구체성
  - 간결성
  - 관련성

**Deliverables**:
- 음성 모의 면접 기능

---

### Phase 11: Negotiation Advisor Agent (Week 21-22)

**목표**: 오퍼 협상 지원

#### Week 21: 연봉 데이터 수집

**Tasks**:
- [ ] Levels.fyi 데이터 수집
- [ ] Extension에서 연봉 데이터 기여 기능
- [ ] Salary DB 구축

**Deliverables**:
- 직무/연차별 연봉 분포 데이터

#### Week 22: Offer Comparison & Negotiation

**Tasks**:
- [ ] Offer Comparison Matrix
  - 연봉, 보너스, 스톡 옵션
  - 복지, 성장 기회
  - Multi-dimensional scoring
- [ ] Negotiation Simulator
  - 시나리오별 예상 결과
- [ ] 협상 스크립트 생성

**Deliverables**:
- 오퍼 비교 및 협상 조언

---

### Phase 12: Beta 테스트 및 출시 (Week 23-24)

**목표**: 200+ 사용자 베타 테스트

#### Week 23: Beta 테스트

**Tasks**:
- [ ] 200명 베타 테스터 모집
  - Product Hunt 사전 등록
  - LinkedIn, Facebook 포스팅
- [ ] 피드백 수집
  - In-app survey
  - User interview
- [ ] 버그 수정
- [ ] UX 개선

**Deliverables**:
- 피드백 기반 개선

#### Week 24: 최적화 및 출시 준비

**Tasks**:
- [ ] Extension 최적화
  - 성능 (메모리, 속도)
  - 크로스 브라우저 (Chrome, Edge, Firefox)
- [ ] 보안 감사
  - OWASP Top 10 체크
  - 데이터 암호화
- [ ] 문서화
  - API docs (Swagger)
  - User guide
  - Extension guide
- [ ] Chrome Web Store 제출
  - 스토어 리스팅
  - 마케팅 자료

**Deliverables**:
- MVP 출시 완료
- 1,000 target users

---

## 8. Git Workflow

### 8.1 브랜치 전략 (Git Flow)

```
main
  └─ develop
       ├─ feature/user-auth
       ├─ feature/job-matcher
       ├─ feature/extension-mvp
       └─ release/v1.0
```

**브랜치 규칙**:
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: 기능 개발
- `bugfix/*`: 버그 수정
- `release/*`: 릴리즈 준비

### 8.2 Commit Convention

```
type(scope): subject

body

footer
```

**Types**:
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포맷팅
- `refactor`: 리팩토링
- `test`: 테스트 추가
- `chore`: 빌드, 설정 변경

**Example**:
```
feat(backend): add job matching API

Implement multi-factor scoring algorithm for job matching.
Includes skill match, experience level, and company fit.

Closes #42
```

### 8.3 PR 프로세스

1. Feature branch 생성
2. 개발 및 로컬 테스트
3. PR 생성 (→ develop)
4. CI 통과 확인
5. Code review (1+ approvals)
6. Merge (Squash and merge)

---

## 9. 테스트 전략

### 9.1 Backend 테스트

```python
# tests/test_job_matcher.py
import pytest
from app.agents.job_matcher import JobMatcherAgent

@pytest.mark.asyncio
async def test_job_matching():
    agent = JobMatcherAgent()
    user_profile = {...}
    jobs = await agent.match_jobs(user_profile, limit=10)

    assert len(jobs) == 10
    assert jobs[0].match_score > 0.8
```

**테스트 범위**:
- Unit tests (pytest): 각 함수, 클래스
- Integration tests: API 엔드포인트
- E2E tests: User flow

**목표 커버리지**: 80%+

### 9.2 Frontend 테스트

```typescript
// __tests__/JobCard.test.tsx
import { render, screen } from '@testing-library/react'
import JobCard from '@/components/jobs/JobCard'

describe('JobCard', () => {
  it('renders job information', () => {
    const job = { title: 'Backend Engineer', company: 'ABC Corp' }
    render(<JobCard job={job} />)
    expect(screen.getByText('Backend Engineer')).toBeInTheDocument()
  })
})
```

**테스트 도구**:
- Vitest
- React Testing Library
- Playwright (E2E)

### 9.3 Extension 테스트

- Unit tests: Extractor 로직
- Integration tests: API 통신
- Manual tests: 각 플랫폼에서 실제 추출

---

## 10. 배포 전략

### 10.1 환경

- **Development**: 로컬 Docker Compose
- **Staging**: Azure AKS (단일 node)
- **Production**: Azure AKS (Multi-node, auto-scaling)

### 10.2 CI/CD Pipeline

```yaml
# .github/workflows/backend-ci.yml
name: Backend CI/CD

on:
  push:
    branches: [develop, main]
    paths:
      - 'apps/backend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd apps/backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd apps/backend
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to AKS
        run: |
          # kubectl apply -f k8s/backend.yaml
```

### 10.3 배포 순서

1. **Week 12**: Staging 환경 구축
2. **Week 18**: Staging 배포 및 테스트
3. **Week 24**: Production 배포

---

## 11. 마일스톤 및 KPI

### 11.1 Phase별 마일스톤

| Week | Milestone | Success Criteria |
|------|-----------|------------------|
| 2 | 개발 환경 구축 | Docker Compose 실행 가능 |
| 4 | 사용자 인증 | 회원가입 → 로그인 → 대시보드 |
| 6 | Knowledge Graph | 500+ 스킬, 100+ 회사 |
| 8 | Job 수집 | 15,000 jobs/day |
| 10 | Profile Analyzer | 이력서 → 준비도 점수 |
| 12 | Job Matcher | 개인화된 추천 10개 |
| 14 | Extension V2 | 4개 플랫폼 지원 |
| 16 | RAG Pipeline | Hybrid search 작동 |
| 18 | Application Assistant | 맞춤 이력서 생성 |
| 20 | Interview Coach | 음성 모의 면접 |
| 22 | Negotiation Advisor | 오퍼 비교 |
| 24 | MVP 출시 | 1,000 users |

### 11.2 핵심 KPI

**Product Metrics** (6개월 목표):
- 총 사용자: 1,000+
- DAU/MAU: 0.3
- 활성화율: 70%
- NPS: 50+

**Technical Metrics**:
- API P95 latency: < 2초
- System uptime: 99.5%
- Job coverage: 25,000 unique jobs
- RAG accuracy: 0.85+

**Business Metrics**:
- Extension 설치: 1,000+
- 일 기여 데이터: 10,000 jobs
- Premium 전환: 10%

---

## 12. 리스크 관리

### 12.1 주요 리스크

| Risk | Impact | Probability | Mitigation |
|------|--------|------------|------------|
| **LLM 비용 초과** | High | Medium | Caching, 작은 모델 사용, 월별 예산 알림 |
| **Extension 채택 저조** | High | Medium | 강력한 인센티브, 마케팅, 바이럴 루프 |
| **LinkedIn 차단** | Medium | Low | 공공 데이터만, 다중 소스 확보 |
| **데이터 품질 저하** | Medium | Medium | AI validation, 사용자 신고, 품질 점수 |
| **개발 일정 지연** | Medium | High | 우선순위 조정, MVP 범위 축소 |

### 12.2 리스크 모니터링

**주간 체크리스트**:
- [ ] LLM API 사용량 확인
- [ ] Extension 설치 수 추적
- [ ] 데이터 수집 상태 확인
- [ ] 버그 심각도 검토
- [ ] 일정 진행률 확인

---

## 13. 다음 단계

### 13.1 즉시 실행 (이번 주)

1. **프로젝트 초기화**
   ```bash
   # Monorepo 생성
   mkdir -p apps/{backend,frontend,extension}
   mkdir -p packages/{types,utils,config}
   mkdir -p infra/{docker,terraform,kubernetes}
   pnpm init
   ```

2. **Backend 프로젝트 생성**
   ```bash
   cd apps/backend
   mkdir -p app/{api,agents,core,db,schemas,services,rag}
   touch app/main.py
   touch requirements.txt
   ```

3. **Frontend 프로젝트 생성**
   ```bash
   cd apps/frontend
   npx create-next-app@latest . --typescript --tailwind --app
   npx shadcn-ui@latest init
   ```

4. **Docker Compose 작성**
   - PostgreSQL, Neo4j, Qdrant, Redis 설정

### 13.2 이번 주 목표

- [ ] Monorepo 구조 완성
- [ ] Backend "Hello World" API
- [ ] Frontend "Hello World" 페이지
- [ ] Docker Compose 실행 성공

### 13.3 팀 구성 (필요 시)

- Backend Engineer (1-2명)
- Frontend Engineer (1명)
- ML Engineer (1명, Part-time)
- DevOps (Part-time)

---

## 부록

### A. 참고 문서

- [기획서](./CareerNavigator_기획서_v1.0.md)
- [LangGraph 문서](https://langchain-ai.github.io/langgraph/)
- [Neo4j 가이드](https://neo4j.com/docs/)
- [Qdrant 문서](https://qdrant.tech/documentation/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Next.js 문서](https://nextjs.org/docs)

### B. 연락처

- **Project Lead**: [Name]
- **Email**: dev@careernavigator.ai
- **GitHub**: https://github.com/careernavigator
- **Slack**: #careernavigator-dev

---

**문서 버전**: 1.0
**최종 업데이트**: 2024-11-24
**다음 리뷰**: Week 4, Week 12, Week 20

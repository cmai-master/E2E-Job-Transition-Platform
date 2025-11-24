# CareerNavigator: AI 기반 이직 솔루션

**Product Requirements Document**  
Version 1.0  
2024-11-24

---

## 목차

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement & Market Analysis](#2-problem-statement--market-analysis)
3. [Product Vision & Core Value Proposition](#3-product-vision--core-value-proposition)
4. [System Architecture](#4-system-architecture)
5. [Data Sourcing Strategy](#5-data-sourcing-strategy)
6. [Core Features & Specifications](#6-core-features--specifications)
7. [Data Model & Entity Design](#7-data-model--entity-design)
8. [Technical Stack](#8-technical-stack)
9. [Implementation Roadmap](#9-implementation-roadmap)
10. [Success Metrics & KPIs](#10-success-metrics--kpis)
11. [Risk Analysis & Mitigation](#11-risk-analysis--mitigation)
12. [Conclusion](#12-conclusion)

---

## 1. Executive Summary

CareerNavigator는 AI 기술을 활용하여 구직자의 이직 전 과정을 지능적으로 지원하는 통합 플랫폼입니다. Multi-Agent Architecture와 Knowledge Graph 기반 시맨틱 모델링을 통해 개인화된 이직 전략 수립부터 오퍼 협상까지 end-to-end 경험을 제공합니다.

### 주요 Pain Points 해결

본 솔루션은 이직 프로세스의 주요 pain point를 다음과 같이 해결합니다:

- **정보 비대칭**: 기업 정보, 연봉 수준, 채용 트렌드에 대한 불충분한 데이터
- **시간 비효율**: 수십 개 채용 플랫폼 모니터링 및 중복 지원서 작성
- **준비 부족**: 기업별 면접 패턴, 기술 면접 대비 체계 부재
- **의사결정 어려움**: 복수 오퍼 비교 시 정량적 평가 기준 부재

### 핵심 차별화 요소

- **혁신적 데이터 소싱**: Browser Extension 기반 User-Contributed Data 전략으로 법적으로 안전하면서도 LinkedIn 포함 모든 플랫폼 데이터 수집 (사용자 1,000명 = 일 10,000개 job)
- **Context-Aware AI Agents**: 사용자의 경력, 스킬, 선호도를 지속적으로 학습하여 개인화된 추천 제공
- **Knowledge Graph 기반 매칭**: 스킬-직무-기업 간 semantic relationship을 활용한 정교한 매칭
- **Production-Ready RAG System**: 실시간 채용 정보, 기업 인텔리전스 통합 검색
- **Agent Orchestration**: 매칭, 코칭, 협상 등 전문화된 에이전트 간 협업

### 핵심 혁신: User-Contributed Data Network

기존 채용 플랫폼과의 가장 큰 차별점은 **사용자가 자신의 검색 데이터를 공유하는 P2P 데이터 네트워크**입니다:

```
전통적 방식 (크롤링):
- 법적 리스크: High (ToS 위반)
- 탐지 위험: High (IP 차단)
- 확장성: Low (인프라 비용 증가)

CareerNavigator 방식 (Browser Extension):
- 법적 리스크: Zero (사용자 본인 데이터)
- 탐지 위험: Zero (정상 사용자 트래픽)
- 확장성: Exponential (사용자 증가 = 데이터 증가)
```

**네트워크 효과**:
- 50명 사용자 → 500 jobs/day
- 500명 사용자 → 5,000 jobs/day
- 1,000명 사용자 → 10,000 jobs/day (LinkedIn 포함)
- 5,000명 사용자 → 50,000 jobs/day

**인센티브 시스템**: Gamification + Premium 보상으로 사용자 참여 유도
- 10 포인트 = Premium 1주일
- 100 포인트 = Premium 3개월
- 1,000 포인트 = Lifetime Premium

---

## 2. Problem Statement & Market Analysis

### 2.1 현재 이직 시장의 문제점

한국 이직 시장은 연간 300만 건 이상의 구직 활동이 발생하지만, 기존 솔루션들은 다음과 같은 한계를 가지고 있습니다.

| 문제 영역 | 현상 및 영향 |
|---------|------------|
| **정보 파편화** | 채용 정보가 LinkedIn, 사람인, 잡코리아, 원티드 등 10개 이상 플랫폼에 분산. 평균적으로 구직자는 하루 2-3시간을 단순 검색에 소비 |
| **스킬 매칭 부정확** | 키워드 기반 검색의 한계로 semantic matching 불가. 'TensorFlow' 경험자가 'ML Framework' 요구 공고를 놓치는 사례 빈발 |
| **준비 체계 부재** | 기업별 면접 패턴, 예상 질문, 기술 면접 유형에 대한 구조화된 정보 부족. 준비 시간 대비 효율성 저하 |
| **협상력 약화** | 시장 연봉 데이터, 복지 비교 정보 부족으로 협상 시 불리한 위치. 연봉 협상에서 평균 15-20% 손실 추정 |

### 2.2 Target User Persona

**Primary**: 3-10년차 IT 전문직 (개발자, 데이터 사이언티스트, PM, 컨설턴트)

- **특성**: 높은 디지털 리터러시, 커리어 성장 지향적, 데이터 기반 의사결정 선호
- **Pain Point**: 시간 부족, 정보 과부하, 체계적 준비 어려움
- **기대 가치**: 효율성, 개인화, 의사결정 지원

---

## 3. Product Vision & Core Value Proposition

### 3.1 Vision Statement

> **"AI 코파일럿이 함께하는 모든 이직 여정에서 최적의 의사결정을 지원한다"**

### 3.2 Core Value Proposition

| 사용자 가치 | 기술적 구현 | 측정 지표 |
|-----------|-----------|----------|
| **시간 절약**: 이직 준비 시간 60% 단축 | Multi-source aggregation, Auto-apply, AI resume optimization | 준비 시간 (Before vs After) |
| **매칭 정확도**: 적합 포지션 발견율 3배 향상 | Knowledge Graph, Semantic Search, LLM-based scoring | 면접 전환율, 오퍼 수락률 |
| **협상력 강화**: 평균 연봉 협상 15% 개선 | Market data aggregation, Offer comparison, Negotiation simulator | 최종 연봉 vs 초기 오퍼 |

---

## 4. System Architecture

### 4.1 High-Level Architecture Overview

CareerNavigator는 Multi-Agent Orchestration 패턴을 채택하여, 각 이직 단계별로 전문화된 AI Agent들이 협업하는 구조입니다. Central Context Manager가 사용자 프로필, 이직 히스토리, 실시간 의사결정을 통합 관리하며, 각 Agent는 독립적으로 작동하되 필요 시 서로 협력합니다.

### 4.2 Multi-Agent Architecture (5C Framework)

시스템은 5C Framework를 기반으로 설계되었습니다:

#### 1. Centralized Context: Context Manager가 모든 Agent에게 일관된 사용자 컨텍스트 제공

User Profile, Career History, Preferences, Application State를 Neo4j Knowledge Graph와 Qdrant Vector DB에 저장. LangGraph의 StateGraph로 컨텍스트 흐름 관리

#### 2. Coordinated Agents: 역할별로 전문화된 Agent 구성

- **Profile Analyzer Agent**: 이력서 파싱, 스킬 추출, 경력 분석
- **Job Matcher Agent**: 채용 공고 검색, 매칭 스코어링, 추천
- **Application Assistant Agent**: 지원서 자동 생성, 최적화
- **Interview Coach Agent**: 모의 면접, 답변 피드백
- **Negotiation Advisor Agent**: 오퍼 분석, 협상 전략 제안

#### 3. Connected Tools: External API 및 데이터 소스 통합

- **Job Boards API**: Indeed API, ZipRecruiter API, 국내 플랫폼 크롤러
- **Company Intelligence**: Crunchbase, Glassdoor, 뉴스 API
- **Salary Data**: Levels.fyi, PayScale, 공공 데이터

#### 4. Contextual Policy Control: 사용자 설정 및 거버넌스

개인정보 보호 정책, 지원 전략 (적극적/보수적), 알림 설정을 중앙 관리

#### 5. Continuous Observe & Improve: 피드백 루프 및 학습

매칭 결과, 면접 성공률, 오퍼 수락률 추적하여 모델 지속 개선

### 4.3 Knowledge Graph Design

Neo4j 기반 Knowledge Graph는 엔티티 간 semantic relationship을 모델링합니다.

| Node Type | Properties | Relationships |
|-----------|-----------|---------------|
| **User** | name, email, location, years_exp | HAS_SKILL, WORKED_AT, PREFERS, APPLIED_TO |
| **Skill** | name, category, proficiency | RELATED_TO (skill-skill), REQUIRED_BY (job) |
| **Job** | title, description, salary_range | POSTED_BY (company), REQUIRES (skill), SIMILAR_TO (job) |
| **Company** | name, size, industry, culture | USES_TECH (technology), IN_INDUSTRY, COMPETES_WITH |

**주요 Query 패턴**: Skill Taxonomy Traversal, Multi-hop Recommendations, Career Path Discovery

### 4.4 RAG Pipeline Architecture

LightRAG 기반 Hybrid Search로 구조화된 지식(KG)과 비구조화 텍스트(Vector DB)를 통합 검색합니다.

```
Indexing → Job descriptions, company reviews, interview experiences를 
          chunking 후 embedding (OpenAI text-embedding-3-large)

Retrieval → User query를 KG Cypher query + Vector similarity search로 병렬 처리

Ranking → LLM-based reranker로 최종 컨텍스트 선정 (Cohere rerank API)

Generation → Claude Sonnet 4로 context-aware 응답 생성
```

---

## 5. Data Sourcing Strategy

### 5.1 데이터 소싱의 현실적 제약

**LinkedIn 크롤링 불가**
- LinkedIn ToS는 크롤링을 명시적으로 금지 (하루 50개 프로필 제한)
- 2024년 법원 판결에서 LinkedIn이 hiQ Labs, Proxycurl 사건 모두 승소
- 공식 API는 매우 제한적 (사용자 명시 승인 필요, 기본 데이터만)
- 법적 리스크가 너무 커서 스타트업에게 부적합

**핵심 인사이트**: 전통적인 크롤링 대신 **사용자 기여 데이터 (User-Contributed Data)** 전략을 최우선으로 채택

### 5.2 Hybrid Data Sourcing 전략 개요

```
┌────────────────────────────────────────────────────────────┐
│                    3-Tier Architecture                     │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Tier 1 (PRIMARY): User-Contributed Data                  │
│  ├─ Browser Extension (Chrome/Edge)                       │
│  ├─ 사용자 1,000명 → 일 10,000개 job                      │
│  ├─ 법적으로 100% 안전 (사용자 본인 데이터)               │
│  └─ 비용: Extension 개발 비용만                            │
│      예상 수집량: 10-50 jobs/user/day                      │
│                                                            │
│  Tier 2 (SECONDARY): Official APIs                        │
│  ├─ Indeed API (공식)                                      │
│  ├─ 워크넷 API (공식)                                      │
│  ├─ ZipRecruiter API                                       │
│  └─ 신생 플랫폼 파트너십                                   │
│                                                            │
│  Tier 3 (TERTIARY): Selective Web Scraping                │
│  ├─ 대기업 채용 페이지 (robots.txt 허용)                  │
│  ├─ RSS/Sitemap monitoring                                │
│  └─ Rate-limited crawler (국내 플랫폼)                     │
│                                                            │
└────────────────────────────────────────────────────────────┘

Target: MVP 6개월 내 25,000+ active job listings
```

### 5.3 Tier 1: User-Contributed Data (최우선 전략) ⭐⭐⭐⭐⭐

#### 5.3.1 Browser Extension: Personal Job Discovery Network

**개념**: 각 사용자가 자신의 LinkedIn/Indeed 검색을 "Personal API"로 전환

**핵심 차별점**:
1. **분산 크롤링**: 1,000명 사용자 = 1,000개 IP주소, 자연스러운 트래픽 패턴
2. **Zero Detection Risk**: LinkedIn은 정상 사용자로 인식
3. **합법성**: 사용자 본인 데이터이므로 ToS 위반 없음
4. **네트워크 효과**: 사용자 증가 = 데이터 커버리지 기하급수적 증가

#### 5.3.2 Extension Architecture

```typescript
// Chrome Extension Architecture

// 1. manifest.json
{
  "manifest_version": 3,
  "name": "CareerNavigator Data Contributor",
  "permissions": ["storage", "activeTab", "scripting"],
  "host_permissions": [
    "https://www.linkedin.com/*",
    "https://www.indeed.com/*",
    "https://www.saramin.co.kr/*"
  ],
  "content_scripts": [{
    "matches": ["https://www.linkedin.com/jobs/*"],
    "js": ["content-script.js"]
  }],
  "background": {
    "service_worker": "background.js"
  }
}

// 2. content-script.js - LinkedIn 페이지에서 데이터 추출
class JobDataExtractor {
  extractFromLinkedIn() {
    const jobs = [];
    document.querySelectorAll('.job-card-container').forEach(card => {
      const jobData = {
        title: card.querySelector('.job-card-list__title')?.textContent,
        company: card.querySelector('.job-card-container__company-name')?.textContent,
        location: card.querySelector('.job-card-container__metadata-item')?.textContent,
        posted_date: this.extractDate(card),
        job_url: card.querySelector('a')?.href,
        // ... more fields
      };
      
      if (this.isValidJob(jobData)) {
        jobs.push(jobData);
      }
    });
    
    return jobs;
  }
  
  // 사용자에게 공유 의사 확인 (Opt-in)
  async promptUserConsent(jobs) {
    return new Promise(resolve => {
      // Show non-intrusive notification
      const consent = this.showConsentDialog({
        message: `Found ${jobs.length} jobs. Share to earn Premium?`,
        jobs_preview: jobs.slice(0, 3),
        reward: "10 points (= 1 week Premium)"
      });
      resolve(consent);
    });
  }
}

// 3. background.js - 서버로 데이터 전송
class DataContributionService {
  async contribute(jobData, userConsent) {
    if (!userConsent) return;
    
    try {
      const response = await fetch('https://api.careernavigator.ai/v1/contribute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Token': await this.getUserToken()
        },
        body: JSON.stringify({
          jobs: jobData,
          source: 'linkedin',
          timestamp: Date.now(),
          user_context: {
            search_query: this.getSearchQuery(),
            filters_applied: this.getActiveFilters()
          }
        })
      });
      
      if (response.ok) {
        const reward = await response.json();
        this.updateUserPoints(reward.points);
        this.showThankYouNotification(reward);
      }
    } catch (error) {
      console.error('Contribution failed:', error);
    }
  }
}
```

#### 5.3.3 Incentive System: Gamification & Rewards

**포인트 시스템**:
```javascript
const REWARD_STRUCTURE = {
  job_contribution: {
    unique_job: 1,        // 1 point per unique job
    with_salary: 2,       // +1 bonus if salary included
    with_description: 2,  // +1 bonus if full description
  },
  
  milestones: {
    first_10: 5,          // Bonus for first 10 contributions
    first_50: 20,         // Bonus for first 50 contributions
    first_100: 50,        // Bonus for first 100 contributions
  },
  
  redemption: {
    10: "Premium 1 week",
    50: "Premium 1 month",
    100: "Premium 3 months",
    500: "Premium 1 year",
    1000: "Lifetime Premium"  // Early contributor 혜택
  },
  
  // 네트워크 효과 보너스
  referral: {
    friend_joins: 10,     // Friend installs extension
    friend_contributes: 5 // Friend makes first contribution
  }
};
```

**성장 시뮬레이션**:
```
Week 1: 50 users × 10 jobs/day = 500 jobs/day
Week 4: 200 users × 10 jobs/day = 2,000 jobs/day
Week 12: 1,000 users × 10 jobs/day = 10,000 jobs/day
Week 24: 5,000 users × 10 jobs/day = 50,000 jobs/day

→ 24주 후: 50,000 daily active jobs
→ Unique jobs (중복 제거 후): ~30,000 jobs
```

#### 5.3.4 Backend: Data Ingestion Pipeline

```python
# FastAPI endpoint for data contribution
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import asyncio

app = FastAPI()

class JobContribution(BaseModel):
    jobs: List[dict]
    source: str
    timestamp: int
    user_context: dict

class DataIngestionService:
    def __init__(self):
        self.redis = Redis()
        self.postgres = PostgresDB()
        self.deduplicator = JobDeduplicator()
        
    async def process_contribution(self, contribution: JobContribution, user_id: str):
        """
        Process user-contributed job data
        """
        # 1. Quick validation
        validated_jobs = [j for j in contribution.jobs if self.validate(j)]
        
        # 2. Deduplication (Redis cache for fast lookup)
        new_jobs = []
        for job in validated_jobs:
            job_hash = self.generate_hash(job)
            if not await self.redis.exists(f"job:{job_hash}"):
                new_jobs.append(job)
                await self.redis.setex(f"job:{job_hash}", 86400, "1")  # 24h cache
        
        # 3. Enrich with AI
        enriched_jobs = await self.enrich_with_llm(new_jobs)
        
        # 4. Store in DB
        await self.postgres.bulk_insert(enriched_jobs)
        
        # 5. Update knowledge graph
        await self.update_neo4j(enriched_jobs)
        
        # 6. Reward user
        points_earned = self.calculate_reward(new_jobs)
        await self.reward_user(user_id, points_earned)
        
        return {
            "points": points_earned,
            "unique_jobs": len(new_jobs),
            "total_points": await self.get_user_points(user_id)
        }

@app.post("/v1/contribute")
async def contribute_data(
    contribution: JobContribution,
    user_id: str = Depends(get_current_user)
):
    """
    Endpoint for user-contributed job data
    """
    service = DataIngestionService()
    reward = await service.process_contribution(contribution, user_id)
    return reward
```

#### 5.3.5 Data Quality Control

```python
class ContributionQualityControl:
    """
    Ensure high-quality user contributions
    """
    
    def validate_job(self, job: dict) -> tuple[bool, str]:
        """
        Validate job data quality
        Returns: (is_valid, reason)
        """
        # Required fields check
        required = ['title', 'company', 'location']
        if not all(field in job for field in required):
            return False, "Missing required fields"
        
        # Spam detection
        if self.is_spam(job):
            return False, "Detected spam content"
        
        # Duplicate check (fuzzy)
        if self.is_near_duplicate(job):
            return False, "Near-duplicate detected"
        
        # Freshness check
        if self.is_outdated(job):
            return False, "Job posting too old"
        
        return True, "Valid"
    
    def enrich_with_llm(self, jobs: List[dict]) -> List[dict]:
        """
        Use LLM to extract and normalize data
        """
        enriched = []
        for job in jobs:
            # GPT-4o-mini for cost efficiency
            prompt = f"""
            Extract and normalize job information:
            
            Raw data: {json.dumps(job)}
            
            Output JSON with:
            - title (normalized)
            - company (canonical name)
            - location (city, country)
            - salary_range (if mentioned)
            - required_skills (list)
            - experience_years (min, max)
            - job_type (full-time, contract, etc)
            """
            
            response = self.llm.complete(prompt, response_format="json")
            enriched.append({**job, **response})
        
        return enriched
```

### 5.4 Tier 2: Official APIs (안정적 기반)

#### 공식 API 통합 전략

| 플랫폼 | API 제공 | 비용 | 데이터 품질 | 도입 우선순위 | 예상 수집량 |
|-------|---------|-----|-----------|-------------|-----------|
| **Indeed** | Publisher API | Job post 기준 과금 | 높음 (글로벌 최대) | **즉시** | 10,000+ jobs |
| **워크넷** | 공공 API | 무료 | 중간 (국내 전통 산업) | **즉시** | 5,000+ jobs |
| **ZipRecruiter** | Jobs API | 파트너십 협상 | 높음 (미국 중심) | Phase 2 | 3,000+ jobs |
| **Glassdoor** | Employer API | 파트너십 필요 | 높음 (리뷰 데이터) | Phase 2 | Company data |

**구현 전략**:
```python
# API Aggregator Pattern
class JobAPIAggregator:
    def __init__(self):
        self.indeed = IndeedAPI(api_key=settings.INDEED_KEY)
        self.worknet = WorknetAPI(api_key=settings.WORKNET_KEY)
        self.ziprecruiter = ZipRecruiterAPI(api_key=settings.ZIP_KEY)
        
    async def search_all(self, query: str, location: str) -> List[Job]:
        """
        Parallel search across all APIs
        """
        tasks = [
            self.indeed.search(query, location),
            self.worknet.search(query, location),
            self.ziprecruiter.search(query, location)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten and deduplicate
        all_jobs = []
        for result in results:
            if isinstance(result, list):
                all_jobs.extend(result)
        
        return self.deduplicate(all_jobs)
```

### 5.5 Tier 3: Selective Web Scraping (보조 수단)

#### 국내 플랫폼 크롤링

| 플랫폼 | robots.txt | 크롤링 난이도 | 법적 리스크 | 전략 | 예상 수집량 |
|-------|-----------|-------------|-----------|------|-----------|
| **사람인** | 부분 허용 | 중간 | 중간 | Rate-limited | 4,000+ jobs |
| **잡코리아** | 부분 허용 | 중간 | 중간 | Rate-limited | 4,000+ jobs |
| **원티드** | API 없음 | 높음 (SPA) | 중간 | Headless browser | 3,000+ jobs |
| **대기업 채용** | 대부분 허용 | 낮음 | 낮음 | Direct crawl | 1,000+ jobs |

**구현 전략**:
```python
# Rate-limited, respectful crawler
class RespectfulCrawler:
    def __init__(self, site: str):
        self.rate_limit = 2  # 2 seconds per request
        self.user_agent = "CareerNavigator/1.0 (contact@careernavigator.ai)"
        self.robots_parser = self.load_robots_txt(site)
        
    async def crawl(self, url: str) -> Optional[dict]:
        # 1. Check robots.txt
        if not self.robots_parser.can_fetch(self.user_agent, url):
            logger.info(f"Blocked by robots.txt: {url}")
            return None
        
        # 2. Rate limiting
        await asyncio.sleep(self.rate_limit)
        
        # 3. Fetch with timeout
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                url,
                headers={"User-Agent": self.user_agent}
            )
        
        # 4. Parse and extract
        return self.parse(response.text)
```

### 5.6 LinkedIn 특화 전략: 3-Phase Approach

LinkedIn은 가장 높은 품질의 데이터를 가지고 있지만 접근이 제한적입니다. 단계적 전략을 제안합니다:

#### Phase 1 (Month 1-6): Browser Extension + OAuth

**전략**: 사용자 본인의 LinkedIn 검색 데이터 활용

```typescript
// Extension: LinkedIn Job Search Extractor
class LinkedInJobExtractor {
  // 사용자가 LinkedIn에서 "AI Engineer" 검색 시
  async extractSearchResults() {
    const jobs = this.parseJobCards();
    
    // 사용자에게 동의 요청
    const consent = await this.requestConsent({
      jobs_count: jobs.length,
      reward: "5 points (0.5 week Premium)",
      privacy: "We only collect job postings, not your personal data"
    });
    
    if (consent) {
      await this.contribute(jobs);
    }
  }
}
```

**장점**:
- ✅ 법적으로 안전 (사용자 본인 데이터)
- ✅ Zero detection risk
- ✅ 자연스러운 트래픽 패턴

**목표**: 1,000명 사용자 × 10 LinkedIn jobs/day = 10,000 LinkedIn jobs/day

#### Phase 2 (Month 6-12): Local RPA Tools

**전략**: Bardeen, Axiom 같은 Local RPA 도구 통합

사용자가 Bardeen을 설치하고 CareerNavigator와 연동하면, 자동으로 LinkedIn 검색 결과를 수집하여 플랫폼으로 전송

```javascript
// Bardeen Playbook Integration (개념)
const playbook = {
  name: "LinkedIn to CareerNavigator",
  trigger: "when_user_opens_linkedin_jobs",
  actions: [
    "scrape_current_page_jobs",
    "send_to_webhook(https://api.careernavigator.ai/bardeen)"
  ],
  consent: "user_opt_in_required"
};
```

**장점**:
- 사용자 브라우저에서 실행 (사용자 IP)
- Human-like behavior
- No-code 설정

**단점**:
- 사용자 설치 필요 (마찰)
- 제3자 서비스 의존성

#### Phase 3 (Year 2+): Official Partnership

**전략**: Talent Solutions Partnership 신청

**자격 요건**:
- 1,000+ 기업 고객
- Product-Market Fit 입증
- 상당한 사용자 베이스

**타임라인**:
```
Year 1: 다른 소스로 시작, PMF 확립
Year 2 Q1: Partnership 신청
Year 2 Q2-Q3: 협상 및 통합
Year 2 Q4: 공식 LinkedIn Job API 접근
```

**예상 비용**: $50K - $200K/year (Enterprise tier)

### 5.7 데이터 소싱 우선순위 (6개월 MVP)

#### Month 1-2: Foundation
- ✅ Indeed API 통합 (10,000 jobs)
- ✅ 워크넷 API 통합 (5,000 jobs)
- ✅ Browser Extension MVP 개발
- ✅ 50 beta users × 10 jobs/day = 500 contributed jobs
- **Total**: ~15,500 jobs/day

#### Month 3-4: Expansion
- ✅ Extension 사용자 확장 (500 users → 5,000 contributed jobs/day)
- ✅ 사람인, 잡코리아 crawler (8,000 jobs)
- ✅ 대기업 채용 페이지 (1,000 jobs)
- **Total**: ~28,500 jobs/day

#### Month 5-6: Optimization
- ✅ Extension 1,000 users (10,000 contributed jobs/day)
- ✅ ZipRecruiter API 통합 (3,000 jobs)
- ✅ 데이터 품질 모니터링 및 중복 제거 고도화
- **Total**: ~36,500 jobs/day
- **Unique jobs** (after deduplication): ~25,000 jobs

### 5.8 데이터 품질 관리

```python
# Comprehensive Deduplication Pipeline
class AdvancedJobDeduplicator:
    def __init__(self):
        self.embedding_model = OpenAIEmbeddings()
        self.fuzzy_matcher = FuzzyMatcher()
        
    async def deduplicate(self, jobs: List[Job]) -> List[Job]:
        """
        Multi-stage deduplication
        """
        # Stage 1: Exact match (hash-based)
        unique_jobs = {}
        for job in jobs:
            job_hash = self.compute_hash(job)
            if job_hash not in unique_jobs:
                unique_jobs[job_hash] = job
        
        # Stage 2: Fuzzy match (company + title + location)
        clusters = self.cluster_similar_jobs(unique_jobs.values())
        
        # Stage 3: Semantic similarity (embedding-based)
        final_jobs = []
        for cluster in clusters:
            representative = self.select_best_job(cluster)
            final_jobs.append(representative)
        
        return final_jobs
    
    def compute_hash(self, job: Job) -> str:
        """
        Generate unique hash for exact matching
        """
        key = f"{job.company}|{job.title}|{job.location}".lower()
        return hashlib.md5(key.encode()).hexdigest()
    
    async def cluster_similar_jobs(self, jobs: List[Job]) -> List[List[Job]]:
        """
        Cluster jobs using embedding similarity
        """
        embeddings = await self.embedding_model.embed_batch(
            [f"{j.title} at {j.company} in {j.location}" for j in jobs]
        )
        
        # DBSCAN clustering
        clusters = DBSCAN(eps=0.1, min_samples=1).fit(embeddings)
        
        # Group by cluster
        result = defaultdict(list)
        for idx, label in enumerate(clusters.labels_):
            result[label].append(jobs[idx])
        
        return list(result.values())
```

### 5.9 법적 리스크 완화 전략

| 리스크 | 확률 | 영향 | 완화 전략 | 담당자 |
|-------|-----|------|----------|-------|
| **Extension 차단** | Low | Medium | - Public data만 수집<br>- Opt-in 방식<br>- 여러 fallback 소스 | CTO |
| **ToS 위반 소송** | Very Low | Critical | - 사용자 본인 데이터 (방어 가능)<br>- Legal counsel 상시 자문 | Legal |
| **사용자 채택 저조** | Medium | High | - 강력한 인센티브<br>- Viral loop 설계<br>- Product Hunt 런칭 | Growth |
| **데이터 품질 저하** | Low | Medium | - AI validation<br>- User reporting system<br>- Quality score 추적 | Data |
| **플랫폼 제재** | Low | Medium | - 다중 소스 확보<br>- API 우선<br>- Rate limiting | Product |

**법무 검토 체크리스트**:
- [ ] Browser Extension ToS 및 Privacy Policy 작성
- [ ] 사용자 데이터 수집 동의서 (GDPR, CCPA 준수)
- [ ] 각 플랫폼 ToS 상세 분석 및 compliance 확인
- [ ] 데이터 보관 및 삭제 정책 수립
- [ ] 저작권 침해 방지 (원본 링크 제공, full text 저장 안 함)

---

## 6. Core Features & Specifications

### 6.1 Phase 1: 진단 및 전략 수립

#### 6.1.1 AI 경력 분석 (Profile Analyzer Agent)

**Feature 1**: 이력서 자동 파싱
- **Input**: PDF/DOCX 이력서 업로드
- **Processing**: PyPDF2, python-docx로 텍스트 추출 → spaCy NER로 엔티티 인식 → GPT-4로 구조 분석
- **Output**: 구조화된 JSON (경력, 학력, 프로젝트, 스킬)

**Feature 2**: 스킬 벡터화 및 Gap Analysis
- 현재 스킬셋을 embedding space에 배치
- 목표 직무 요구사항과 cosine similarity 계산
- **Output**: 스킬 매트릭스, 부족 스킬 리스트, 추천 학습 경로

**Feature 3**: 이직 준비도 평가
- **알고리즘**: Weighted scoring model
  - 경력 연차: 30% (주니어/시니어 적합성)
  - 스킬 적합도: 40% (현재 보유 vs 시장 수요)
  - 시장 타이밍: 30% (채용 시즌, 경기 전망)
- **Output**: 0-100점 준비도 점수 + 액션 아이템

#### 6.1.2 개인화된 이직 로드맵

**Feature 1**: 단계별 액션 플랜 자동 생성
```
Week 1-2: 프로필 최적화, 네트워킹 시작
Week 3-4: 목표 기업 리스트업, 지원 시작
Week 5-8: 면접 준비 및 진행
Week 9-12: 오퍼 협상 및 온보딩 준비
```

**Feature 2**: 마일스톤 추적 대시보드
- 진행률 시각화 (Progress bar, Gantt chart)
- 완료된 태스크 체크리스트
- 다음 액션 아이템 하이라이트

### 6.2 Phase 2: 지능형 포지션 매칭

#### 6.2.1 Multi-Source Job Aggregation

**데이터 소스별 수집 전략**:

| 소스 | 수집 방법 | 수집 주기 | 예상 공고 수 |
|-----|----------|----------|-----------|
| Indeed API | REST API | 실시간 | 10,000+ |
| 워크넷 | 공공 API | 1시간 | 5,000+ |
| 대기업 채용 페이지 | Web crawler | 1일 | 1,000+ |
| 사람인/잡코리아 | Rate-limited crawler | 1시간 | 8,000+ |
| 사용자 기여 | Browser extension | 실시간 | 500+ (초기) |

**중복 제거 및 정규화**:
- Fuzzy string matching (fuzzywuzzy) + Entity Resolution
- 동일 공고 판별 기준: Company name (90%+ match) + Job title (85%+ match) + Location (exact)

#### 6.2.2 Semantic Job Matching

**Multi-Factor Scoring**: 5개 차원 종합 평가

| 매칭 차원 | 계산 방식 | 가중치 |
|----------|----------|-------|
| **Skill Match** | Cosine similarity (user_skills, job_requirements) | 35% |
| **Experience Level** | Years of experience vs required range | 20% |
| **Company Fit** | Culture, size, industry preference matching | 20% |
| **Location/Salary** | Location preference + salary expectation | 15% |
| **Career Growth** | Learning opportunity, promotion path | 10% |

**최종 매칭 스코어**:
```python
def calculate_match_score(user, job):
    skill_score = cosine_similarity(user.skill_vector, job.skill_vector)
    exp_score = experience_fit(user.years_exp, job.required_exp)
    company_score = company_culture_match(user.preferences, job.company)
    location_score = location_salary_fit(user, job)
    growth_score = career_growth_potential(user, job)
    
    return (
        skill_score * 0.35 +
        exp_score * 0.20 +
        company_score * 0.20 +
        location_score * 0.15 +
        growth_score * 0.10
    )
```

**Explainable AI**: 매칭 점수 근거 제시
- 예시: "Python (90% match), AWS (80% match), Team size preference (75% match)"
- 각 차원별 기여도 막대 그래프 시각화

#### 6.2.3 Company Intelligence Dashboard

**데이터 소스**:
- Crunchbase: 펀딩, 투자자, 성장률
- Glassdoor: 직원 리뷰, 평점
- Google News API: 최근 6개월 뉴스
- StackShare: 기술 스택

**Feature**:
1. **기업 프로필 종합**: 사업 영역, 재무 상태, 투자 유치 이력
2. **리뷰 통합**: Sentiment analysis로 긍정/부정 트렌드 분석
3. **기술 스택 분석**: Tech radar 시각화
4. **성장성 지표**: 직원 수 증가율, 펀딩 라운드 진행 상황

### 6.3 Phase 3: 지원 자동화

#### 6.3.1 AI Resume Optimizer

**Feature 1**: Job-tailored Resume
- 공고 키워드 추출 (TF-IDF + NER)
- Resume 내 관련 경험 강조 재배치
- ATS (Applicant Tracking System) 통과율 시뮬레이션

**Feature 2**: Cover Letter Generator
```
Template:
1. Why this company (recent news, mission alignment)
2. Why this role (skill match, career goals)
3. My fit (quantified achievements)
4. Call to action
```

**Feature 3**: Version Management
- 공고별 이력서 버전 저장
- A/B 테스트: 어떤 버전이 응답률 높은지 추적

#### 6.3.2 Application Tracker

**Feature**:
1. **Kanban Board**: 지원 중, 서류 통과, 면접 예정, 오퍼 받음 상태 관리
2. **자동 리마인더**: 지원 후 7일 (follow-up), 면접 전 1일 (준비)
3. **Statistics Dashboard**: 
   - 지원율 (Apply rate)
   - 응답률 (Response rate)
   - 면접 전환율 (Interview conversion)

### 6.4 Phase 4: 면접 코파일럿

#### 6.4.1 Interview Preparation Hub

**Feature 1**: 기업별 면접 DB (크라우드소싱)
- 1000+ 기업 면접 후기
- 예상 질문 (빈도 순 정렬)
- 면접관 스타일 (압박 vs 편안함)

**Feature 2**: 직무별 기술 면접 패턴
- 알고리즘: LeetCode 스타일 문제 + 풀이 전략
- 시스템 디자인: 대규모 시스템 설계 템플릿
- ML: 모델 선택, 하이퍼파라미터 튜닝 질문

**Feature 3**: Behavioral Questions
- STAR 메소드 프레임워크
- 답변 템플릿 50개 (Leadership, Teamwork, Conflict resolution)

#### 6.4.2 AI Mock Interview

**Feature 1**: Real-time Voice Interview
- **Tech Stack**: Whisper API (STT) → GPT-4 (면접관 역할) → ElevenLabs (TTS)
- **시나리오**: 기술 면접, 행동 면접, 케이스 인터뷰
- **난이도 조절**: Easy, Medium, Hard

**Feature 2**: 답변 분석 및 피드백
- **평가 기준**:
  - STAR 구조 준수 (0-10점)
  - 구체성 (specific examples) (0-10점)
  - 간결성 (rambling 여부) (0-10점)
  - Relevance (질문과의 적합도) (0-10점)
- **개선 제안**: "Your answer lacked specific metrics. Try: 'I improved performance by 30%' instead of 'I improved performance significantly'"

### 6.5 Phase 5: 오퍼 협상 어시스턴트

#### 6.5.1 Offer Comparison Matrix

**Multi-dimensional Analysis**:

| 차원 | 측정 방법 | 가중치 |
|-----|----------|-------|
| Base Salary | 직접 비교 | 30% |
| Bonus & Equity | Expected value (3년) | 25% |
| Benefits | 항목별 점수화 | 15% |
| Career Growth | 승진 속도, 학습 기회 | 15% |
| Work-Life Balance | 근무 시간, 유연성 | 10% |
| Company Stability | 재무 건전성, 업계 전망 | 5% |

**Total Compensation Calculator**:
```python
def calculate_total_comp(offer, years=3):
    base_total = offer.base_salary * years
    bonus_total = offer.annual_bonus * years
    equity_value = offer.equity_shares * offer.share_price * (1 + offer.growth_rate) ** years
    
    return base_total + bonus_total + equity_value
```

#### 6.5.2 Negotiation Strategy Advisor

**Feature 1**: Market Benchmarking
- 동일 직무/연차 연봉 분포 (10th, 50th, 90th percentile)
- 데이터 소스: Levels.fyi, Glassdoor, 사용자 기여 데이터

**Feature 2**: Negotiation Simulator
- 시나리오별 예상 결과:
  - Conservative: Ask for 5% increase → 70% 수락 확률
  - Moderate: Ask for 10-15% → 50% 수락 확률
  - Aggressive: Ask for 20%+ → 30% 수락 확률

**Feature 3**: 협상 스크립트 생성
```
Template:
"Thank you for the offer. I'm excited about [specific aspect]. 
Based on my research showing [market data], and considering [your unique value], 
I was hoping we could discuss [specific ask]. 
Would you be open to exploring [alternative if rejected]?"
```

---

## 7. Data Model & Entity Design

### 7.1 Core Entities

#### User Profile Schema

```json
{
  "user_id": "uuid",
  "personal_info": {
    "name": "string",
    "email": "string",
    "location": {
      "city": "string",
      "country": "string"
    },
    "linkedin_url": "string",
    "github_url": "string"
  },
  "career_history": [
    {
      "company": "string",
      "title": "string",
      "start_date": "date",
      "end_date": "date",
      "responsibilities": ["string"],
      "achievements": [
        {
          "description": "string",
          "metrics": "string"
        }
      ]
    }
  ],
  "skills": [
    {
      "skill_name": "string",
      "category": "technical|domain|soft",
      "proficiency_level": "1-5",
      "years_used": "number"
    }
  ],
  "preferences": {
    "target_roles": ["string"],
    "target_companies": ["string"],
    "salary_expectation": {
      "min": "number",
      "max": "number",
      "currency": "KRW|USD"
    },
    "location_preference": ["string"],
    "work_style": "remote|hybrid|onsite",
    "company_size": "startup|scaleup|enterprise",
    "industry": ["string"]
  },
  "embeddings": {
    "profile_vector": "float[1536]"
  },
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

#### Job Posting Schema

```json
{
  "job_id": "uuid",
  "source": "indeed|worknet|saramin|jobkorea|company_site",
  "source_url": "string",
  "company_id": "uuid",
  "title": "string",
  "description": "text",
  "requirements": {
    "skills_required": ["string"],
    "skills_preferred": ["string"],
    "experience_years": {
      "min": "number",
      "max": "number"
    },
    "education": "string",
    "certifications": ["string"]
  },
  "responsibilities": ["string"],
  "compensation": {
    "salary_range": {
      "min": "number",
      "max": "number",
      "currency": "KRW|USD"
    },
    "equity": "boolean",
    "benefits": ["string"]
  },
  "location": {
    "city": "string",
    "country": "string",
    "remote_option": "boolean"
  },
  "embeddings": {
    "job_vector": "float[1536]"
  },
  "posted_date": "timestamp",
  "deadline": "timestamp",
  "status": "active|closed",
  "view_count": "number",
  "apply_count": "number"
}
```

#### Company Schema

```json
{
  "company_id": "uuid",
  "name": "string",
  "industry": "string",
  "size": "1-50|51-200|201-1000|1000+",
  "founded_year": "number",
  "headquarters": {
    "city": "string",
    "country": "string"
  },
  "description": "text",
  "website": "string",
  "social_links": {
    "linkedin": "string",
    "twitter": "string",
    "github": "string"
  },
  "funding": {
    "total_raised": "number",
    "last_round": "seed|series_a|series_b|...",
    "investors": ["string"]
  },
  "tech_stack": ["string"],
  "culture": {
    "values": ["string"],
    "perks": ["string"]
  },
  "ratings": {
    "glassdoor": "float",
    "jobplanet": "float"
  },
  "growth_metrics": {
    "employee_growth_rate": "float",
    "revenue_growth_rate": "float"
  }
}
```

#### Application Schema

```json
{
  "application_id": "uuid",
  "user_id": "uuid",
  "job_id": "uuid",
  "status": "draft|submitted|screening|interview_scheduled|interview_completed|offer_received|accepted|rejected",
  "applied_date": "timestamp",
  "resume_version": "string",
  "cover_letter": "text",
  "timeline": [
    {
      "status": "string",
      "date": "timestamp",
      "notes": "string"
    }
  ],
  "interview_records": [
    {
      "round": "number",
      "type": "phone|technical|behavioral|final",
      "date": "timestamp",
      "interviewer": "string",
      "notes": "text",
      "feedback": "text"
    }
  ],
  "offer_details": {
    "base_salary": "number",
    "bonus": "number",
    "equity": "string",
    "start_date": "date",
    "negotiation_history": ["string"]
  }
}
```

### 7.2 Application State Machine

```
States:
DRAFT → User가 지원 준비 중
SUBMITTED → 지원서 제출 완료
SCREENING → 서류 전형 중
INTERVIEW_SCHEDULED → 면접 일정 확정
INTERVIEW_COMPLETED → 면접 완료, 결과 대기
OFFER_RECEIVED → 오퍼 받음
ACCEPTED → 오퍼 수락
REJECTED → 탈락 또는 거절

Transitions:
DRAFT → SUBMITTED: submit_application()
SUBMITTED → SCREENING: company_received()
SCREENING → INTERVIEW_SCHEDULED: passed_screening()
SCREENING → REJECTED: failed_screening()
INTERVIEW_SCHEDULED → INTERVIEW_COMPLETED: complete_interview()
INTERVIEW_COMPLETED → OFFER_RECEIVED: receive_offer()
INTERVIEW_COMPLETED → REJECTED: failed_interview()
OFFER_RECEIVED → ACCEPTED: accept_offer()
OFFER_RECEIVED → REJECTED: decline_offer()
```

### 7.3 Neo4j Graph Schema

```cypher
// Nodes
CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE;
CREATE CONSTRAINT job_id IF NOT EXISTS FOR (j:Job) REQUIRE j.id IS UNIQUE;
CREATE CONSTRAINT company_id IF NOT EXISTS FOR (c:Company) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT skill_id IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE;

// Relationships
(:User)-[:HAS_SKILL {proficiency: int, years: int}]->(:Skill)
(:User)-[:WORKED_AT {start_date: date, end_date: date, title: string}]->(:Company)
(:User)-[:APPLIED_TO {date: timestamp, status: string}]->(:Job)
(:User)-[:PREFERS {weight: float}]->(:Company|Industry|Location)

(:Job)-[:REQUIRES {importance: string}]->(:Skill)
(:Job)-[:POSTED_BY]->(:Company)
(:Job)-[:SIMILAR_TO {similarity: float}]->(:Job)

(:Company)-[:USES_TECH]->(:Skill)
(:Company)-[:IN_INDUSTRY]->(:Industry)
(:Company)-[:COMPETES_WITH]->(:Company)

(:Skill)-[:RELATED_TO {similarity: float}]->(:Skill)
(:Skill)-[:CATEGORY_OF]->(:SkillCategory)
```

### 7.4 Qdrant Vector Collections

```python
# Collection 1: User Profiles
user_collection = {
    "vectors": {
        "size": 1536,  # OpenAI text-embedding-3-large
        "distance": "Cosine"
    },
    "payload_schema": {
        "user_id": "keyword",
        "skills": "keyword[]",
        "years_experience": "integer",
        "target_roles": "text[]"
    }
}

# Collection 2: Job Postings
job_collection = {
    "vectors": {
        "size": 1536,
        "distance": "Cosine"
    },
    "payload_schema": {
        "job_id": "keyword",
        "company_name": "keyword",
        "required_skills": "keyword[]",
        "salary_range": "float[]",
        "location": "geo"
    }
}

# Collection 3: Company Profiles
company_collection = {
    "vectors": {
        "size": 1536,
        "distance": "Cosine"
    },
    "payload_schema": {
        "company_id": "keyword",
        "industry": "keyword",
        "tech_stack": "keyword[]",
        "culture_values": "text[]"
    }
}
```

---

## 8. Technical Stack

### 8.1 전체 스택 개요

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **LLM** | Claude Sonnet 4, GPT-4o | Long context (200K), reasoning capability |
| **Orchestration** | LangGraph, LangChain | Agent coordination, state management |
| **Knowledge Graph** | Neo4j | Graph queries, relationship traversal |
| **Vector DB** | Qdrant | Fast similarity search, filtering |
| **RAG Framework** | LightRAG | Hybrid KG + vector retrieval |
| **Backend** | FastAPI (Python 3.11+) | Async, high performance |
| **Frontend** | Next.js 14, React, TypeScript | SSR, streaming responses |
| **Cloud** | Azure (AKS, Cosmos DB, Functions) | Scalability, managed services |
| **Monitoring** | LangSmith, Prometheus, Grafana | LLM tracing, metrics, alerting |

### 8.2 상세 기술 스택

#### Backend Stack

```python
# Core Framework
- FastAPI 0.104+
- Pydantic 2.0 (Data validation)
- SQLAlchemy 2.0 (ORM)
- Alembic (DB migrations)

# AI/ML
- LangChain 0.1.0
- LangGraph (Multi-agent orchestration)
- OpenAI SDK (GPT-4, embeddings)
- Anthropic SDK (Claude)
- Cohere (Reranking)

# Data Processing
- Pandas, NumPy
- spaCy (NER)
- Sentence-Transformers (Embeddings)
- PyPDF2, python-docx (Document parsing)

# Graph & Vector DB
- Neo4j Python Driver
- Qdrant Client
- LightRAG

# Web Scraping (when applicable)
- BeautifulSoup4
- Playwright (Headless browser)
- Scrapy (Crawler framework)
```

#### Frontend Stack

```typescript
// Core Framework
- Next.js 14 (App Router)
- React 18
- TypeScript 5.0

// State Management
- Zustand (Global state)
- React Query (Server state)

// UI Components
- shadcn/ui (Component library)
- Tailwind CSS 3.0
- Radix UI (Headless components)

// Visualization
- Recharts (Charts)
- React Flow (Graph visualization)
- D3.js (Custom viz)

// Form & Validation
- React Hook Form
- Zod (Schema validation)
```

#### Infrastructure

```yaml
# Cloud Provider: Azure
- Azure Kubernetes Service (AKS): Container orchestration
- Azure Cosmos DB: MongoDB-compatible NoSQL
- Azure Functions: Serverless crawlers
- Azure Blob Storage: Resume, documents
- Azure CDN: Static assets

# Databases
- Neo4j AuraDB: Managed graph database
- Qdrant Cloud: Managed vector database
- PostgreSQL: Relational data (Azure Database)
- Redis: Caching, session store

# CI/CD
- GitHub Actions: Build, test, deploy
- Docker: Containerization
- Terraform: Infrastructure as Code

# Monitoring & Logging
- LangSmith: LLM observability
- Prometheus + Grafana: Metrics
- Azure Application Insights: APM
- Sentry: Error tracking
```

### 8.3 API Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (FastAPI)                    │
│                  Rate Limiting, Auth, Logging                │
└─────────────────────────┬───────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐
    │  Agent   │    │  Data    │    │  User    │
    │ Service  │    │ Service  │    │ Service  │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │                │                │
    ┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐
    │LangGraph │    │ Crawlers │    │Postgres  │
    │Workflows │    │ + APIs   │    │ + Redis  │
    └──────────┘    └──────────┘    └──────────┘
         │
    ┌────▼──────────────────────────┐
    │  Context Management Layer     │
    │  (Neo4j + Qdrant + LightRAG) │
    └───────────────────────────────┘
```

### 8.4 Agent Communication Protocol

```python
# LangGraph State Schema
from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    # User context
    user_id: str
    user_profile: dict
    
    # Current task
    task: str
    task_type: str  # "job_search" | "resume_optimize" | "interview_prep"
    
    # Agent coordination
    messages: List[BaseMessage]
    current_agent: str
    next_agent: Optional[str]
    
    # Domain-specific data
    job_listings: List[dict]
    matched_jobs: List[dict]
    application_draft: Optional[dict]
    interview_feedback: Optional[dict]
    
    # Metadata
    iteration_count: int
    max_iterations: int
```

---

## 9. Implementation Roadmap

### 9.1 6-Month MVP Development Plan

#### Month 1-2: Foundation & Data Collection Infrastructure

**Week 1-2: Architecture Setup**
- [ ] Project scaffolding (monorepo: backend + frontend + extension)
- [ ] Database schema design & migration scripts
- [ ] API design (OpenAPI spec)
- [ ] Dev environment setup (Docker Compose)
- [ ] **Browser Extension boilerplate** (Manifest V3, React)

**Week 3-4: User Management & Authentication**
- [ ] User signup/login (OAuth + Email)
- [ ] Profile CRUD APIs
- [ ] Resume upload & parsing MVP
- [ ] Frontend: Landing page + Auth flows
- [ ] **Extension: Authentication flow** (OAuth for user linking)

**Week 5-6: Knowledge Graph Foundation**
- [ ] Neo4j schema implementation
- [ ] Skill taxonomy (500+ skills)
- [ ] Company data seed (100+ companies)
- [ ] Graph query optimization

**Week 7-8: Multi-Source Job Aggregation**
- [ ] Indeed API integration (10,000 jobs)
- [ ] 워크넷 API integration (5,000 jobs)
- [ ] Job deduplication pipeline (hash + fuzzy + semantic)
- [ ] **Extension MVP**: LinkedIn job data extractor
  - [ ] Content script for LinkedIn job pages
  - [ ] Opt-in consent UI
  - [ ] Data contribution API endpoint
- [ ] Basic matching algorithm (keyword-based)

**Deliverable**: 
- User signup → Resume upload → 15,000+ jobs available
- **50 beta users with extension installed** → 500 contributed jobs/day

#### Month 3-4: AI Agents & User-Contributed Data Scale

**Week 9-10: Profile Analyzer Agent**
- [ ] Resume parsing enhancement (GPT-4 integration)
- [ ] Skill extraction & normalization
- [ ] Career gap analysis algorithm
- [ ] Readiness assessment

**Week 11-12: Job Matcher Agent**
- [ ] Embedding generation (User profile + Jobs)
- [ ] Qdrant vector search integration
- [ ] Multi-factor scoring implementation
- [ ] Explainable AI (match reasoning)

**Week 13-14: Browser Extension Enhancement & Growth**
- [ ] **Extension V2**: 
  - [ ] Multi-platform support (Indeed, 사람인, 잡코리아)
  - [ ] Gamification UI (points, leaderboard)
  - [ ] Batch extraction (multiple pages)
  - [ ] Offline queue (sync when online)
- [ ] **Incentive system backend**:
  - [ ] Points calculation & tracking
  - [ ] Reward redemption (Premium unlock)
  - [ ] Referral program implementation
- [ ] **Growth hacking**:
  - [ ] Product Hunt launch preparation
  - [ ] Landing page for extension
  - [ ] Viral sharing mechanics

**Week 15-16: RAG Pipeline & Data Quality**
- [ ] LightRAG setup
- [ ] Company intelligence integration (Glassdoor, Crunchbase)
- [ ] Hybrid retrieval (KG + Vector)
- [ ] Context ranking (Cohere rerank)
- [ ] **Data quality monitoring dashboard**
  - [ ] Contribution quality scores
  - [ ] Duplicate detection metrics
  - [ ] User contribution analytics

**Deliverable**: 
- 개인화된 Job recommendations + 맞춤형 이력서 생성
- **500 active extension users** → 5,000 contributed jobs/day
- Total: ~28,000 jobs/day

#### Month 5-6: Advanced Features & Scale

**Week 17-18: Application Assistant & Interview DB**
- [ ] Resume optimizer (job-tailored versions)
- [ ] Cover letter generator
- [ ] Application tracking (Kanban board)
- [ ] Interview questions DB (seed 100+ companies)
- [ ] Crowdsourcing mechanism (user-contributed interview questions)

**Week 19-20: Interview Coach Agent**
- [ ] Mock interview MVP (text-based)
- [ ] STAR method evaluation
- [ ] Voice interview integration (Whisper + TTS)
- [ ] Real-time feedback generation
- [ ] Answer scoring algorithm

**Week 21-22: Negotiation Advisor & Extension V3**
- [ ] Salary data aggregation (Levels.fyi, user contributions)
- [ ] Offer comparison matrix
- [ ] Negotiation simulator
- [ ] **Extension V3**:
  - [ ] Salary data contribution feature
  - [ ] Company review contribution
  - [ ] Interview feedback collection

**Week 23-24: Beta Testing & Optimization**
- [ ] Comprehensive testing with 200+ users
- [ ] **Extension optimization**:
  - [ ] Performance tuning (memory, speed)
  - [ ] Cross-browser testing (Chrome, Edge, Firefox)
  - [ ] Privacy & security audit
- [ ] Bug fixes & UX improvements
- [ ] Documentation (API docs, user guide, extension guide)
- [ ] **Extension store submission**:
  - [ ] Chrome Web Store listing
  - [ ] Edge Add-ons listing
  - [ ] Marketing assets (screenshots, demo video)

**Deliverable**: 
- End-to-end 이직 여정 지원 (매칭 → 지원 → 면접 → 협상)
- **1,000+ active extension users** → 10,000 contributed jobs/day
- Total: ~35,000 jobs/day → 25,000 unique jobs

### 9.2 Phase별 리소스 배분

| Phase | Backend | Frontend | Extension | ML/AI | DevOps | Total |
|-------|---------|----------|-----------|-------|--------|-------|
| Month 1-2 | 50% | 20% | 20% | 0% | 10% | 100% |
| Month 3-4 | 30% | 15% | 20% | 30% | 5% | 100% |
| Month 5-6 | 25% | 25% | 15% | 25% | 10% | 100% |

**Extension 개발 리소스**: 전체 15-20% 지속 투입 (Frontend engineer 겸임)

### 9.3 Extension Growth Strategy

#### Phase 1: Beta (Week 8-12)
```
Target: 50 users
Strategy:
- Personal network (friends, colleagues)
- LinkedIn/Facebook posts
- Beta tester recruitment (early adopter benefits)

Incentive:
- Early contributor badge
- Lifetime Premium (500 points 달성 시)
```

#### Phase 2: Product Hunt Launch (Week 13-16)
```
Target: 500 users
Strategy:
- Product Hunt launch
- Tech community (GeekNews, Disquiet, Reddit)
- Press release (TechCrunch Korea, Platum)

Incentive:
- Limited time: Double points (first 1000 users)
- Exclusive features for early adopters
```

#### Phase 3: Viral Growth (Week 17-24)
```
Target: 1,000+ users
Strategy:
- Referral program (invite 5 friends → bonus points)
- Social sharing (auto-post contributions on LinkedIn)
- Partnership with career communities

Incentive:
- Leaderboard & badges
- Monthly top contributors: Special rewards
```

### 9.4 Risk Mitigation Timeline

| Risk | Checkpoint | Mitigation Action | Owner |
|------|-----------|-------------------|-------|
| **Extension low adoption** | Week 12 | Improve UX, increase rewards, marketing push | Growth |
| **Data quality issues** | Week 16 | AI validation, user reporting, quality scoring | Data |
| **LinkedIn detection** | Week 20 | Monitor user reports, adjust extraction logic, legal review | Legal/Eng |
| **Platform blocking** | Week 8, 16, 24 | Diversify data sources, API partnerships | Product |
| **LLM cost overrun** | Week 12, 20 | Caching, smaller models, prompt optimization | ML |
| **User churn** | Week 20 | Retention features, engagement loops, value prop refinement | Product |

### 9.5 Technical Milestones & KPIs

| Milestone | Week | Success Criteria | Risk if Failed |
|-----------|------|-----------------|----------------|
| Extension MVP Launch | 8 | 50 installs, 500 jobs contributed | Fall back to API-only strategy |
| 500 Active Users | 16 | 5,000 jobs/day contribution | Slow growth, need marketing boost |
| Product-Market Fit | 20 | NPS > 40, 30%+ DAU/MAU | Pivot or iterate on value prop |
| 1,000 Users | 24 | 10,000 jobs/day, 25K unique jobs | Scale infrastructure, hire growth team |

### 9.6 Post-MVP Roadmap (Month 7-12)

**Month 7-8: Scale & Enterprise Prep**
- Scale to 5,000+ extension users
- Enterprise features (team accounts, bulk operations)
- LinkedIn Partnership exploration

**Month 9-10: Advanced AI Features**
- Personalized career path predictions
- Automated job application (with approval)
- Smart scheduling (interview calendar optimization)

**Month 11-12: Monetization & Series A Prep**
- Premium tier launch
- B2B pilot (HR tech partnerships)
- Metrics dashboard for investors
- Series A pitch deck & roadshow

---

## 10. Success Metrics & KPIs

### 10.1 Product Metrics (6-Month Targets)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **User Activation Rate** | 70% | Complete profile + 1+ job save |
| **Application Conversion** | 25% | Job view → Application submit |
| **Interview Pass Rate** | 35% | Interview scheduled → Offer |
| **User Satisfaction (NPS)** | 50+ | Survey after offer accept |
| **DAU / MAU Ratio** | 0.3 | Daily active / Monthly active |
| **Avg. Time to Offer** | -30% | vs. traditional methods |

### 10.2 Technical Metrics

| Metric | Target | Tool |
|--------|--------|------|
| **RAG Accuracy** | Context relevance > 0.85 | LangSmith evaluation |
| **Matching Precision@10** | 5+ relevant jobs in top 10 | Human annotation |
| **API Response Time** | P95 < 2초 | Prometheus |
| **System Uptime** | 99.5% | Azure Monitor |
| **LLM Token Usage** | < $0.50 per user per month | LangSmith |
| **Job Coverage** | 20,000+ active jobs | Internal DB |

### 10.3 Business Metrics (12-Month Targets)

| Metric | 6-Month | 12-Month | Notes |
|--------|---------|----------|-------|
| **Total Users** | 1,000 | 10,000 | Beta → GA transition |
| **Paid Users** | 100 (10%) | 2,000 (20%) | Freemium model |
| **MRR** | $10K | $200K | $100 ARPU |
| **Offer Acceptance Rate** | 50% | 65% | Users accepting offers via platform |

### 10.4 Data Quality Metrics

| Metric | Target | Check Frequency |
|--------|--------|----------------|
| **Job Freshness** | 95% updated in last 7 days | Daily |
| **Duplicate Rate** | < 5% | Daily |
| **Missing Fields** | < 10% jobs with incomplete data | Daily |
| **User Profile Completeness** | 80% with complete profiles | Weekly |

---

## 11. Risk Analysis & Mitigation

### 11.1 고위험 리스크

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|------------|-------------------|
| **Data Privacy Breach** | Critical (서비스 중단) | Low | - End-to-end encryption<br>- SOC2 Type 2 인증<br>- 정기 보안 감사 (분기 1회)<br>- Bug bounty program |
| **LinkedIn/Platform Blocking** | High (데이터 소스 상실) | Medium | - 공식 API 우선 활용<br>- 다중 소스 확보 (5+ sources)<br>- Rate limiting 엄격 준수<br>- Legal review 정기화 |
| **LLM Cost Overrun** | High (수익성 악화) | Medium | - Aggressive caching (Redis)<br>- Prompt optimization<br>- Smaller models for simple tasks<br>- Monthly budget alerts |

### 11.2 중위험 리스크

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Cold Start Problem** | 초기 사용자 추천 부정확 | - 상세한 온보딩 설문<br>- 공개 이력서 크롤링 (opt-in)<br>- 협업 필터링 도입 |
| **Scraper Detection** | 데이터 수집 차단 | - User-Agent rotation<br>- Proxy pool (residential IPs)<br>- Human-like behavior patterns |
| **Interview DB Sparse** | 특정 기업 정보 부족 | - Incentivize user contributions<br>- Partnerships with interview prep platforms |
| **Matching Algorithm Bias** | 특정 그룹 차별 | - Fairness metrics monitoring<br>- Diverse training data<br>- Regular bias audits |

### 11.3 저위험 리스크

| Risk | Mitigation |
|------|-----------|
| **API Deprecation** | Multi-vendor strategy, version pinning |
| **Model Hallucination** | Human-in-the-loop for critical outputs |
| **User Churn** | Engagement features (gamification, streaks) |

### 11.4 리스크 모니터링 대시보드

```python
# Weekly Risk Review Checklist
risk_dashboard = {
    "data_sources": {
        "indeed_api_health": monitor_api_status("indeed"),
        "crawler_success_rate": calculate_crawler_success(),
        "data_freshness": check_last_update_time()
    },
    "cost": {
        "llm_spend_mtd": get_openai_usage_mtd(),
        "burn_rate": calculate_burn_rate(),
        "runway_months": calculate_runway()
    },
    "quality": {
        "matching_accuracy": evaluate_matching_precision(),
        "user_satisfaction": get_nps_score(),
        "bug_severity": count_critical_bugs()
    },
    "security": {
        "failed_login_attempts": count_failed_logins(),
        "data_access_anomalies": detect_unusual_access(),
        "vulnerability_scan": run_security_scan()
    }
}
```

---

## 12. Conclusion

### 12.1 핵심 요약

CareerNavigator는 AI 기술을 활용하여 이직 프로세스의 근본적인 비효율성을 해결하는 혁신적인 플랫폼입니다. 

**차별화 요소**:
- Multi-Agent Architecture와 Knowledge Graph 기반 semantic modeling
- 기존 채용 플랫폼 대비 3배 이상 정확한 매칭
- 60% 시간 절감 실현
- 현실적이고 합법적인 데이터 소싱 전략

**핵심 성공 요인**:
1. **데이터 전략**: 공식 API 우선, 합법적 크롤링, 사용자 기여 데이터 통합
2. **기술 스택**: Production-ready stack (LangGraph, Neo4j, Qdrant, LightRAG)
3. **User Experience**: End-to-end 이직 여정 지원
4. **확장성**: Multi-tenant architecture, cloud-native design

### 12.2 Next Steps

#### Immediate Actions (Week 1-2)

1. **Tech Stack 최종 확정**
   - [ ] LLM provider 계약 (Anthropic + OpenAI)
   - [ ] Neo4j AuraDB 계정 생성
   - [ ] Azure 리소스 프로비저닝

2. **Core Team 구성**
   - [ ] Backend Engineer (2명)
   - [ ] Frontend Engineer (1명)
   - [ ] ML Engineer (1명)
   - [ ] Part-time DevOps

3. **Legal & Compliance**
   - [ ] 변호사 상담 (데이터 크롤링 legal opinion)
   - [ ] 개인정보 보호 정책 초안
   - [ ] 각 플랫폼 ToS 상세 검토

#### Short-term Goals (Month 1-2)

1. **Architecture PoC**
   - [ ] RAG pipeline 구현 (LightRAG + Neo4j + Qdrant)
   - [ ] 1개 Agent 구현 (Profile Analyzer)
   - [ ] End-to-end test: Resume upload → Skill extraction → Job matching

2. **Data Sourcing MVP**
   - [ ] Indeed API integration
   - [ ] 워크넷 API integration
   - [ ] 1개 대기업 crawler (네이버 채용 페이지)

3. **Go-to-Market Prep**
   - [ ] Beta tester 모집 (target: 50명)
   - [ ] Landing page 제작
   - [ ] Pitch deck (투자 유치용)

### 12.3 Long-term Vision (12-24 Months)

**Phase 2: Enterprise Expansion**
- HR 솔루션: 기업용 채용 최적화 도구
- Talent pooling & matching for recruiters
- ATS integration

**Phase 3: Global Expansion**
- 미국/유럽 시장 진출
- Multi-language support
- Local job board partnerships

**Phase 4: Platform Evolution**
- 커리어 코칭 마켓플레이스
- Skills training 통합 (Coursera, Udemy 연동)
- Salary negotiation 에이전트 서비스

### 12.4 투자 필요성

**Funding Requirements**:
- **Pre-seed**: $500K (MVP 개발 6개월)
  - Team salaries: $300K
  - Infrastructure: $100K (API costs, cloud)
  - Legal/compliance: $50K
  - Marketing: $50K

- **Seed**: $2M (Product-Market Fit 확립, 12개월)
  - Team expansion (10명)
  - Enterprise partnerships
  - Advanced AI features
  - Series A 준비

---

## Appendix

### A. Glossary

| Term | Definition |
|------|-----------|
| **ATS** | Applicant Tracking System - 기업이 사용하는 지원자 관리 시스템 |
| **CFAA** | Computer Fraud and Abuse Act - 미국 컴퓨터 사기 및 남용 방지법 |
| **Cold Start** | 신규 사용자/아이템에 대한 데이터 부족으로 추천이 어려운 문제 |
| **Entity Resolution** | 동일한 실체를 나타내는 서로 다른 레코드를 식별하는 프로세스 |
| **RAG** | Retrieval-Augmented Generation - 검색 기반 생성 모델 |
| **Semantic Matching** | 키워드 일치가 아닌 의미 기반 매칭 |
| **ToS** | Terms of Service - 서비스 이용 약관 |

### B. References

1. LangGraph Documentation: https://langchain-ai.github.io/langgraph/
2. Neo4j Best Practices: https://neo4j.com/developer/guide-data-modeling/
3. LightRAG Paper: https://arxiv.org/abs/2410.05779
4. hiQ Labs v. LinkedIn Case: https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn
5. Indeed Publisher API: https://opensource.indeedeng.io/api-documentation/

### C. Contact Information

**Product Owner**: [Name]  
**Email**: product@careernavigator.ai  
**Website**: https://careernavigator.ai (coming soon)

---

*End of Document*

**Document Version**: 1.0  
**Last Updated**: 2024-11-24  
**Status**: Draft for Internal Review

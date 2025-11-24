# CareerNavigator

AI-powered career transition platform with multi-agent architecture.

## Project Overview

CareerNavigator는 AI 기술을 활용한 이직 지원 플랫폼입니다:

- **시간 절약**: 이직 준비 시간 60% 단축
- **매칭 정확도**: 적합 포지션 발견율 3배 향상
- **협상력 강화**: 평균 연봉 협상 15% 개선

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy 2.0
- **Migration**: Alembic

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript 5.0
- **UI**: Tailwind CSS, shadcn/ui
- **State**: Zustand, React Query

### AI/ML
- **Orchestration**: LangGraph, LangChain
- **LLM**: Claude Sonnet 4, GPT-4o
- **Embeddings**: OpenAI text-embedding-3-large

### Data Layer
- **Graph DB**: Neo4j 5.x
- **Vector DB**: Qdrant 1.7+
- **RDBMS**: PostgreSQL 15+
- **Cache**: Redis 7+

## Project Structure

```
careernavigator/
├── apps/
│   ├── backend/          # FastAPI Backend
│   ├── frontend/         # Next.js Frontend
│   └── extension/        # Browser Extension
├── packages/
│   ├── types/           # Shared TypeScript Types
│   ├── utils/           # Shared Utilities
│   └── config/          # Shared Config
├── infra/
│   ├── docker/          # Docker Compose
│   ├── terraform/       # IaC
│   └── kubernetes/      # K8s manifests
└── docs/                # Documentation
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ (LTS)
- pnpm 8+
- Docker Desktop
- Docker Compose

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/careernavigator.git
cd careernavigator
```

2. Install dependencies:
```bash
pnpm install
```

3. Start Docker services:
```bash
cd infra/docker
docker-compose up -d
```

4. Run backend:
```bash
cd apps/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

5. Run frontend:
```bash
cd apps/frontend
pnpm dev
```

### Environment Variables

Copy `.env.example` to `.env` in each app directory and configure:

- Backend: `apps/backend/.env`
- Frontend: `apps/frontend/.env.local`

## Development

### Running All Services

```bash
# Start all services with Docker Compose
docker-compose up

# Development mode (with hot reload)
pnpm dev
```

### Testing

```bash
# Run all tests
pnpm test

# Run backend tests
cd apps/backend
pytest

# Run frontend tests
cd apps/frontend
pnpm test
```

### Linting

```bash
# Lint all packages
pnpm lint
```

## Documentation

- [Development Plan](./DEVELOPMENT_PLAN.md)
- [Project Specification](./CareerNavigator_기획서_v1.0.md)
- [API Documentation](./docs/api/)
- [Architecture](./docs/architecture/)

## Contributing

Please read our contributing guidelines before submitting PRs.

## License

MIT License

## Contact

- Email: dev@careernavigator.ai
- GitHub: https://github.com/careernavigator

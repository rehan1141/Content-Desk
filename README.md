# Content Desk

A human-first desktop workspace for content creators. Moving ideas from initial thought to structured content seamlessly across platforms.

## Overview

Content Desk is built around the core creative loop:

$$\text{THOUGHT} \longrightarrow \text{IDEA} \longrightarrow \text{CONTENT} \longrightarrow \text{PUBLISH}$$

It bridges friction-free quick capture with structured multi-platform content creation (YouTube, Instagram, LinkedIn).

## Tech Stack

* **Desktop Host**: Tauri (v2)
* **Frontend**: React + TypeScript + Vite + Vanilla CSS
* **Backend**: Python (FastAPI + Uvicorn)
* **ORM & Database**: SQLAlchemy + PostgreSQL
* **Testing**: Pytest

## Architecture

```text
Content Desk
 ├── frontend/      # React + TypeScript + Tauri Desktop Host
 └── backend/       # FastAPI REST API + SQLAlchemy ORM + PostgreSQL
```

## Quick Start (Development)

### Prerequisites
* **Node.js**: v18+ (tested on v24)
* **Python**: 3.9+
* **PostgreSQL**: Local instance or Postgres.app
* **Rust**: Required for Tauri desktop bundling (`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`)

### Running Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Running Frontend
```bash
cd frontend
npm install
npm run dev
```

## Status
Milestone 1 — Repository & Architecture Foundation.

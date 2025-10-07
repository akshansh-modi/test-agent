# 🚀 **VentureLens**  
### _AI Due Diligence You Can Trust._

🧠 **An AI-powered analyst that verifies startup claims, benchmarks performance, and generates investor-ready insights — instantly.**

🌐 **Live Demo:** [https://agenticwizards.dev/](https://agenticwizards.dev/)  
🔗 Built for **Google Gen AI Hackathon 2025**

</div>

---

## 🏆 Overview

Early-stage investors spend hours analyzing messy founder data — pitch decks, updates, and scattered market information — only to risk missing critical red flags.  
**VentureLens** changes that.

It acts as an **AI analyst**, powered by **Google Cloud** and **Vertex AI**, that reads founder pitch decks, verifies claims using **retrieval-augmented reasoning (RAG)**, and produces a **benchmark-backed investor memo** with citations and risk analysis.

---

## 💡 Problem

> “Investors are drowning in data — but starving for verified insight.”

- Pitch decks often contain **inconsistent or inflated metrics** (ARR, TAM, churn).  
- Market validation requires **hours of manual research**.  
- Evaluation results vary from analyst to analyst — low consistency and scalability.  

---

## 🌟 Solution — _VentureLens_

**VentureLens** transforms unstructured founder data into structured, verifiable insights through:

1. 📄 **PDF Pitch Deck Ingestion** — Upload any founder deck (PDF format).  
2. 🤖 **Claim Extraction** — Identify key metrics like ARR, MRR, TAM, churn, and customers.  
3. 🔍 **Verification (RAG + Web)** — Cross-check claims using a **RAG Engine Corpus** and **live web scraping** for factual accuracy.  
4. 📊 **Benchmarking (BigQuery)** — Compare startups with public datasets: **GDELT**, **GitHub Archive**, **Patents**, and **Google Trends**.  
5. ⚠️ **Risk Radar** — Detect inconsistencies and visualize red flags.  
6. 🧾 **Memo Generation (Gemini)** — Output a clean, cited investor memo with scoring sliders and recommendations.

---

## 🔍 Unique Approach

| 💡 Feature | 🧩 Description |
|------------|----------------|
| **Document + Web Verification** | Combines **RAG corpus + Gemini reasoning + live scraping** to cross-check every claim from the uploaded deck. |
| **Modular Multi-Agent Architecture** | Independent AI agents — Collector, Benchmarker, Risk, Note-Writer — ensure transparency and explainability. |
| **Explainable Insights** | Every metric includes citations from the pitch deck or verified public sources. |
| **Risk Radar Visualization** | Rule-based radar detects inconsistencies (ARR vs MRR, TAM inflation, trend decline). |
| **Scalable Cloud Storage** | **Google Cloud Storage** handles all uploads, processed text, and memo exports securely. |

---

## 🧠 Tech Stack

<div align="center">

| Layer | Technologies Used | Purpose |
|-------|-------------------|----------|
| **Frontend** | ⚛️ Next.js · 💨 TailwindCSS · 📊 Recharts | Modern, interactive investor dashboard |
| **Backend** | 🟩 Node.js (Express) · ☁️ Cloud Run | Core API and analysis orchestration |
| **Storage** | 🗄️ Google Cloud Storage Buckets | Uploads, text processing, and PDF exports |
| **AI / ML** | 🤖 Vertex AI Gemini 2.5 Pro · 🔍 Vertex AI Grounding | Claim extraction, reasoning, and memo generation |
| **Retrieval Engine** | 🧩 RAG Corpus + Web Scraping | Verifies startup claims against external data |
| **Benchmarking** | 📈 BigQuery Public Datasets (GDELT, GitHub, Patents, Google Trends) | Sector and performance benchmarking |
| **Vision** | 👁️ Cloud Vision API | OCR extraction from PDF decks |
| **Monitoring** | 🔎 Cloud Logging + Cloud Monitoring | Debugging and performance analytics |

</div>

---

## 🧩 Multi-Agent System Architecture (Google ADK)

The intelligence behind **VentureLens** is powered by a **multi-agent coordination framework** built using the **Google ADK (Agent Development Kit)**.  
Instead of one monolithic model, VentureLens deploys a **hierarchical agent network** where a **Financial Coordinator Agent** orchestrates four specialized sub-agents.  
This structure mirrors the workflow of a professional investment team — modular, explainable, and evidence-driven.

---

### 🤖 1. Financial Coordinator Agent (Main Agent)
- **Role:** Acts as the central decision-maker.  
- **Function:**  
  - Initiates and coordinates all sub-agents.  
  - Consolidates their outputs (claims, analysis, plans, risk reports).  
  - Synthesizes results into a unified **investor-ready report**.  
  - Computes an overall **investment confidence score** and recommendation.  
- **Final Output:** Structured summary, growth potential, and downloadable investor memo.

---

### 🧾 2. Collector Agent
- **Objective:** Detect **verifiable claims** about the startup from both the uploaded PDF deck and the public web.  
- **Tools:** Uses **Google Search APIs** via ADK to confirm:  
  - Official company website  
  - Product presence  
  - Public image or press mentions  
- **Output:** JSON file of verified claims with confidence scores and source URLs.

---

### 📊 3. Data Analyst Agent
- **Objective:** Build an **in-depth, current market analysis** for the startup or relevant stock ticker.  
- **Process:**  
  - Uses **Google Search** iteratively to gather unique, recent (last 90 days) insights.  
  - Focuses on **SEC filings**, **industry news**, and **market sentiment**.  
  - Produces a structured market intelligence report derived entirely from verified search results.  
- **Output:** Comprehensive summary of sector trends and competitive landscape.

---

### ⚙️ 4. Execution Agent
- **Objective:** Design a **detailed execution plan** for an investment strategy.  
- **Scope:**  
  - Aligns with user’s **risk tolerance**, **investment timeframe**, and **preferred execution methods**.  
  - Determines best entry/exit points and scaling conditions.  
- **Output:** Fact-based step-by-step plan for initiating, maintaining, or exiting investment positions.

---

### ⚠️ 5. Risk Evaluation Agent
- **Objective:** Produce a **complete risk assessment** of the investment strategy.  
- **Responsibilities:**  
  - Identify operational, market, and execution risks.  
  - Quantify risk exposure relative to user’s parameters.  
  - Recommend mitigation strategies and contingency actions.  
- **Output:** Structured risk matrix and recommendations appended to the final investor memo.

---

## 🧭 Current Prototype Capabilities

✅ **Ingests PDF pitch decks only**  
✅ **Extracts key startup metrics** using Vertex AI Gemini reasoning  
✅ **Cross-verifies claims** via RAG corpus and limited web scraping  
✅ **Visualizes red flags** through the Risk Radar  
✅ **Benchmarks startup activity** using mock BigQuery datasets  
✅ **Generates investor memos** with citations and scoring sliders  

---

### 🔜 Future Scope

- 🎤 **Founder call (MP4) analysis** with Speech-to-Text  
- 📧 **Email update ingestion** for continuous startup monitoring  
- ⚡ **Real-time BigQuery benchmarking pipeline** for live market signals  
- 🧮 **Sector-specific RAG datasets** for domain-optimized accuracy  

---

## 🧠 Example Use Case

1. Upload a SaaS startup’s **PDF pitch deck**.  
2. **VentureLens** extracts metrics: ARR = \$1.2M, MRR = \$70k → flags ARR mismatch (12× rule).  
3. The **RAG corpus** cross-checks the TAM claim (“\$3B market”) → confirms only \$1.8B via verified web data.  
4. **Risk Radar** displays two alerts — ARR mismatch & inflated TAM.  
5. **Benchmarks** from BigQuery show the sector trend rising +6%.  
6. **Gemini** composes the investor memo:  

> “Proceed to diligence. Strong traction, moderate TAM inflation detected.”

---

## 💡 Final Thoughts

> **VentureLens** transforms static founder decks into **actionable, verified investment intelligence** —  
> empowering investors with **clarity, confidence, and speed**.  
> It’s not just due diligence — it’s **AI diligence, redefined.**  
>  
> 🧭 _Where intelligence meets investment — powered by Google Cloud and Vertex AI._

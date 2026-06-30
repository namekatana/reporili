<div align="center">

<img src="frontend/public/logo.png" alt="Reporili" width="72" height="72" />

# Reporili

**Legal documents from your actual codebase**

Drop a ZIP or paste a GitHub URL. We scan auth, payments, analytics, and data handling — then generate a tailored Privacy Policy, Terms of Service, and Disclaimer.

**Live:** [reporili.tech](https://reporili.tech)

<br />

<a href="https://fastapi.tiangolo.com/"><img src="docs/readme/badge-fastapi.svg" alt="FastAPI" height="36" /></a>
&nbsp;
<a href="https://astro.build/"><img src="docs/readme/badge-astro.svg" alt="Astro" height="36" /></a>
&nbsp;
<a href="https://svelte.dev/"><img src="docs/readme/badge-svelte.svg" alt="Svelte" height="36" /></a>
&nbsp;
<a href="https://ai.google.dev/"><img src="docs/readme/badge-gemini.svg" alt="Gemini 2.5 Flash" height="36" /></a>

</div>

<br />

<table>
<tr>
<td width="72" valign="top">

<img src="docs/readme/icon-scan.svg" alt="" width="48" height="48" />

</td>
<td>

### Repo-aware generation

No generic templates. Documents reflect what your stack actually does — authentication, billing, tracking, storage, and cookies detected from source.

</td>
</tr>
</table>

<table>
<tr>
<td width="72" valign="top">

<img src="docs/readme/icon-github.svg" alt="" width="48" height="48" />

</td>
<td>

### ZIP or GitHub

Upload a `.zip` archive or paste a public repository URL. Private repos work with an optional `GITHUB_TOKEN`.

</td>
</tr>
</table>

<table>
<tr>
<td width="72" valign="top">

<img src="docs/readme/icon-export.svg" alt="" width="48" height="48" />

</td>
<td>

### Three documents, three exports

Privacy Policy, Terms of Service, and Disclaimer — export as **Markdown**, **HTML**, or **DOCX**.

</td>
</tr>
</table>

<table>
<tr>
<td width="72" valign="top">

<img src="docs/readme/icon-history.svg" alt="" width="48" height="48" />

</td>
<td>

### Optional local history

Save generations on your device with a single toggle. Nothing is stored on a server beyond the generation request itself.

</td>
</tr>
</table>

<br />

## How it works

```
01  Add your repo          ZIP upload or GitHub link
02  We scan the code        Auth, billing, tracking, cloud
03  Get your docs           Export as Markdown, HTML, or DOCX
```

<br />

## Quick start

### Local development

**Backend** — Python 3.12, port `8000`

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
cp .env.example .env            # add GEMINI_API_KEY
uvicorn app.main:app --reload --port 8000
```

**Frontend** — Node 22+, port `4321`

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:4321](http://localhost:4321). API requests proxy to the backend in dev.

### Docker

```bash
cp backend/.env.example backend/.env   # set GEMINI_API_KEY
docker compose up -d --build
```

App runs on [http://localhost](http://localhost) (nginx → frontend + `/api` → backend).

<br />

## Environment

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google AI Studio API key |
| `GEMINI_MODEL` | No | Default `gemini-2.5-flash` |
| `GITHUB_TOKEN` | No | Higher GitHub API rate limits |
| `MAX_FILE_BYTES` | No | Per-file scan limit |
| `MAX_TOTAL_BYTES` | No | Total scan budget |

<br />

## Project structure

```
reporili/
├── backend/          FastAPI, repo parser, Gemini generator
├── frontend/         Astro + Svelte UI
├── docs/readme/      README SVG assets and brand logos
├── deploy/           nginx config
└── docker-compose.yml
```

<br />

## Stack

| Layer | Tech |
|-------|------|
| API | FastAPI, Uvicorn |
| AI | Google Gemini 2.5 Flash |
| UI | Astro 7, Svelte 5, Tailwind 4 |
| Export | marked, docx |
| Deploy | Docker, nginx |

<br />

<div align="center">

**AI drafts, not a law firm.** Review all documents with qualified counsel before publishing.

<br /><br />

<a href="https://github.com/namekatana/reporili">
  <img src="docs/readme/badge-github.svg" alt="View on GitHub" height="40" />
</a>

</div>

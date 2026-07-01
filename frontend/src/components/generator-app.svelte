<script lang="ts">
  import { tick } from "svelte";
  import { generateFromGithub, generateFromZip } from "../lib/api-client";
  import { exportHtml, exportMarkdown } from "../lib/export-documents";
  import { saveHistoryEntry } from "../lib/document-history";
  import type { GenerateResponse } from "../lib/types";
  import AnalysisSummary from "./analysis-summary.svelte";
  import CustomScrollbar from "./custom-scrollbar.svelte";
  import DocumentHistoryPanel from "./document-history-panel.svelte";
  import DocumentViewer from "./document-viewer.svelte";
  import DropZone from "./drop-zone.svelte";
  import GithubInput from "./github-input.svelte";
  import SiteFooter from "./site-footer.svelte";

  const steps = [
    { num: "1", title: "Add your code", desc: "Drop a ZIP or paste a public GitHub URL" },
    { num: "2", title: "We scan your stack", desc: "Auth, payments, analytics, cookies, storage" },
    { num: "3", title: "Export three docs", desc: "Privacy, Terms, and Disclaimer — MD, HTML, or DOCX" },
  ];

  let loading = $state(false);
  let error = $state("");
  let githubUrl = $state("");
  let selectedFile = $state<File | null>(null);
  let result = $state<GenerateResponse | null>(null);
  let historyRefresh = $state(0);
  let exportingDocx = $state(false);
  let resultsSection = $state<HTMLElement | null>(null);

  const canGenerate = $derived(
    !loading && (selectedFile !== null || githubUrl.trim().length > 0),
  );

  const inputSummary = $derived.by(() => {
    if (selectedFile) {
      return selectedFile.name;
    }
    if (githubUrl.trim()) {
      return githubUrl.trim();
    }
    return "";
  });

  function onFileSelect(file: File) {
    selectedFile = file;
    githubUrl = "";
    error = "";
  }

  function onGithubChange(value: string) {
    githubUrl = value;
    if (value.trim()) {
      selectedFile = null;
    }
    error = "";
  }

  async function scrollToResults() {
    await tick();
    resultsSection?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function handleGenerate() {
    if (!canGenerate) {
      return;
    }

    loading = true;
    error = "";
    result = null;

    try {
      if (selectedFile) {
        result = await generateFromZip(selectedFile);
      } else {
        result = await generateFromGithub(githubUrl.trim());
      }

      if (result) {
        saveHistoryEntry(result);
        historyRefresh += 1;
        await scrollToResults();
      }
    } catch (exc) {
      error = exc instanceof Error ? exc.message : "Generation failed";
    } finally {
      loading = false;
    }
  }

  function handleExportMd() {
    if (!result) {
      return;
    }
    exportMarkdown(result.documents, result.analysis.projectName);
  }

  function handleExportHtml() {
    if (!result) {
      return;
    }
    exportHtml(result.documents, result.analysis.projectName);
  }

  async function handleExportDocx() {
    if (!result || exportingDocx) {
      return;
    }

    exportingDocx = true;

    try {
      const { exportDocx } = await import("../lib/export-docx");
      await exportDocx(result.documents, result.analysis.projectName);
    } catch (exc) {
      error = exc instanceof Error ? exc.message : "DOCX export failed";
    } finally {
      exportingDocx = false;
    }
  }

  function handleRestoreFromHistory(entry: GenerateResponse) {
    result = {
      analysis: entry.analysis,
      documents: entry.documents,
    };
    error = "";
    void scrollToResults();
  }
</script>

<CustomScrollbar variant="site">
<div class="page">
  <header class="topbar">
    <div class="brand">
      <picture>
        <source srcset="/logo.webp" type="image/webp" />
        <img class="logo" src="/logo.png" alt="Reporili" width="30" height="30" />
      </picture>
      <span class="brand-divider" aria-hidden="true"></span>
      <span class="brand-name">Reporili</span>
    </div>

    <span class="tag">Beta</span>
  </header>

  <main class="main">
    <section class="hero">
      <p class="eyebrow">For developers shipping SaaS and apps</p>
      <h1 class="headline">Legal docs from your codebase</h1>
      <p class="subline">
        Upload a repo. Get three tailored documents in minutes — not generic templates.
      </p>
    </section>

    <section class="workspace" class:workspace-ready={canGenerate}>
      <div class="workspace-head">
        <div>
          <h2 class="workspace-title">Start here</h2>
          <p class="workspace-hint">ZIP archive or public GitHub repository</p>
        </div>
        {#if inputSummary}
          <span class="input-status">{inputSummary}</span>
        {/if}
      </div>

      <div class="input-split">
        <DropZone disabled={loading} onFileSelect={onFileSelect} />
        <div class="split-label">or</div>
        <GithubInput disabled={loading} value={githubUrl} onValueChange={onGithubChange} />
      </div>

      {#if selectedFile}
        <div class="file-chip">
          <span class="file-name">{selectedFile.name}</span>
          <button
            class="clear-btn"
            type="button"
            disabled={loading}
            onclick={() => (selectedFile = null)}
          >
            Remove
          </button>
        </div>
      {/if}

      <p class="upload-consent">
        You confirm you have the right to share this code. <a href="/terms">Terms</a>
      </p>

      <button class="generate-btn" class:generate-ready={canGenerate} disabled={!canGenerate} onclick={handleGenerate}>
        {#if loading}
          <span class="spinner"></span>
          Scanning and writing...
        {:else}
          Generate documents
        {/if}
      </button>

      {#if error}
        <div class="error-float" role="alert">{error}</div>
      {/if}

      <DocumentHistoryPanel onRestore={handleRestoreFromHistory} refreshToken={historyRefresh} />
    </section>

    {#if !result && !loading}
      <section class="steps">
        <h2 class="section-label">How it works</h2>
        <div class="steps-grid">
          {#each steps as step}
            <div class="step-card">
              <span class="step-num">{step.num}</span>
              <p class="step-title">{step.title}</p>
              <p class="step-desc">{step.desc}</p>
            </div>
          {/each}
        </div>
      </section>
    {/if}

    {#if result}
      <section class="results" bind:this={resultsSection}>
        <div class="results-head">
          <h2 class="results-title">Your documents are ready</h2>
          <p class="results-hint">Review each tab, then export. AI drafts — have a lawyer review before publishing.</p>
        </div>
        <AnalysisSummary analysis={result.analysis} />
        <DocumentViewer
          documents={result.documents}
          onExportMd={handleExportMd}
          onExportHtml={handleExportHtml}
          onExportDocx={handleExportDocx}
          exportingDocx={exportingDocx}
        />
      </section>
    {/if}
  </main>

  <SiteFooter />
</div>
</CustomScrollbar>

<style>
  .page {
    display: flex;
    flex-direction: column;
    min-height: 100%;
  }

  .topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem 2rem;
    max-width: 1120px;
    width: 100%;
    margin: 0 auto;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    flex-shrink: 0;
  }

  .brand-divider {
    width: 1px;
    height: 18px;
    background: #333;
    border-radius: 1px;
    flex-shrink: 0;
  }

  .logo {
    display: block;
    width: 30px;
    height: 30px;
    object-fit: contain;
  }

  .brand-name {
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-bright);
  }

  .tag {
    flex-shrink: 0;
    padding: 0.3rem 0.75rem;
    background: var(--color-float);
    border-radius: var(--radius-pill);
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--color-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .main {
    flex: 1;
    width: 100%;
    max-width: 1120px;
    margin: 0 auto;
    padding: 0 2rem 3rem;
  }

  .hero {
    padding: 0.25rem 0 2rem;
  }

  .eyebrow {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--color-muted);
    margin-bottom: 0.85rem;
  }

  .headline {
    font-size: clamp(2rem, 5vw, 2.85rem);
    font-weight: 700;
    color: var(--color-bright);
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin-bottom: 0.85rem;
    max-width: 15ch;
  }

  .subline {
    font-size: 1.02rem;
    color: var(--color-soft);
    line-height: 1.6;
    max-width: 42ch;
  }

  .workspace {
    padding: 1.75rem;
    background: var(--color-surface);
    border-radius: calc(var(--radius-panel) + 4px);
    margin-bottom: 2rem;
    transition: box-shadow 0.25s;
  }

  .workspace-ready {
    box-shadow: inset 0 0 0 1px #2e2e2e;
  }

  .workspace-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.35rem;
  }

  .workspace-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--color-bright);
    margin-bottom: 0.25rem;
  }

  .workspace-hint {
    font-size: 0.88rem;
    color: var(--color-muted);
  }

  .input-status {
    flex-shrink: 0;
    max-width: 220px;
    padding: 0.45rem 0.85rem;
    background: var(--color-float);
    border-radius: var(--radius-pill);
    font-size: 0.76rem;
    color: var(--color-soft);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .input-split {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 1rem;
    align-items: stretch;
    margin-bottom: 1rem;
  }

  .split-label {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--color-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0 0.25rem;
  }

  .file-chip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.85rem 1.15rem;
    background: var(--color-float);
    border-radius: var(--radius-control);
    margin-bottom: 1rem;
  }

  .file-name {
    font-size: 0.88rem;
    color: var(--color-soft);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .clear-btn {
    flex-shrink: 0;
    padding: 0.4rem 0.9rem;
    background: var(--color-elevated);
    border: none;
    border-radius: var(--radius-pill);
    color: var(--color-muted);
    font-size: 0.78rem;
    cursor: pointer;
    transition: color 0.2s, background 0.2s;
  }

  .clear-btn:hover:not(:disabled) {
    background: #333;
    color: var(--color-bright);
  }

  .upload-consent {
    margin-bottom: 0.85rem;
    font-size: 0.78rem;
    line-height: 1.55;
    color: var(--color-muted);
    text-align: center;
  }

  .upload-consent a {
    color: var(--color-soft);
    text-decoration: underline;
    text-underline-offset: 2px;
  }

  .upload-consent a:hover {
    color: var(--color-bright);
  }

  .generate-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.65rem;
    width: 100%;
    padding: 1.05rem 1.5rem;
    background: #2a2a2a;
    border: none;
    border-radius: var(--radius-panel);
    color: var(--color-muted);
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s, transform 0.15s, opacity 0.2s, color 0.2s;
  }

  .generate-btn.generate-ready {
    background: #f2f2f2;
    color: #0a0a0a;
  }

  .generate-btn.generate-ready:hover:not(:disabled) {
    background: #fff;
    transform: translateY(-1px);
  }

  .generate-btn:disabled {
    opacity: 0.55;
    cursor: not-allowed;
    transform: none;
  }

  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(0, 0, 0, 0.15);
    border-top-color: #111;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .error-float {
    margin-top: 1rem;
    padding: 0.9rem 1.15rem;
    background: #1a1212;
    border-radius: var(--radius-control);
    color: #e09090;
    font-size: 0.88rem;
  }

  .section-label {
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--color-muted);
    margin-bottom: 1rem;
  }

  .steps {
    margin-bottom: 2rem;
  }

  .steps-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
  }

  .step-card {
    padding: 1.35rem 1.25rem;
    background: var(--color-surface);
    border-radius: var(--radius-panel);
  }

  .step-num {
    display: block;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--color-muted);
    margin-bottom: 0.55rem;
  }

  .step-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--color-bright);
    margin-bottom: 0.35rem;
  }

  .step-desc {
    font-size: 0.82rem;
    color: var(--color-muted);
    line-height: 1.5;
  }

  .results {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    scroll-margin-top: 1rem;
  }

  .results-head {
    padding: 0.25rem 0 0.5rem;
  }

  .results-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--color-bright);
    margin-bottom: 0.25rem;
  }

  .results-hint {
    font-size: 0.88rem;
    color: var(--color-muted);
  }

  @media (max-width: 900px) {
    .headline {
      max-width: none;
    }

    .steps-grid {
      grid-template-columns: 1fr;
    }

    .input-split {
      grid-template-columns: 1fr;
    }

    .split-label {
      padding: 0.25rem 0;
    }

    .workspace-head {
      flex-direction: column;
    }

    .input-status {
      max-width: 100%;
    }
  }

  @media (max-width: 700px) {
    .topbar,
    .main {
      padding-left: 1.25rem;
      padding-right: 1.25rem;
    }
  }
</style>

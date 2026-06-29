<script lang="ts">
  import { renderMarkdown } from "../lib/export-documents";
  import { documentList, type DocumentKey, type GeneratedDocuments } from "../lib/types";

  type DocumentViewerProps = {
    documents: GeneratedDocuments;
    onExportMd: () => void;
    onExportHtml: () => void;
  };

  let { documents, onExportMd, onExportHtml }: DocumentViewerProps = $props();

  let activeKey = $state<DocumentKey>("privacyPolicy");

  const activeDoc = $derived(documentList.find((d) => d.key === activeKey)!);
  const activeContent = $derived(documents[activeKey]);
  const activeHtml = $derived(renderMarkdown(activeContent));
</script>

<div class="viewer-panel">
  <div class="toolbar">
    <div class="tabs">
      {#each documentList as doc}
        <button
          class="tab"
          class:selected={activeKey === doc.key}
          onclick={() => (activeKey = doc.key)}
        >
          {doc.label}
        </button>
      {/each}
    </div>

    <div class="exports">
      <button class="export-btn" onclick={onExportMd}>Export MD</button>
      <button class="export-btn primary" onclick={onExportHtml}>Export HTML</button>
    </div>
  </div>

  <div class="content-float">
    <h3 class="doc-title">{activeDoc.label}</h3>
    <div class="prose-doc">
      {@html activeHtml}
    </div>
  </div>
</div>

<style>
  .viewer-panel {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .toolbar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.85rem 1rem;
    background: var(--color-surface);
    border-radius: var(--radius-panel);
  }

  .tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .tab {
    padding: 0.55rem 1rem;
    background: transparent;
    border: none;
    border-radius: var(--radius-pill);
    color: var(--color-muted);
    font-size: 0.85rem;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
  }

  .tab:hover {
    background: var(--color-elevated);
    color: var(--color-soft);
  }

  .tab.selected {
    background: var(--color-elevated);
    color: var(--color-bright);
  }

  .exports {
    display: flex;
    gap: 0.5rem;
  }

  .export-btn {
    padding: 0.55rem 1.1rem;
    background: var(--color-elevated);
    border: none;
    border-radius: var(--radius-pill);
    color: var(--color-soft);
    font-size: 0.85rem;
    cursor: pointer;
    transition: background 0.2s, color 0.2s, transform 0.15s;
  }

  .export-btn:hover {
    background: #333;
    color: var(--color-bright);
    transform: translateY(-1px);
  }

  .export-btn.primary {
    background: #f0f0f0;
    color: #111;
  }

  .export-btn.primary:hover {
    background: #fff;
    color: #000;
  }

  .content-float {
    padding: 1.75rem 2rem;
    background: var(--color-surface);
    border-radius: var(--radius-panel);
    box-shadow: var(--shadow-soft);
    min-height: 360px;
    max-height: 65vh;
    overflow-y: auto;
  }

  .doc-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 1.25rem;
  }
</style>

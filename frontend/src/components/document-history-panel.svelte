<script lang="ts">
  import { untrack } from "svelte";
  import {    clearHistory,
    formatHistoryDate,
    isHistoryEnabled,
    loadHistory,
    removeHistoryEntry,
    setHistoryEnabled,
    type HistoryEntry,
  } from "../lib/document-history";
  import type { GenerateResponse } from "../lib/types";

  type DocumentHistoryPanelProps = {
    onRestore: (entry: GenerateResponse) => void;
    refreshToken?: number;
  };

  let { onRestore, refreshToken = 0 }: DocumentHistoryPanelProps = $props();

  let enabled = $state(isHistoryEnabled());
  let entries = $state<HistoryEntry[]>(loadHistory());
  let expanded = $state(entries.length > 0);

  function toggleEnabled() {
    enabled = !enabled;
    setHistoryEnabled(enabled);
  }

  function handleRestore(entry: HistoryEntry) {
    onRestore(entry);
  }

  function handleRemove(id: string) {
    entries = removeHistoryEntry(id);
  }

  function handleClear() {
    clearHistory();
    entries = [];
  }

  function reloadEntries(openWhenFound = false) {
    const loaded = loadHistory();
    entries = loaded;
    if (openWhenFound && loaded.length > 0) {
      expanded = true;
    }
  }

  $effect(() => {
    refreshToken;
    untrack(() => reloadEntries(true));
  });
</script>

<section class="history-panel">
  <div class="history-head">
    <div>
      <h2 class="history-title">Document history</h2>
      <p class="history-hint">Optional local storage on this device</p>
    </div>

    <button
      class="save-toggle"
      class:active={enabled}
      type="button"
      aria-pressed={enabled}
      onclick={toggleEnabled}
    >
      <span class="save-toggle-switch" aria-hidden="true">
        <span class="save-toggle-knob"></span>
      </span>
      <span class="save-toggle-text">Save generations</span>
    </button>
  </div>

  {#if entries.length > 0}
    <button class="history-expand" type="button" onclick={() => (expanded = !expanded)}>
      {expanded ? "Hide" : "Show"} {entries.length} saved {entries.length === 1 ? "set" : "sets"}
    </button>
  {:else if enabled}
    <p class="history-empty">New generations will appear here.</p>
  {/if}

  {#if expanded && entries.length > 0}
    <div class="history-list">
      {#each entries as entry (entry.id)}
        <article class="history-item">
          <div class="history-meta">
            <p class="history-name">{entry.analysis.projectName}</p>
            <p class="history-sub">
              {formatHistoryDate(entry.savedAt)} · {entry.analysis.source} · {entry.analysis.fileCount} files
            </p>
          </div>

          <div class="history-actions">
            <button class="history-btn" type="button" onclick={() => handleRestore(entry)}>
              Open
            </button>
            <button class="history-btn" type="button" onclick={() => handleRemove(entry.id)}>
              Remove
            </button>
          </div>
        </article>
      {/each}
    </div>

    <button class="history-clear" type="button" onclick={handleClear}>Clear all history</button>
  {/if}
</section>

<style>
  .history-panel {
    margin-top: 2rem;
    padding: 1.25rem 1.35rem;
    background: var(--color-float);
    border-radius: var(--radius-panel);
  }

  .history-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .history-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-bright);
    margin-bottom: 0.25rem;
  }

  .history-hint {
    font-size: 0.8rem;
    color: var(--color-muted);
  }

  .save-toggle {
    display: inline-flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.5rem 0.9rem 0.5rem 0.55rem;
    background: var(--color-elevated);
    border: none;
    border-radius: var(--radius-pill);
    cursor: pointer;
    transition: background 0.2s;
  }

  .save-toggle:hover {
    background: #333;
  }

  .save-toggle-switch {
    position: relative;
    width: 36px;
    height: 20px;
    flex-shrink: 0;
    border-radius: var(--radius-pill);
    background: #2a2a2a;
    transition: background 0.2s;
  }

  .save-toggle.active .save-toggle-switch {
    background: #e8e8e8;
  }

  .save-toggle-knob {
    position: absolute;
    top: 2px;
    left: 2px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #7a7a7a;
    transition: transform 0.2s, background 0.2s;
  }

  .save-toggle.active .save-toggle-knob {
    transform: translateX(16px);
    background: #111;
  }

  .save-toggle-text {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--color-soft);
    transition: color 0.2s;
  }

  .save-toggle.active .save-toggle-text {
    color: var(--color-bright);
  }

  .history-expand,
  .history-clear {
    margin-top: 1rem;
    padding: 0.55rem 0.9rem;
    background: var(--color-elevated);
    border: none;
    border-radius: var(--radius-pill);
    color: var(--color-soft);
    font-size: 0.8rem;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
  }

  .history-expand:hover,
  .history-clear:hover {
    background: #333;
    color: var(--color-bright);
  }

  .history-empty {
    margin-top: 0.85rem;
    font-size: 0.82rem;
    color: var(--color-muted);
  }

  .history-list {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
  }

  .history-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.85rem 1rem;
    background: var(--color-elevated);
    border-radius: var(--radius-control);
  }

  .history-name {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--color-bright);
    margin-bottom: 0.2rem;
  }

  .history-sub {
    font-size: 0.76rem;
    color: var(--color-muted);
  }

  .history-actions {
    display: flex;
    gap: 0.45rem;
    flex-shrink: 0;
  }

  .history-btn {
    padding: 0.45rem 0.85rem;
    background: var(--color-elevated);
    border: none;
    border-radius: var(--radius-pill);
    color: var(--color-soft);
    font-size: 0.78rem;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
  }

  .history-btn:hover {
    background: #333;
    color: var(--color-bright);
  }

  @media (max-width: 700px) {
    .history-item {
      flex-direction: column;
      align-items: flex-start;
    }

    .history-actions {
      width: 100%;
    }

    .history-btn {
      flex: 1;
    }
  }
</style>

<script lang="ts">
  import type { RepoAnalysis } from "../lib/types";

  type AnalysisSummaryProps = {
    analysis: RepoAnalysis;
  };

  let { analysis }: AnalysisSummaryProps = $props();
</script>

<div class="summary-panel">
  <div class="header">
    <h2 class="project">{analysis.projectName}</h2>
    <span class="badge">{analysis.fileCount} files</span>
  </div>

  {#if analysis.stack.length}
    <div class="row">
      <span class="label">Stack</span>
      <div class="chips">
        {#each analysis.stack as item}
          <span class="chip">{item}</span>
        {/each}
      </div>
    </div>
  {/if}

  {#if analysis.patterns.length}
    <div class="row">
      <span class="label">Detected</span>
      <div class="chips">
        {#each analysis.patterns as pattern}
          <span class="chip accent">{pattern.category}</span>
        {/each}
      </div>
    </div>
  {:else}
    <p class="empty">No data patterns found in this scan</p>
  {/if}
</div>

<style>
  .summary-panel {
    padding: 1.35rem 1.5rem;
    background: var(--color-surface);
    border-radius: var(--radius-panel);
  }

  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.25rem;
  }

  .project {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--color-bright);
  }

  .badge {
    padding: 0.35rem 0.85rem;
    background: var(--color-elevated);
    border-radius: var(--radius-pill);
    font-size: 0.8rem;
    color: var(--color-muted);
    white-space: nowrap;
  }

  .row {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    margin-bottom: 1rem;
  }

  .row:last-child {
    margin-bottom: 0;
  }

  .label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--color-muted);
  }

  .chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .chip {
    padding: 0.4rem 0.85rem;
    background: var(--color-elevated);
    border-radius: var(--radius-pill);
    font-size: 0.82rem;
    color: var(--color-soft);
  }

  .chip.accent {
    background: #2e2e2e;
    color: var(--color-bright);
  }

  .empty {
    font-size: 0.875rem;
    color: var(--color-muted);
  }
</style>

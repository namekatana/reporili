<script lang="ts">
  type GithubInputProps = {
    disabled?: boolean;
    value: string;
    onValueChange: (value: string) => void;
  };

  let { disabled = false, value, onValueChange }: GithubInputProps = $props();

  const hasValue = $derived(value.trim().length > 0);
</script>

<div class="github-panel" class:highlighted={hasValue}>
  <div class="panel-top">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
    </svg>
    <span class="panel-label">GitHub URL</span>
  </div>
  <input
    id="github-url"
    class="input"
    type="url"
    placeholder="github.com/owner/repo"
    {disabled}
    {value}
    oninput={(e) => onValueChange((e.target as HTMLInputElement).value)}
  />
  <p class="panel-hint">Public repos only, no download needed</p>
</div>

<style>
  .github-panel {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    height: 100%;
    min-height: 180px;
    padding: 1.75rem 1.25rem;
    background: var(--color-float);
    border-radius: var(--radius-panel);
    transition: background 0.2s, box-shadow 0.2s;
  }

  .github-panel.highlighted {
    background: var(--color-elevated);
    box-shadow: inset 0 0 0 1px #3a3a3a;
  }

  .panel-top {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--color-soft);
  }

  .panel-label {
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--color-bright);
  }

  .input {
    width: 100%;
    padding: 0.85rem 1rem;
    background: var(--color-elevated);
    border: none;
    border-radius: var(--radius-control);
    color: var(--color-bright);
    font-size: 0.92rem;
    transition: background 0.2s;
  }

  .input::placeholder {
    color: var(--color-muted);
  }

  .input:focus {
    outline: none;
    background: #2c2c2c;
  }

  .input:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }

  .panel-hint {
    margin-top: auto;
    font-size: 0.78rem;
    color: var(--color-muted);
  }
</style>

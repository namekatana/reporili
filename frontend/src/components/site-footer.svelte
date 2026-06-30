<script lang="ts">
  import { resolveGithubUrl } from "../lib/site-config";

  const githubUrl = resolveGithubUrl();
</script>

<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <span class="footer-name">Reporili</span>
      <span class="footer-note">AI drafts, not a law firm</span>
    </div>

    <nav class="footer-nav" aria-label="Legal">
      <a class="footer-link" href="/privacy">Privacy</a>
      <a class="footer-link" href="/terms">Terms</a>
      <a class="footer-link" href="/disclaimer">Disclaimer</a>
    </nav>

    <div class="footer-actions">
      <a class="github-btn" href={githubUrl} target="_blank" rel="noopener noreferrer">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
        </svg>
        View on GitHub
      </a>
    </div>
  </div>
</footer>

<style>
  .site-footer {
    margin-top: auto;
    padding: 0 2rem 2rem;
  }

  .footer-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    max-width: 1120px;
    margin: 0 auto;
    padding: 1.1rem 1.35rem;
    background: var(--color-surface);
    border-radius: var(--radius-panel);
  }

  .footer-brand {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
  }

  .footer-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--color-bright);
  }

  .footer-note {
    font-size: 0.78rem;
    color: var(--color-muted);
  }

  .footer-nav {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .footer-link {
    font-size: 0.82rem;
    color: var(--color-muted);
    text-decoration: none;
    transition: color 0.2s;
  }

  .footer-link:hover {
    color: var(--color-bright);
  }

  .footer-actions {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .github-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.65rem 1rem;
    background: var(--color-elevated);
    border-radius: var(--radius-pill);
    color: var(--color-bright);
    font-size: 0.82rem;
    font-weight: 500;
    text-decoration: none;
    transition: background 0.2s, color 0.2s;
  }

  .github-btn:hover {
    background: #333;
    color: #fff;
  }

  @media (max-width: 700px) {
    .site-footer {
      padding-left: 1.25rem;
      padding-right: 1.25rem;
    }

    .footer-inner {
      flex-direction: column;
      align-items: flex-start;
    }

    .footer-nav {
      order: 2;
    }

    .footer-actions {
      order: 3;
      width: 100%;
    }

    .github-btn {
      width: 100%;
      justify-content: center;
    }
  }
</style>

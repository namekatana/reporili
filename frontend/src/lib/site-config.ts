export function resolveSiteUrl(): string {
  return (import.meta.env.PUBLIC_SITE_URL ?? "https://reporili.tech").replace(/\/$/, "");
}

export function resolveGithubUrl(): string {
  return import.meta.env.PUBLIC_GITHUB_URL ?? "https://github.com/namekatana/reporili";
}

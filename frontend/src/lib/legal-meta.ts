export const legalLastUpdated = "30 June 2026";

export const governingLawCountry = "Ukraine";

export type LegalDocId = "privacy" | "terms" | "disclaimer";

export type LegalNavItem = {
  id: LegalDocId;
  href: string;
  label: string;
  shortLabel: string;
  subtitle: string;
};

export const legalNav: LegalNavItem[] = [
  {
    id: "privacy",
    href: "/privacy",
    label: "Privacy Policy",
    shortLabel: "Privacy",
    subtitle: "How we handle uploads, logs, and third-party AI processing.",
  },
  {
    id: "terms",
    href: "/terms",
    label: "Terms of Service",
    shortLabel: "Terms",
    subtitle: "Usage rules, your responsibilities, and Beta service terms.",
  },
  {
    id: "disclaimer",
    href: "/disclaimer",
    label: "Disclaimer",
    shortLabel: "Disclaimer",
    subtitle: "AI-generated drafts only — not legal advice.",
  },
];

export function resolveLegalNavItem(id: LegalDocId): LegalNavItem {
  const item = legalNav.find((entry) => entry.id === id);
  if (!item) {
    throw new Error(`Unknown legal document: ${id}`);
  }
  return item;
}

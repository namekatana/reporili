export const siteName = "Reporili";

export const defaultTitle = "Reporili — Privacy Policy, Terms & Disclaimer from your codebase";

export const defaultDescription =
  "Generate tailored Privacy Policy, Terms of Service, and Disclaimer by scanning your GitHub repo or ZIP. Built for developers shipping SaaS, apps, and APIs.";

export function resolveSiteUrl(): string {
  return (import.meta.env.PUBLIC_SITE_URL ?? "https://reporili.tech").replace(/\/$/, "");
}

export function buildJsonLd(siteUrl: string, pageUrl: string) {
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebSite",
        "@id": `${siteUrl}/#website`,
        url: siteUrl,
        name: siteName,
        description: defaultDescription,
        inLanguage: "en-US",
      },
      {
        "@type": "WebApplication",
        "@id": `${siteUrl}/#app`,
        url: pageUrl,
        name: siteName,
        description: defaultDescription,
        applicationCategory: "BusinessApplication",
        operatingSystem: "Web",
        browserRequirements: "Requires JavaScript",
        offers: {
          "@type": "Offer",
          price: "0",
          priceCurrency: "USD",
        },
        featureList: [
          "Privacy Policy generation",
          "Terms of Service generation",
          "Disclaimer generation",
          "GitHub repository scan",
          "ZIP upload",
          "Markdown, HTML, and DOCX export",
        ],
      },
      {
        "@type": "Organization",
        "@id": `${siteUrl}/#organization`,
        name: siteName,
        url: siteUrl,
        logo: `${siteUrl}/logo.png`,
        sameAs: ["https://github.com/namekatana/reporili"],
      },
    ],
  };
}

import { resolveGithubUrl, resolveSiteUrl } from "./site-config";

export const siteName = "Reporili";

export const defaultTitle = "Reporili — Privacy Policy, Terms & Disclaimer from your codebase";

export const defaultDescription =
  "Generate tailored Privacy Policy, Terms of Service, and Disclaimer by scanning your GitHub repo or ZIP. Built for developers shipping SaaS, apps, and APIs.";

export { resolveSiteUrl };

export function buildJsonLd(siteUrl: string, pageUrl: string) {
  const githubUrl = resolveGithubUrl().replace(/\/$/, "");

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
        sameAs: [githubUrl],
      },
    ],
  };
}

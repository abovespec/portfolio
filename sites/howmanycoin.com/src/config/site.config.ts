/**
 * Per-site configuration schema.
 *
 * Every site in the network owns its own copy of this file (via the
 * create-site CLI). Layouts, components, and schema generators read from
 * this single object so branding, SEO, feature flags, and legal/monetization
 * settings can be tuned without touching template code.
 *
 * Token placeholders prefixed with __ are replaced by scripts/create-site.mjs.
 */

export type OgImageStrategy = 'generated' | 'static';
export type OrganizationType = 'Organization' | 'Person';

export interface NavLink {
  label: string;
  href: string;
}

export interface SiteConfig {
  identity: {
    /** Human-friendly site name (used in titles, schema). */
    name: string;
    /** Bare domain, no scheme, no trailing slash. e.g. "example.com". */
    domain: string;
    /** ~160-char site-wide default description. */
    description: string;
    /** BCP-47 language tag. Defaults to 'en' for the network. */
    language: string;
    /** IANA timezone (used for publish/updated date formatting). */
    timezone: string;
  };
  branding: {
    /** Hex color for <meta name="theme-color"> and primary UI accents. */
    themeColor: string;
    /** Hex color used for links/CTAs. */
    accentColor: string;
    /** Text displayed in header as logo (or alt text if a logo image is swapped in). */
    logoText: string;
    /** 'generated' = runtime/og-image generation; 'static' = serve defaultOgImage. */
    ogImageStrategy: OgImageStrategy;
  };
  org: {
    organizationName: string;
    organizationUrl: string;
    /** Canonical social profile URLs (Organization.sameAs in schema.org). */
    sameAs: string[];
    contactEmail: string;
  };
  seo: {
    /** Rendered between page title and site name. */
    titleSeparator: string;
    /** Path under /public (or absolute URL) for the fallback OG image. */
    defaultOgImage: string;
    /** @handle including the leading @, or empty string. */
    twitterHandle: string;
  };
  features: {
    hasBlog: boolean;
    hasTool: boolean;
    hasGame: boolean;
    hasSponsoredIntake: boolean;
  };
  monetization: {
    /** FTC-style disclosure string rendered on affiliate content. */
    affiliateDisclosure: string;
    adsenseId?: string;
    ezoicId?: string;
  };
  schemaDefaults: {
    organizationType: OrganizationType;
    foundingYear: number;
  };
  nav: {
    primary: NavLink[];
  };
}

export const siteConfig: SiteConfig = {
  identity: {
    name: 'howmanycoin',
    domain: 'howmanycoin.com',
    description:
      'Live crypto pair conversion rates and token-supply explainers. How many USDC is 1 ETH, right now? Direct swap links included.',
    language: 'en',
    timezone: 'UTC',
  },
  branding: {
    themeColor: '#f7f8fa',
    accentColor: '#3730a3',
    logoText: 'howmanycoin',
    ogImageStrategy: 'static',
  },
  org: {
    organizationName: 'howmanycoin',
    organizationUrl: 'https://howmanycoin.com',
    sameAs: [],
    contactEmail: 'hello@howmanycoin.com',
  },
  seo: {
    titleSeparator: ' | ',
    defaultOgImage: '/og-default.svg',
    twitterHandle: '',
  },
  features: {
    hasBlog: false,
    hasTool: false,
    hasGame: false,
    hasSponsoredIntake: true,
  },
  monetization: {
    affiliateDisclosure:
      'Rates shown are estimates sourced from CoinGecko, refreshed every 60 seconds. Swap and exchange links on this page are affiliate links; if you use one we may earn a commission at no extra cost to you. Not financial advice.',
  },
  schemaDefaults: {
    organizationType: 'Organization',
    foundingYear: new Date().getFullYear(),
  },
  nav: {
    primary: [
      { label: 'Convert', href: '/convert/' },
      { label: 'Supply', href: '/supply/' },
      { label: 'Guides', href: '/guides/' },
      { label: 'Methodology', href: '/methodology/' },
      { label: 'About', href: '/about/' },
    ],
  },
};

/** Public site URL (no trailing slash). */
export const siteUrl = `https://${siteConfig.identity.domain}`;

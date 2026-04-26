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
    name: 'ColorPalette',
    domain: 'colorpalette.io',
    description: 'Free color palette generator, WCAG contrast checker, CSS gradient builder, and HEX/RGB/HSL converter.',
    language: 'en',
    timezone: 'UTC',
  },
  branding: {
    themeColor: '#701a75',
    accentColor: '#c026d3',
    logoText: 'ColorPalette',
    ogImageStrategy: 'static',
  },
  org: {
    organizationName: 'ColorPalette',
    organizationUrl: 'https://colorpalette.io',
    sameAs: [],
    contactEmail: 'hello@colorpalette.io',
  },
  seo: {
    titleSeparator: ' | ',
    defaultOgImage: '/og-default.png',
    twitterHandle: '',
  },
  features: {
    hasBlog: true,
    hasTool: false,
    hasGame: false,
    hasSponsoredIntake: false,
  },
  monetization: {
    affiliateDisclosure:
      'This page may contain affiliate links. If you click one and make a purchase we may earn a small commission at no extra cost to you. Our editorial opinions are our own.',
  },
  schemaDefaults: {
    organizationType: 'Organization',
    foundingYear: new Date().getFullYear(),
  },
  nav: {
    primary: [
      { label: 'Home', href: '/' },
      { label: 'Blog', href: '/blog/' },
      { label: 'About', href: '/about/' },
      { label: 'Contact', href: '/contact/' },
    ],
  },
};

/** Public site URL (no trailing slash). */
export const siteUrl = `https://${siteConfig.identity.domain}`;

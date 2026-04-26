export type OgImageStrategy = 'generated' | 'static';
export type OrganizationType = 'Organization' | 'Person';

export interface NavLink {
  label: string;
  href: string;
}

export interface SiteConfig {
  identity: {
    name: string;
    domain: string;
    description: string;
    language: string;
    timezone: string;
  };
  branding: {
    themeColor: string;
    accentColor: string;
    logoText: string;
    ogImageStrategy: OgImageStrategy;
  };
  org: {
    organizationName: string;
    organizationUrl: string;
    sameAs: string[];
    contactEmail: string;
  };
  seo: {
    titleSeparator: string;
    defaultOgImage: string;
    twitterHandle: string;
  };
  features: {
    hasBlog: boolean;
    hasTool: boolean;
    hasGame: boolean;
    hasSponsoredIntake: boolean;
  };
  monetization: {
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
    name: 'RegexBuilder',
    domain: 'regexbuilder.io',
    description: 'Free online regexbuilder tool — no signup, instant results in your browser.',
    language: 'en',
    timezone: 'UTC',
  },
  branding: {
    themeColor: '#be123c',
    accentColor: '#fb7185',
    logoText: 'RegexBuilder',
    ogImageStrategy: 'static',
  },
  org: {
    organizationName: 'RegexBuilder',
    organizationUrl: 'https://regexbuilder.io',
    sameAs: [],
    contactEmail: 'hello@regexbuilder.io',
  },
  seo: {
    titleSeparator: ' | ',
    defaultOgImage: '/og-default.png',
    twitterHandle: '',
  },
  features: {
    hasBlog: false,
    hasTool: false,
    hasGame: false,
    hasSponsoredIntake: false,
  },
  monetization: {
    affiliateDisclosure:
      'This page may contain affiliate links. If you click one and make a purchase we may earn a small commission at no extra cost to you.',
  },
  schemaDefaults: {
    organizationType: 'Organization',
    foundingYear: new Date().getFullYear(),
  },
  nav: {
    primary: [
      { label: 'Home', href: '/' },
      { label: 'About', href: '/about/' },
      { label: 'Contact', href: '/contact/' },
    ],
  },
};

export const siteUrl = `https://${siteConfig.identity.domain}`;

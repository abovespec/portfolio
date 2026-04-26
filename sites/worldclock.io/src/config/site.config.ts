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
    name: 'WorldClock',
    domain: 'worldclock.io',
    description: 'Free online worldclock tool — no signup, instant results in your browser.',
    language: 'en',
    timezone: 'UTC',
  },
  branding: {
    themeColor: '#a21caf',
    accentColor: '#e879f9',
    logoText: 'WorldClock',
    ogImageStrategy: 'static',
  },
  org: {
    organizationName: 'WorldClock',
    organizationUrl: 'https://worldclock.io',
    sameAs: [],
    contactEmail: 'hello@worldclock.io',
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
      'This page may contain affiliate links. If you click one and make a purchase we may earn a small commission at no extra cost to you.',
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

export const siteUrl = `https://${siteConfig.identity.domain}`;

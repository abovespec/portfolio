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
    name: 'PaintCalc',
    domain: 'paintcalc.io',
    description: 'Paint calculator, flooring estimator, roofing square footage, HVAC BTU sizing, and solar savings tools.',
    language: 'en',
    timezone: 'UTC',
  },
  branding: {
    themeColor: '#e11d48',
    accentColor: '#fb7185',
    logoText: 'PaintCalc',
    ogImageStrategy: 'static',
  },
  org: {
    organizationName: 'PaintCalc',
    organizationUrl: 'https://paintcalc.io',
    sameAs: [],
    contactEmail: 'hello@paintcalc.io',
  },
  seo: {
    titleSeparator: ' | ',
    defaultOgImage: '/og-default.png',
    twitterHandle: '',
  },
  features: {
    hasBlog: true,
    hasTool: true,
    hasGame: false,
    hasSponsoredIntake: true,
  },
  monetization: {
    affiliateDisclosure:
      'This page may contain affiliate links. If you click one and make a purchase we may earn a small commission at no extra cost to you. Our editorial opinions are our own.',
  },
  schemaDefaults: {
    organizationType: 'Organization',
    foundingYear: 2025,
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

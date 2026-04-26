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
    name: 'SellerProfit',
    domain: 'sellerprofit.io',
    description: 'Amazon FBA fee calculator, eBay fee calc, Etsy profit estimator, and dropshipping margin tools for online sellers.',
    language: 'en',
    timezone: 'UTC',
  },
  branding: {
    themeColor: '#059669',
    accentColor: '#10b981',
    logoText: 'SellerProfit',
    ogImageStrategy: 'static',
  },
  org: {
    organizationName: 'SellerProfit',
    organizationUrl: 'https://sellerprofit.io',
    sameAs: [],
    contactEmail: 'hello@sellerprofit.io',
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

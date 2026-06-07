---
title: "The Compound Interest Formula Explained: Variables, Examples, and How to Use It"
description: "A clear breakdown of the compound interest formula — what each variable means, how to plug in real numbers, and how monthly, annual, and daily compounding change your results."
publishDate: 2026-05-22
updatedDate: 2026-05-22
author: "Editorial Team"
tags: ["compound interest", "financial formulas", "investing", "financial basics", "math"]
draft: false
reviewedBy: ""
lastReviewedAt: 2026-05-22
sources:
  - text: "Investopedia — Compound Interest Definition and Formula"
    url: "https://www.investopedia.com/terms/c/compoundinterest.asp"
  - text: "Khan Academy — Compound interest"
    url: "https://www.khanacademy.org/economics-finance-domain/core-finance/interest-tutorial/compound-interest-tutorial/a/compound-interest-basics"
  - text: "CFPB — What is compound interest?"
    url: "https://www.consumerfinance.gov/ask-cfpb/what-is-compound-interest-en-2218/"
---

> **Financial Disclaimer:** This article is for educational and informational purposes only. It does not constitute financial, investment, or tax advice. Consult a licensed financial advisor before making decisions about your savings or investments.

Compound interest is the mechanism behind both wealth building in savings accounts and debt spiraling on credit cards. The formula itself is not complicated, but the variables inside it matter enormously. Once you understand how to read the formula and work with its inputs, you can model almost any savings or investment scenario with confidence.

For more on this topic, see [*How Does Compound Interest Work? A Plain-English Guide*](/blog/how-does-compound-interest-work).

## The Formula

**A = P(1 + r/n)^(nt)**

That's it. Five variables. Here is what each one means:

- **A** — the final amount (what you end up with after interest)
- **P** — the principal (your starting amount)
- **r** — the annual interest rate expressed as a decimal (so 5% becomes 0.05, 7.5% becomes 0.075)
- **n** — the number of compounding periods per year (annually = 1, monthly = 12, daily = 365)
- **t** — the number of years your money grows

The key insight is that **r/n** is the per-period interest rate, and **(nt)** is the total number of periods. When interest compounds monthly, the annual rate is divided into 12 smaller slices — each slice earns interest on everything that came before it.

## Worked Example 1: Annual Compounding

**Scenario:** You deposit $3,000 in a savings account at 4% interest, compounded annually, for 5 years.

Plugging in:
- P = 3,000
- r = 0.04
- n = 1
- t = 5

**A = 3,000 × (1 + 0.04/1)^(1×5)**  
A = 3,000 × (1.04)^5  
A = 3,000 × 1.2167  
**A = $3,650.10**

Your $3,000 grows by $650.10 over five years. No extra contributions — just the original deposit and time.

## Worked Example 2: Monthly Compounding

**Scenario:** Same $3,000, same 4% annual rate, but now compounding monthly for 5 years.

- P = 3,000
- r = 0.04
- n = 12
- t = 5

**A = 3,000 × (1 + 0.04/12)^(12×5)**  
A = 3,000 × (1.003333...)^60  
A = 3,000 × 1.2212  
**A = $3,663.60**

Monthly compounding produces $13.50 more than annual compounding on this particular scenario. That gap widens substantially as the principal and time horizon increase.

## Worked Example 3: Daily Compounding

**Scenario:** Same deposit again, but compounding 365 times per year.

- P = 3,000
- r = 0.04
- n = 365
- t = 5

**A = 3,000 × (1 + 0.04/365)^(365×5)**  
A = 3,000 × (1.000109...)^1825  
A = 3,000 × 1.2214  
**A = $3,664.20**

Daily compounding adds only another $0.60 compared to monthly in this scenario. The difference between monthly and daily compounding is often negligible; what matters far more is the rate and the time.

## How Compounding Frequency Stacks Up

Here is a direct comparison using $10,000 at 6% annual interest over 15 years:

| Compounding Frequency | Final Amount |
|-----------------------|--------------|
| Annually | $23,965.58 |
| Quarterly | $24,272.48 |
| Monthly | $24,409.83 |
| Daily | $24,596.03 |

The annual-to-daily difference is about $630 on $10,000 over 15 years. On a larger balance — say, $100,000 over 30 years — that same proportional gap becomes substantial. Still, chasing daily compounding while ignoring the interest rate is the wrong priority. A 5% account compounding daily will still underperform a 6% account compounding annually over long periods.

## What Happens When You Add Contributions?

The standard compound interest formula assumes a single lump-sum deposit. Real-world saving usually involves regular contributions. The formula for that is the **future value of an annuity**:

For more on this topic, see [*Simple Interest vs. Compound Interest: Key Differences with Real Examples*](/blog/simple-interest-vs-compound-interest).

**FV = PMT × [((1 + r/n)^(nt) − 1) / (r/n)]**

Where PMT is the regular payment per period. For example, $200/month at 6% annual rate over 20 years:

- PMT = 200
- r = 0.06
- n = 12
- t = 20

FV = 200 × [((1.005)^240 − 1) / 0.005]  
FV = 200 × [(3.3102 − 1) / 0.005]  
FV = 200 × [2.3102 / 0.005]  
FV = 200 × 462.04  
**FV ≈ $92,408**

You contributed $48,000 total ($200 × 240 months). The remaining $44,408 is pure compound growth. That's nearly a 1:1 ratio of contributions to gains — which is why consistent monthly investing is so powerful.

## Common Mistakes When Using the Formula

**1. Forgetting to convert the rate to a decimal.** If your rate is 5%, r = 0.05, not 5. Using 5 directly gives you a nonsensical result — it would imply 500% annual interest.

**2. Mismatching n and t.** If n = 12 (monthly), then t must be in years, not months. If you have 36 months of data, t = 3.

**3. Confusing nominal rate with effective rate.** The formula uses the nominal (stated) annual rate. The actual rate you earn after compounding is higher — this is called the **effective annual rate (EAR)**, calculated as: EAR = (1 + r/n)^n − 1. For 6% compounded monthly, the EAR is about 6.17%.

**4. Ignoring taxes and fees.** In a taxable account, interest is usually taxed as ordinary income in the year it's earned. The formula models gross growth; net growth after taxes and any account fees will be lower.

## Using the Formula vs. Using a Calculator

Working through the formula manually is valuable for understanding the mechanics. For planning purposes, a [financial calculator](/) lets you vary any input — rate, time, contributions, compounding frequency — and immediately see the result. This is especially useful for comparing scenarios: "what if I increase my monthly contribution by $50?" or "how much does an extra year matter?"

For more on this topic, see [*How to Use a Loan Calculator: Inputs, Outputs, and What the Numbers Mean*](/blog/how-to-use-a-loan-calculator).

## The Bottom Line

The compound interest formula A = P(1 + r/n)^(nt) has five moving parts, and all five affect your final result:

- A higher rate (r) compounds faster
- A longer time horizon (t) creates exponential growth
- More frequent compounding (n) adds modest gains
- A larger starting principal (P) scales everything up

Of these, **time is the one variable you cannot buy back.** The formula rewards patience more than any other input. Start early, let it run, and resist the urge to withdraw. The math does the rest.

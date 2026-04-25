---
title: "How to Calculate Gross Profit Margin: Step-by-Step with Examples"
description: "Learn the gross profit margin formula, walk through four worked examples across retail, SaaS, manufacturing, and services, and avoid the most common calculation errors."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["how to calculate gross profit margin", "gross profit margin formula", "gross margin calculation", "COGS", "profit margin"]
draft: false
reviewedBy: ""
lastReviewedAt: 2026-04-25
sources:
  - text: "Investopedia — How to Calculate Gross Profit Margin"
    url: "https://www.investopedia.com/terms/g/gross_profit_margin.asp"
  - text: "Corporate Finance Institute — Gross Margin Formula"
    url: "https://corporatefinanceinstitute.com/resources/accounting/gross-profit-margin-formula/"
  - text: "U.S. Small Business Administration — Financial Management"
    url: "https://www.sba.gov/business-guide/manage-your-business/manage-your-finances"
  - text: "NYU Stern School of Business — Margins by Sector"
    url: "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/margin.html"
---

> **Financial information for educational purposes.** The figures in this article reflect general market data and should not be treated as financial advice for your specific business. Consult a financial professional for personalized guidance.

Gross profit margin is one of the most important numbers on an income statement — and one of the easiest to calculate once you know which numbers to use. This guide walks through the formula step by step, applies it to four different business types, shows you how to use it in a spreadsheet, and highlights the mistakes that cause incorrect results.

---

## The Gross Profit Margin Formula

**Step 1: Calculate Gross Profit**

```
Gross Profit = Revenue − Cost of Goods Sold (COGS)
```

**Step 2: Calculate Gross Margin Percentage**

```
Gross Profit Margin (%) = (Gross Profit ÷ Revenue) × 100
```

Combined into one formula:

```
Gross Profit Margin (%) = ((Revenue − COGS) ÷ Revenue) × 100
```

That is all there is to it. The complexity lives not in the formula but in correctly identifying what belongs in COGS and what belongs in operating expenses — more on that below.

---

## What Is COGS?

Cost of Goods Sold (COGS) includes the **direct costs** of producing the goods or services your business sells. What qualifies as a direct cost depends on the type of business:

| Business Type | Typical COGS Components |
|---|---|
| **Product retailer** | Wholesale purchase cost, inbound freight, import duties |
| **Manufacturer** | Raw materials, direct labor on production line, manufacturing overhead (factory rent, equipment depreciation) |
| **Restaurant** | Food and beverage ingredients, packaging |
| **Software / SaaS** | Hosting and infrastructure, customer support directly tied to product delivery, third-party API costs |
| **Service business** | Direct labor cost of delivering the service (not management salaries), subcontractors, materials consumed |

**What is NOT in COGS:**
- Office rent (unless it's a factory/production floor)
- Sales team salaries
- Marketing and advertising
- Management and executive compensation
- Administrative costs
- Interest expense
- Taxes

If you include non-COGS items in your cost figure, your gross margin will be understated.

---

## Step-by-Step Worked Examples

### Example 1: Retail Business

**Green Leaf Garden Center** sells garden supplies.

| | Amount |
|---|---|
| Annual Revenue | $480,000 |
| Inventory purchased for resale (merchandise) | $220,000 |
| Inbound freight on inventory | $14,000 |
| **Total COGS** | **$234,000** |

**Calculation:**
1. Gross Profit = $480,000 − $234,000 = $246,000
2. Gross Margin = ($246,000 ÷ $480,000) × 100 = **51.25%**

For every $1 in sales, $0.51 is available after product costs to cover store rent, staff, marketing, and profit.

---

### Example 2: Manufacturing Business

**Ironside Metal Works** makes custom steel brackets.

| | Amount |
|---|---|
| Annual Revenue | $1,200,000 |
| Raw materials (steel, fasteners) | $360,000 |
| Direct labor (production workers only) | $240,000 |
| Factory overhead (factory lease, machine depreciation) | $120,000 |
| **Total COGS** | **$720,000** |

**Calculation:**
1. Gross Profit = $1,200,000 − $720,000 = $480,000
2. Gross Margin = ($480,000 ÷ $1,200,000) × 100 = **40%**

A 40% gross margin is reasonable for a metal fabrication business. The company has $480,000 to cover office overhead, sales, and profit.

---

### Example 3: SaaS / Software Business

**PlanTrack** is a project management SaaS with $2,000,000 in annual recurring revenue.

| | Amount |
|---|---|
| Annual Recurring Revenue (ARR) | $2,000,000 |
| Cloud hosting (AWS/GCP) | $140,000 |
| Third-party APIs and services | $40,000 |
| Customer support team (product delivery only) | $120,000 |
| **Total COGS** | **$300,000** |

**Calculation:**
1. Gross Profit = $2,000,000 − $300,000 = $1,700,000
2. Gross Margin = ($1,700,000 ÷ $2,000,000) × 100 = **85%**

An 85% gross margin is typical for mature SaaS businesses. The high margin reflects that software has minimal incremental cost per additional customer — serving 1,000 customers costs nearly the same in infrastructure as serving 500.

---

### Example 4: Service Business (Consulting)

**Apex Strategy Consulting** bills $800,000 in annual consulting fees.

| | Amount |
|---|---|
| Revenue | $800,000 |
| Consultant salaries (billable staff delivering projects) | $340,000 |
| Subcontractor fees | $60,000 |
| **Total COGS** | **$400,000** |

Note: The managing partners' salaries, office rent, and marketing costs are **not** in COGS — they are operating expenses.

**Calculation:**
1. Gross Profit = $800,000 − $400,000 = $400,000
2. Gross Margin = ($400,000 ÷ $800,000) × 100 = **50%**

A 50% gross margin for a consulting firm is healthy. The remaining 50% must cover all overhead and leave a net profit.

---

## How to Calculate Gross Margin in a Spreadsheet

If you manage finances in Excel or Google Sheets, here is the standard setup:

| Cell | Label | Value |
|------|-------|-------|
| B1 | Revenue | 480000 |
| B2 | COGS | 234000 |
| B3 | Gross Profit | =B1-B2 |
| B4 | Gross Margin % | =(B3/B1)*100 |

For a dynamic model across multiple periods, apply the same formula to each column (month, quarter, year) and add a row for the trend chart.

---

## Common Calculation Errors

### Error 1: Including operating expenses in COGS

Salaries for non-production staff, office rent, and marketing spend are **not** COGS. Including them understates your gross margin and makes it look like your production efficiency is worse than it is.

### Error 2: Using gross revenue instead of net revenue

If your revenue figure includes refunds, returns, and allowances, subtract those first to get **net revenue** before dividing. Most income statements already show net revenue on the top line, but verify.

**Formula adjustment:**
```
Net Revenue = Gross Revenue − Returns − Allowances − Discounts
Gross Margin = ((Net Revenue − COGS) ÷ Net Revenue) × 100
```

### Error 3: Forgetting freight and import costs in retail COGS

For physical product businesses, the cost of getting inventory to your warehouse (inbound freight, import duties, customs fees) is part of the cost of that inventory and belongs in COGS. Omitting it overstates gross margin.

### Error 4: Misclassifying service delivery vs. overhead labor

For service businesses, only the direct cost of *delivering* services belongs in COGS. Management oversight, business development time, and administrative hours are operating expenses. Misclassifying these in either direction distorts your gross margin.

---

## Interpreting Your Result

Once you have your gross margin percentage:

1. **Compare to industry benchmarks.** See our [industry margin benchmarks guide](/blog/what-is-a-good-profit-margin/) to assess where you stand.
2. **Track the trend.** Calculate gross margin for each of the past 4–8 quarters. Is it rising, stable, or falling?
3. **Identify the driver of any change.** If gross margin fell, was it a price decrease, a COGS increase, or a product mix shift toward lower-margin items?
4. **Set a target.** Based on your industry benchmark and overhead structure, determine the minimum gross margin you need to achieve a healthy net margin after all operating costs.

---

## Key Takeaways

- Gross Profit Margin = ((Revenue − COGS) ÷ Revenue) × 100
- COGS includes only direct production costs — not overhead, admin, marketing, or taxes
- The formula is the same across industries; what varies is which costs qualify as COGS
- Common errors include mixing operating expenses into COGS and using gross instead of net revenue
- Always interpret your result in the context of your specific industry's typical margin range

Use our [profit margin calculator](/tools/profit-margin-calculator/) to compute your gross margin instantly — just enter your revenue and COGS figures.

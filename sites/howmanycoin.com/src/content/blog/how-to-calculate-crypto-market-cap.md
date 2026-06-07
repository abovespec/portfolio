---
title: "How to Calculate Crypto Market Cap (Step by Step)"
description: "Learn the market cap formula, walk through a worked Bitcoin example, and understand the difference between circulating supply, total supply, and FDV."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["market cap", "crypto math", "circulating supply", "bitcoin", "coingecko"]
draft: false
---

Cryptocurrency market cap sounds like a complicated metric, but the underlying math is straightforward. Once you understand the formula and know where to find the numbers, you can calculate it yourself in seconds — and read any crypto data site with much more confidence.

## The Formula

**Market Cap = Current Price × Circulating Supply**

That is the entire calculation. Two inputs, one output. The result is denominated in fiat currency (typically USD) and tells you the total market value of all coins currently in active circulation.

For more on this topic, see [*How to Convert Bitcoin to USD: The Math and the Methods*](/blog/how-to-convert-bitcoin-to-usd).

Every major data aggregator — [CoinGecko](https://www.coingecko.com), [CoinMarketCap](https://coinmarketcap.com) — computes and displays this figure automatically. But knowing how to derive it yourself means you can sanity-check reported figures and understand why market cap moves even when you haven't traded anything.

## A Worked Example: Bitcoin

Bitcoin is the most familiar case. The protocol enforces a hard cap of 21 million coins, and new coins enter circulation through a process called mining. As of early 2026, roughly 19.8 million BTC are in circulation (you can verify this in real time on CoinGecko or CoinMarketCap).

To illustrate the formula without tying it to a live price:

- **Hypothetical scenario:** BTC trades at $60,000 per coin.
- **Circulating supply:** 19,800,000 BTC.
- **Market cap:** $60,000 × 19,800,000 = **$1,188,000,000,000** (approximately $1.19 trillion).

Now suppose the price drops to $50,000 but the circulating supply stays the same (mining adds coins slowly, so supply barely changes day to day):

For more on this topic, see [*Circulating Supply in Crypto: What It Is and Why It Changes*](/blog/what-is-circulating-supply).

- **Market cap:** $50,000 × 19,800,000 = **$990,000,000,000** (~$990 billion).

The same number of coins now represents $198 billion less in total market value. Market cap moves in real time because the price input is constantly changing. Supply changes too, but far more slowly.

This is why market cap can fall sharply even if "nothing happened" to the underlying network — it is a price-sensitive metric.

For more on this topic, see [*What Is Market Cap in Crypto? The Metric That Matters Most*](/blog/what-is-crypto-market-cap).

## Circulating Supply vs. Total Supply vs. Max Supply

These three terms appear on every crypto data page and are frequently confused. They answer different questions:

**Circulating supply** — The number of coins or tokens that are currently active in the market. These are the coins that can be bought, sold, and transferred right now. This is the figure used in the market cap formula.

**Total supply** — All coins that have been created (minted) so far, minus any that have been permanently destroyed (burned). This includes coins held by teams, investors, and ecosystem treasuries that are not yet in active circulation.

**Max supply** — The maximum number of coins that will ever exist, as defined by the protocol or token contract. Bitcoin's max supply is 21 million. Some assets have no defined max supply — Ethereum does not have a hard cap, though its issuance rate and burn mechanism (introduced with EIP-1559) keep the supply dynamics in check.

The relationship between these figures: **Circulating Supply ≤ Total Supply ≤ Max Supply**

When circulating supply equals max supply, every coin that will ever exist is already in circulation. For Bitcoin, that will happen around the year 2140, when the last satoshis are mined.

## Where to Find These Numbers

You do not need to derive supply figures from raw blockchain data. Both CoinGecko and CoinMarketCap publish circulating supply, total supply, and max supply for most listed assets on each coin's individual page.

Look for a section typically labeled "Supply" or find it in the data table below the price chart. For Bitcoin specifically, you can also check [blockchain.info](https://blockchain.info) or the Bitcoin Core reference implementation for authoritative supply data.

When supply figures differ slightly between sites, it is usually because of timing — data aggregators poll different sources at different intervals. For most purposes, the figures are close enough to be practically identical.

## Fully Diluted Valuation (FDV)

Once you know market cap, the next concept to understand is **fully diluted valuation (FDV)**:

**FDV = Current Price × Max Supply**

FDV answers the question: *if every coin that will ever exist were already in circulation at today's price, what would the total market value be?*

For Bitcoin, where circulating supply is already very close to max supply, market cap and FDV are nearly identical. For younger tokens with large locked reserves — team allocations, investor tranches, ecosystem funds — FDV can be many times larger than current market cap. A token with a $100 million market cap and a $2 billion FDV has a lot of supply that has not yet entered the market.

This matters because those tokens generally will enter the market eventually, on a vesting schedule defined at the project's launch. When they do, they increase supply. If demand does not increase proportionally, price tends to face downward pressure. Checking FDV is a basic step in evaluating any newer crypto project.

## Putting It Together

Market cap calculation is a two-step process in practice:

1. Look up the current price and circulating supply on CoinGecko or CoinMarketCap.
2. Multiply them.

Then compare that number against FDV to understand how much supply expansion may still be coming. And always pair the market cap figure with trading volume — a high market cap combined with very low daily trading volume suggests thin liquidity, which can make large trades difficult to execute at the quoted price.

---

*This article is for informational purposes only and does not constitute financial or investment advice. Cryptocurrency markets are highly volatile. Always conduct your own research and consult a qualified financial advisor before making investment decisions.*

#!/usr/bin/env python3
"""Generate 40 seed MDX pages for howmanycoin.com MVP.

Runs once — writes files directly into content/pairs/, content/supply/,
content/guides/ under the howmanycoin.com site directory.
"""
import os, json

BASE = os.path.expanduser(
    "~/site-network/sites/howmanycoin.com/content"
)


# ------------------------------------------------------------------ #
#  PAIR PAGES  (25)                                                     #
# ------------------------------------------------------------------ #
PAIRS = [
    # (slug, title, description, base, quote, category, featured, keywords)
    ("btc-usd", "BTC to USD — Live Bitcoin to US Dollar Rate",
     "Live BTC to USD rate. Enter any amount to convert Bitcoin to US Dollars instantly.",
     "btc", "usd", "major", True,
     ["bitcoin to usd", "btc to dollar", "btc usd rate", "bitcoin usd converter"]),

    ("btc-eur", "BTC to EUR — Live Bitcoin to Euro Rate",
     "Live BTC to EUR rate. Convert Bitcoin to Euros in real time.",
     "btc", "eur", "major", False,
     ["bitcoin to euro", "btc to euro", "btc eur price", "bitcoin eur converter"]),

    ("btc-gbp", "BTC to GBP — Live Bitcoin to British Pound Rate",
     "Live BTC to GBP rate. Convert Bitcoin to British Pounds instantly.",
     "btc", "gbp", "major", False,
     ["bitcoin to pound", "btc to gbp", "bitcoin pound converter", "btc gbp rate"]),

    ("btc-jpy", "BTC to JPY — Live Bitcoin to Japanese Yen Rate",
     "Live BTC to JPY rate. Convert Bitcoin to Japanese Yen in real time.",
     "btc", "jpy", "major", False,
     ["bitcoin to yen", "btc to yen", "bitcoin yen converter", "btc jpy rate"]),

    ("eth-usd", "ETH to USD — Live Ethereum to US Dollar Rate",
     "Live ETH to USD rate. Convert Ethereum to US Dollars instantly.",
     "eth", "usd", "major", True,
     ["ethereum to usd", "eth to dollar", "eth usd rate", "ethereum usd converter"]),

    ("eth-btc", "ETH to BTC — Live Ethereum to Bitcoin Rate",
     "Live ETH to BTC rate. Convert Ethereum to Bitcoin instantly.",
     "eth", "btc", "major", True,
     ["ethereum to bitcoin", "eth to btc", "eth btc ratio", "eth btc converter"]),

    ("sol-usd", "SOL to USD — Live Solana to US Dollar Rate",
     "Live SOL to USD rate. Convert Solana to US Dollars instantly.",
     "sol", "usd", "l1", True,
     ["solana to usd", "sol to dollar", "sol usd price", "solana usd converter"]),

    ("sol-btc", "SOL to BTC — Live Solana to Bitcoin Rate",
     "Live SOL to BTC rate. Convert Solana to Bitcoin in real time.",
     "sol", "btc", "l1", False,
     ["solana to bitcoin", "sol to btc", "sol btc rate", "solana btc converter"]),

    ("sol-eth", "SOL to ETH — Live Solana to Ethereum Rate",
     "Live SOL to ETH rate. Convert Solana to Ethereum instantly.",
     "sol", "eth", "l1", False,
     ["solana to ethereum", "sol to eth", "sol eth rate", "solana eth converter"]),

    ("usdc-usd", "USDC to USD — Live USD Coin to Dollar Rate",
     "Live USDC to USD rate. Convert USD Coin to US Dollars in real time.",
     "usdc", "usd", "stablecoin", False,
     ["usdc to usd", "usd coin to dollar", "usdc usd rate"]),

    ("usdt-usd", "USDT to USD — Live Tether to Dollar Rate",
     "Live USDT to USD rate. Convert Tether to US Dollars instantly.",
     "usdt", "usd", "stablecoin", False,
     ["tether to usd", "usdt to usd", "usdt usd rate", "tether dollar converter"]),

    ("dai-usd", "DAI to USD — Live Dai to Dollar Rate",
     "Live DAI to USD rate. Convert Dai to US Dollars in real time.",
     "dai", "usd", "stablecoin", False,
     ["dai to usd", "dai to dollar", "makerdao to usd", "dai usd rate"]),

    ("doge-usd", "DOGE to USD — Live Dogecoin to Dollar Rate",
     "Live DOGE to USD rate. Convert Dogecoin to US Dollars instantly.",
     "doge", "usd", "meme", True,
     ["dogecoin to usd", "doge to dollar", "doge usd price", "dogecoin usd converter"]),

    ("shib-usd", "SHIB to USD — Live Shiba Inu to Dollar Rate",
     "Live SHIB to USD rate. Convert Shiba Inu to US Dollars in real time.",
     "shib", "usd", "meme", False,
     ["shiba inu to usd", "shib to usd", "shib usd price", "shib usd converter"]),

    ("pepe-usd", "PEPE to USD — Live Pepe to Dollar Rate",
     "Live PEPE to USD rate. Convert Pepe to US Dollars instantly.",
     "pepe", "usd", "meme", False,
     ["pepe to usd", "pepe to dollar", "pepe usd price", "pepe coin converter"]),

    ("bnb-usd", "BNB to USD — Live BNB to Dollar Rate",
     "Live BNB to USD rate. Convert BNB to US Dollars in real time.",
     "bnb", "usd", "l1", False,
     ["bnb to usd", "binance to usd", "bnb usd price", "binance coin usd"]),

    ("matic-usd", "MATIC to USD — Live Polygon to Dollar Rate",
     "Live MATIC to USD rate. Convert Polygon to US Dollars instantly.",
     "matic", "usd", "l1", False,
     ["polygon to usd", "matic to usd", "matic usd price", "polygon usd converter"]),

    ("avax-usd", "AVAX to USD — Live Avalanche to Dollar Rate",
     "Live AVAX to USD rate. Convert Avalanche to US Dollars in real time.",
     "avax", "usd", "l1", False,
     ["avalanche to usd", "avax to usd", "avax usd price", "avalanche usd"]),

    ("arb-usd", "ARB to USD — Live Arbitrum to Dollar Rate",
     "Live ARB to USD rate. Convert Arbitrum to US Dollars instantly.",
     "arb", "usd", "defi", False,
     ["arbitrum to usd", "arb to usd", "arb usd price", "arbitrum usd"]),

    ("op-usd", "OP to USD — Live Optimism to Dollar Rate",
     "Live OP to USD rate. Convert Optimism to US Dollars in real time.",
     "op", "usd", "defi", False,
     ["optimism to usd", "op to usd", "op usd price", "optimism usd"]),

    ("xrp-usd", "XRP to USD — Live XRP to Dollar Rate",
     "Live XRP to USD rate. Convert XRP to US Dollars in real time.",
     "xrp", "usd", "major", False,
     ["xrp to usd", "ripple to usd", "xrp usd price", "ripple usd converter"]),

    ("ada-usd", "ADA to USD — Live Cardano to Dollar Rate",
     "Live ADA to USD rate. Convert Cardano to US Dollars instantly.",
     "ada", "usd", "l1", False,
     ["cardano to usd", "ada to usd", "ada usd price", "cardano usd converter"]),

    ("ton-usd", "TON to USD — Live Toncoin to Dollar Rate",
     "Live TON to USD rate. Convert Toncoin to US Dollars in real time.",
     "ton", "usd", "l1", False,
     ["toncoin to usd", "ton to usd", "ton usd price", "toncoin usd converter"]),

    ("btc-usdc", "BTC to USDC — Live Bitcoin to USD Coin Rate",
     "Live BTC to USDC rate. Convert Bitcoin to USD Coin instantly.",
     "btc", "usdc", "stablecoin", False,
     ["bitcoin to usdc", "btc to usdc", "btc usdc rate", "bitcoin usdc converter"]),

    ("eth-usdc", "ETH to USDC — Live Ethereum to USD Coin Rate",
     "Live ETH to USDC rate. Convert Ethereum to USD Coin in real time.",
     "eth", "usdc", "stablecoin", False,
     ["ethereum to usdc", "eth to usdc", "eth usdc rate", "ethereum usdc converter"]),
]


# ------------------------------------------------------------------ #
#  SUPPLY PAGES  (10)                                                   #
# ------------------------------------------------------------------ #
SUPPLY = [
    # (slug, title, description, token, supplyType, total, circulating, max, burn)
    ("bitcoin-supply", "Bitcoin Total Supply: 21 Million Hard Cap",
     "Bitcoin has a hard cap of 21 million coins. No more will ever be created. Explore circulating supply, halving schedule, and why the fixed supply matters.",
     "btc", "fixed", "21,000,000", "19,800,000", "21,000,000", False),

    ("ethereum-supply", "Ethereum Supply: Emissions, Burns and Net Issuance",
     "Ethereum has no hard cap. New ETH is minted as block rewards while EIP-1559 burns fees. Explore net issuance, circulating supply and the impact of burning.",
     "eth", "emission", "120,230,000", "120,230,000", None, False),

    ("solana-supply", "Solana Supply: Emission Schedule and Staking",
     "Solana issues new tokens each year with a decreasing emission rate. Staked tokens reduce the liquid supply. See the schedule and circulating figures.",
     "sol", "emission", "477,000,000", "472,000,000", None, False),

    ("bnb-supply", "BNB Supply: 200 Million Cap and Quarterly Burns",
     "BNB has a max supply of 200 million tokens. Binance conducts quarterly auto-burns to reduce supply toward the cap. Explore current figures.",
     "bnb", "capped", "153,856,150", "153,856,150", "200,000,000", True),

    ("matic-supply", "Polygon (MATIC) Supply: 10 Billion Hard Cap",
     "Polygon has a fixed max supply of 10 billion MATIC tokens. Only a fraction are currently circulating. See the full breakdown.",
     "matic", "capped", "10,000,000,000", "9,284,669,962", "10,000,000,000", False),

    ("avalanche-supply", "Avalanche (AVAX) Supply: 720 Million Cap",
     "Avalanche caps total supply at 720 million AVAX. Explore circulating supply, staking ratios and remaining emissions.",
     "avax", "capped", "430,271,500", "397,051,300", "720,000,000", False),

    ("dogecoin-supply", "Dogecoin Supply: Unlimited Inflation Explained",
     "Dogecoin has no hard cap. 5 billion new DOGE are minted every year, creating a steady 1% inflation rate. See why this matters.",
     "doge", "emission", "147,000,000,000", "147,000,000,000", None, False),

    ("shiba-inu-supply", "Shiba Inu (SHIB) Supply: Near 1 Quadrillion Fixed",
     "SHIB has a nearly fixed supply of ~1 quadrillion tokens. No new SHIB will ever be minted. See what happened to the burned tokens.",
     "shib", "fixed", "999,982,287,232,215", "589,299,370,189,573", "999,982,287,232,215", False),

    ("ripple-xrp-supply", "XRP Supply: 100 Billion Cap and Escrow",
     "XRP caps at 100 billion tokens. Ripple holds a large portion in escrow, releasing up to 1 billion monthly. Explore circulating supply.",
     "xrp", "fixed", "100,000,000,000", "56,962,671,351", "100,000,000,000", False),

    ("cardano-supply", "Cardano (ADA) Supply: 45 Billion Hard Cap",
     "Cardano caps total supply at 45 billion ADA. A large portion is still not circulating. See the full supply breakdown and staking impact.",
     "ada", "capped", "45,000,000,000", "36,144,594,406", "45,000,000,000", False),
]


# ------------------------------------------------------------------ #
#  GUIDE PAGES  (5)                                                     #
# ------------------------------------------------------------------ #
GUIDES = [
    ("market-cap-vs-price", "Market Cap vs Price: Why It Matters",
     "Understanding market capitalisation is the single most important skill for evaluating crypto projects. Learn why a low coin price does not mean a coin is cheap.",
     "market-cap",
     ["market cap vs price", "crypto market capitalization", "why market cap matters"]),

    ("fully-diluted-valuation", "Fully Diluted Valuation (FDV) Explained",
     "Fully diluted valuation assumes all tokens are in circulation. Compare FDV to market cap to spot tokens that may face future selling pressure from unlocks.",
     "fully-diluted",
     ["fully diluted valuation", "fdv crypto", "fdv vs market cap", "what is fdv"]),

    ("circulating-vs-total-supply", "Circulating vs Total vs Max Supply",
     "What does circulating supply mean? How is total supply different? Why does max supply matter? A plain-English guide to supply terminology in crypto.",
     "circulating-vs-total",
     ["circulating vs total supply", "crypto supply explained", "max supply vs total"]),

    ("token-emissions-schedule", "Token Emissions Schedule: When Are New Tokens Released?",
     "Emission schedules control how fast new tokens enter circulation. Learn to read emission charts, understand halving events and plan around unlock schedules.",
     "token-emissions",
     ["token emissions", "crypto unlock schedule", "token emission schedule", "halving schedule"]),

    ("supply-shocks", "Crypto Supply Shocks: What Happens When Supply Drops?",
     "When tokens are burned or locked, the circulating supply shrinks. Explore real examples of supply shocks and how they impact price dynamics.",
     "supply-shocks",
     ["supply shock crypto", "token burns price impact", "deflationary crypto"]),
]


# ------------------------------------------------------------------ #
#  TEMPLATE                                                           #
# ------------------------------------------------------------------ #

PAIR_TEMPLATE = """---
title: "{title}"
description: "{description}"
base: "{base}"
quote: "{quote}"
category: "{category}"
featured: {featured}
seoKeywords: [{keywords}]
---

import PairPage from "~/components/PairPage.astro";

<PairPage />
"""

SUPPLY_TEMPLATE = """---
title: "{title}"
description: "{description}"
token: "{token}"
supplyType: "{supplyType}"
totalSupply: "{total}"
circulatingSupply: "{circulating}"
burnMechanism: {burn}
seoKeywords: [{keywords}]
---

import SupplyPage from "~/components/SupplyPage.astro";

<SupplyPage />
"""

GUIDE_TEMPLATE = """---
title: "{title}"
description: "{description}"
topic: "{topic}"
seoKeywords: [{keywords}]
---

import GuidePage from "~/components/GuidePage.astro";

<GuidePage />
"""


# ------------------------------------------------------------------ #
#  WRITE FILES                                                        #
# ------------------------------------------------------------------ #

def write_pair():
    for slug, title, desc, base, quote, cat, feat, kws in PAIRS:
        path = os.path.join(BASE, "pairs", f"{slug}.mdx")
        kws_str = ", ".join(f'"{k}"' for k in kws)
        with open(path, "w") as f:
            f.write(PAIR_TEMPLATE.format(
                title=title, description=desc,
                base=base, quote=quote,
                category=cat, featured="true" if feat else "false",
                keywords=kws_str,
            ))
    print(f"  Written {len(PAIRS)} pair pages")


def write_supply():
    for slug, title, desc, token, stype, total, circ, mx, burn in SUPPLY:
        path = os.path.join(BASE, "supply", f"{slug}.mdx")
        kws_str = ", ".join(f'"{k}"' for k in SUPPLY[-1][-1])  # placeholder, fixed below
        # each entry's keywords are the last element
    # redo properly:
    pass


def write_supply_v2():
    for i, (slug, title, desc, token, stype, total, circ, mx, burn) in enumerate(SUPPLY):
        kws_map = {
            "bitcoin-supply": '"bitcoin supply", "btc max supply", "21 million bitcoin"',
            "ethereum-supply": '"ethereum supply", "eth supply schedule", "eip-1559 burn"',
            "solana-supply": '"solana supply", "sol emission schedule", "sol staking supply"',
            "bnb-supply": '"bnb supply", "bnb burn schedule", "binance coin max supply"',
            "matic-supply": '"polygon supply", "matic max supply", "polygon token supply"',
            "avalanche-supply": '"avalanche supply", "avax supply", "avax staking supply"',
            "dogecoin-supply": '"dogecoin supply", "doge inflation rate", "unlimited dogecoin"',
            "shiba-inu-supply": '"shiba inu supply", "shib total supply", "shib burned"',
            "ripple-xrp-supply": '"xrp supply", "ripple escrow", "xrp max supply"',
            "cardano-supply": '"cardano supply", "ada total supply", "cardano max supply"',
        }
        path = os.path.join(BASE, "supply", f"{slug}.mdx")
        with open(path, "w") as f:
            f.write(SUPPLY_TEMPLATE.format(
                title=title, description=desc,
                token=token, supplyType=stype,
                total=total, circulating=circ,
                burn="true" if burn else "false",
                keywords=kws_map.get(slug, ""),
            ))
    print(f"  Written {len(SUPPLY)} supply pages")


def write_guides_v2():
    kws_map = {
        "market-cap-vs-price": '"market cap vs price", "crypto market capitalization", "why market cap matters"',
        "fully-diluted-valuation": '"fully diluted valuation", "fdv crypto", "fdv vs market cap", "what is fdv"',
        "circulating-vs-total-supply": '"circulating vs total supply", "crypto supply explained", "max supply vs total"',
        "token-emissions-schedule": '"token emissions", "crypto unlock schedule", "token emission schedule", "halving schedule"',
        "supply-shocks": '"supply shock crypto", "token burns price impact", "deflationary crypto"',
    }
    for slug, title, desc, topic, _ in GUIDES:
        path = os.path.join(BASE, "guides", f"{slug}.mdx")
        with open(path, "w") as f:
            f.write(GUIDE_TEMPLATE.format(
                title=title, description=desc,
                topic=topic,
                keywords=kws_map.get(slug, ""),
            ))
    print(f"  Written {len(GUIDES)} guide pages")


if __name__ == "__main__":
    for d in ["pairs", "supply", "guides"]:
        os.makedirs(os.path.join(BASE, d), exist_ok=True)
    write_pair()
    write_supply_v2()
    write_guides_v2()
    print("Done — 40 seed pages written.")

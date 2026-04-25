---
title: "Myers Diff Algorithm: How git diff Finds Changes"
description: "A developer-friendly explanation of the Myers diff algorithm — the O((n+m)d) approach that powers git diff, unified diffs, and most modern code review tools."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["myers diff", "algorithms", "git", "diff", "computer science"]
draft: false
---

The Myers diff algorithm is the engine behind `git diff`, GNU diff, and most online diff tools. Published by Eugene Myers in 1986, it finds the shortest edit script between two sequences — the minimum number of insertions and deletions needed to transform one into the other.

## The edit graph

Myers models the problem as a path-finding problem on an "edit graph."

Given sequences `A = [a₁, a₂, ..., aₙ]` and `B = [b₁, b₂, ..., bₘ]`, build a grid of size (n+1) × (m+1). Each point (x, y) represents the state "consumed x elements from A and y elements from B."

Three types of moves:
- **Right** (x, y) → (x+1, y): delete element `aₓ₊₁` from A. Cost: 1.
- **Down** (x, y) → (x, y+1): insert element `bᵧ₊₁` from B. Cost: 1.
- **Diagonal** (x, y) → (x+1, y+1) when `aₓ₊₁ == bᵧ₊₁`: match, no edit. Cost: 0.

A shortest path from (0,0) to (n,m) is the minimum edit script.

## The key insight: diagonals

Myers observed that all points with the same value of `k = x - y` lie on the same diagonal. A search state can be represented as a single number `k` plus the furthest point reached on that diagonal.

The algorithm works in rounds, where round `d` finds all reachable states with exactly `d` edits:

1. Start at (0, 0) with d=0.
2. For each round d, extend each reachable diagonal as far as possible using free diagonal moves (matching elements).
3. For each diagonal, try moving from d-1 rounds either right (delete) or down (insert) to reach a new diagonal.
4. Stop when (n, m) is reached.

Because the algorithm extends matching runs greedily (taking as many free diagonal steps as possible), it naturally finds long matching sequences first.

## Complexity

- **Time:** O((n + m) × d), where d is the edit distance (number of changes)
- **Space:** O(d) for the bidirectional version (O(d²) naïve)

When files are nearly identical (small d), this is extremely fast. In the worst case (completely different files), it degrades to O(n × m) — the same as classical LCS — but that's rare for typical code changes.

## A simplified implementation

Here's the core idea in Python, simplified for clarity:

```python
def myers_diff(a, b):
    n, m = len(a), len(b)
    max_d = n + m
    # v[k] = furthest x reached on diagonal k
    v = {1: 0}
    trace = []

    for d in range(max_d + 1):
        snapshot = dict(v)
        trace.append(snapshot)
        for k in range(-d, d + 1, 2):
            # Move right (delete from a) or down (insert from b)
            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                x = v.get(k + 1, 0)  # from diagonal k+1 (move down)
            else:
                x = v.get(k - 1, 0) + 1  # from diagonal k-1 (move right)
            y = x - k
            # Extend diagonal (match elements)
            while x < n and y < m and a[x] == b[y]:
                x += 1
                y += 1
            v[k] = x
            if x >= n and y >= m:
                return _backtrack(trace, a, b, n, m)
    return []

def _backtrack(trace, a, b, n, m):
    x, y = n, m
    edits = []
    for d, snapshot in reversed(list(enumerate(trace))):
        k = x - y
        if k == -d or (k != d and snapshot.get(k - 1, -1) < snapshot.get(k + 1, -1)):
            prev_k = k + 1
        else:
            prev_k = k - 1
        prev_x = snapshot.get(prev_k, 0)
        prev_y = prev_x - prev_k
        # Walk back along the diagonal
        while x > prev_x + 1 and y > prev_y + 1:
            edits.append(('equal', a[x-1], b[y-1]))
            x -= 1
            y -= 1
        if d > 0:
            if x == prev_x + 1:
                edits.append(('delete', a[x-1], None))
                x -= 1
            else:
                edits.append(('insert', None, b[y-1]))
                y -= 1
        while x > prev_x and y > prev_y:
            edits.append(('equal', a[x-1], b[y-1]))
            x -= 1
            y -= 1
    return list(reversed(edits))
```

Production implementations (like the one in Python's `difflib`) are more optimized, but the above captures the algorithm's structure.

## Why other algorithms exist

Myers has one known weakness: when a block of code is moved from one location to another, Myers reports it as a delete and an insert rather than a move. This makes moved-block diffs harder to read.

**Patience diff** (used optionally in git via `--diff-algorithm=patience`) addresses this by first matching unique lines between the two files, then recursively diffing the segments between matches. It produces more readable diffs for refactored code.

**Histogram diff** (used by JGit and optionally in git) extends patience with better handling of repeated elements. Many developers prefer it for code review:

```bash
git config --global diff.algorithm histogram
```

**Minimal diff** (`--diff-algorithm=minimal`) guarantees the true minimum edit distance but can be slower for large files.

## How this appears in practice

A unified diff produced by Myers looks like this:

```diff
@@ -1,6 +1,7 @@
 function greet(name) {
-  console.log("Hello, " + name);
+  console.log(`Hello, ${name}!`);
+  return true;
 }
 
 module.exports = { greet };
```

Lines with `-` were in the original; `+` lines are in the new version; unmarked lines are context (unchanged). The `@@` header shows which line ranges are shown.

## Tools using Myers

- GNU diff (the standard Unix `diff` command)
- git (default algorithm)
- GitHub and GitLab pull request diffs
- VS Code's built-in diff view
- Python's `difflib` module (similar, not identical)
- [textdiff.pro](/) — browser-based diff using the Myers algorithm

## Going deeper

Myers' original paper ([Software — Practice and Experience, 1986](https://link.springer.com/article/10.1007/BF01840446)) is readable and worth reviewing if you want the full mathematical treatment. The paper also covers the bidirectional (linear-space) variant.

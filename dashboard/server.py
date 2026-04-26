#!/usr/bin/env python3
"""
Site Network Dashboard — serves on 0.0.0.0:4399
  /                       → dashboard (mirrors SuperVault Sites Index)
  /preview/{domain}/...   → serves sites/{domain}/dist/ with asset-path rewriting
"""
import http.server
import socketserver
import mimetypes
import re
from pathlib import Path
from html import escape

PORT = 4399
BASE = Path(__file__).parent.parent
VAULT_INDEX = BASE / "SuperVault/Site Network/Sites/200 Sites Index.md"
SITES_DIR = BASE / "sites"

STATUS_BADGE = {
    "Live":               ("bg-emerald-100 text-emerald-800 border border-emerald-200", "Live"),
    "MVP · deploy-ready": ("bg-sky-100 text-sky-800 border border-sky-200",             "Deploy-ready"),
    "MVP · local only":   ("bg-amber-100 text-amber-800 border border-amber-200",       "Local only"),
    "⚠ test artifact":    ("bg-slate-100 text-slate-500 border border-slate-200",       "Test"),
}

# ── parser ────────────────────────────────────────────────────────────────────

def parse_sites(content):
    sites, in_table = [], False
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("| # |") or line.startswith("|---|"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                in_table = False
                continue
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) < 6:
                continue
            num, domain, tool, status = cols[0], cols[1], cols[2], cols[3]
            wrangler, ci = cols[4], cols[5]
            notes = cols[6] if len(cols) > 6 else ""
            try:
                int(num)
            except ValueError:
                continue
            status = status.strip("*").strip()
            has_preview = (SITES_DIR / domain / "dist" / "index.html").exists()
            sites.append({
                "num": num, "domain": domain, "tool": tool,
                "status": status, "wrangler": wrangler, "ci": ci,
                "notes": notes, "has_preview": has_preview,
            })
    return sites

# ── dashboard HTML ────────────────────────────────────────────────────────────

def totals(sites):
    counts = {}
    for s in sites:
        counts[s["status"]] = counts.get(s["status"], 0) + 1
    return counts


def render_row(s):
    badge_cls, badge_label = STATUS_BADGE.get(s["status"], ("bg-slate-100 text-slate-600", s["status"]))
    wdot = '<span class="inline-block w-2 h-2 rounded-full bg-emerald-400"></span>' if s["wrangler"] == "yes" else '<span class="inline-block w-2 h-2 rounded-full bg-slate-300"></span>'
    cdot = '<span class="inline-block w-2 h-2 rounded-full bg-emerald-400"></span>' if s["ci"] == "yes" else '<span class="inline-block w-2 h-2 rounded-full bg-slate-300"></span>'
    ymyl = '<span class="text-xs font-medium text-orange-600 bg-orange-50 border border-orange-200 rounded px-1.5 py-0.5 ml-1">YMYL</span>' if "YMYL" in s["notes"] else ""
    d = escape(s["domain"])
    if s["has_preview"]:
        domain_cell = f'<a href="/preview/{d}/" class="font-mono text-sm text-blue-600 hover:underline">{d}</a>'
    else:
        domain_cell = f'<span class="font-mono text-sm text-slate-500">{d}</span>'
    return f"""
    <tr class="border-b border-slate-100 hover:bg-slate-50 transition-colors">
      <td class="px-3 py-2.5 text-xs text-slate-400 text-right w-8">{escape(s['num'])}</td>
      <td class="px-3 py-2.5">{domain_cell}</td>
      <td class="px-3 py-2.5 text-sm text-slate-600 max-w-xs truncate">{escape(s['tool'])}</td>
      <td class="px-3 py-2.5">
        <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium {badge_cls}">{badge_label}</span>{ymyl}
      </td>
      <td class="px-3 py-2.5 text-center">{wdot}</td>
      <td class="px-3 py-2.5 text-center">{cdot}</td>
    </tr>"""


def render_dashboard(sites):
    counts = totals(sites)
    live_n  = counts.get("Live", 0)
    ready_n = counts.get("MVP · deploy-ready", 0)
    local_n = counts.get("MVP · local only", 0)
    total_real = live_n + ready_n + local_n
    rows = "\n".join(render_row(s) for s in sites if s["status"] != "⚠ test artifact")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Site Network Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}.truncate{{max-width:280px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}</style>
</head>
<body class="bg-slate-50 min-h-screen">
<div class="max-w-5xl mx-auto px-4 py-8">
  <div class="flex items-center justify-between mb-6">
    <div>
      <h1 class="text-2xl font-bold text-slate-900">Site Network</h1>
      <p class="text-sm text-slate-500 mt-0.5">Live mirror of SuperVault Sites Index · click a domain to preview</p>
    </div>
    <div class="text-xs text-slate-400 font-mono">{total_real} sites</div>
  </div>
  <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
    <div class="rounded-xl border border-slate-200 bg-white p-4"><div class="text-2xl font-bold text-emerald-600">{live_n}</div><div class="text-xs text-slate-500 mt-0.5">Live</div></div>
    <div class="rounded-xl border border-slate-200 bg-white p-4"><div class="text-2xl font-bold text-sky-600">{ready_n}</div><div class="text-xs text-slate-500 mt-0.5">Deploy-ready</div></div>
    <div class="rounded-xl border border-slate-200 bg-white p-4"><div class="text-2xl font-bold text-amber-600">{local_n}</div><div class="text-xs text-slate-500 mt-0.5">Local only</div></div>
    <div class="rounded-xl border border-slate-200 bg-white p-4"><div class="text-2xl font-bold text-slate-700">{total_real}</div><div class="text-xs text-slate-500 mt-0.5">Total real sites</div></div>
  </div>
  <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
    <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
      <h2 class="text-sm font-semibold text-slate-700">All Sites</h2>
      <input id="search" type="text" placeholder="Filter…"
        class="text-sm border border-slate-200 rounded-lg px-3 py-1.5 outline-none focus:ring-2 focus:ring-sky-200 w-48"
        oninput="filterTable(this.value)"/>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-left" id="siteTable">
        <thead>
          <tr class="border-b border-slate-100 bg-slate-50">
            <th class="px-3 py-2 text-xs font-medium text-slate-400 text-right">#</th>
            <th class="px-3 py-2 text-xs font-medium text-slate-500">Domain</th>
            <th class="px-3 py-2 text-xs font-medium text-slate-500">Tool / Niche</th>
            <th class="px-3 py-2 text-xs font-medium text-slate-500">Status</th>
            <th class="px-3 py-2 text-xs font-medium text-slate-500 text-center">Wrangler</th>
            <th class="px-3 py-2 text-xs font-medium text-slate-500 text-center">CI</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
  <p class="text-xs text-slate-400 mt-4 text-center">Mirrors SuperVault/Site Network/Sites/200 Sites Index.md — reload to refresh</p>
</div>
<script>
function filterTable(q){{
  q=q.toLowerCase();
  document.querySelectorAll('#siteTable tbody tr').forEach(r=>{{
    r.style.display=r.textContent.toLowerCase().includes(q)?'':'none';
  }});
}}
</script>
</body></html>"""

# ── preview file server ───────────────────────────────────────────────────────

# Rewrite root-relative asset paths inside HTML to include the /preview/{domain} prefix.
# Matches src="/...", href="/..." but NOT href="//..." (protocol-relative) or href="https://..."
# Also rewrites Astro island hydration attributes (component-url, renderer-url).
_PATH_RE = re.compile(r'((?:src|href|action|component-url|renderer-url)=")(/(?!/))'.encode())

def _rewrite_html(data: bytes, prefix: str) -> bytes:
    pfx = prefix.encode()
    return _PATH_RE.sub(lambda m: m.group(1) + pfx + m.group(2), data)


def serve_preview(handler, domain: str, rel_path: str):
    dist = SITES_DIR / domain / "dist"
    if not dist.is_dir():
        handler.send_error(404, f"No dist/ for {domain}")
        return

    # normalise path: strip leading slash, default to index.html
    rel_path = rel_path.lstrip("/") or "index.html"
    target = (dist / rel_path).resolve()

    # safety: stay inside dist/
    try:
        target.relative_to(dist.resolve())
    except ValueError:
        handler.send_error(403)
        return

    # directory → index.html
    if target.is_dir():
        target = target / "index.html"

    if not target.exists():
        # try adding .html
        target = Path(str(target) + ".html")
    if not target.exists():
        handler.send_error(404, f"Not found: {rel_path}")
        return

    data = target.read_bytes()
    mime, _ = mimetypes.guess_type(str(target))
    mime = mime or "application/octet-stream"

    if "html" in mime:
        prefix = f"/preview/{domain}"
        data = _rewrite_html(data, prefix)

    handler.send_response(200)
    handler.send_header("Content-Type", mime)
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)

# ── request handler ───────────────────────────────────────────────────────────

_PREVIEW_RE = re.compile(r"^/preview/([^/]+)(/.*)$")

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            path = self.path.split("?")[0]
            m = _PREVIEW_RE.match(path)
            if m:
                serve_preview(self, m.group(1), m.group(2))
                return

            # dashboard
            content = VAULT_INDEX.read_text(encoding="utf-8")
            sites = parse_sites(content)
            body = render_dashboard(sites).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            import traceback; traceback.print_exc()
            msg = f"Error: {e}".encode()
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(msg)

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Dashboard  → http://100.109.92.100:{PORT}/")
        print(f"Preview eg → http://100.109.92.100:{PORT}/preview/caseconvert.io/")
        httpd.serve_forever()

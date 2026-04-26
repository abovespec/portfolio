export const prerender = false;

import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ url }) => {
  const raw = url.searchParams.get('url') || '';
  if (!raw) {
    return new Response(JSON.stringify({ error: 'url parameter required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Normalize: add https:// if no protocol given
  const target = /^https?:\/\//i.test(raw) ? raw : `https://${raw}`;

  let targetUrl: URL;
  try {
    targetUrl = new URL(target);
  } catch {
    return new Response(JSON.stringify({ error: 'invalid url' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Block requests to private/internal addresses
  const hostname = targetUrl.hostname;
  if (
    hostname === 'localhost' ||
    hostname.startsWith('127.') ||
    hostname.startsWith('192.168.') ||
    hostname.startsWith('10.') ||
    hostname === '0.0.0.0'
  ) {
    return new Response(JSON.stringify({ error: 'private addresses not allowed' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const start = Date.now();
  try {
    const res = await fetch(targetUrl.toString(), {
      method: 'HEAD',
      redirect: 'follow',
      signal: AbortSignal.timeout(8000),
      headers: {
        'User-Agent': 'IsItDown.fyi/1.0 status-checker',
      },
    });

    const responseTime = Date.now() - start;
    // Any HTTP response (even 4xx/5xx) means the server is reachable.
    // We consider the site "up" if we get a response at all.
    const up = res.status < 500;

    return new Response(
      JSON.stringify({ up, statusCode: res.status, responseTime }),
      { headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } },
    );
  } catch {
    const responseTime = Date.now() - start;
    // Timeout or connection failure = down
    return new Response(
      JSON.stringify({ up: false, statusCode: null, responseTime }),
      { headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } },
    );
  }
};

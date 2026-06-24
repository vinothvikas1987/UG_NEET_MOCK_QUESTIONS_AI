// Cloudflare Worker - Email Usage Tracker
// Deploy this to Cloudflare Workers (free tier)

export default {
  async fetch(request, env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);
    const action = url.searchParams.get('action');
    const email = url.searchParams.get('email');

    if (!email || !action) {
      return new Response(JSON.stringify({ error: 'Missing email or action' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const MAX_FREE = 5;
    const key = `usage:${email}`;

    if (action === 'check') {
      const count = parseInt(await env.EMAIL_KV.get(key) || '0');
      return new Response(JSON.stringify({
        email,
        used: count,
        remaining: Math.max(0, MAX_FREE - count),
        blocked: count >= MAX_FREE
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    if (action === 'use') {
      const current = parseInt(await env.EMAIL_KV.get(key) || '0');
      if (current >= MAX_FREE) {
        return new Response(JSON.stringify({
          email,
          used: current,
          remaining: 0,
          blocked: true,
          message: 'Free limit reached. Contact vinothvikas1987@gmail.com for access.'
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }
      const newCount = current + 1;
      await env.EMAIL_KV.put(key, newCount.toString());
      return new Response(JSON.stringify({
        email,
        used: newCount,
        remaining: Math.max(0, MAX_FREE - newCount),
        blocked: newCount >= MAX_FREE
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    return new Response(JSON.stringify({ error: 'Invalid action' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  },
};

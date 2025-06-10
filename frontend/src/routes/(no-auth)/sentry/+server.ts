import type { RequestHandler } from '@sveltejs/kit';
import { ThirdPartyProxies } from '$lib/utils/thirdPartyProxies';
import { PUBLIC_SENTRY_DSN } from '$env/static/public';

/**
 * Proxy handler for Sentry error reporting.
 * Routes client-side error reports through our server to avoid CORS issues
 * and hide the Sentry DSN from the client.
 */
const sentryProxyHandler = ThirdPartyProxies.sentry(PUBLIC_SENTRY_DSN);

export const GET: RequestHandler = sentryProxyHandler;
export const POST: RequestHandler = sentryProxyHandler;
export const PATCH: RequestHandler = sentryProxyHandler;
export const PUT: RequestHandler = sentryProxyHandler;
export const DELETE: RequestHandler = sentryProxyHandler;
export const OPTIONS: RequestHandler = sentryProxyHandler;
export const HEAD: RequestHandler = sentryProxyHandler;

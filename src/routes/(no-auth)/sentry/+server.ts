import type { RequestHandler } from '@sveltejs/kit';
import { getProxyRequestHandler } from '$lib/utils/proxyUtils';
import { PUBLIC_SENTRY_DSN } from '$env/static/public';

function getSentryProxiedUrl(_url: URL, _request: Request): string {
	const dsn = new URL(PUBLIC_SENTRY_DSN);
	const projectId = dsn.pathname.replace(/^\/|\/$/g, '');
	return `https://sentry.io/api/${projectId}/envelope/`;
}

export const GET: RequestHandler = getProxyRequestHandler(getSentryProxiedUrl);
export const POST: RequestHandler = getProxyRequestHandler(getSentryProxiedUrl);
export const PATCH: RequestHandler = getProxyRequestHandler(getSentryProxiedUrl);
export const PUT: RequestHandler = getProxyRequestHandler(getSentryProxiedUrl);
export const DELETE: RequestHandler = getProxyRequestHandler(getSentryProxiedUrl);
export const OPTIONS: RequestHandler = getProxyRequestHandler(getSentryProxiedUrl);
export const HEAD: RequestHandler = getProxyRequestHandler(getSentryProxiedUrl);

import type { Handle } from '@sveltejs/kit';
import { serverInit } from '@jill64/sentry-sveltekit-cloudflare';
import { PUBLIC_BASE_API_URL, PUBLIC_SENTRY_DSN } from '$env/static/public';
import { getProxyRequestHandler } from '$lib/utils/proxyUtils';

const PROXY_PATH = '/api';

/* Create a proxy request handler using `getProxyRequestHandler` */

function getBackendProxiedUrl(url: URL, _request: Request): string {
	// Forward the request to the backend server
	const proxiedUrl = `${PUBLIC_BASE_API_URL}${url.pathname}${url.search}`;
	return proxiedUrl;
}

const backendProxyHandler = getProxyRequestHandler(getBackendProxiedUrl);

/* Wrap server-side hooks to send errors to Sentry */

const { onHandle, onError } = serverInit(PUBLIC_SENTRY_DSN);

/* Server-side hooks */

export const handle: Handle = onHandle(async ({ event, resolve }) => {
	// Intercept requests to `/api` and forwards the to the backend server
	if (event.url.pathname.startsWith(PROXY_PATH)) {
		return backendProxyHandler(event);
	}

	// Otherwise, continue with SvelteKit's default request handler
	const response = await resolve(event);
	return response;
});

export const handleError = onError();

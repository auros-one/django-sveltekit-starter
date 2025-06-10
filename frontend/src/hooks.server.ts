import type { Handle } from '@sveltejs/kit';
import { serverInit } from '@jill64/sentry-sveltekit-cloudflare';
import { PUBLIC_SENTRY_DSN } from '$env/static/public';
import { backendProxyHandler } from '$lib/utils/backendProxy';

const PROXY_PATH = '/api';

/* Wrap server-side hooks to send errors to Sentry */

const { onHandle, onError } = serverInit(PUBLIC_SENTRY_DSN);

/* Server-side hooks */

export const handle: Handle = onHandle(async ({ event, resolve }) => {
	// Intercept requests to `/api` and forward to the backend server
	if (event.url.pathname.startsWith(PROXY_PATH)) {
		// Proxy to backend with tenant information
		return backendProxyHandler(event);
	}

	// Otherwise, continue with SvelteKit's default request handler
	const response = await resolve(event);
	return response;
});

export const handleError = onError();

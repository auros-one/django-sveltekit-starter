import type { Handle } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';
import { PUBLIC_BASE_API_URL } from '$env/static/public';

const PROXY_PATH = '/api';

const handleApiProxy: Handle = async ({ event }) => {
	/**
	 * Proxy requests to the backend API.
	 *
	 * https://sami.website/blog/sveltekit-api-reverse-proxy
	 */

	const origin = event.request.headers.get('Origin');

	// reject requests that don't come from the webapp, to avoid your proxy being abused.
	//if (!origin || new URL(origin).origin !== event.url.origin) {
	//	throw error(403, 'Request Forbidden.');
	//}

	// strip `/api` from the request path
	const strippedPath = event.url.pathname.substring(PROXY_PATH.length);

	// build the new URL path with your API base URL, the stripped path and the query string
	const urlPath = `${PUBLIC_BASE_API_URL}${strippedPath}${event.url.search}`;
	const proxiedUrl = new URL(urlPath);

	// Create a new headers object with only the headers to forward
	const forwardedHeadersList = [
		'content-type',
		'authorization',
		'user-agent',
		'accept',
		'accept-encoding',
		'content-length'
	];
	const forwardedHeaders: Record<string, string> = {};
	for (const header of forwardedHeadersList) {
		if (event.request.headers.has(header)) {
			forwardedHeaders[header] = event.request.headers.get(header) || '';
		}
	}
	forwardedHeaders['host'] = proxiedUrl.hostname; // Add the correct 'host' header

	// The body is only passed if it's not empty
	const body = (await event.request.text()) || '';
	let requestData = {
		method: event.request.method,
		headers: forwardedHeaders,
		duplex: 'half' // this is required for some reason: https://github.com/nodejs/node/issues/46221
	};
	if (body) {
		requestData['body'] = body;
	}

	// make the request to the backend API
	return fetch(proxiedUrl.toString(), requestData).catch((err) => {
		// put the keys in a string:
		const keys = Object.keys(err);
		const keaysString = keys.join(', ');
		throw error(
			500,
			`error "${err} "(keys: ${keysString}) (${err?.cause?.code}) ${err?.cause?.reason}`
		);
	});
};

export const handle: Handle = async ({ event, resolve }) => {
	// intercept requests to `/api` and handle them with `handleApiProxy`
	if (event.url.pathname.startsWith(PROXY_PATH)) {
		return await handleApiProxy({ event, resolve });
	}

	// otherwise, continue with SvelteKit's default request handler
	const response = await resolve(event);
	return response;
};

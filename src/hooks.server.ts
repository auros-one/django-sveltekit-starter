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

	// reject requests that don't come from the webapp, to avoid your proxy being abused.
	// --> This is broken on localhost and untested in production
	//const origin = event.request.headers.get('Origin');
	//if (!origin || new URL(origin).origin !== event.url.origin) {
	//	throw error(403, 'Request Forbidden.');
	//}

	// strip `/api` from the request path
	const strippedPath = event.url.pathname.substring(PROXY_PATH.length);

	// build the new URL path with your API base URL, the stripped path and the query string
	const urlPath = `${PUBLIC_BASE_API_URL}${strippedPath}${event.url.search}`;
	const proxiedUrl = new URL(urlPath);

	// Forward all headers
	const forwardedHeaders: Record<string, string> = {};
	for (const [header, value] of event.request.headers) {
		forwardedHeaders[header] = value;
	}
	forwardedHeaders['host'] = proxiedUrl.host; // Add the correct 'host' header

	// The body is only passed if it's not empty
	const body = event.request.body; // get the body as a stream
	const requestData: {
		method: string;
		headers: Record<string, string>;
		duplex: string;
		body?: ReadableStream | null;
	} = {
		method: event.request.method,
		headers: forwardedHeaders,
		duplex: 'half',
		body: body
	};

	// make the request to the backend API
	return fetch(proxiedUrl.toString(), requestData).catch((err) => {
		// put the keys in a string:
		const keys = Object.keys(err);
		const keysString = keys.join(', ');
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

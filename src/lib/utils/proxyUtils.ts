import { error } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';

/**
 * Returns a RequestHandler that proxies a request to another URL.
 * The URL is determined by the required getProxiedUrl function.
 *
 * Example: a proxy to Mixpanel
 *
 * function getMixpanelProxiedUrl(url: URL, request: Request): string {
 *     // Get the destination pathname by removing the '/mixpanel' prefix
 *     const destinationPathname = url.pathname.replace('/mixpanel', '');
 *
 *     // Construct the proxy url
 *     const proxiedUrl = `https://api-js.mixpanel.com${destinationPathname}${url.search}`;
 *
 *     return proxiedUrl;
 * }
 *
 * export const GET: RequestHandler = getProxyRequestHandler(getMixpanelProxiedUrl);
 * export const POST: RequestHandler = getProxyRequestHandler(getMixpanelProxiedUrl);
 * export const PATCH: RequestHandler = getProxyRequestHandler(getMixpanelProxiedUrl);
 * export const PUT: RequestHandler = getProxyRequestHandler(getMixpanelProxiedUrl);
 * export const DELETE: RequestHandler = getProxyRequestHandler(getMixpanelProxiedUrl);
 * export const OPTIONS: RequestHandler = getProxyRequestHandler(getMixpanelProxiedUrl);
 * export const HEAD: RequestHandler = getProxyRequestHandler(getMixpanelProxiedUrl);
 *
 * @param getProxiedUrl A function that returns the URL to proxy to.
 * @returns A RequestHandler that proxies a request to another URL.
 */
export function getProxyRequestHandler(
	getProxiedUrl: (url: URL, request: Request) => string
): RequestHandler {
	const proxyRequest: RequestHandler = async ({ url, request }) => {
		const destinationUrl = getProxiedUrl(url, request);

		// Forward all headers
		const forwardedHeaders: Record<string, string> = {};
		for (const [header, value] of request.headers) {
			forwardedHeaders[header] = value;
		}
		forwardedHeaders['host'] = new URL(destinationUrl).host; // Add the correct 'host' header

		// The body is only passed if it's not empty
		const body = request.body; // get the body as a stream
		const requestData: {
			method: string;
			headers: Record<string, string>;
			duplex: string;
			body?: ReadableStream | null;
		} = {
			method: request.method,
			headers: forwardedHeaders,
			duplex: 'half',
			body: body
		};

		// make the request to the backend API
		return fetch(destinationUrl.toString(), requestData).catch((err) => {
			// put the keys in a string:
			const keys = Object.keys(err);
			const keysString = keys.join(', ');
			throw error(
				500,
				`error "${err} "(keys: ${keysString}) (${err?.cause?.code}) ${err?.cause?.reason}`
			);
		});
	};
	return proxyRequest;
}

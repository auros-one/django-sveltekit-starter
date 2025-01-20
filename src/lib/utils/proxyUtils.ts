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

		// Forward all headers except 'host'
		const forwardedHeaders: Record<string, string> = {};
		for (const [header, value] of request.headers) {
			if (header !== 'host') {
				// Don't forward the original host header
				forwardedHeaders[header] = value;
			}
		}
		forwardedHeaders['host'] = new URL(destinationUrl).host;

		const requestData = {
			method: request.method,
			headers: forwardedHeaders,
			duplex: 'half' as const,
			body: request.body,
			redirect: 'manual' as const // Add this line to handle redirects manually
		};

		return fetch(destinationUrl.toString(), requestData).catch((err) => {
			const keys = Object.keys(err);
			const keysString = keys.join(', ');
			error(
				500,
				`error "${err} "(keys: ${keysString}) (${err?.cause?.code}) ${err?.cause?.reason}`
			);
		});
	};
	return proxyRequest;
}

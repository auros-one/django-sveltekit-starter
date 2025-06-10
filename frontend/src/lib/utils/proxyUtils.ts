import { error } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';

export interface ProxyOptions {
	/**
	 * Function to determine the destination URL for the proxy request
	 */
	getDestinationUrl: (_url: URL, _request: Request) => string;

	/**
	 * Optional function to transform the request before sending
	 * Can modify headers, body, etc.
	 */
	transformRequest?: (_request: Request) => Request | Promise<Request>;

	/**
	 * Optional function to transform the response before returning
	 * Can access request context like URL and cookies
	 */
	transformResponse?: (
		_response: Response,
		_context: { url: URL; cookies: any }
	) => Response | Promise<Response>;

	/**
	 * Headers to always exclude from forwarding (in addition to 'host')
	 */
	excludeHeaders?: string[];
}

/**
 * Creates a RequestHandler that proxies requests with optional transformations.
 *
 * @param options Configuration for the proxy behavior
 * @returns A RequestHandler that proxies requests according to the options
 *
 * @example
 * ```typescript
 * // Simple proxy
 * const handler = createProxyHandler({
 *   getDestinationUrl: (url) => `https://api.example.com${url.pathname}`
 * });
 *
 * // Proxy with request transformation
 * const authHandler = createProxyHandler({
 *   getDestinationUrl: (url) => `https://api.example.com${url.pathname}`,
 *   transformRequest: (request) => {
 *     const headers = new Headers(request.headers);
 *     headers.set('Authorization', 'Bearer token');
 *     return new Request(request, { headers });
 *   }
 * });
 * ```
 */
export function createProxyHandler(options: ProxyOptions): RequestHandler {
	const { getDestinationUrl, transformRequest, transformResponse, excludeHeaders = [] } = options;

	const excludeSet = new Set(['host', ...excludeHeaders.map((h) => h.toLowerCase())]);

	return async ({ url, request, cookies }) => {
		try {
			// Apply request transformation if provided
			const transformedRequest = transformRequest ? await transformRequest(request) : request;

			// Get destination URL
			const destinationUrl = getDestinationUrl(url, transformedRequest);

			// Forward headers, excluding specified ones
			const forwardedHeaders: Record<string, string> = {};
			for (const [header, value] of transformedRequest.headers) {
				if (!excludeSet.has(header.toLowerCase())) {
					forwardedHeaders[header] = value;
				}
			}

			// Set the correct host header for the destination
			forwardedHeaders['host'] = new URL(destinationUrl).host;

			// Prepare request options
			const requestOptions = {
				method: transformedRequest.method,
				headers: forwardedHeaders,
				body: transformedRequest.body,
				duplex: 'half' as const,
				redirect: 'manual' as const
			};

			// Make the proxy request
			const response = await fetch(destinationUrl, requestOptions);

			// Apply response transformation if provided
			return transformResponse ? await transformResponse(response, { url, cookies }) : response;
		} catch (err) {
			const errorMessage = err instanceof Error ? err.message : String(err);

			error(500, `Proxy error: ${errorMessage}`);
		}
	};
}

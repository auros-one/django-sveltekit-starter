import { createProxyHandler } from './proxyUtils';
import { PUBLIC_BASE_API_URL } from '$env/static/public';
import { TENANT_DOMAIN } from '$env/static/private';

if (!TENANT_DOMAIN) {
	console.error(
		'❌ TENANT_DOMAIN environment variable is required!\n' +
			'Set it when building or running the app:\n' +
			'  TENANT_DOMAIN=demo.localhost npm run dev\n' +
			'  TENANT_DOMAIN=demo.myapp.com npm run build'
	);
	throw new Error('TENANT_DOMAIN must be set');
}

/**
 * Backend proxy handler that forwards requests to the backend API
 * with automatic tenant context injection.
 *
 * Features:
 * - Automatically adds X-Tenant-Domain header (set at build time)
 * - Forwards all requests to PUBLIC_BASE_API_URL
 * - Preserves all other headers a nd request properties
 * - Sets user cookie on successful login/signup
 */
export const backendProxyHandler = createProxyHandler({
	getDestinationUrl: (url) => {
		// Forward the request to the backend server
		return `${PUBLIC_BASE_API_URL}${url.pathname}${url.search}`;
	},

	transformRequest: (request) => {
		// Add the secure tenant header - this is set server-side
		// Users CANNOT modify this value!
		const headers = new Headers(request.headers);
		headers.set('X-Tenant-Domain', TENANT_DOMAIN);

		// Return new request with tenant header
		return new Request(request, { headers });
	},

	transformResponse: async (response, { url, cookies }) => {
		// Check if this is a successful auth-related response
		const authPaths = [
			'/api/accounts/login/',
			'/api/accounts/token/refresh/',
			'/api/accounts/user/'
		];

		if (authPaths.some((path) => url.pathname === path) && response.ok) {
			try {
				// Clone the response so we can read the body
				const clonedResponse = response.clone();
				const data = await clonedResponse.json();

				// Handle user endpoint response (returns user directly)
				if (url.pathname === '/api/accounts/user/') {
					cookies.set('user', JSON.stringify(data), {
						path: '/',
						httpOnly: true,
						secure: true,
						sameSite: 'lax',
						maxAge: 60 * 60 * 24 * 30, // 30 days
						encode: (value: string) => value // Don't URL encode the cookie
					});
				} else {
					// Set cookies based on the response data
					// Login responses include user data
					if (data.user) {
						cookies.set('user', JSON.stringify(data.user), {
							path: '/',
							httpOnly: true,
							secure: true,
							sameSite: 'lax',
							maxAge: 60 * 60 * 24 * 30, // 30 days
							encode: (value: string) => value // Don't URL encode the cookie
						});
					}

					// Login responses also include refresh token
					if (data.refresh) {
						cookies.set('refresh-token', data.refresh, {
							path: '/',
							httpOnly: true,
							secure: true,
							sameSite: 'lax',
							maxAge: 60 * 60 * 24 * 30, // 30 days
							encode: (value: string) => value // Don't URL encode the cookie
						});
					}
				}
			} catch {
				// If parsing fails, just return the original response
			}
		}

		// Handle logout - clear cookies
		if (url.pathname === '/api/accounts/logout/' && response.ok) {
			cookies.delete('user', { path: '/' });
			cookies.delete('refresh-token', { path: '/' });
		}

		return response;
	}
});

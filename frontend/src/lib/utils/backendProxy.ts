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
 * - Forwards all requests to PUBLIC_BASE_API_URL
 * - Automatically adds X-Tenant-Domain header (set at build time)
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
	}
});

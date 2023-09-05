import { error, redirect } from '@sveltejs/kit';
import { apiPath } from '$lib/api/paths';
import type { RequestHandler } from './$types';

export const GET = (async ({ cookies }) => {
	// refresh-token cookie is required
	const refreshToken = cookies.get('refresh-token');
	if (refreshToken === undefined) throw redirect(302, '/account/login');

	// get new JWT from backend
	const response = await fetch(apiPath.accounts.refresh, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include',
		body: JSON.stringify({ refresh: refreshToken })
	});

	// forward response to client
	if (response.ok) {
		const data = await response.json();
		return new Response(JSON.stringify(data));
	} else {
		const data = await response.text();
		throw error(response.status, 'Failed to refresh JWT: ' + data);
	}
}) satisfies RequestHandler;

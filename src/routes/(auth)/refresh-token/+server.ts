import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { PUBLIC_BASE_API_URL } from '$env/static/public';

export const GET = (async ({ cookies, fetch }) => {
	try {
		// refresh-token cookie is required
		const refreshToken = cookies.get('refresh-token');
		if (refreshToken === undefined) throw error(401);

		// get new JWT from backend
		const response = await fetch(PUBLIC_BASE_API_URL + '/api/accounts/token/refresh/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ refresh: refreshToken })
		});

		if (!response.ok) {
			cookies.delete('refresh-token', { path: '/' });
			throw error(401);
		}
		return response;
	} catch (err) {
		cookies.delete('refresh-token', { path: '/' });
		throw error(500, `${err}`);
	}
}) satisfies RequestHandler;

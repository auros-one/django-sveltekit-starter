import { error, redirect } from '@sveltejs/kit';
import { apiPath } from '$lib/api/paths';
import type { RequestHandler } from './$types';

export const GET = (async ({ cookies, fetch }) => {
	try {
		// refresh-token cookie is required
		const refreshToken = cookies.get('refresh-token');
		if (refreshToken === undefined) throw redirect(302, '/account/login');

		// get new JWT from backend
		const response = await fetch(apiPath.accounts.refresh, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ refresh: refreshToken })
		});

		if (response.status == 401) {
			const data = await response.json();
			// if the refresh token is invalid, delete it and redirect to login
			if (data.code == 'token_not_valid') {
				cookies.delete('refresh-token');
				throw redirect(302, '/account/login');
			}
		}
		return response;
	} catch (err) {
		throw error(500, `${err}`);
	}
}) satisfies RequestHandler;

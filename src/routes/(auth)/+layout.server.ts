/**
 * Server-side check for the refresh-token cookie.
 * If it is not present, redirect to the login page.
 */
import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import type { User } from '$lib/stores/account';

const COOKIES_TO_FORWARD = ['user'];

export const load = (async ({ cookies }) => {
	try {
		// The refresh-token cookie determines if the user is authenticated
		const refreshToken = cookies.get('refresh-token');
		if (refreshToken === undefined) {
			throw new Error('refresh-token Cookie not found');
		}

		// Parse all required cookies and return them
		const parsedCookies: Record<string, User> = {};
		COOKIES_TO_FORWARD.forEach((cookieName) => {
			const cookieValue = cookies.get(cookieName);
			parsedCookies[cookieName] = cookieValue ? JSON.parse(cookieValue) : null;
		});

		return parsedCookies as {
			user: User;
		};
	} catch (e) {
		// If anything goes wrong, clear all cookies and redirect to the login page
		COOKIES_TO_FORWARD.forEach((cookie) => cookies.delete(cookie));
		cookies.delete('refresh-token');
		throw redirect(302, '/welcome');
	}
}) satisfies LayoutServerLoad;

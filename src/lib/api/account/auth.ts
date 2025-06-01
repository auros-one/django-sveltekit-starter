import { invalidateAll } from '$app/navigation';
import { jwt } from '$lib/stores/auth';
import { user } from '$lib/stores/account';
import { apiClient } from '$lib/api';
import type { components } from '$lib/api/backend-api-schema';

export async function signup(
	email: string,
	password1: string,
	password2: string
): Promise<undefined | { [key: string]: [string] }> {
	/**
	 * Sign up a new user. Returns undefined if successful, or an error object if not.
	 */
	const { error, response } = await apiClient.POST('/accounts/signup/', {
		body: {
			email,
			password1,
			password2
		}
	});
	if (response.status.toString().startsWith('5')) {
		return { non_field_errors: ['Something went wrong on our end. Please try again later.'] };
	}
	if (error) {
		return error as { [key: string]: [string] };
	}
	return undefined;
}

export async function login(
	email: string,
	password: string
): Promise<{ [key: string]: [string] } | components['schemas']['JWT']> {
	const { data, error, response } = await apiClient.POST('/accounts/login/', {
		body: {
			email,
			password
		}
	});
	if (response.status.toString().startsWith('5')) {
		return { non_field_errors: ['Something went wrong on our end. Please try again later.'] };
	}
	if (error) {
		return error;
	}
	jwt.set(data.access);
	user.set(data.user);
	return data;
}

export async function logout() {
	await apiClient.POST('/accounts/logout/');

	// Cause all load functions belonging to the currently active page to re-run.
	// This will trigger auth protection which will redirct the user to the login page.
	invalidateAll();
}

export async function requestPasswordReset(email: string) {
	const { data, error, response } = await apiClient.POST('/accounts/password/reset/', {
		body: {
			email
		}
	});
	if (response.status.toString().startsWith('5')) {
		return { non_field_errors: ['Something went wrong on our end. Please try again later.'] };
	}
	if (error) {
		return error;
	}
	return data;
}

// JWT Refresh

export async function refresh(): Promise<{ token: string; expiration: string }> {
	const response = await fetch('/refresh-token', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include'
	});
	if (response.status === 200) {
		const data = (await response.json()) as { access: string; access_expiration: string };
		return { token: data.access, expiration: data.access_expiration };
	} else {
		throw new Error('Could not refresh JWT');
	}
}

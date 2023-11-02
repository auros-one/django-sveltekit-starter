import { apiPath } from '$lib/api/paths';
import { goto, invalidateAll } from '$app/navigation';
import { jwt } from '$lib/stores/auth';
import { user } from '$lib/stores/account';

export async function signup(email: string, password1: string, password2: string) {
	const response = await fetch(apiPath.accounts.signup, {
		method: 'POST',
		body: JSON.stringify({ email, password1, password2 }),
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include'
	});
	if (response.status.toString().startsWith('5')) {
		return { non_field_errors: ['Something went wrong on our end. Please try again later.'] };
	}
	return await response.json();
}

export async function login(email: string, password: string) {
	const response = await fetch(apiPath.accounts.login, {
		method: 'POST',
		body: JSON.stringify({ email, password }),
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include'
	});
	if (response.status.toString().startsWith('5')) {
		return { non_field_errors: ['Something went wrong on our end. Please try again later.'] };
	}
	const data = await response.json();
	if (response.ok) {
		// on success, set jwt and user
		jwt.set(data.access);
		user.set(data.user);
	}
	return data;
}

export async function logout() {
	await fetch(apiPath.accounts.logout, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include'
	});

	// Cause all load functions belonging to the currently active page to re-run.
	// This will trigger auth protection which will redirct the user to the login page.
	invalidateAll();
}

export async function requestPasswordReset(email: string) {
	const response = await fetch(apiPath.accounts.password_reset, {
		method: 'POST',
		body: JSON.stringify({ email }),
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include'
	});
	if (response.status.toString().startsWith('5')) {
		return { non_field_errors: ['Something went wrong on our end. Please try again later.'] };
	}
	const data = await response.json();
	return data;
}

export async function confirmPasswordReset(
	password1: string,
	password2: string,
	uid: string,
	token: string
): Promise<Response> {
	const response = await fetch(apiPath.accounts.password_reset_confirm, {
		method: 'POST',
		body: JSON.stringify({
			new_password1: password1,
			new_password2: password2,
			uid: uid,
			token: token
		}),
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include'
	});
	return response;
}

export async function verifyEmail(key: string) {
	const response = await fetch(apiPath.accounts.verify_email, {
		method: 'POST',
		body: JSON.stringify({ key }),
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include'
	});
	return response;
}

export async function ressendVerifyEmail(email: string) {
	const response = await fetch(apiPath.accounts.resend_email, {
		method: 'POST',
		body: JSON.stringify({ email }),
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include'
	});
	if (response.status.toString().startsWith('5')) {
		return { non_field_errors: ['Something went wrong on our end. Please try again later.'] };
	}
	const data = await response.json();
	return data;
}

// JWT Refresh

export async function refresh(): Promise<{ token: string; expiration: string }> {
	const response = await fetch('/refresh-token/', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include'
	});
	if (response.status === 200) {
		const data = await response.json();
		return { token: data.access, expiration: data.access_expiration };
	} else {
		throw new Error('Could not refresh JWT');
	}
}

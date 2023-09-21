import { apiPath } from '$lib/api/paths';
import { invalidateAll } from '$app/navigation';
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

	if (refreshTokenLoop) {
		clearInterval(refreshTokenLoop);
		refreshTokenLoop = undefined;
	}

	invalidateAll();
}

// JWT Refresh

let refreshTokenLoop: number | undefined = undefined;

export async function refresh() {
	const response = await fetch('/refresh-token/', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include'
	});
	const data = await response.json();
	if (!response.ok) {
		throw new Error(data.error);
	} else {
		return { token: data.access, expiration: data.access_expiration };
	}
}

export async function initJWTRefreshLoop() {
	const { token, expiration } = await refresh();
	jwt.set(token);

	// start loop to refresh jwt
	const expirationDate = new Date(expiration);
	const refreshRateMS = expirationDate.valueOf() - Date.now() - 5000;

	// stop existing loop if it exists
	if (typeof refreshTokenLoop === 'number') clearInterval(refreshTokenLoop);

	// start new loop
	refreshTokenLoop = setInterval(async () => {
		const updatedTokenInfo = await refresh();
		jwt.set(updatedTokenInfo.token);
	}, refreshRateMS);
}

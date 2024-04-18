import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export function persisted<T>(key: string, initial: T | null): ReturnType<typeof writable<T>> {
	const json = getCookie(key);
	const initialValue = json ? JSON.parse(json) : initial;
	const store = writable<T>(initialValue);

	store.subscribe((value: T | null) => {
		setCookie<T>(key, value);
	});

	return store;
}

function getCookie(key: string): string | undefined {
	if (browser) {
		return document.cookie
			.split('; ')
			.find((row) => row.startsWith(`${key}=`))
			?.split('=')[1];
	}
}

function setCookie<T>(key: string, value: T | null): void {
	if (browser) {
		if (value === null) {
			// Set the cookie to expire in the past, effectively deleting it
			document.cookie = `${key}=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Strict; Secure; Path=/`;
		} else {
			const json = JSON.stringify(value);
			const expires = new Date();
			expires.setFullYear(expires.getFullYear() + 1);
			document.cookie = `${key}=${json}; Expires=${expires.toString()}; SameSite=Strict; Secure; Path=/`;
		}
	}
}

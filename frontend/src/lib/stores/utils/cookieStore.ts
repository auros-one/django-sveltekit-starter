import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import Cookies from 'js-cookie';

export function persisted<T>(key: string, initial: T | null): ReturnType<typeof writable<T>> {
	const json = Cookies.get(key);
	const initialValue = json ? JSON.parse(json) : initial;
	const store = writable<T>(initialValue);

	store.subscribe((value: T | null) => {
		setCookie<T>(key, value);
	});

	return store;
}

function setCookie<T>(key: string, value: T | null): void {
	if (browser) {
		if (value === null) {
			Cookies.remove(key);
		} else {
			const json = JSON.stringify(value);
			Cookies.set(key, json, { expires: 365 });
		}
	}
}

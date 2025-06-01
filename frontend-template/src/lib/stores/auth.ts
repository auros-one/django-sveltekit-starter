import { writable } from 'svelte/store';
import { waitForStore } from '$lib/stores/utils/waitForStore';

export const jwt = writable<string | undefined>(undefined);

/**
 * Waits for a JWT token to become available in the Svelte store and returns it.
 * If the token is not available within the specified timeout period, the function rejects with an error.
 */
export async function waitForJWT(timeout: number = 10000): Promise<string> {
	return waitForStore(jwt, timeout);
}

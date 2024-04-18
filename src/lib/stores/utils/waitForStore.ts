import { get, type Readable } from 'svelte/store';

/**
 * Waits for a store's value to become available (non-undefined) and returns it.
 * If the value is not available within the specified timeout period, the function rejects with an error.
 *
 * @param {Readable<T>} store - The Svelte store to wait for a value from.
 * @param {number} [timeout=10000] - The maximum amount of time (in milliseconds) to wait for the store's value.
 * @returns {Promise<T>} A promise that resolves with the store's value if it becomes available before the timeout,
 *                       otherwise it rejects with an error.
 *
 * @example
 * // Usage example
 * waitForStore(jwt)
 *   .then(token => console.log('Token:', token))
 *   .catch(error => console.error('Error:', error));
 */
export async function waitForStore<T>(
	store: Readable<T | undefined>,
	timeout: number = 10000
): Promise<T> {
	return new Promise((resolve, reject) => {
		// Check if the store's value is available
		let currentValue = get(store);
		if (currentValue !== undefined) {
			resolve(currentValue);
			return;
		}

		// If not available, set up a timeout
		const timeoutId = setTimeout(() => {
			currentValue = get(store);
			if (currentValue !== undefined) {
				resolve(currentValue);
			} else {
				reject(new Error('Store value is not available within the specified timeout.'));
			}
		}, timeout);

		// Setup a subscription to the store
		const unsubscribe = store.subscribe((value) => {
			if (value !== undefined) {
				clearTimeout(timeoutId);
				unsubscribe();
				resolve(value);
			}
		});
	});
}

import { jwt } from '$lib/stores/auth';
import { refresh } from '$lib/api/account/auth';

interface JWTRefreshOptions {
	onRefreshError?: () => void;
}

/**
 * Initializes a JWT refresh loop that automatically refreshes the token before it expires.
 * The refresh happens 5 seconds before the token's expiration time.
 *
 * @param options Configuration options for the refresh loop
 * @returns A function to stop the refresh loop
 */
export async function initJWTRefreshLoop(options: JWTRefreshOptions = {}) {
	const { onRefreshError } = options;

	// Initial refresh
	const result = await refresh();
	jwt.set(result.token);

	const expirationDate = new Date(result.expiration);
	const refreshRateMS = expirationDate.valueOf() - Date.now() - 5000;

	const refreshTokenLoop = setInterval(async () => {
		try {
			const updatedTokenInfo = await refresh();
			jwt.set(updatedTokenInfo.token);
		} catch {
			if (onRefreshError) {
				onRefreshError();
			}
			clearInterval(refreshTokenLoop);
		}
	}, refreshRateMS);

	// Return a cleanup function
	return () => {
		clearInterval(refreshTokenLoop);
	};
}

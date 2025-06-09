<script lang="ts">
	import { getUser } from '$lib/api/account/user';
	import { onMount, onDestroy } from 'svelte';
	import { user } from '$lib/stores/account';
	import { jwt } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { refresh } from '$lib/api/account/auth';
	import { page } from '$app/stores';

	/**
	 * AuthProvider component handles all authentication logic including:
	 * - JWT refresh loop
	 * - User state management
	 * - Redirects to login when auth fails
	 */

	export let data: { user: any };
	export let isLoading: boolean = true;

	$user = data.user;

	let refreshTokenLoop: ReturnType<typeof setInterval> | undefined = undefined;

	function redirectToLogin() {
		const currentPath = encodeURIComponent($page.url.pathname + $page.url.search);
		goto(`/account/sign-in?next=${currentPath}`);
	}

	async function initJWTRefreshLoop() {
		const result = await refresh();
		$jwt = result.token;

		const expirationDate = new Date(result.expiration);
		const refreshRateMS = expirationDate.valueOf() - Date.now() - 5000;

		refreshTokenLoop = setInterval(async () => {
			try {
				const updatedTokenInfo = await refresh();
				$jwt = updatedTokenInfo.token;
			} catch {
				redirectToLogin();
				clearInterval(refreshTokenLoop);
			}
		}, refreshRateMS);
	}

	onMount(async () => {
		try {
			await initJWTRefreshLoop();
			await getUser();
			isLoading = false;
		} catch {
			redirectToLogin();
		}
	});

	onDestroy(() => {
		if (typeof refreshTokenLoop === 'number') clearInterval(refreshTokenLoop);
	});
</script>

<!-- AuthProvider doesn't render anything, it just handles auth logic -->
<slot />

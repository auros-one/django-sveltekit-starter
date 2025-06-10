<script lang="ts">
	console.log('AuthProvider', new Date().toISOString());
	import { getUser } from '$lib/api/account/user';
	import { onMount, onDestroy } from 'svelte';
	import { user } from '$lib/stores/account';
	import { goto } from '$app/navigation';
	import { initJWTRefreshLoop } from '$lib/utils/jwt';
	import { page } from '$app/stores';

	/**
	 * AuthProvider component handles all authentication logic including:
	 * - JWT refresh loop
	 * - User state management
	 * - Redirects to login when auth fails
	 */

	export let data: { user: any };
	export let isLoading: boolean = true;

	// Set the initial user from server-side data
	if (data.user) {
		$user = data.user;
		// If we have valid user data from server, we're not loading
		isLoading = false;
	}

	let stopRefreshLoop: (() => void) | undefined = undefined;

	function redirectToLogin() {
		const currentPath = encodeURIComponent($page.url.pathname + $page.url.search);
		goto(`/account/sign-in?next=${currentPath}`);
	}

	onMount(async () => {
		try {
			stopRefreshLoop = await initJWTRefreshLoop({
				onRefreshError: redirectToLogin
			});
			await getUser();
			isLoading = false;
		} catch {
			redirectToLogin();
		}
	});

	onDestroy(() => {
		if (stopRefreshLoop) {
			stopRefreshLoop();
		}
	});
</script>

<!-- AuthProvider doesn't render anything, it just handles auth logic -->
<slot />

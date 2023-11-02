<script lang="ts">
	import { getUser } from '$lib/api/account/user';
	import { onMount, onDestroy } from 'svelte';
	import { user } from '$lib/stores/account';
	import { jwt } from '$lib/stores/auth';
	import Spinner from '$lib/components/loading/Spinner.svelte';
	import colors from 'tailwindcss/colors';
	import { goto } from '$app/navigation';
	import { refresh } from '$lib/api/account/auth';

	/**
	 * This is a layout component that is used to wrap all authenticated routes.
	 *
	 * The 'onMount' of this component starts the JWT refresh loop, which will
	 * refresh the JWT token when it is about to expire. If anything goes wrong
     * during the refresh loop, the user is redirected to the login page.
	 */

	let refreshTokenLoop: number | undefined = undefined;

	function handleJWTError(_: any) {
		goto('/account/login');
	}

	async function initJWTRefreshLoop() {
		const result = await refresh();
		jwt.set(result.token);

		const expirationDate = new Date(result.expiration);
		const refreshRateMS = expirationDate.valueOf() - Date.now() - 5000;

		refreshTokenLoop = setInterval(async () => {
			try {
				const updatedTokenInfo = await refresh();
				jwt.set(updatedTokenInfo.token);
			} catch (e) {
				handleJWTError(e);
				clearInterval(refreshTokenLoop); // Clear the interval if an error occurs
			}
		}, refreshRateMS);
	}

	onMount(async () => {
		try {
			await initJWTRefreshLoop();
			getUser();
		} catch (e) {
			handleJWTError(e);
		}
	});

	onDestroy(() => {
		// Clear the interval when the component is destroyed
		if (typeof refreshTokenLoop === 'number') clearInterval(refreshTokenLoop);
	});
</script>

{#if $jwt && $user}
	<slot />
{:else}
	<div class="flex h-[95%] flex-col items-center justify-center">
		<Spinner size={50} color={colors.slate[600]} />
	</div>
{/if}

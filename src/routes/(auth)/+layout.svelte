<script>
	import { getUser } from '$lib/api/account/user';
	import { onMount } from 'svelte';
	import { initJWTRefreshLoop } from '$lib/api/account/auth';
	import { user } from '$lib/stores/account';
	import { jwt } from '$lib/stores/auth';
	import Spinner from '$lib/components/loading/Spinner.svelte';
	import colors from 'tailwindcss/colors';
	onMount(async () => {
		await initJWTRefreshLoop();
		getUser(); // TODO: might want to include user data in the refresh response instead of making a separate request
	});
</script>

{#if $jwt && $user}
	<slot />
{:else}
	<div class="flex h-[95%] flex-col items-center justify-center">
		<Spinner size={50} color={colors.slate[600]} />
	</div>
{/if}

<script lang="ts">
	import { ressendVerifyEmail } from '$lib/api/account/auth';
	import { user } from '$lib/stores/account';
	import Spinner from './loading/Spinner.svelte';

	let loading: boolean = false;
	let sent: boolean = false;

	async function onSendVerificationEmail() {
		if (!$user) return;
		loading = true;
		const res = await ressendVerifyEmail($user.email);
		if (res) sent = true;
		loading = false;
	}
</script>

<button
	on:click={onSendVerificationEmail}
	class="flex justify-center rounded-md bg-primary-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
>
	{#if loading}
		<Spinner color="#FFFFFF" size={20} ringThickness={2} />
	{:else if sent}
		Sent! Check your email
	{:else}
		Send new verification email
	{/if}
</button>

<script lang="ts">
	import { ressendVerifyEmail } from '$lib/api/account/auth';
	import { user } from '$lib/stores/account';
	import Button from './Button.svelte';
	let sent: boolean = false;

	async function onSendVerificationEmail() {
		if (!$user) return;
		const res = await ressendVerifyEmail($user.email);
		if (res) sent = true;
	}
</script>

<Button on:click={onSendVerificationEmail} disabled={sent}>
	{#if sent}
		Sent! Check your email
	{:else}
		Send new verification email
	{/if}
</Button>

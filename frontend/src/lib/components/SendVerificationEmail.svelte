<script lang="ts">
	import { apiClient } from '$lib/api';
	import { user } from '$lib/stores/account';
	import Button from './Button.svelte';
	let sent: boolean = false;
	let error: string | null = null;

	async function onSendVerificationEmail() {
		error = null;
		const { response } = await apiClient.POST('/accounts/resend-email/', {
			body: {
				email: $user.email
			}
		});
		if (response.status.toString().startsWith('2')) {
			sent = true;
		} else if (response.status.toString().startsWith('5')) {
			error = 'Something went wrong on our end. Please try again later.';
		} else {
			error = 'Something went wrong. Please try again later.';
		}
	}
</script>

<div class="w-full rounded-lg bg-white px-6 py-4 shadow-sm">
	<div class="flex flex-row items-center gap-2">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			stroke-width="1.5"
			stroke="currentColor"
			class="h-6 w-6 text-blue-500"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75"
			/>
		</svg>

		<h3 class="mb-[3px] text-lg font-semibold leading-7 text-gray-900">Email Verification</h3>
	</div>

	<div class="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
		<div class="flex-1">
			<p class="text-sm text-gray-600">
				Ensure your account is secure by verifying your email address. Can't find the email? Check
				your spam folder.
			</p>
			{#if error}
				<p class="mt-2 text-sm text-red-600">{error}</p>
			{/if}
		</div>

		<Button on:click={onSendVerificationEmail} disabled={sent} class="whitespace-nowrap">
			{#if sent}
				✓ Sent! Check your email
			{:else}
				Send verification email
			{/if}
		</Button>
	</div>
</div>

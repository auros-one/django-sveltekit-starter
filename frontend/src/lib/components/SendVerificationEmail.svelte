<script lang="ts">
	import { apiClient } from '$lib/api';
	import { user } from '$lib/stores/account';
	import Button from './Button.svelte';
	let sent: boolean = false;
	let error: string | null = null;

	async function onSendVerificationEmail() {
		error = null;
		const { response } = await apiClient.POST('/accounts/signup/resend-email/', {
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

<div class="w-full rounded-lg bg-white px-6 py-4">
	<div class="flex flex-row items-center gap-2">
		{#if $user.verified}
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				class="h-6 w-6"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
				/>
			</svg>
		{:else}
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				class="h-6 w-6"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z"
				/>
			</svg>
		{/if}

		<h3 class="mb-[3px] text-lg font-semibold leading-7 text-gray-900">
			{#if $user.verified}Your Email Is Verified{:else}Verify Your Email{/if}
		</h3>
	</div>

	<div class="flex flex-row items-center justify-between">
		{#if $user.verified}
			<p class="mb">Your email is verified. Verification helps keep your account secure.</p>
		{:else}
			<p class="mb">
				Can't find the email? Check your spam folder or resend the verification email.
			</p>

			<Button on:click={onSendVerificationEmail} disabled={sent}>
				{#if sent}
					Sent! Check your email
				{:else}
					Send new verification email
				{/if}
			</Button>

			{#if error}
				<p class="mt-2 text-red-600">{error}</p>
			{/if}
		{/if}
	</div>
</div>

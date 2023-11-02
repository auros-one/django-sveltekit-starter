<script lang="ts">
	import { page } from '$app/stores';

	import { verifyEmail } from '$lib/api/account/auth';
	import Spinner from '$lib/components/loading/Spinner.svelte';
	import { onMount } from 'svelte';

	let key: string | null = $page.data.key;

	let loading: boolean = true;
	let success: boolean = false;
	let error: string | undefined;

	if (key === null) {
		error = 'Invalid url. Please try again.';
	}

	async function onVerifyEmail() {
		if (key === null) return;
		loading = true;

		const response = await verifyEmail(key);

		if (response.status.toString().startsWith('2')) {
			success = true;
		} else if (response.status.toString().startsWith('4')) {
			error = 'Invalid url. Please try again.';
		} else {
			error = 'Something went wrong. Please try again later.';
		}

		loading = false;
	}

	onMount(onVerifyEmail);
</script>

<div class="flex min-h-full flex-col items-center justify-center px-6 py-12 lg:px-8">
	{#if loading}
		<div class="flex max-w-xs flex-col items-center text-center text-gray-500">
			<Spinner />
			<p class="font-sm mt-4 text-gray-600">Verifying email...</p>
		</div>
	{:else if success}
		<div class="flex max-w-xs flex-col items-center text-center text-gray-500">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				class="mx-auto h-12 w-auto text-green-500"
			>
				<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
			</svg>

			<p class="font-sm text-gray-800">Email verified</p>
			<a
				class="text-md mt-5 font-semibold leading-6 text-primary-600 hover:text-primary-500"
				href="/account/login">Log in</a
			>
		</div>
	{:else}
		<div class="flex max-w-xs flex-col items-center text-center text-gray-500">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				class="mx-auto h-12 w-auto text-red-500"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
				/>
			</svg>

			<p class="font-sm text-gray-800">
				{error ? error : 'Something went wrong, please try again'}
			</p>
			<a
				class="text-md mt-5 font-semibold leading-6 text-primary-600 hover:text-primary-500"
				href="/account/login">Log in</a
			>
		</div>
	{/if}
</div>

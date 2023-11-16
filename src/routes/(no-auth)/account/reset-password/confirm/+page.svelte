<script lang="ts">
	import { page } from '$app/stores';
	import { confirmPasswordReset } from '$lib/api/account/auth';
	import Button from '$lib/components/Button.svelte';
	import Spinner from '$lib/components/loading/Spinner.svelte';

	let token: string | null = $page.data.token;
	let uid: string | null = $page.data.uid;

	let loading: boolean = false;
	let success: boolean = false;
	let error: string | undefined;

	if (token === null || uid === null) {
		error = 'Invalid url. Please try again.';
	}

	async function onUpdatePassword(e: Event) {
		if (token === null || uid === null) return;
		loading = true;
		const formData = Object.fromEntries(new FormData(e.target as HTMLFormElement));
		const response = await confirmPasswordReset(
			formData.password1 as string,
			formData.password2 as string,
			uid,
			token
		);
		if (response.status.toString().startsWith('2')) {
			success = true;
		} else if (response.status.toString().startsWith('4')) {
			error = 'Invalid url. Please try again.';
		} else {
			error = 'Something went wrong. Please try again later.';
		}
		loading = false;
	}
</script>

<div class="flex min-h-full flex-col items-center justify-center px-6 py-12 lg:px-8">
	{#if error}
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

			<p class="font-sm text-gray-800">{error}</p>
			<p class="text-md mt-5">
				Forgot your password?<br /><a
					class="font-semibold leading-6 text-primary-600 hover:text-primary-500"
					href="/account/reset-password">Click here</a
				> to reset your password.
			</p>
		</div>
	{:else if loading}
		<div class="flex max-w-xs flex-col items-center text-center text-gray-500">
			<Spinner />
			<p class="font-sm mt-4 text-gray-600">Updating password...</p>
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

			<p class="font-sm text-gray-800">Password updated</p>
			<p class="text-md mt-5">
				You can now <a
					class="font-semibold leading-6 text-primary-600 hover:text-primary-500"
					href="/account/login">log in</a
				> with your new password.
			</p>
		</div>
	{:else}
		<div class="sm:mx-auto sm:w-full sm:max-w-sm">
			<a href="/welcome"
				><img class="mx-auto h-10 w-auto" src="/favicon.png" alt="Company logo" /></a
			>
			<h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
				Reset your password
			</h2>
		</div>

		<div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
			<form class="space-y-6" method="POST" on:submit|preventDefault={onUpdatePassword}>
				<div>
					<div class="flex items-center justify-between">
						<label for="password1" class="block text-sm font-medium leading-6 text-gray-900"
							>Password</label
						>
					</div>
					<div class="mt-2">
						<input
							id="password1"
							name="password1"
							type="password"
							autocomplete="new-password"
							required
							class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
						/>
					</div>
				</div>

				<div>
					<div class="flex items-center justify-between">
						<label for="password2" class="block text-sm font-medium leading-6 text-gray-900"
							>Repeat Password</label
						>
					</div>
					<div class="mt-2">
						<input
							id="password2"
							name="password2"
							type="password"
							autocomplete="new-password"
							required
							class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
						/>
					</div>
				</div>

				<div>
					<Button bind:loading type="submit" class="w-full">Update password</Button>
				</div>
			</form>

			<p class="mt-10 text-center text-sm text-gray-500">
				Not a member?
				<a
					href="/account/sign-up"
					class="font-semibold leading-6 text-primary-600 hover:text-primary-500">Sign up</a
				>
			</p>
		</div>
	{/if}
</div>

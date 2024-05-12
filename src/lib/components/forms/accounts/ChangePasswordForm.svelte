<script lang="ts">
	import { apiClient } from '$lib/api/index';
	import Button from '$lib/components/Button.svelte';
	import { waitForJWT } from '$lib/stores/auth';

	let loading: boolean = false;
	let errorPasswordChange: string | undefined = undefined;
	let messagePasswordChange: string | undefined = undefined;
	async function onChangePassword(e: Event) {
		errorPasswordChange = undefined;
		messagePasswordChange = undefined;
		loading = true;

		const formData = Object.fromEntries(new FormData(e.target as HTMLFormElement));
		let old_password = formData.password as string;
		let new_password = formData['new-password'] as string;
		let response = await apiClient.POST('/accounts/password/change/', {
			body: {
				old_password: old_password,
				new_password1: new_password,
				new_password2: new_password
			},
			headers: {
				'Content-Type': 'application/json',
				Authorization: 'Bearer ' + (await waitForJWT())
			},
			credentials: 'include'
		});

		if (response.error) {
			// response.error is a key-value json of errors. Turn it into 1 long string: "<error 1>. <error 2>."
			// eslint-disable-next-line @typescript-eslint/ban-ts-comment
			// @ts-ignore
			errorPasswordChange = Object.values(response.error).join('. ');
		} else {
			messagePasswordChange = 'Password changed successfully.';
		}
		loading = false;
	}
</script>

<form class="w-[440px] rounded-lg bg-white px-6 py-4" on:submit|preventDefault={onChangePassword}>
	<h2 class="mb-6 text-lg font-semibold leading-7 text-gray-900">Update Password</h2>

	<label for="password" class="block text-sm font-medium leading-6 text-gray-700"
		>Current Password</label
	>
	<div class="mb-4 mt-2">
		<input
			id="password"
			name="password"
			type="password"
			autocomplete="current-password"
			required
			disabled={loading}
			class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
		/>
	</div>
	<label for="email" class="block text-sm font-medium leading-6 text-gray-700">New Password</label>
	<div class="mb-8 mt-2">
		<input
			id="new-password"
			name="new-password"
			type="password"
			autocomplete="new-password"
			required
			disabled={loading}
			class="mb-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
		/>
		{#if errorPasswordChange}
			<p class="text-sm text-red-500">{errorPasswordChange}</p>
		{:else if messagePasswordChange}
			<p class="text-sm text-green-500">{messagePasswordChange}</p>
		{/if}
	</div>
	<div class="flex items-center justify-between">
		<a
			href="/account/reset-password"
			target="_blank"
			class="text-sm font-semibold leading-6 text-primary-600 hover:text-primary-500"
			>Forgot your password?</a
		>
		<Button bind:loading type="submit" class="w-auto">Save</Button>
	</div>
</form>

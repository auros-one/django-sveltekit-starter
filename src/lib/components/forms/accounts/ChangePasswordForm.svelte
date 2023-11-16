<script lang="ts">
	import { apiClient } from '$lib/api/index';
	import { jwt } from '$lib/stores/auth';
	import Button from '$lib/components/Button.svelte';

	let loading: boolean = false;
	let errorPasswordChange: string | undefined = undefined;
	let messagePasswordChange: string | undefined = undefined;
	async function onChangePassword(e: Event) {
		errorPasswordChange = undefined;
		messagePasswordChange = undefined;
		if (jwt === undefined) throw new Error('No jwt token');
		loading = true;

		const formData = Object.fromEntries(new FormData(e.target as HTMLFormElement));
		let old_password = formData.password as string;
		let new_password = formData['new-password'] as string;
		let reponse = await apiClient.POST('/accounts/password/change/', {
			body: {
				old_password: old_password,
				new_password1: new_password,
				new_password2: new_password
			},
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${$jwt}`
			},
			credentials: 'include'
		});

		if (reponse.error) {
			// reponse.error is a key-value json of errors. Turn it into 1 long string: "<error 1>. <error 2>."
			// eslint-disable-next-line @typescript-eslint/ban-ts-comment
			// @ts-ignore
			errorPasswordChange = Object.values(reponse.error).join('. ');
		} else {
			messagePasswordChange = 'Password changed successfully.';
		}
		loading = false;
	}
</script>

<form class="w-80" on:submit|preventDefault={onChangePassword}>
	<h3 class="mb-2 text-base font-semibold leading-7 text-gray-900">Change Password</h3>
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
	<div class="mb-2 mt-2">
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
	<Button bind:loading type="submit">Update Password</Button>
</form>

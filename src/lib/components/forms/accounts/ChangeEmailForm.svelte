<script lang="ts">
	import { apiClient } from '$lib/api/index';
	import { jwt } from '$lib/stores/auth';
	import Button from '$lib/components/Button.svelte';

	let loading: boolean = false;
	let error: string | undefined = undefined;
	let success: boolean = false;
	async function onChangeEmail(e: Event) {
		error = undefined;
		success = false;
		if ($jwt === undefined) throw new Error('No jwt token');
		loading = true;

		const formData = Object.fromEntries(new FormData(e.target as HTMLFormElement));
		let reponse = await apiClient.POST('/accounts/change-email/', {
			body: {
				new_email: formData.new_email as string,
				password: formData.password as string
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
			error = Object.values(reponse.error).join('. ');
		} else {
			success = true;
		}
		loading = false;
	}
</script>

<form class="w-80" on:submit|preventDefault={onChangeEmail}>
	<h3 class="mb-2 text-base font-semibold leading-7 text-gray-900">Change Email</h3>
	<label for="new_email" class="block text-sm font-medium leading-6 text-gray-700">New Email</label>
	<div class="mb-4 mt-2">
		<input
			id="new_email"
			name="new_email"
			type="email"
			autocomplete="email"
			required
			disabled={loading}
			class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
		/>
	</div>
	<label for="email" class="block text-sm font-medium leading-6 text-gray-700">Password</label>
	<div class="mb-2 mt-2">
		<input
			id="password"
			name="password"
			type="password"
			autocomplete="current-password"
			required
			disabled={loading}
			class="mb-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
		/>
		{#if error}
			<p class="text-sm text-red-500">{error}</p>
		{:else if success}
			<p class="text-sm text-green-500">Email changed successfully.</p>
		{/if}
	</div>
	<Button type="submit" bind:loading>Update Email</Button>
</form>

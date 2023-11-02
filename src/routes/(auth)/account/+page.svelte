<script>
	import { logout } from '$lib/api/account/auth';
	import SendVerificationEmail from '$lib/components/SendVerificationEmail.svelte';
	import ChangeEmailForm from '$lib/components/forms/accounts/ChangeEmailForm.svelte';
	import ChangePasswordForm from '$lib/components/forms/accounts/ChangePasswordForm.svelte';
	import { user } from '$lib/stores/account';
</script>

<div class="flex h-full flex-col items-center justify-center gap-4">
	<h1 class="my-4 text-2xl font-bold">Account</h1>

	{#if $user}
		<table class="mx-auto divide-y divide-gray-200 border border-gray-200">
			<thead class="bg-gray-50">
				<tr>
					<th
						colspan="2"
						class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-800"
						>User Details</th
					>
				</tr>
			</thead>
			<tbody class="divide-y divide-gray-200 bg-white">
				{#each Object.entries($user) as [key, value]}
					<tr>
						<td class="whitespace-nowrap px-4 py-3"
							><pre class="w-min rounded-md bg-gray-200 px-2 py-0.5 text-sm">{key}</pre></td
						>
						<td class="whitespace-nowrap px-6 py-4"
							>{Array.isArray(value) ? value.join(', ') : JSON.stringify(value)}</td
						>
					</tr>
				{/each}
			</tbody>
		</table>
	{/if}
	{#if !$user?.verified}
		<SendVerificationEmail />
	{/if}
	<ChangePasswordForm />
	<ChangeEmailForm />
	<button
		on:click={logout}
		class="flex justify-center rounded-md bg-red-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
		>Log out</button
	>
</div>

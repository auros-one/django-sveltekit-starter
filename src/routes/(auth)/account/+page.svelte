<script>
	import { logout } from '$lib/api/account/auth';
	import Button from '$lib/components/Button.svelte';
	import SendVerificationEmail from '$lib/components/SendVerificationEmail.svelte';
	import ChangeEmailForm from '$lib/components/forms/accounts/ChangeEmailForm.svelte';
	import ChangePasswordForm from '$lib/components/forms/accounts/ChangePasswordForm.svelte';
	import { user } from '$lib/stores/account';
</script>

<div class="flex flex-col items-center justify-center gap-12 p-8">
	<p class="text-2xl font-bold">{$user?.email}</p>
	<div class="flex w-min flex-col items-center gap-8">
		<SendVerificationEmail />
		<div class="flew-row flex gap-4">
			<ChangeEmailForm />
			<ChangePasswordForm />
		</div>
		<Button class="bg-red-600 px-8 hover:bg-red-500" on:click={logout}>Log out</Button>
	</div>
</div>

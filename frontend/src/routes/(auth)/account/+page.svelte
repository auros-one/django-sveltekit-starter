<script>
	import { logout } from '$lib/api/account/auth';
	import Button from '$lib/components/Button.svelte';
	import SendVerificationEmail from '$lib/components/SendVerificationEmail.svelte';
	import ChangeEmailForm from '$lib/components/forms/accounts/ChangeEmailForm.svelte';
	import ChangePasswordForm from '$lib/components/forms/accounts/ChangePasswordForm.svelte';
	import { user } from '$lib/stores/account';

	let showEmailForm = false;
	let showPasswordForm = false;
</script>

<div class="min-h-screen bg-gray-50 py-8">
	<div class="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
		<!-- Page Header -->
		<div class="mb-8 text-center">
			<h1 class="text-3xl font-bold text-gray-900">Account Settings</h1>
			<div class="mt-3 flex items-center justify-center gap-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="h-5 w-5 text-gray-500"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75"
					/>
				</svg>
				<p class="text-lg text-gray-600">{$user?.email}</p>
			</div>
		</div>

		<!-- Main Content -->
		<div class="space-y-8">
			<!-- Email Verification Section -->
			<div class="flex justify-center">
				<div class="w-full max-w-2xl">
					<SendVerificationEmail />
				</div>
			</div>

			<!-- Account Management Forms -->
			<div class="mx-auto max-w-2xl space-y-4">
				<!-- Change Email Section -->
				<div
					class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm transition-all duration-300"
				>
					<button
						on:click={() => (showEmailForm = !showEmailForm)}
						class="flex w-full items-center justify-between p-6 text-left hover:bg-gray-50 focus:bg-gray-50 focus:outline-none"
					>
						<div class="flex items-center gap-4">
							<div class="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke-width="1.5"
									stroke="currentColor"
									class="h-6 w-6 text-blue-600"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75"
									/>
								</svg>
							</div>
							<div>
								<h3 class="text-lg font-semibold text-gray-900">Update Email Address</h3>
								<p class="mt-1 text-sm text-gray-500">
									Change the email address associated with your account
								</p>
							</div>
						</div>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="h-5 w-5 text-gray-400 transition-transform duration-300 {showEmailForm
								? 'rotate-180'
								: ''}"
						>
							<path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
						</svg>
					</button>
					{#if showEmailForm}
						<div class="border-t border-gray-200 p-6">
							<ChangeEmailForm />
						</div>
					{/if}
				</div>

				<!-- Change Password Section -->
				<div
					class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm transition-all duration-300"
				>
					<button
						on:click={() => (showPasswordForm = !showPasswordForm)}
						class="flex w-full items-center justify-between p-6 text-left hover:bg-gray-50 focus:bg-gray-50 focus:outline-none"
					>
						<div class="flex items-center gap-4">
							<div class="flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke-width="1.5"
									stroke="currentColor"
									class="h-6 w-6 text-green-600"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M15.75 5.25a3 3 0 0 1 3 3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1 1 21.75 8.25Z"
									/>
								</svg>
							</div>
							<div>
								<h3 class="text-lg font-semibold text-gray-900">Update Password</h3>
								<p class="mt-1 text-sm text-gray-500">
									Change your account password for enhanced security
								</p>
							</div>
						</div>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="h-5 w-5 text-gray-400 transition-transform duration-300 {showPasswordForm
								? 'rotate-180'
								: ''}"
						>
							<path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
						</svg>
					</button>
					{#if showPasswordForm}
						<div class="border-t border-gray-200 p-6">
							<ChangePasswordForm />
						</div>
					{/if}
				</div>
			</div>

			<!-- Logout Section -->
			<div class="border-t border-gray-200 pt-8">
				<div class="flex justify-center">
					<div class="rounded-lg bg-white p-6 shadow-sm">
						<h3 class="mb-3 text-lg font-semibold text-gray-900">Account Actions</h3>
						<p class="mb-4 text-sm text-gray-600">
							You can sign out of your account at any time. You'll need to sign in again to access
							your account.
						</p>
						<Button class="bg-red-600 px-8 hover:bg-red-500" on:click={logout}>Sign out</Button>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

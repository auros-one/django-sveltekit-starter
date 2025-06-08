<script lang="ts">
	import { requestPasswordReset } from '$lib/api/account/auth';
	import Button from '$lib/components/Button.svelte';

	let loading: boolean = false;
	let sent: boolean = false;
	let errors: { [key: string]: [] } | undefined;

	async function onReset(e: Event) {
		loading = true;
		const formData = Object.fromEntries(new FormData(e.target as HTMLFormElement));
		const data = (await requestPasswordReset(formData.email as string)) as
			| { [key: string]: [] }
			| { non_field_errors: [] };
		if (data.non_field_errors) errors = data;
		else sent = true;
		loading = false;
	}
</script>

<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
	<div class="sm:mx-auto sm:w-full sm:max-w-sm">
		<a href="/welcome"><img class="mx-auto h-10 w-auto" src="/icon.png" alt="Company logo" /></a>
		<h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
			Reset your password
		</h2>
	</div>

	<div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
		<form class="space-y-6" on:submit|preventDefault={onReset}>
			<div>
				<label for="email" class="block text-sm font-medium leading-6 text-gray-900"
					>Email address</label
				>
				<div class="mt-2">
					<input
						id="email"
						name="email"
						type="email"
						autocomplete="email"
						required
						class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
					/>
				</div>
			</div>
			<div>
				{#if errors}
					{#each Object.keys(errors) as key}
						{#each errors[key] as error}
							<p class="text-sm text-red-500">{error}</p>
						{/each}
					{/each}
				{/if}
			</div>

			<div>
				<Button type="submit" bind:loading disabled={sent} class="w-full">
					{#if sent}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="mr-2 h-5 w-5"
						>
							<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
						</svg>

						Reset link sent! Check your email
					{:else}
						Send reset link
					{/if}
				</Button>
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
</div>

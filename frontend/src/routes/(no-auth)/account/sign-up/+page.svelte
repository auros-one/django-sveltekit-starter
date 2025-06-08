<script lang="ts">
	import { goto } from '$app/navigation';
	import { login, signup } from '$lib/api/account/auth';
	import Button from '$lib/components/Button.svelte';

	let loading: boolean = false;
	let errors: { [key: string]: [string] } | undefined;

	async function onSignup(e: Event) {
		loading = true;
		const formData = Object.fromEntries(new FormData(e.target as HTMLFormElement));
		const email = formData.email as string;
		const password1 = formData.password1 as string;
		const password2 = formData.password2 as string;

		if (
			typeof email !== 'string' ||
			typeof password1 !== 'string' ||
			typeof password2 !== 'string' ||
			!email ||
			!password1 ||
			!password2
		) {
			errors = { message: ['Invalid email or password'] };
		} else if (password1 !== password2) {
			errors = { message: ['Passwords do not match'] };
		} else {
			// sign up returns undefined if successful, or an error object if not
			errors = await signup(email, password1, password2);
		}

		// If signup is successful, sign in and redirect to home
		if (errors === undefined) {
			await login(email, password1);
			await goto('/');
		}
		loading = false;
	}
</script>

<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
	<div class="sm:mx-auto sm:w-full sm:max-w-sm">
		<a href="/welcome"><img class="mx-auto h-10 w-auto" src="/icon.png" alt="Company logo" /></a>
		<h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
			Sign up for an account
		</h2>
	</div>

	<div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
		<form class="space-y-6" on:submit|preventDefault={onSignup}>
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
				{#if errors?.email}
					{#each errors.email as error}
						<p class="mt-1 text-sm text-red-500">{error}</p>
					{/each}
				{/if}
			</div>

			<div>
				<label for="password1" class="block text-sm font-medium leading-6 text-gray-900"
					>Password</label
				>
				<div class="mt-2">
					<input
						id="password1"
						name="password1"
						type="password"
						required
						class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
					/>
				</div>
				{#if errors?.password1}
					{#each errors.password1 as error}
						<p class="mt-1 text-sm text-red-500">{error}</p>
					{/each}
				{/if}
			</div>

			<div>
				<label for="password2" class="block text-sm font-medium leading-6 text-gray-900"
					>Confirm password</label
				>
				<div class="mt-2">
					<input
						id="password2"
						name="password2"
						type="password"
						required
						class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
					/>
				</div>
				{#if errors?.password2}
					{#each errors.password2 as error}
						<p class="mt-1 text-sm text-red-500">{error}</p>
					{/each}
				{/if}
			</div>

			<div>
				{#if errors?.non_field_errors || errors?.message}
					{#each errors.non_field_errors || errors.message || [] as error}
						<p class="text-sm text-red-500">{error}</p>
					{/each}
				{/if}
			</div>

			<div>
				<Button bind:loading type="submit" class="w-full">Sign up</Button>
			</div>
		</form>

		<p class="mt-10 text-center text-sm text-gray-500">
			Already have an account?
			<a
				href="/account/sign-in"
				class="font-semibold leading-6 text-primary-600 hover:text-primary-500">Sign in</a
			>
		</p>
	</div>
</div>

<script lang="ts">
	import { goto } from '$app/navigation';
	import { login, signup } from '$lib/api/account/auth';
	import Button from '$lib/components/Button.svelte';

	let loading: boolean = false;
	let errors: { [key: string]: [string] } | undefined;

	async function onSignup(e: Event) {
		loading = true;
		const formData = Object.fromEntries(new FormData(e.target as HTMLFormElement));
		const email = formData.email;
		const password1 = formData.password1;
		const password2 = formData.password2;

		if (
			typeof email !== 'string' ||
			typeof password1 !== 'string' ||
			typeof password2 !== 'string' ||
			!email ||
			!password1 ||
			!password2
		) {
			errors = { message: ['Invalid email or password'] };
			loading = false;
			return;
		}

		if (password1 !== password2) {
			errors = { message: ['Passwords do not match'] };
			loading = false;
			return;
		}

		const signupData = await signup(email, password1, password2);
		if (!signupData.access) {
			errors = signupData;
			loading = false;
			return;
		}

		await login(email, password1);
		await goto('/');
		loading = false;
	}
</script>

<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
	<div class="sm:mx-auto sm:w-full sm:max-w-sm">
		<a href="/welcome"><img class="mx-auto h-10 w-auto" src="/favicon.png" alt="Company logo" /></a>
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
				<Button bind:loading type="submit" class="w-full">Sign up</Button>
			</div>
		</form>

		<p class="mt-10 text-center text-sm text-gray-500">
			Already have an account?
			<a
				href="/account/login"
				class="font-semibold leading-6 text-primary-600 hover:text-primary-500">Log in</a
			>
		</p>
	</div>
</div>

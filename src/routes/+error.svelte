<script lang="ts">
	import { page } from '$app/stores';

	let errorMessage: string = $page.error?.message || 'An error ocurred';
</script>

<svelte:head>
	<title>{$page.status} - {errorMessage}</title>
</svelte:head>

<main class="bg-lunar_white relative min-h-full">
	<div class="mx-auto max-w-7xl px-6 py-32 text-center sm:py-40 lg:px-8">
		<p class="text-base font-semibold leading-8 text-gray-700">{$page.status}</p>
		{#if $page.status == 404}
			<h1 class="mt-4 text-3xl font-bold tracking-tight text-gray-700 sm:text-5xl">
				Page not found
			</h1>
			<p class="mt-4 text-base text-gray-700 sm:mt-6">
				Sorry, we couldn't find the page you're looking for.
			</p>
		{:else}
			<h1 class="mt-4 text-3xl font-bold tracking-tight text-gray-700 sm:text-5xl">
				{errorMessage}
			</h1>
			<p class="mt-4 text-base text-gray-700 sm:mt-6">
				Something went wrong, please try again later.
			</p>
		{/if}
		<div class="mt-10 flex justify-center">
			<a href="/" class="text-sm font-semibold leading-7 text-gray-700"
				><span aria-hidden="true">&larr;</span> Back to home</a
			>
		</div>
	</div>
</main>

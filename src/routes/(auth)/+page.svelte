<script>
	import { logout } from '$lib/api/account/auth';
	import { user } from '$lib/stores/account';
</script>

<div class="flex h-[80%] flex-col items-center justify-center gap-4">
	<a href="/welcome"><img class="mx-auto h-10 w-auto" src="/favicon.png" alt="Company logo" /></a>
	<h1 class="my-4 text-2xl font-bold">User Homepage</h1>
	<h2 class="text-lg">Logged in as {$user?.email}</h2>
	<button
		on:click={logout}
		class="flex justify-center rounded-md bg-primary-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
		>Log out</button
	>
</div>

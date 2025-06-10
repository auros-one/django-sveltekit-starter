<main class="container mx-auto w-screen text-center">
	<h1 class="mb-4 text-2xl font-bold">Error Testing</h1>
	<button
		class="rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700"
		on:click={() => {
			throw new Error('This is a test exception');
		}}
	>
		Throw Exception
	</button>
	<button
		class="rounded bg-red-500 px-4 py-2 font-bold text-white hover:bg-red-700"
		on:click={() => {
			console.error('This is an error message');
		}}
	>
		Log Error Message
	</button>
</main>

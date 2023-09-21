<script>
	function unknownFunction() {
		throw new Error('Unknown function');
	}
</script>

<div class="flex h-[75%] flex-col items-center justify-center">
	<h1 class="m-10 text-xl font-bold">Test Sentry</h1>
	<button
		class="rounded-lg border border-red-700 bg-red-200 p-4 font-bold text-red-800"
		type="button"
		on:click={unknownFunction}>Click to raise an error</button
	>
</div>

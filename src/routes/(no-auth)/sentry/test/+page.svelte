<script>
	function unknownFunction() {
		throw new Error('Unknown function');
	}
</script>

<div class="flex flex-col justify-center items-center h-[75%]">
	<h1 class="text-xl font-bold m-10">Test Sentry</h1>
	<button
		class="bg-red-200 border border-red-700 p-4 rounded-lg font-bold text-red-800"
		type="button"
		on:click={unknownFunction}>Click to raise an error</button
	>
</div>

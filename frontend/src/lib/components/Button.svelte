<script lang="ts">
	import Spinner from './loading/Spinner.svelte';

	export let loading: boolean = false;
	let clazz: string = '';
	export { clazz as class };
	let _disabled: boolean = false;
	export { _disabled as disabled };
</script>

<button
	on:click
	disabled={loading || _disabled}
	{...$$restProps}
	class={'inline-flex h-[38px] items-center justify-center gap-2 rounded-md bg-primary-500 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 ' +
		clazz}
>
	<p class:opacity-0={loading} class="flex flex-row items-center justify-center"><slot /></p>
	<div class:opacity-0={!loading} class="absolute">
		<Spinner size={20} duration="0.3s" color="#FFFFFF" />
	</div>
</button>

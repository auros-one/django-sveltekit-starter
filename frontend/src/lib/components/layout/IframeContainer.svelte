<script lang="ts">
	import { onMount } from 'svelte';
	import Spinner from '$lib/components/loading/Spinner.svelte';

	export let src: string;
	export let title: string;

	let loading = true;
	let iframeElement: HTMLIFrameElement;

	onMount(() => {
		// Handle iframe load
		if (iframeElement) {
			iframeElement.addEventListener('load', () => {
				loading = false;
			});
		}
	});
</script>

<div class="iframe-container">
	{#if loading}
		<div class="loading-overlay">
			<Spinner size={40} />
			<p class="mt-4 text-sm text-gray-600">Loading {title}...</p>
		</div>
	{/if}

	<iframe
		bind:this={iframeElement}
		{src}
		{title}
		class="iframe-content"
		frameborder="0"
		on:load={() => (loading = false)}
	/>
</div>

<style>
	.iframe-container {
		position: fixed;
		top: 64px; /* Height of navbar */
		left: 0;
		right: 0;
		bottom: 0;
		background: white;
	}

	.loading-overlay {
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.9);
		z-index: 10;
	}

	.iframe-content {
		width: 100%;
		height: 100%;
		border: none;
		display: block;
	}

	/* For mobile, adjust for navbar height */
	@media (max-width: 768px) {
		.iframe-container {
			top: 64px;
		}
	}
</style>

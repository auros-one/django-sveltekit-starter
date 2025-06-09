<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import Spinner from '$lib/components/loading/Spinner.svelte';

	export let src: string;
	export let title: string;
	export let navbarHeight = 64; // Make this configurable

	let iframeElement: HTMLIFrameElement;
	let showOverlay = true;

	onMount(() => {
		// Check if iframe is already loaded
		if (iframeElement) {
			// Check readyState for already loaded iframe
			const checkLoaded = () => {
				try {
					// If we can access the contentDocument, it's loaded
					// Also check readyState if available
					if (
						iframeElement.contentDocument?.readyState === 'complete' ||
						iframeElement.contentWindow
					) {
						// Add a small delay to ensure content is painted
						setTimeout(() => {
							// Add another small delay before hiding overlay for smoother transition
							setTimeout(() => {
								showOverlay = false;
							}, 100);
						}, 150);
					}
				} catch {
					// Cross-origin iframes will throw an error when accessing contentDocument
					// In this case, we'll assume it's loaded if the src is set
					if (iframeElement.src) {
						setTimeout(() => {
							setTimeout(() => {
								showOverlay = false;
							}, 100);
						}, 150);
					}
				}
			};

			// Check immediately
			checkLoaded();

			// Also set up load event listener in case it's not loaded yet
			const handleLoad = () => {
				setTimeout(() => {
					setTimeout(() => {
						showOverlay = false;
					}, 100);
				}, 150);
			};

			iframeElement.addEventListener('load', handleLoad);

			// Cleanup
			return () => {
				iframeElement.removeEventListener('load', handleLoad);
			};
		}
	});
</script>

<div class="iframe-container" style="--navbar-height: {navbarHeight}px">
	{#if showOverlay}
		<div class="loading-overlay" transition:fade={{ duration: 50 }}>
			<Spinner />
			<p class="mt-4 text-sm text-gray-600">Loading {title}...</p>
		</div>
	{/if}

	<iframe bind:this={iframeElement} {src} {title} class="iframe-content" frameborder="0"></iframe>
</div>

<style>
	.iframe-container {
		position: fixed;
		top: var(--navbar-height);
		left: 0;
		right: 0;
		bottom: 0;
		background: #f8f9fa; /* Light gray background to prevent black flash */
	}

	.loading-overlay {
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: #ffffff;
		z-index: 10;
	}

	.iframe-content {
		width: 100%;
		height: 100%;
		border: none;
		display: block;
		background: white; /* Ensure iframe has white background */
		opacity: 1;
		transition: opacity 0.2s ease-in-out;
	}

	/* Prevent iframe flash by hiding it initially */
	.iframe-container:has(.loading-overlay) .iframe-content {
		opacity: 0.01; /* Almost invisible but still loads */
	}

	/* For mobile, adjust for navbar height */
	@media (max-width: 768px) {
		.iframe-container {
			top: var(--navbar-height);
		}
	}
</style>

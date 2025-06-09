<script lang="ts">
	import ArtifactList from '$lib/components/ArtifactList.svelte';
	import AICodingAssistants from '$lib/components/AICodingAssistants.svelte';
	import { artifacts } from '$lib/data/artifacts';
	import { browser } from '$app/environment';

	let copyingStates: Record<string, boolean> = {};

	async function copyArtifactPrompt(filename: string) {
		try {
			// Set copying state
			copyingStates[filename] = true;

			// Fetch the artifact content from static folder
			const response = await fetch(`/artifacts/${filename}`);
			if (!response.ok) {
				throw new Error('Failed to fetch artifact');
			}

			const content = await response.text();

			// Copy to clipboard
			if (browser && window.navigator.clipboard) {
				await window.navigator.clipboard.writeText(content);
			}

			// Keep the "Copied!" state for 2 seconds
			setTimeout(() => {
				copyingStates[filename] = false;
			}, 2000);
		} catch (error) {
			console.error('Failed to copy artifact:', error);
			copyingStates[filename] = false;
			if (browser && window.alert) {
				window.alert('Failed to copy artifact. Please try again.');
			}
		}
	}
</script>

<svelte:head>
	<title>Artifacts - Django SvelteKit Starter</title>
</svelte:head>

<div class="min-h-screen bg-gray-50">
	<!-- Header Section -->
	<div class="border-b border-gray-200 bg-white">
		<div class="px-4 py-12 sm:px-6 lg:px-8">
			<div class="mx-auto max-w-7xl">
				<div class="text-center">
					<h1 class="text-4xl font-bold text-gray-900 sm:text-5xl">Artifacts</h1>
					<p class="mt-4 text-xl text-gray-600">
						AI Coders can add these to your <span class="text-primary-600">Django x SvelteKit</span>
						project
					</p>

					<!-- AI Assistant Section -->
					<div class="mt-10">
						<AICodingAssistants />
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Artifacts Grid -->
	<div class="px-4 py-12 sm:px-6 lg:px-8">
		<div class="mx-auto max-w-7xl">
			<ArtifactList {artifacts} {copyingStates} onCopy={copyArtifactPrompt} />

			<!-- Add New Artifact CTA -->
			<div class="mt-16 rounded-lg border border-gray-200 bg-white p-8 shadow-sm">
				<div class="text-center">
					<h3 class="text-xl font-semibold text-gray-900">Want to contribute an artifact?</h3>
					<p class="mt-3 text-base text-gray-600">
						Artifacts are specifications that help AI coders build features. Check out the
						<a
							href="https://github.com/yourusername/yourrepo/tree/main/artifacts/README.md"
							target="_blank"
							class="font-medium text-primary-600 hover:text-primary-700">artifact guide</a
						>
						to learn how to create one.
					</p>
				</div>
			</div>
		</div>
	</div>
</div>

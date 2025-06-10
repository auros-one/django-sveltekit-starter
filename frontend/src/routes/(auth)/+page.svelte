<script lang="ts">
	import AICodingAssistants from '$lib/components/AICodingAssistants.svelte';
</script>

<svelte:head>
	<title>Django SvelteKit Starter - Home</title>
</svelte:head>

<div class="min-h-screen">
	<!-- Hero Section - Simplified -->
	<div class="bg-white">
		<div class="px-4 py-16 sm:px-6 lg:px-8">
			<div class="mx-auto max-w-4xl text-center">
				<h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
					Django-SvelteKit
				</h1>
				<p class="mt-4 text-xl text-gray-600">
					A modern full-stack template for AI-powered development
				</p>
				<div class="mt-8 flex justify-center">
					<a
						href="https://github.com/your-org/django-sveltekit-starter"
						target="_blank"
						class="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-6 py-3 text-base font-medium text-gray-700 transition-colors hover:bg-gray-50"
					>
						<svg class="-ml-1 mr-2 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
							<path
								fill-rule="evenodd"
								d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z"
								clip-rule="evenodd"
							/>
						</svg>
						View on GitHub
					</a>
				</div>
			</div>
		</div>
	</div>

	<!-- AI Coder Section -->
	<div class="bg-white px-4 py-16 sm:px-6 lg:px-8">
		<div class="mx-auto max-w-6xl">
			<div class="mb-12 text-center">
				<h2 class="text-3xl font-bold text-gray-900">Supercharge Development with AI Coders</h2>
				<p class="mt-4 text-lg text-gray-600">
					This template is optimized for AI-assisted development. Use tools like Cursor, Windsurf,
					or GitHub Copilot to build features faster than ever.
				</p>
			</div>

			<div class="mx-auto max-w-4xl">
				<div class="mb-8 text-center">
					<AICodingAssistants />
				</div>
			</div>
		</div>
	</div>

	<!-- Artifacts Section -->
	<div class="relative bg-gradient-to-b from-white to-gray-50 px-4 py-20 sm:px-6 lg:px-8">
		<div class="mx-auto max-w-6xl">
			<!-- Section Header -->
			<div class="mb-8 text-center">
				<h2 class="mb-4 text-4xl font-bold text-gray-900">
					Build Faster with <span class="text-primary-600">Artifacts</span>
				</h2>
				<div class="mb-4 inline-flex items-center gap-2 rounded-full bg-primary-50 px-4 py-2">
					<svg
						class="h-5 w-5 text-primary-600"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M13 10V3L4 14h7v7l9-11h-7z"
						/>
					</svg>
					<span class="text-sm font-semibold text-primary-700">AI-Ready Components</span>
				</div>
			</div>

			<div class="text-center">
				<div class="mx-auto max-w-2xl">
					<div class="flex items-center justify-center">
						<h4 class="mb-4 ml-4 text-center text-xl font-medium text-gray-900">
							Django-SvelteKit feature specs that AI coders can implement for you
						</h4>
					</div>
				</div>
			</div>

			<!-- Example Artifacts Preview -->
			<div class="mx-auto mb-12 max-w-4xl overflow-hidden rounded-xl bg-gray-900">
				<div class="border-b border-gray-800 p-6">
					<div class="flex items-center gap-2 font-mono text-sm text-gray-400">
						<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
							/>
						</svg>
						Available Artifacts
					</div>
				</div>
				<div class="divide-y divide-gray-800">
					<div
						class="group flex items-center justify-between px-6 py-4 transition-colors hover:bg-gray-800/50"
					>
						<div class="flex items-center gap-4">
							<div class="flex-shrink-0">
								<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500/10">
									<svg
										class="h-5 w-5 text-blue-400"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
										/>
									</svg>
								</div>
							</div>
							<div>
								<h4 class="font-medium text-white">ChatUI Streaming Interface</h4>
								<p class="text-sm text-gray-400">
									Real-time chat with token streaming and markdown support
								</p>
							</div>
						</div>
						<span class="text-xs text-gray-500 group-hover:text-gray-400">Advanced</span>
					</div>
					<div
						class="group flex items-center justify-between px-6 py-4 transition-colors hover:bg-gray-800/50"
					>
						<div class="flex items-center gap-4">
							<div class="flex-shrink-0">
								<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-green-500/10">
									<svg
										class="h-5 w-5 text-green-400"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
										/>
									</svg>
								</div>
							</div>
							<div>
								<h4 class="font-medium text-white">Data Table Component</h4>
								<p class="text-sm text-gray-400">
									Sortable, paginated tables with TypeScript generics
								</p>
							</div>
						</div>
						<span class="text-xs text-gray-500 group-hover:text-gray-400">Beginner</span>
					</div>
					<div
						class="group flex items-center justify-between px-6 py-4 transition-colors hover:bg-gray-800/50"
					>
						<div class="flex items-center gap-4">
							<div class="flex-shrink-0">
								<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-500/10">
									<svg
										class="h-5 w-5 text-purple-400"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M12 4v16m8-8H4"
										/>
									</svg>
								</div>
							</div>
							<div>
								<h4 class="font-medium text-white">More artifacts coming soon...</h4>
								<p class="text-sm text-gray-400">
									Authentication flows, dashboards, API integrations, and more
								</p>
							</div>
						</div>
						<span class="text-xs text-gray-500 group-hover:text-gray-400">Various</span>
					</div>
				</div>
			</div>

			<!-- CTA -->
			<div class="text-center">
				<a
					href="/admin/artifacts"
					class="inline-flex transform items-center justify-center rounded-lg border border-transparent bg-primary-600 px-8 py-4 text-base font-medium text-white shadow-lg transition-all duration-200 hover:scale-105 hover:bg-primary-700 hover:shadow-xl"
				>
					Browse Artifacts
					<svg
						class="-mr-1 ml-2 h-5 w-5"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 20 20"
						fill="currentColor"
					>
						<path
							fill-rule="evenodd"
							d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
							clip-rule="evenodd"
						/>
					</svg>
				</a>
				<p class="mt-4 text-sm text-gray-500">
					Works with Claude, GPT-4, Cursor, and other AI coding assistants
				</p>
			</div>
		</div>
	</div>

	<!-- Support Section -->
	<div class="bg-gray-50 px-4 py-16 sm:px-6 lg:px-8">
		<div class="mx-auto max-w-4xl">
			<div class="text-center">
				<h2 class="text-3xl font-bold text-gray-900">Need Help?</h2>
				<p class="mt-4 text-lg text-gray-600">
					We're here to help you get started and solve any issues you might encounter
				</p>
				<div class="mt-8 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
					<a
						href="https://github.com/your-org/django-sveltekit-starter/issues/new"
						target="_blank"
						class="inline-flex items-center rounded-md border border-transparent bg-gray-800 px-6 py-3 text-base font-medium text-white transition-colors hover:bg-gray-900"
					>
						<svg class="mr-2 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
							<path
								fill-rule="evenodd"
								d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z"
								clip-rule="evenodd"
							/>
						</svg>
						Create an Issue on GitHub
					</a>
					<a
						href="mailto:support@yourcompany.com"
						class="inline-flex items-center rounded-md border border-gray-300 bg-white px-6 py-3 text-base font-medium text-gray-700 transition-colors hover:bg-gray-50"
					>
						<svg
							class="mr-2 h-5 w-5"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"
							/>
						</svg>
						Contact Us Directly
					</a>
				</div>
			</div>
		</div>
	</div>
</div>

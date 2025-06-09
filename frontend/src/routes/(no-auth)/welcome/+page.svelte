<script lang="ts">
	let copiedCommand = '';

	function copyToClipboard(command: string) {
		window.navigator.clipboard.writeText(command);
		copiedCommand = command;
		setTimeout(() => {
			copiedCommand = '';
		}, 2000);
	}
</script>

<div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
	<div class="container mx-auto px-6 py-16">
		<!-- Header -->
		<div class="mb-16 text-center">
			<a href="/welcome" class="mb-6 inline-block">
				<img class="h-12 w-auto" src="/icon.png" alt="Django-SvelteKit Starter" />
			</a>
			<h1 class="mb-4 text-4xl font-bold text-slate-900 md:text-6xl">
				Django-SvelteKit
				<span
					class="bg-gradient-to-r from-primary-600 to-primary-500 bg-clip-text text-transparent"
				>
					Starter
				</span>
			</h1>
			<p class="mx-auto max-w-2xl text-xl leading-relaxed text-slate-600">
				A production-ready monorepo template for building full-stack applications with Django
				backend and SvelteKit frontend
			</p>
			<div class="mt-8 flex flex-col justify-center gap-4 sm:flex-row">
				<a
					href="https://github.com/auros-one/django-sveltekit-starter"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex items-center justify-center gap-2 rounded-lg bg-slate-900 px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-slate-800"
				>
					<svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
						<path
							d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.237 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
						/>
					</svg>
					<span>Explore on GitHub</span>
				</a>
				<a
					href="#getting-started"
					class="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-300 bg-white px-6 py-3 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50"
				>
					Get Started
					<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M19 9l-7 7-7-7"
						/>
					</svg>
				</a>
			</div>
		</div>

		<!-- AI Coding Integration Feature Section -->
		<div class="mb-16">
			<h2 class="mb-4 text-2xl font-bold text-slate-900">AI-First Development</h2>
			<p class="mb-4 max-w-3xl text-lg text-slate-600">
				Built for the AI-assisted development era. Our comprehensive engineering handbook provides
				AI coders with structured guidelines, best practices, and real-world examples to accelerate
				development.
			</p>

			<div class="mb-8 text-left">
				<a
					href="https://www.linkedin.com/company/auros-one/"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex items-center text-base text-primary-600 underline hover:text-primary-700"
				>
					Read our latest review of the top AI coders
				</a>
			</div>

			<div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between lg:gap-8">
				<!-- AI Logos -->
				<div class="flex flex-wrap items-center justify-center gap-6 lg:justify-start">
					<!-- Claude -->
					<div>
						<div
							class="flex h-12 w-12 items-center justify-center overflow-hidden rounded-xl bg-white shadow-sm"
						>
							<img
								src="/landing-page/claude.png"
								alt="Claude"
								class="h-full w-full object-contain p-2"
							/>
						</div>
						<p class="mt-2 text-center text-sm font-medium text-slate-700">Claude</p>
					</div>

					<!-- OpenAI Codex -->
					<div>
						<div
							class="flex h-12 w-12 items-center justify-center overflow-hidden rounded-xl bg-white shadow-sm"
						>
							<img
								src="/landing-page/openai.png"
								alt="OpenAI"
								class="h-full w-full object-contain p-2"
							/>
						</div>
						<p class="mt-2 text-center text-sm font-medium text-slate-700">OpenAI</p>
					</div>

					<!-- Devin -->
					<div>
						<div
							class="flex h-12 w-12 items-center justify-center overflow-hidden rounded-xl bg-white shadow-sm"
						>
							<img
								src="/landing-page/devin.png"
								alt="Devin"
								class="h-full w-full object-contain p-2"
							/>
						</div>
						<p class="mt-2 text-center text-sm font-medium text-slate-700">Devin</p>
					</div>

					<!-- Cursor -->
					<div>
						<div
							class="flex h-12 w-12 items-center justify-center overflow-hidden rounded-xl bg-white shadow-sm"
						>
							<img
								src="/landing-page/cursor.png"
								alt="Cursor"
								class="h-full w-full object-contain p-2"
							/>
						</div>
						<p class="mt-2 text-center text-sm font-medium text-slate-700">Cursor</p>
					</div>
				</div>

				<!-- Handshake Emoji -->
				<div class="flex justify-center lg:px-4">
					<span class="text-4xl">🤝</span>
				</div>

				<!-- Engineering Handbook Callout -->
				<div class="flex justify-center lg:block">
					<a
						href="https://github.com/auros-one/django-sveltekit-starter/tree/main/engineering-handbook"
						target="_blank"
						rel="noopener noreferrer"
						class="block max-w-lg flex-1 rounded-xl border border-slate-200 bg-slate-50 p-5 transition-all duration-200 hover:border-slate-300 hover:bg-slate-100 hover:shadow-sm"
					>
						<div class="flex items-start gap-3">
							<div class="flex-shrink-0">
								<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-100">
									<svg
										class="h-4 w-4 text-primary-600"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
										/>
									</svg>
								</div>
							</div>
							<div class="flex-1">
								<div class="flex items-center justify-between">
									<h3 class="text-sm font-semibold text-slate-900">Engineering Handbook</h3>
									<svg
										class="ml-2 h-3 w-3 text-slate-400"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
										/>
									</svg>
								</div>
								<p class="mt-1 text-xs text-slate-600">
									Structured guidelines and patterns specifically for AI coding assistants.
								</p>
							</div>
						</div>
					</a>
				</div>
			</div>
		</div>

		<!-- Getting Started Section -->
		<div class="mb-16" id="getting-started">
			<h2 class="mb-6 text-2xl font-bold text-slate-900">Getting Started</h2>
			<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
				<!-- Step 1 -->
				<div class="relative rounded-lg border border-slate-200 bg-white p-6">
					<div
						class="mb-3 flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-sm font-semibold text-slate-600"
					>
						1
					</div>
					<h3 class="mb-2 font-semibold text-slate-900">Prerequisites</h3>
					<p class="mb-3 text-sm text-slate-600">
						Ensure you have Docker and Git installed on your system
					</p>
					<div class="flex items-center gap-3">
						<a
							href="https://docs.docker.com/get-docker/"
							target="_blank"
							rel="noopener noreferrer"
							class="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-50 transition-colors hover:bg-slate-100"
							title="Install Docker"
						>
							<img src="/landing-page/docker.png" alt="Docker" class="h-6 w-6 object-contain" />
						</a>
						<a
							href="https://git-scm.com/downloads"
							target="_blank"
							rel="noopener noreferrer"
							class="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-50 transition-colors hover:bg-slate-100"
							title="Install Git"
						>
							<img src="/landing-page/git.png" alt="Git" class="h-6 w-6 object-contain" />
						</a>
					</div>
				</div>

				<!-- Step 2 -->
				<div class="relative rounded-lg border border-slate-200 bg-white p-6">
					<div
						class="mb-3 flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-sm font-semibold text-slate-600"
					>
						2
					</div>
					<h3 class="mb-2 font-semibold text-slate-900">Fork & Clone</h3>
					<p class="mb-3 text-sm text-slate-600">
						Fork the repository and clone it to your local machine
					</p>
					<a
						href="https://github.com/auros-one/django-sveltekit-starter/fork"
						target="_blank"
						rel="noopener noreferrer"
						class="inline-flex items-center gap-2 text-sm font-medium text-slate-700 transition-colors hover:text-slate-900"
					>
						<svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
							<path
								d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.237 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
							/>
						</svg>
						Fork on GitHub
					</a>
				</div>

				<!-- Step 3 -->
				<div class="relative rounded-lg border border-slate-200 bg-white p-6">
					<div
						class="mb-3 flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-sm font-semibold text-slate-600"
					>
						3
					</div>
					<h3 class="mb-2 font-semibold text-slate-900">Install</h3>
					<p class="mb-3 text-sm text-slate-600">Set up the project with all dependencies</p>
					<div class="group relative">
						<pre
							class="overflow-x-auto rounded-lg bg-slate-900 px-4 py-3 text-sm text-slate-100"><code
								>make install</code
							></pre>
						<button
							on:click={() => copyToClipboard('make install')}
							class="absolute right-2 top-2 rounded-md bg-slate-800 p-1.5 text-slate-400 opacity-0 transition-opacity hover:bg-slate-700 hover:text-slate-200 group-hover:opacity-100"
							title="Copy to clipboard"
						>
							{#if copiedCommand === 'make install'}
								<svg
									class="h-4 w-4 text-green-400"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M5 13l4 4L19 7"
									/>
								</svg>
							{:else}
								<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"
									/>
								</svg>
							{/if}
						</button>
					</div>
				</div>

				<!-- Step 4 -->
				<div class="relative rounded-lg border border-slate-200 bg-white p-6">
					<div
						class="mb-3 flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-sm font-semibold text-slate-600"
					>
						4
					</div>
					<h3 class="mb-2 font-semibold text-slate-900">Start Building</h3>
					<p class="mb-3 text-sm text-slate-600">Launch the development environment</p>
					<div class="group relative">
						<pre
							class="overflow-x-auto rounded-lg bg-slate-900 px-4 py-3 text-sm text-slate-100"><code
								>make run</code
							></pre>
						<button
							on:click={() => copyToClipboard('make run')}
							class="absolute right-2 top-2 rounded-md bg-slate-800 p-1.5 text-slate-400 opacity-0 transition-opacity hover:bg-slate-700 hover:text-slate-200 group-hover:opacity-100"
							title="Copy to clipboard"
						>
							{#if copiedCommand === 'make run'}
								<svg
									class="h-4 w-4 text-green-400"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M5 13l4 4L19 7"
									/>
								</svg>
							{:else}
								<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"
									/>
								</svg>
							{/if}
						</button>
					</div>
				</div>
			</div>
			<div class="mt-6 text-sm text-slate-600">
				<p>
					Need more details? Check out the <a
						href="https://github.com/auros-one/django-sveltekit-starter#readme"
						target="_blank"
						rel="noopener noreferrer"
						class="text-primary-600 underline hover:text-primary-700">full documentation</a
					> on GitHub.
				</p>
			</div>
		</div>

		<!-- Features Grid -->
		<div class="mb-16">
			<h2 class="mb-8 text-center text-2xl font-bold text-slate-900">
				Everything You Need, Out of the Box
			</h2>
			<div class="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
				<div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
					<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-green-100">
						<svg
							class="h-6 w-6 text-green-600"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
							/>
						</svg>
					</div>
					<h3 class="mb-2 font-semibold text-slate-900">Type Safety</h3>
					<p class="text-sm text-slate-600">
						Auto-generated TypeScript types from Django OpenAPI schema ensuring end-to-end type
						safety
					</p>
				</div>

				<div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
					<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100">
						<svg
							class="h-6 w-6 text-blue-600"
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
					</div>
					<h3 class="mb-2 font-semibold text-slate-900">Modern Stack</h3>
					<p class="text-sm text-slate-600">
						Django REST Framework backend with SvelteKit frontend, JWT auth, and Celery task
						processing
					</p>
				</div>

				<div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
					<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100">
						<svg
							class="h-6 w-6 text-purple-600"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
							/>
						</svg>
					</div>
					<h3 class="mb-2 font-semibold text-slate-900">Production Ready</h3>
					<p class="text-sm text-slate-600">
						Docker deployment, Ansible automation, Terraform infrastructure, and comprehensive CI/CD
					</p>
				</div>

				<div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
					<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-orange-100">
						<svg
							class="h-6 w-6 text-orange-600"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
							/>
						</svg>
					</div>
					<h3 class="mb-2 font-semibold text-slate-900">Monorepo</h3>
					<p class="text-sm text-slate-600">
						Atomic commits, shared tooling, and simplified workflow with intelligent pre-commit
						hooks
					</p>
				</div>

				<div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
					<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-teal-100">
						<svg
							class="h-6 w-6 text-teal-600"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"
							/>
						</svg>
					</div>
					<h3 class="mb-2 font-semibold text-slate-900">Docker Compose</h3>
					<p class="text-sm text-slate-600">
						One-command development environment with PostgreSQL, Redis, and all services configured
					</p>
				</div>

				<div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
					<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-red-100">
						<svg class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
							/>
						</svg>
					</div>
					<h3 class="mb-2 font-semibold text-slate-900">JWT Authentication</h3>
					<p class="text-sm text-slate-600">
						Secure JWT tokens with HTTP-only cookies, route protection, and multi-tenancy support
					</p>
				</div>
			</div>
		</div>

		<!-- Tech Stack -->
		<div class="mb-16 text-center">
			<h2 class="mb-8 text-2xl font-bold text-slate-900">Built with Modern Technologies</h2>
			<div class="flex flex-wrap justify-center gap-4">
				<span
					class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm"
					>Django 4.2+</span
				>
				<span
					class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm"
					>SvelteKit 2+</span
				>
				<span
					class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm"
					>TypeScript</span
				>
				<span
					class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm"
					>PostgreSQL</span
				>
				<span
					class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm"
					>Redis</span
				>
				<span
					class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm"
					>Docker</span
				>
			</div>
		</div>

		<!-- CTA Section -->
		<div class="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm md:p-12">
			<h2 class="mb-4 text-2xl font-bold text-slate-900">Get Started</h2>
			<p class="mx-auto mb-8 max-w-lg text-slate-600">
				Ready to explore the template? Sign in to see the admin interface or create a new account to
				get started.
			</p>
			<div class="flex flex-col justify-center gap-4 sm:flex-row">
				<a
					href="/account/sign-in"
					class="inline-flex items-center justify-center rounded-lg border border-transparent bg-primary-600 px-6 py-3 text-base font-medium text-white transition-colors duration-200 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
				>
					Sign In
				</a>
				<a
					href="/account/sign-up"
					class="inline-flex items-center justify-center rounded-lg border border-slate-300 bg-white px-6 py-3 text-base font-medium text-slate-700 transition-colors duration-200 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
				>
					Create Account
				</a>
			</div>
			<p class="mt-6 text-sm text-slate-500">
				Default admin: <code class="rounded bg-slate-100 px-2 py-1 text-xs">admin@admin.com</code> /
				<code class="rounded bg-slate-100 px-2 py-1 text-xs">admin</code>
			</p>
		</div>
	</div>

	<!-- Footer -->
	<footer class="border-t border-slate-200 bg-white">
		<div class="container mx-auto px-6 py-8">
			<div class="flex flex-col items-center justify-between gap-4 sm:flex-row">
				<p class="text-sm text-slate-600">
					Made with
					<span class="text-red-500">❤</span>
					by
					<a
						href="https://auros.one/"
						target="_blank"
						rel="noopener noreferrer"
						class="text-primary-600 underline hover:text-primary-700"
					>
						Auros One
					</a>
				</p>
				<a
					href="https://github.com/auros-one/django-sveltekit-starter"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex items-center gap-2 text-sm text-slate-600 transition-colors hover:text-slate-900"
				>
					<svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
						<path
							d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.237 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
						/>
					</svg>
					Fork this project
				</a>
			</div>
		</div>
	</footer>
</div>

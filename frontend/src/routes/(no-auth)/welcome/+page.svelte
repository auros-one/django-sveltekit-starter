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
		</div>

		<!-- Features Grid -->
		<div class="mb-16 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
			<div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
				<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-green-100">
					<svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
					Auto-generated TypeScript types from Django OpenAPI schema ensuring end-to-end type safety
				</p>
			</div>

			<div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
				<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100">
					<svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
					Atomic commits, shared tooling, and simplified workflow with intelligent pre-commit hooks
				</p>
			</div>

			<div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
				<div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-teal-100">
					<svg class="h-6 w-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
</div>

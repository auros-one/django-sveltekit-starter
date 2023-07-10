# BlackBear SvelteKit x Supabase x TailwindCSS Template

## Installing

```bash
cp .env.example .env
npm install
npm run check
```

## Developing

```bash
npm run dev
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.

## Troubleshooting

If your IDE is complaining about missing modules, for example`Cannot find module '$lib/...' or '$app/...' from language server for .svelte files in default configuration of sveltekit`

run `npm run check` might resolve the issue. ([soure](https://github.com/sveltejs/language-tools/issues/1459#issuecomment-1465270092))

## Supabase Setup

Add your [project URL and public API (anon) key](https://supabase.com/dashboard/project/_/settings/api) to the `.env` file (copy `.env.example`)

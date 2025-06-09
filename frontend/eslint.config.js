import eslint from '@eslint/js';
import tseslint from '@typescript-eslint/eslint-plugin';
import tsparser from '@typescript-eslint/parser';
import sveltePlugin from 'eslint-plugin-svelte';
import * as svelteParser from 'svelte-eslint-parser';
import prettier from 'eslint-config-prettier';

export default [
	eslint.configs.recommended,
	{
		ignores: [
			'.DS_Store',
			'node_modules/**',
			'build/**',
			'.svelte-kit/**',
			'package/**',
			'.env',
			'.env.*',
			'!.env.example',
			'pnpm-lock.yaml',
			'package-lock.json',
			'yarn.lock',
			'vite.config.ts',
			'tailwind.config.js',
			'postcss.config.js',
			'src/app.d.ts'
		]
	},
	{
		files: ['**/*.{js,ts,svelte}'],
		plugins: {
			'@typescript-eslint': tseslint,
			svelte: sveltePlugin
		},
		languageOptions: {
			parser: tsparser,
			parserOptions: {
				sourceType: 'module',
				ecmaVersion: 2020,
				extraFileExtensions: ['.svelte']
			},
			globals: {
				// Browser globals
				window: 'readonly',
				document: 'readonly',
				fetch: 'readonly',
				Headers: 'readonly',
				Request: 'readonly',
				Response: 'readonly',
				URL: 'readonly',
				FormData: 'readonly',
				HTMLFormElement: 'readonly',
				HTMLInputElement: 'readonly',
				HTMLIFrameElement: 'readonly',
				Event: 'readonly',
				KeyboardEvent: 'readonly',
				// Node.js globals
				process: 'readonly',
				console: 'readonly',
				setTimeout: 'readonly',
				clearTimeout: 'readonly',
				setInterval: 'readonly',
				clearInterval: 'readonly',
				require: 'readonly'
			}
		},
		rules: {
			'no-unused-vars': [
				'error',
				{
					argsIgnorePattern: '^_',
					varsIgnorePattern: '^_'
				}
			]
		}
	},
	{
		files: ['**/*.svelte'],
		plugins: {
			svelte: sveltePlugin
		},
		processor: sveltePlugin.processors['.svelte'],
		languageOptions: {
			parser: svelteParser,
			parserOptions: {
				parser: tsparser
			}
		},
		rules: {
			'svelte/no-at-html-tags': 'off'
		}
	},
	prettier
];

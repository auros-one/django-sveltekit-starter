/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				primary: {
					50: '#f0f7ff',
					100: '#e0eefb',
					200: '#b9dbf7',
					300: '#8dc2f0',
					400: '#5aa3e5',
					500: '#3484d6',
					600: '#2468b7',
					700: '#1d5394',
					800: '#1a447a',
					900: '#193966',
					950: '#0f2444'
				}
			}
		}
	},
	plugins: [require('@tailwindcss/forms')]
};

import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter({
			pages: '../backend/site',
			assets: '../backend/site',
			fallback: 'fallback.html',
			precompress: false,
			strict: true
		}),
		// adapter: adapter({
		// 	pages: 'build',
		// 	assets: 'build',
		// 	fallback: 'fallback.html',
		// 	precompress: false,
		// 	strict: true
		// }),
		alias: {
			$components: 'src/components',
			$schemas: 'src/lib/schemas'
		}
	}
};

export default config;

import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		proxy: {
			// Proxy all API request starting with /api to FastAPI server
			'/api': {
				target: 'http://127.0.0.1:8000', // FastAPI server URL
				changeOrigin: true // needed for virtual hosted sites
				// rewrite: (path) => path.replace(/^\/api/, ''),
			}
		}
	}
});

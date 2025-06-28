<script lang="ts">
	import { page } from '$app/state';
	import { Heading, Span, A } from 'flowbite-svelte';
</script>


<main
	class="flex flex-col min-h-screen w-full items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8 dark:bg-gray-900"
>
	<Heading tag="h1" class="text-8xl font-bold tracking-wide">
		<Span class="text-primary-600 dark:text-primary-600">
			{page.status}
		</Span>
	</Heading>

	<Heading tag="h2">
		<Span class="text-gray-600 dark:text-gray-400">
			{page.error?.message || 'An unexpected error occurred.'}
		</Span>
	</Heading>


    <Span class="text-gray-500 dark:text-gray-400 mt-4">
        Please try again later or go back to the
        <A href="/" class="text-primary-600 dark:text-primary-500 hover:underline">
            home page
        </A>.
    </Span>
</main>

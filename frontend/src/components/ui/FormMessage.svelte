<script lang="ts" module>
	export interface FormMessageType {
		type: 'error' | 'success' | 'info';
		message: string;
	}
</script>

<script lang="ts">
	import { type HTMLAttributes } from 'svelte/elements';
	import Icon from './Icon.svelte';

	interface FormMessageProps extends HTMLAttributes<HTMLDivElement> {
		type?: 'error' | 'success' | 'info';
		message: string;
	}

	const { type, message, ...props }: FormMessageProps = $props();

	const iconSize = 'size-5'; // Default icon size, can be adjusted as needed
</script>

<div {...props} class={['flex items-center justify-start gap-1.5', props.class]}>
	{#if type === 'error'}
		<Icon name="mdi--close-circle-outline" class={['text-error', iconSize]} />
	{:else if type === 'success'}
		<Icon name="mdi--tick-circle-outline" class={['text-success', iconSize]} />
	{:else if type === 'info'}
		<Icon name="mdi--information-variant-circle-outline" class={['text-warning', iconSize]} />
	{/if}
	<span class="text-sm">{message}</span>
</div>

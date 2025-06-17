<!-- 
@component

@name Icon

@description 
A simple custom wrapper for Iconify icons.

@props
- `name`: The name of the iconify icon to display.



@Example
<Icon icon="mdi:home" />
 
-->
<script lang="ts">
	import { type HTMLAttributes } from 'svelte/elements';

	interface IconProps extends HTMLAttributes<HTMLSpanElement> {
		name: string;
	}

	let props: IconProps = $props();
</script>

<span {...props} class={[`iconify ${props.name}`, props.class]}></span>

<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { LayoutData } from './$types';
	import Icon from '$components/ui/Icon.svelte';

	let { data, children }: { data: LayoutData; children: Snippet } = $props();

	const authUser = $derived(data.authenticatedUser);
</script>

<div class="navbar bg-base-300 px-5 py-3.5 shadow-sm">
	<div class="flex-1">
		<a class="btn btn-ghost text-xl" href="/dashboard">PriceTracker</a>
	</div>
	<div class="flex-row items-center space-x-2">
		<!-- Search Box -->
		<input type="text" placeholder="Search" class="input input-bordered w-44 md:w-56" />
		<!-- Users Management -->
		{#if authUser.role === 'admin'}
			<a href="/dashboard/users" class="btn">Users</a>
		{/if}
		<!-- Configs -->
		<a href="/dashboard/configs" class="btn">Configuration</a>
		<!-- User Area -->
		<div class="dropdown dropdown-end">
			<div tabindex="0" role="button" class="btn btn-circle avatar">
				<div class="w-10 rounded-full">
					{#if authUser.avatar}
						<img
							alt="Tailwind CSS Navbar component"
							src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp"
						/>
					{:else}
						<div
							class="hover:bg-accent-content flex h-full w-full items-center justify-center rounded-b-full"
						>
							<Icon name="mdi--clipboard-user-outline" class="text-info size-8" />
						</div>
					{/if}
				</div>
			</div>
			<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
			<ul
				tabindex="0"
				class="menu menu-md dropdown-content bg-base-100 rounded-box z-1 mt-2.5 w-56 space-y-1.5 p-2.5 shadow"
			>
				<li>
					<a
						type="button"
						class="btn btn-xs btn-soft btn-outline btn-info"
						href="/dashboard/profile"
					>
						<Icon name="mdi--user" class="size-5" />
						Profile
					</a>
				</li>
				<li>
					<button type="button" class="btn btn-xs btn-soft btn-outline btn-info">
						<Icon name="mdi--account-arrow-left-outline" class="size-5" />
						Logout
					</button>
				</li>
			</ul>
		</div>
	</div>
</div>

<main class="space-y-1.5 py-3.5">
	{@render children()}
</main>

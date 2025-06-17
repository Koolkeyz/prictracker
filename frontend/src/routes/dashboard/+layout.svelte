<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { LayoutData } from './$types';
	import {
		Navbar,
		NavBrand,
		NavHamburger,
		NavLi,
		NavUl,
		DarkMode,
		Search,
		Avatar,
		Dropdown,
		DropdownHeader,
		DropdownGroup,
		DropdownItem,
		avatar
	} from 'flowbite-svelte';
	import { UserCircleSolid, UserSettingsSolid, ReplyAllSolid } from 'flowbite-svelte-icons';
	import { fly } from 'svelte/transition';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';

	let { data, children }: { data: LayoutData; children: Snippet } = $props();

	const authUser = $derived(data.authUser);

	let activeUrl = $derived(page.url.pathname);
	let activeClass =
		'text-white bg-green-700 md:bg-transparent md:text-green-700 md:dark:text-white dark:bg-green-600 md:dark:bg-transparent';
	let nonActiveClass =
		'text-gray-700 hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-green-700 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent';

	const logoutUser = async () => {
		try {
			await fetch('/api/logout', {
				method: 'GET',
				headers: {
					Accept: 'application/json',
					'Content-Type': 'application/json'
				},
				credentials: 'include'
			});

			goto('/', { replaceState: true });
		} catch (error) {
			console.error('Logout error:', error);
		}
	};
</script>

<Navbar
	class="bg-gray-50 dark:bg-gray-900"
	fluid={true}
	closeOnClickOutside={true}
	navContainerClass="px-2"
>
	<NavBrand href="/">
		<img src="/favicon.svg" class="me-2.5 h-6 sm:h-8" alt="Flowbite Logo" />
		<span
			class="text-primary-700 self-center whitespace-nowrap text-xl font-semibold sm:text-2xl dark:text-white"
		>
			PriceTracker
		</span>
	</NavBrand>
	<section class="flex gap-1.5">
		<div class="flex items-center md:order-2">
			<div class="flex items-center justify-end gap-1.5">
				<div class="place-content-center rounded-full md:hidden">
					<DarkMode class="me-2 rounded-full px-3 py-3" />
				</div>

				{#if authUser.avatar}
					<Avatar id="avatar-menu" src={authUser.avatar} class="hover:cursor-pointer" />
				{:else}
					<Avatar id="avatar-menu" class="hover:cursor-pointer">
						<UserCircleSolid />
					</Avatar>
				{/if}

				<NavHamburger />
			</div>
		</div>
		<Dropdown placement="bottom" triggeredBy="#avatar-menu">
			<DropdownHeader>
				<span class="block text-sm">{`${authUser.firstName} ${authUser.lastName}`}</span>
				<span class="block truncate text-sm font-medium">adrian.gookool@agostinislimited.com</span>
			</DropdownHeader>
			<DropdownGroup>
				<DropdownItem href={'/dashboard/profile'} class="flex items-center gap-2">
					<UserSettingsSolid />
					Settings
				</DropdownItem>
			</DropdownGroup>
			<DropdownHeader
				class="flex cursor-pointer items-center gap-2 hover:bg-gray-100 dark:hover:bg-gray-700"
				onclick={() => logoutUser()}
			>
				<ReplyAllSolid />
				Sign out
			</DropdownHeader>
		</Dropdown>

		<NavUl
			ulClass="pr-2"
			{activeUrl}
			{activeClass}
			{nonActiveClass}
			transition={fly}
			transitionParams={{ y: -20, duration: 250 }}
		>
			<NavLi href="/dashboard">Home</NavLi>
			<NavLi href="/dashboard/configs">Configurations</NavLi>
			<NavLi href="/dashboard/products">Products</NavLi>
		</NavUl>
		<div class="hidden place-content-center rounded-full md:block">
			<DarkMode class="me-2 rounded-full px-3 py-3" />
		</div>
	</section>
</Navbar>

<main class="mx-auto min-h-screen w-full bg-gray-50 px-6 dark:bg-gray-900">
	{@render children()}
</main>

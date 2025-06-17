<script lang="ts" module>
	import { z, ZodError, type ZodIssue } from 'zod';

	// Zod Schema for validating login form data
	const loginSchema = z.object({
		username: z.string().min(1, 'Username is required'),
		password: z.string().min(6, 'Password must be at least 6 characters')
	});

	// API request function to handle sign-in
	const signInRequest = async (data: {
		body: {
			username: string;
			password: string;
		};
	}): Promise<{ access_token: string; token_type: string }> => {
		const body = new URLSearchParams({
			grant_type: 'password',
			username: data.body.username,
			password: data.body.password,
			scope: '',
			client_id: '',
			client_secret: ''
		});

		const response = await fetch(`/api/token`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
				Accept: 'application/json'
			},
			body: body,
			credentials: 'include'
		});

		if (!response.ok) {
			const errorData = await response.json();
			throw new Error(`${errorData.detail || 'Unknown error'}`);
		}

		const tokenData = await response.json();
		return {
			access_token: tokenData.access_token,
			token_type: tokenData.token_type
		};
	};
</script>

<script lang="ts">
	import { goto } from '$app/navigation';
	import Icon from '$components/Icon.svelte';
	import { A, Button, Card, Heading, Input, Label, P, Span, Toast } from 'flowbite-svelte';
	import {
		CheckCircleSolid,
		EyeOutline,
		EyeSlashOutline,
		InfoCircleOutline,
		LockSolid,
		UserCircleSolid,
		ExclamationCircleSolid
	} from 'flowbite-svelte-icons';

	// Login Form State
	let loginForm = $state({
		username: undefined as string | undefined,
		password: undefined as string | undefined,
		errors: {
			username: undefined as undefined | ZodIssue,
			password: undefined as undefined | ZodIssue
		}
	});

	// State for determining if the user is signing in
	let isSigningIn = $state(false);
	// State for showing/hiding password
	let showPassword = $state(false);
	// State for showing/hiding toast notifications
	let showToast = $state(false);
	// State for toast message and type
	let toastMessage = $state('Login successful!');
	let toastType = $state<'error' | 'success'>('success');

	// Function to handle form submission
	const handleSubmit = async (e: Event) => {
		e.preventDefault();

		try {
			const validatedData = loginSchema.parse(loginForm);
			isSigningIn = true;
			await signInRequest({
				body: {
					password: validatedData.password,
					username: validatedData.username
				}
			});

			// On Successful login, show the toast
			toastType = 'success';
			showToast = true;

			setTimeout(() => {
				isSigningIn = false;
			}, 1000); // Simulate a short delay for the toast

			setTimeout(() => {
				goto('/dashboard');
			}, 1000);
		} catch (err) {
			console.error('Error occurred during login:');
			if (err instanceof ZodError) {
				err.errors.forEach((error) => {
					console.error(
						`Zod Error: ${error.code} - ${error.message} on field ${error.path.join('.')}`
					);
					if (error.path.at(0) === 'username') loginForm.errors.username = error;
					else if (error.path.at(0) === 'password') loginForm.errors.password = error;
				});
			} else {
				const error = err as Error;
				console.error(`Error: ${error.message}`);
				toastMessage = error.message || 'An unexpected error occurred. Please try again.';
				toastType = 'error';
				showToast = true;
			}
			setTimeout(() => {
				isSigningIn = false;
			}, 800); // Simulate a short delay for the toast
		} finally {
			setTimeout(() => {
				showToast = false;
			}, 5000); // Hide toast after 3 seconds
		}
	};
</script>

<svelte:head>
	<title>Login - PriceTracker</title>
	<meta name="description" content="Login to your PriceTracker account" />
</svelte:head>

<Toast
	dismissable={false}
	color={toastType === 'success' ? 'emerald' : 'rose'}
	position="top-right"
	toastStatus={showToast}
>
	{#snippet icon()}
		{#if toastType === 'success'}
			<CheckCircleSolid class=" h-6 w-6" />
		{:else}
			<ExclamationCircleSolid class=" h-6 w-6" />
		{/if}
	{/snippet}
	{toastMessage}
</Toast>

<main
	class="flex min-h-screen w-full items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8 dark:bg-gray-900"
>
	{#if isSigningIn}
		<Icon
			name="svg-spinners--blocks-shuffle-3"
			class="text-primary-700 size-80 place-self-center"
		/>
	{:else}
		<div class="w-full max-w-full place-content-center place-items-center space-y-8">
			<!-- Logo/Brand Section -->
			<div class="text-center">
				<Heading tag="h1">PriceTracker</Heading>
				<P align={'center'} class="mt-2 text-gray-600 dark:text-gray-400">
					Track prices across multiple platforms
				</P>
			</div>

			<!-- Login Card -->
			<Card class="p-6 sm:p-8">
				<form class="flex flex-col space-y-6" onsubmit={handleSubmit}>
					<Heading tag="h4" class="text-gray-900 dark:text-white">Sign in to your account</Heading>

					<Label id="username-label">
						<Span italic>Username</Span>
						<Input
							type="text"
							name="username"
							placeholder="Enter your username"
							bind:value={loginForm.username}
							class="ps-10"
						>
							{#snippet left()}
								<UserCircleSolid class="h-5 w-5 text-gray-500 dark:text-gray-400" />
							{/snippet}
						</Input>
						{#if loginForm.errors.username}
							<div class="container mt-1.5 flex items-center gap-1 text-red-600 dark:text-red-400">
								<InfoCircleOutline class="h-6 w-6 " />
								<Span italic class="">
									{loginForm.errors.username.message}
								</Span>
							</div>
						{/if}
					</Label>

					<Label id="password-label">
						<Span italic>Password</Span>
						<Input
							type={showPassword ? 'text' : 'password'}
							name="password"
							placeholder="••••••••"
							required
							bind:value={loginForm.password}
							class="pe-10 ps-10"
						>
							{#snippet left()}
								<LockSolid class="h-5 w-5 text-gray-500 dark:text-gray-400" />
							{/snippet}

							{#snippet right()}
								<button
									type="button"
									onclick={() => (showPassword = !showPassword)}
									class="pointer-events-auto"
								>
									{#if showPassword}
										<EyeSlashOutline class="h-5 w-5 text-gray-500 dark:text-gray-400" />
									{:else}
										<EyeOutline class="h-5 w-5 text-gray-500 dark:text-gray-400" />
									{/if}
								</button>
							{/snippet}
						</Input>
						{#if loginForm.errors.password}
							<div class="container mt-1.5 flex items-center gap-1 text-red-600 dark:text-red-400">
								<InfoCircleOutline class="h-6 w-6 " />
								<Span italic class="">
									{loginForm.errors.password.message}
								</Span>
							</div>
						{/if}
					</Label>

					<div class="flex items-center justify-between">
						<A href="/password-reset" class="text-sm">Forgot password?</A>
					</div>

					<Button type="submit" class="w-full" id="login-button">Sign in</Button>
				</form>
			</Card>
		</div>
	{/if}
</main>

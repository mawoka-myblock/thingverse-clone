<script context="module">
	export const load = ({ page }) => {
		return {
			props: {
				page: page
			}
		};
	};
</script>

<script>
	import { apiurl } from '$lib/stores';
	import { Circle } from 'svelte-loading-spinners';
	import { goto } from '$app/navigation';
	let feedback = '';
	let loggedInSuccessfully = false;
	let loginData = {
		password: '',
		email: ''
	};
	export let page;
	let valid = {
		password: false,
		email: false
	};
	let submitLoading = false;

	const login = async () => {
		submitLoading = true;
		console.log('login');
		const formData = new FormData();
		formData.append('username', loginData.email);
		formData.append('password', loginData.password);
		const res = await fetch(`${apiurl}/api/v1/users/token/cookie`, {
			method: 'POST',
			body: formData
		});
		console.log('HALLO!');
		if (res.status === 200) {
			goto(`${page.query.get('ref')}`);
		} else {
			if (res.status === 401) {
				feedback = 'Wrong email and/or password!';
				
			}
			submitLoading = false
		}
	};
</script>

<div>
	{#if loggedInSuccessfully}
		<div class="h-full absolute w-full bg-black opacity-80 z-10 grid place-items-center">
			<div>
				<Circle size="30" unit="rem"/>
			</div>
			
		</div>
	{/if}
	<div class="h-screen flex">
		<div
			class="w-1/2 bg-gradient-to-tr from-mawoka-300 via-mawoka-200 to-mawoka-100 justify-around items-center hidden lg:flex"
		>
			<div>
				<h1 class="text-white font-bold text-4xl font-sans">ThingWorld</h1>
				<p class="text-white mt-1">The only open-source Thingiverse!</p>
				<a
					href="/internal/about"
					class="block w-28 bg-white text-mawoka-300 mt-4 py-2 rounded-2xl font-bold mb-2 text-center"
					>Read More</a
				>
			</div>
		</div>
		<div class="flex lg:w-1/2 justify-center items-center bg-white w-screen">
			<form class="bg-white" on:submit|preventDefault={login}>
				<h1 class="text-gray-800 font-bold text-2xl mb-1">Hello Again!</h1>
				<p class="text-sm font-normal text-gray-600 mb-7">Welcome Back</p>
				<div class="form-control">
					<label class="input-group input-group-vertical input-group-l">
						<span>Email</span>
						<input
							type="text"
							placeholder="info@site.com"
							class="input input-bordered"
							bind:value={loginData.email}
						/>
					</label>
					<label class="input-group input-group-vertical input-group-l pt-4">
						<span>Password</span>
						<input
							type="password"
							placeholder="Your Password"
							class="input input-bordered"
							bind:value={loginData.password}
						/>
					</label>
				</div>
				{#if submitLoading}
					<button
						type="submit"
						class="w-full bg-gradient-to-r from-mawoka-300 via-mawoka-200 to-mawoka-100 mt-4 py-2 rounded-2xl text-black font-semibold mb-2 flex justify-center"
						><Circle size="1.5" unit="rem" color="#000000" /></button
					>
				{:else}
					<button
						type="submit"
						class="block w-full bg-gradient-to-r from-mawoka-300 via-mawoka-200 to-mawoka-100 mt-4 py-2 rounded-2xl text-black font-semibold mb-2"
						>Login</button
					>
				{/if}
				<span>
					<p class="text-red-600 ml-2">{feedback}</p>
				</span>
				<span
					><a href="/account/reset-password" class="text-sm ml-2 hover:text-blue-500 cursor-pointer"
						>Forgot Password?</a
					></span
				>
				<span
					><a href="/account/register" class="text-sm ml-2 hover:text-blue-500 cursor-pointer"
						>Don't have an account?</a
					></span
				>
			</form>
		</div>
	</div>
</div>

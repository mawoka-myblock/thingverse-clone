<script>
	import { apiurl } from '$lib/stores';
	import { Circle } from 'svelte-loading-spinners';
	import { goto } from '$app/navigation';
	import passwordChecker from 'zxcvbn';
	import tippy from 'sveltejs-tippy';

	let feedback = '';
	let registerData = {
		password1: '',
		password2: '',
		username: '',
		email: ''
	};
	let dataValid = {
		password1: false,
		password2: false,
		username: false,
		email: false
	};
	let submitLoading = false;
	let passwordFeedback = '';
	let errorModalOpen = false;
	let successModalOpen = false;

	const checkPasswordStrength = (password) => {
		let result = passwordChecker(password);
		if (result.score >= 3) {
			dataValid.password1 = true;
			passwordFeedback = '';
		} else {
			dataValid.password1 = false;
			passwordFeedback =
				'To crack your password, it would take ' +
				result.crack_times_display.offline_slow_hashing_1e4_per_second;
			console.log(passwordFeedback);
		}
	};

	$: dataValid.email =
		/^([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x22([^\x0d\x22\x5c\x80-\xff]|\x5c[\x00-\x7f])*\x22)(\x2e([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x22([^\x0d\x22\x5c\x80-\xff]|\x5c[\x00-\x7f])*\x22))*\x40([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x5b([^\x0d\x5b-\x5d\x80-\xff]|\x5c[\x00-\x7f])*\x5d)(\x2e([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x5b([^\x0d\x5b-\x5d\x80-\xff]|\x5c[\x00-\x7f])*\x5d))*$/.test(
			registerData.email
		);
	$: dataValid.password2 =
		registerData.password1 === registerData.password2 && registerData.password2.length !== 0
			? true
			: false;
	$: dataValid.username =
		registerData.username.length >= 5 && registerData.username.length <= 32 ? true : false;

	$: checkPasswordStrength(registerData.password1);

	const register = async () => {
		if (!Object.values(dataValid).every(Boolean)) {
		}
		submitLoading = true;
		const res = await fetch(`${apiurl}/api/v1/users/create`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				username: registerData.username,
				password: registerData.password1,
				email: registerData.email
			})
		});
		if (res.status === 400) {
			errorModalOpen = true;
			registerData = {
				password1: '',
				password2: '',
				username: '',
				email: ''
			};
			dataValid = {
				password1: false,
				password2: false,
				username: false,
				email: false
			};
			passwordFeedback = '';

			
		} else if (res.status === 200) {
			successModalOpen = true
		}
		submitLoading = false
	};
</script>

<div>
	<div id="error-modal" class="modal" class:modal-open={errorModalOpen}>
		<div class="modal-box">
			<p>
				The username or the email you chose already exists. Try creating your account with a new
				mail-address or another username!
			</p>
			<div class="modal-action">
				<button
					class="btn"
					on:click={() => {
						errorModalOpen = false;
					}}>Close</button
				>
			</div>
		</div>
	</div>
	<div id="success-modal" class="modal" class:modal-open={successModalOpen}>
		<div class="modal-box">
			<p>
				You created your account successfully, so please click on the link in the email you should
				have received! After that, you can log in.
			</p>
			<div class="modal-action">
				<button
					class="btn"
					on:click={() => {
						goto('/account/login');
					}}>Close</button
				>
			</div>
		</div>
	</div>

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
			<form class="bg-white" on:submit|preventDefault={register}>
				<h1 class="text-gray-800 font-bold text-2xl mb-1">Nice to meet you!</h1>
				<p class="text-sm font-normal text-gray-600 mb-7">Feel like home!</p>
				<div class="form-control w-full">
					<label class="input-group input-group-vertical input-group-l">
						<span>Email</span>
						<input
							type="text"
							placeholder="info@site.com"
							class="input input-bordered"
							class:input-error={!dataValid.email}
							bind:value={registerData.email}
						/>
					</label>
					<label class="input-group input-group-vertical input-group-l pt-4">
						<span>Username</span>
						<input
							type="text"
							placeholder="HansWurst"
							class="input input-bordered"
							class:input-error={!dataValid.username}
							bind:value={registerData.username}
						/>
					</label>
					<label class="input-group input-group-vertical input-group-l pt-4">
						<span>Password</span>
						<input
							type="password"
							placeholder="Your Password"
							class="input input-bordered"
							class:input-error={!dataValid.password1}
							bind:value={registerData.password1}
						/>
					</label>
					<span>
						<p class="text-red-600 ml-2 w-full text-center">{passwordFeedback}</p>
					</span>
					<label class="input-group input-group-vertical input-group-l pt-4">
						<span>Repeat Password</span>
						<input
							type="password"
							placeholder="Your Password, again!"
							class="input input-bordered"
							class:input-error={!dataValid.password2}
							bind:value={registerData.password2}
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
						disabled={!Object.values(dataValid).every(Boolean)}
						class:grayscale={!Object.values(dataValid).every(Boolean)}
						type="submit"
						class="block w-full bg-gradient-to-r from-mawoka-300 via-mawoka-200 to-mawoka-100 mt-4 py-2 rounded-2xl text-black font-semibold mb-2"
						>Register</button
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
					><a href="/account/login?ref=/" class="text-sm ml-2 hover:text-blue-500 cursor-pointer"
						>Already have an account?</a
					></span
				>
			</form>
		</div>
	</div>
</div>

<script>
	import { apiurl } from '$lib/stores';
	import { Circle } from 'svelte-loading-spinners';
	import { goto } from '$app/navigation';

	let url = '';
	const getUserData = async () => {
		const res = await fetch(`${apiurl}/api/v1/users/me`);
		if (res.status !== 200) {
			goto('/account/login?ref=' + window.location.href);
		}
		const json = await res.json();
		return json;
	};

	const getUserAvatar = async (email) => {
		const utf8 = new TextEncoder().encode(email);
		const hashBuffer = await crypto.subtle.digest('SHA-256', utf8);
		const hashArray = Array.from(new Uint8Array(hashBuffer));
		const hashHex = hashArray.map((bytes) => bytes.toString(16).padStart(2, '0')).join('');
		return 'https://seccdn.libravatar.org/avatar/' + hashHex;
	};
</script>

{#await getUserData()}
	<div class="h-full absolute w-full bg-black opacity-80 z-10 grid place-items-center">
		<div>
			<Circle size="30" unit="rem" />
		</div>
	</div>
{:then userdata}
	<div>
		<div class="grid grid-cols-4 mt-8 grid-flow-row auto-rows-max">
			<div class="col-start-2 col-end-3">
				<h1 class="text-3xl">Hello, {userdata.username}</h1>
			</div>
			<div class="col-start-2 mt-8">
				<p><a href="/accounts/collections">Your Collections</a></p>
			</div>
		</div>
	</div>
{/await}

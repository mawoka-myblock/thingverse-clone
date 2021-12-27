<script context="module">
	import { apiurl } from '$lib/stores';
	export const load = async ({ page: { params }, fetch }) => {
		const { slug } = params;
		const res = await fetch(`${apiurl}/api/v1/things/thing/${slug}`);

		if (res.status === 404 || res.status === 400) {
			return { status: 404, error };
		} else {
			const data = await res.json();
			const user = await fetch(`${apiurl}/api/v1/users/user/${data.user_id}`);

			return { props: { thing: data, user: await user.json() } };
		}
	};
</script>

<script>
	export let thing;
	export let user;
	import { marked, options } from 'marked';
	import {onMount} from "svelte"
	import sanitizeHtml from 'sanitize-html';
	import Navbar from '$lib/navbar.svelte';
	import { DateTime } from 'luxon';
	import { Circle } from 'svelte-loading-spinners';
	import { goto } from '$app/navigation';
	import 'swiper/css';
	import { Swiper, SwiperSlide } from 'swiper/svelte';
	import tippy from 'sveltejs-tippy';
	import { loggedin } from '$lib/stores';
	let selectedCol;
	let createCol;
	let url = ""
	onMount(() => (url = window.location.href));
	console.log($loggedin)
	const getCollectionsFunc = async () => {
		const res = await fetch(`${apiurl}/api/v1/collections/my`);
		if (res.status !== 200) {
			goto('/account/login?ref=', url);
		}
		return await res.json();
	};

	let getCollections = getCollectionsFunc()
	const prettyfyDate = (date) => {
		const dt = DateTime.fromISO(date);
		let minute;
		if (dt.minute <= 9) {
			minute = `0${dt.minute}`;
		} else {
			minute = dt.minute;
		}
		return `${dt.day}.${dt.month}.${dt.year} at ${dt.hour}:${minute}`;
		//const time = date.substring(11)
		//const datum = date.substring(0, 10)
		// return `${datum} um ${time}`
	};

	const createNewCollection = async () => {
		const res = await fetch(`${apiurl}/api/v1/collections/create`, {
			method: "POST",
			body: JSON.stringify({name: createCol})
		})
		if (res.status === 401) {
			goto('/account/login?ref=', url);
		}
		console.log("Created new Collection")
		getCollections = getCollectionsFunc()
	}
	const addToCollection = async () => {
		const res = await fetch(`${apiurl}/api/v1/collections/${selectedCol}/update?thing=${thing._id}`, {
			method: "PUT",
		})
		if (res.status === 401) {
			goto('/account/login?ref=', url);
		}

	}
	loggedin.subscribe(value => {console.log("val", value)})
	$: console.log(selectedCol)
</script>

<Navbar />
<div class="pt-20">
	<section>
		<h1 class="text-4xl text-center font-bold">{thing.title}</h1>
		<p class="text-center">
			By: <a class="text-center underline" href={`/user/${thing.user_id}`}>{user.username}</a>
		</p>
	</section>
	<section>
		<div class="grid lg:grid-cols-4 pt-8 lg:px-16 grid-cols-2 ">
			<div class="col-span-2 row-span-3 border-slate-200 border-2 rounded-lg">
				<Swiper spaceBetween={50} slidesPerView={1}>
					{#each thing.pictures as pic_url}
						<SwiperSlide>
							<img src={pic_url} loading="lazy" alt="Model" />
						</SwiperSlide>
					{/each}
				</Swiper>
			</div>
			<div class="pl-4">
				<div
					class="grid grid-cols-1 divide-y leading-6 rounded-lg shadow-lg overflow-hidden border-slate-200 border-2"
				>
					<p class="p-2">Likes: {thing.like_count}</p>
					<p class="p-2">Comments: {thing.comment_count}</p>
					<p class="p-2">Makes: {thing.make_count}</p>
					<p class="p-2">Remixes: {thing.remixes}</p>
					<p class="p-2">Downloads: {thing.downloads}</p>
					<p class="p-2" use:tippy={{ content: 'DD.MM.YYYY at HH:MM' }}>
						Created on: {prettyfyDate(thing.creation_date)}
					</p>
				</div>
			</div>
			<div>
				<div class="grid grid-cols-2 pl-4">
					<a
						class="btn col-span-2"
						href={`${apiurl}/api/v1/cdn/download/${user.username}/${thing.file}`}>Download</a
					>
					<!-- {#if $loggedin} -->
					{#if true}
						{#await getCollections}
							<div class="text-center flex justify-center">
								<div>
									<Circle size="1" unit="rem" />
								</div>
							</div>
						{:then cols}
							{#if cols.length === 0}
								<div class="pt-8 col-span-2">
									<form on:submit|preventDefault={createNewCollection} class="grid grid-cols-2 grid-rows-1 gap-2">
										<input bind:value={createCol} type="text" placeholder="Whatever you like!" class="input input-bordered" />
										<button type="submit" class="btn">Create!</button>
									</form>
									
								</div>
							{:else}
							
								<div class="pt-8 col-span-2">
									<form on:submit|preventDefault={addToCollection} class="grid grid-cols-2 grid-rows-1 gap-2">
										<select bind:value={selectedCol} class="">
											<!-- <option disabled="disabled" selected="selected">Choose</option> -->
											{#each cols as col}
												<option value={col._id} class="text-black">{col.name}</option>
											{/each}
										</select>
										<button type="submit" class="btn">Add!</button>
									</form>
									
								</div>
							{/if}
						{/await}
					{/if}
				</div>
			</div>
			<div
				class="ml-4 rounded-lg shadow-lg overflow-hidden w-full h-full col-span-2 row-span-2 mt-8 border-slate-200 border-2"
			>
				<article class="prose w-full h-full ml-4">
					{@html sanitizeHtml(marked(thing.description))}
				</article>
			</div>
		</div>
	</section>
</div>

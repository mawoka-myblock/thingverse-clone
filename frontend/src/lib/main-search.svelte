<script>
	import { apiurl } from '$lib/stores';
	let results = { hits: [] };
	let searchTerm = '';
	let results_available = false;
    let search_count = -1

	const handle = (term) => {
        if (search_count >= search_count)
		fetch(`${apiurl}/api/v1/search/things?query=${term}&query_by=title,description`)
			.then((response) => response.json())
			.then((data) => (results = data));
		results_available = results.found != 0;
        search_count = search_count+1
	};
	$: {
		handle(searchTerm);
	}
</script>

<div class="flex justify-center">
	<input
		type="text"
		placeholder="Search"
		class="input input-bordered w-9/12 text-center h-20 text-2xl"
		bind:value={searchTerm}
	/>
</div>
<div class="flex justify-center">
	{#if results_available && search_count >= 1 && searchTerm !== ""}
		{#each results.hits as hit}
			<ul class="bg-white border border-gray-100 w-9/12 mt-2">
				<li
					class="pl-4 pr-2 py-1 border-b-2 border-gray-100 relative cursor-pointer hover:bg-yellow-50 hover:text-gray-900 w-full"
				><a href={`/thing/${hit.document.id}`} class="w-full block">{hit.document.title}</a>
			</ul>
		{/each}
	{:else if search_count === 0}
		<p>Please start searching!</p>
	{/if}
</div>

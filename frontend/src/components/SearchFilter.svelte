<script lang="ts">
import Fuse, {type IFuseOptions} from "fuse.js";
import {Search, type SearchProps} from 'flowbite-svelte';




interface SearchFilterProps extends SearchProps {
    searchOptions: IFuseOptions<any>;
    searchData: any[];
}

let props: SearchFilterProps = $props();



</script>


<Search {...props} >

</Search>

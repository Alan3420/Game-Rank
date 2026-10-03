<template>
    <nav v-if="totalPages > 1" class="pagination-bar" aria-label="Pagination">
        <button
            type="button"
            class="page-btn page-nav"
            :disabled="currentPage === 1"
            @click="cambiarPagina(currentPage - 1)"
            aria-label="Previous page"
        >
            <i aria-hidden="true" class="pi pi-chevron-left"></i>
        </button>

        <template v-for="(item, i) in paginasVisibles" :key="i">
            <span v-if="item === '...'" class="page-ellipsis">…</span>
            <button
                v-else
                type="button"
                class="page-btn"
                :class="{ 'is-active': currentPage === item }"
                :aria-current="currentPage === item ? 'page' : null"
                :aria-label="'Page ' + item"
                @click="cambiarPagina(item)"
            >{{ item }}</button>
        </template>

        <button
            type="button"
            class="page-btn page-nav"
            :disabled="currentPage === totalPages"
            @click="cambiarPagina(currentPage + 1)"
            aria-label="Next page"
        >
            <i aria-hidden="true" class="pi pi-chevron-right"></i>
        </button>
    </nav>
</template>


<script>
import pagination from "./script_pagination.js";

export default {
    name: "Pagination",
    ...pagination
};
</script>

<style scoped src="./style_pagination.css"></style>

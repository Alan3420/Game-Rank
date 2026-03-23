<template>
    <div class="content-overview">
        <h1>Contenido Principal</h1>
    </div>
</template>

<script>
import { getContentOverview } from "../services/content_service";

export default {
    data() {
        return {
            contentOverview: null
        }
    },
    async mounted() {
        try {
            this.contentOverview = await getContentOverview;
        } catch (error) {
            console.error('Error fetching content overview:', error);
        }
    }
}

</script>


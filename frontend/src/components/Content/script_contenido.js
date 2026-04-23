import { getContentOverview } from "../../services/resume_cards";
import { getContentByName } from "../../services/buscar"

export default {
    name : "contenido",
    data() {
        return {
            games: [],
            game_name: null,
            page: 1,
            per_page: 10,
            loading: false,
            hasNext: true,
            maxGames: 200,
            showLoadMoreButton: false,
            apiCallCount: 0
        }
    },
    mounted() {
        this.getContent();
        this.debouncedScroll = this.debounce(this.handleScroll, 500)
        window.addEventListener("scroll", this.debouncedScroll);

    },
    beforeUnmount() {
        window.removeEventListener("scroll", this.debouncedScroll);
    },


    methods: {
        async getContent() {
            if (this.loading || !this.hasNext || this.games.length >= this.maxGames) return;

            this.loading = true;

            try {
                const response = await getContentOverview(this.page, this.game_name);

                this.games = [...this.games, ...response.games];

                this.hasNext = !!response.next;

                this.page++;
                this.apiCallCount++;

                if (this.apiCallCount >= 2) {
                    this.showLoadMoreButton = true;
                    window.removeEventListener("scroll", this.debouncedScroll);
                }

            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false;
            }
        },


        async getContentCard() {
            try {
                if (!this.game_name || this.game_name.trim() === '') {
                    alert("Escribe un nombre de juego")
                    return
                }
                const response = await getContentByName(this.game_name)
                alert(`Resultados: ${JSON.stringify(response)}`)
                console.log(response)
            } catch (error) {
                console.error("ERRORS:", error)
            }
        },

        handleScroll() {
            const scrollTop = window.scrollY;
            const windowHeight = window.innerHeight;
            const fullHeight = document.documentElement.scrollHeight;


            if (this.apiCallCount < 2 && scrollTop + windowHeight >= fullHeight - 1000) {
                this.getContent();
            }
        },

        loadMore() {
            this.getContent();
        },

        goToDetail(gameId) {
            this.$router.push(`/game/${gameId}`);
        },

        debounce(fn, delay) {
            let timer = null
            return function (...args) {
                clearTimeout(timer)
                timer = setTimeout(() => fn.apply(this, args), delay)
            }
        }
    }
}

// Barra de paginacion que se usa en el catalogo, en los proximos
// lanzamientos del Home y en la lista de favoritos del perfil.
// El padre controla la pagina actual con v-model:current-page.
export default {

    props: {
        currentPage: {
            type: Number,
            required: true
        },
        totalPages: {
            type: Number,
            required: true
        }
    },

    emits: ["update:currentPage"],

    computed: {

        // Cuando hay pocas paginas las mostramos todas; si hay muchas
        // dejamos 1, los vecinos de la actual y la ultima, con "..."
        // de separador para que se vea el salto.
        paginasVisibles() {

            var total = this.totalPages;
            var actual = this.currentPage;

            if (total <= 7) {
                var todas = [];
                for (var i = 1; i <= total; i++) {
                    todas.push(i);
                }
                return todas;
            }

            var conjunto = new Set();
            conjunto.add(1);
            conjunto.add(total);

            var inicio = actual - 2;
            if (inicio < 2) {
                inicio = 2;
            }
            var fin = actual + 2;
            if (fin > total - 1) {
                fin = total - 1;
            }
            for (var k = inicio; k <= fin; k++) {
                conjunto.add(k);
            }

            var ordenado = Array.from(conjunto).sort(function (a, b) {
                return a - b;
            });

            var resultado = [];
            for (var j = 0; j < ordenado.length; j++) {
                if (j > 0 && ordenado[j] - ordenado[j - 1] > 1) {
                    resultado.push('...');
                }
                resultado.push(ordenado[j]);
            }
            return resultado;
        }
    },

    methods: {

        cambiarPagina(pagina) {
            if (pagina < 1) {
                return;
            }
            if (pagina > this.totalPages) {
                return;
            }
            if (pagina === this.currentPage) {
                return;
            }
            this.$emit("update:currentPage", pagina);
        }
    }
};

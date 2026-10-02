// Clase del sello de Metacritic, la misma en todo el mundo de cartas:
// verde desde 80, amarillo desde 50, rojo por debajo y "na" sin nota.
export function claseMetacritic(score) {
    if (!score && score !== 0) {
        return 'mc-na';
    }
    if (score >= 80) {
        return 'mc-green';
    }
    if (score >= 50) {
        return 'mc-yellow';
    }
    return 'mc-red';
}

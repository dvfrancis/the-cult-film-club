// Make sure allFilters is available in your context!
const allFilters = JSON.parse(document.getElementById('all-filters-data').textContent);

function updateDropdowns() {
    const genreSelect = document.getElementById('genre-select');
    const subgenreSelect = document.getElementById('subgenre-select');
    const directorSelect = document.getElementById('director-select');
    const decadeSelect = document.getElementById('decade-select');
    const genre = genreSelect.value;
    const subgenre = subgenreSelect.value;
    const director = directorSelect.value;
    const decade = decadeSelect.value;

    // GENRES
    const genres = [...new Set(
        allFilters
        .filter(f =>
            (!subgenre || f.subgenre === subgenre) &&
            (!director || f.director === director) &&
            (!decade || String(f.decade) === decade)
        )
        .map(f => f.genre)
        .filter(Boolean)
    )].sort();
    genreSelect.innerHTML = '<option value="">All Genres</option>' +
        genres.map(g => `<option value="${g}"${g === genre ? ' selected' : ''}>${g}</option>`).join('');

    // SUBGENRES
    const subgenres = [...new Set(
        allFilters
        .filter(f =>
            (!genre || f.genre === genre) &&
            (!director || f.director === director) &&
            (!decade || String(f.decade) === decade)
        )
        .map(f => f.subgenre)
        .filter(Boolean)
    )].sort();
    subgenreSelect.innerHTML = '<option value="">All Subgenres</option>' +
        subgenres.map(s => `<option value="${s}"${s === subgenre ? ' selected' : ''}>${s}</option>`).join('');

    // DIRECTORS
    const directors = [...new Set(
        allFilters
        .filter(f =>
            (!genre || f.genre === genre) &&
            (!subgenre || f.subgenre === subgenre) &&
            (!decade || String(f.decade) === decade)
        )
        .map(f => f.director)
        .filter(Boolean)
    )].sort();
    directorSelect.innerHTML = '<option value="">All Directors</option>' +
        directors.map(d => `<option value="${d}"${d === director ? ' selected' : ''}>${d}</option>`).join('');

    // DECADES
    const decades = [...new Set(
        allFilters
        .filter(f =>
            (!genre || f.genre === genre) &&
            (!subgenre || f.subgenre === subgenre) &&
            (!director || f.director === director)
        )
        .map(f => f.decade)
        .filter(Boolean)
    )].sort((a, b) => a - b);
    decadeSelect.innerHTML = '<option value="">All Decades</option>' +
        decades.map(d => `<option value="${d}"${String(d) === decade ? ' selected' : ''}>${d}s</option>`).join('');
}

document.addEventListener('DOMContentLoaded', function () {
    const genreSelect = document.getElementById('genre-select');
    const subgenreSelect = document.getElementById('subgenre-select');
    const directorSelect = document.getElementById('director-select');
    const decadeSelect = document.getElementById('decade-select');
    const resetBtn = document.getElementById('reset-filters-btn');

    genreSelect.addEventListener('change', function () {
        document.getElementById('filter-form').submit();
    });
    subgenreSelect.addEventListener('change', function () {
        document.getElementById('filter-form').submit();
    });
    directorSelect.addEventListener('change', function () {
        document.getElementById('filter-form').submit();
    });
    decadeSelect.addEventListener('change', function () {
        document.getElementById('filter-form').submit();
    });
    resetBtn.addEventListener('click', function (e) {
        e.preventDefault();
        genreSelect.value = '';
        subgenreSelect.value = '';
        directorSelect.value = '';
        decadeSelect.value = '';
        document.getElementById('filter-form').submit();
    });
});
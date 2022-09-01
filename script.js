const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;
// https://stackoverflow.com/questions/14267781/sorting-html-table-with-javascript/53880407#53880407
const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
    )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

// do the work...
document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
    const table = th.closest('table');
    const tbody = table.querySelector('tbody');

    // add up arrow for last clicked th if ascending, down arrow if descending
    //  remove previous arrows
    document.querySelectorAll('th').forEach(th => {
        th.innerHTML = th.innerHTML.replace("▲", "");
        th.innerHTML = th.innerHTML.replace("▼", "");
    });
    th.innerHTML += this.asc ? " &#9660;" : " &#9650;";
    // breed ▼ ▲ ▼ ▲ ▼ ▲
    Array.from(tbody.querySelectorAll('tr'))
      .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
      .forEach(tr => tbody.appendChild(tr) );
})));




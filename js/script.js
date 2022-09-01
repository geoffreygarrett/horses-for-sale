// const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

// getCellValue returns "data-sort-value" attribute if it exists, otherwise returns the innerText
const getCellValue = (tr, idx) => tr.children[idx].getAttribute('data-sort-value') || tr.children[idx].innerText || tr.children[idx].textContent;

// https://stackoverflow.com/questions/14267781/sorting-html-table-with-javascript/53880407#53880407
const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
    )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));



// for 'listing age' column, convert the integer value of days to format '<X> <unit>'s ago for the largest unit for the 10th column
function largestUnit(days) {
    const units = ['year', 'month', 'week', 'day'];
    const unitValues = [365, 30, 7, 1];
    for (let i = 0; i < units.length; i++) {
        if (days >= unitValues[i]) {
            const unit = units[i];
            const value = Math.floor(days / unitValues[i]);
            return value + " " + unit + (value > 1 ? "s" : "");
        }
    }
    return "today";
}

const formatAge = (days) => {
    return days === 0 ? "today" : largestUnit(days);
}

const formatPrice = (price) => {
    // formats price as 'kR <thousands>'
    // if price cannot be converted to integer, return 'Not mentioned'
    const intValue = parseInt(price);
    if (isNaN(intValue)) {
        return "Not mentioned";
    }
    const thousands = Math.floor(intValue / 1000);
    return "kR " + thousands;
}


const formatTimeDelta = (seconds) => {
    // format seconds in 'hour' h, 'minute' m, if hours > 0, otherwise 'minute' m
    // priorize hours over minutes
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const hourString = hours > 0 ? hours + " h " : "";
    const minuteString = minutes > 0 ? minutes + " m" : "";
    return hourString + minuteString;

}

const addFilter = () => {
    // add filter to column by name in innerText
    // add a drop down to all column names found in headers, adding a min and max fields
    // add a button to apply the filter
    // add a button to clear the filter
    // add a button to clear all filters
    const table = document.querySelector('table');
    const thead = table.querySelector('thead');
    const headers = thead.querySelectorAll('th');
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');
    const filterDiv = document.createElement('div');
    filterDiv.setAttribute('id', 'filter-div');
    const filterTable = document.createElement('table');
    filterTable.setAttribute('id', 'filter-table');
    const filterTableBody = document.createElement('tbody');
    filterTableBody.setAttribute('id', 'filter-table-body');
    filterTable.appendChild(filterTableBody);
    filterDiv.appendChild(filterTable);
    const filterButtonDiv = document.createElement('div');
    filterButtonDiv.setAttribute('id', 'filter-button-div');
    const filterButton = document.createElement('button');
    filterButton.setAttribute('id', 'filter-button');
    filterButton.innerText = "Filter";
    filterButtonDiv.appendChild(filterButton);
    const clearFilterButton = document.createElement('button');
    clearFilterButton.setAttribute('id', 'clear-filter-button');
    clearFilterButton.innerText = "Clear Filter";
    filterButtonDiv.appendChild(clearFilterButton);
    const clearAllFiltersButton = document.createElement('button');
    clearAllFiltersButton.setAttribute('id', 'clear-all-filters-button');
    clearAllFiltersButton.innerText = "Clear All Filters";
    filterButtonDiv.appendChild(clearAllFiltersButton);
    filterDiv.appendChild(filterButtonDiv);
    const filterDivContainer = document.createElement('div');
    filterDivContainer.setAttribute('id', 'filter-div-container');
    filterDivContainer.appendChild(filterDiv);
    table.parentNode.insertBefore(filterDivContainer, table);
    for (let i = 0; i < headers.length; i++) {
        const header = headers[i];
        const headerText = header.innerText;
        const row = document.createElement('tr');
        const headerCell = document.createElement('td');
        headerCell.innerText = headerText;
        row.appendChild(headerCell);
        const minCell = document.createElement('td');
        const minInput = document.createElement('input');
        minInput.setAttribute('id', 'min-' + headerText);
        minInput.setAttribute('type', 'text');
        minCell.appendChild(minInput);
        row.appendChild(minCell);
        const maxCell = document.createElement('td');
        const maxInput = document.createElement('input');
        maxInput.setAttribute('id', 'max-' + headerText);
        maxInput.setAttribute('type', 'text');
        maxCell.appendChild(maxInput);
        row.appendChild(maxCell);
        filterTableBody.appendChild(row);
    }
    const filter = () => {
        for (let i = 0; i < headers.length; i++) {
            const header = headers[i];
            const headerText = header.innerText;
            const minInput = document.querySelector('#min-' + headerText);
            const maxInput = document.querySelector('#max-' + headerText);
            const min = minInput.value;
            const max = maxInput.value;
            for (let j = 0; j < rows.length; j++) {
                const row = rows[j];
                const cell = row.children[i];
                // value is 'data-sort-value' if it exists, otherwise innerText
                const value = cell.getAttribute('data-sort-value') || cell.innerText;
                if (min !== '' && value < min) {
                    row.style.display = 'none';
                } else if (max !== '' && value > max) {
                    row.style.display = 'none';
                } else {
                    row.style.display = 'table-row';
                }
            }
        }
    }
    const clearFilter = () => {
        for (let i = 0; i < headers.length; i++) {
            const header = headers[i];
            const headerText = header.innerText;
            const minInput = document.querySelector('#min-' + headerText);
            const maxInput = document.querySelector('#max-' + headerText);
            minInput.value = '';
            maxInput.value = '';
        }
        for (let j = 0; j < rows.length; j++) {
            const row = rows[j];
            row.style.display = 'table-row';
        }
    }
    const clearAllFilters = () => {
        clearFilter();
        filterDivContainer.style.display = 'none';
    }
    filterButton.addEventListener('click', filter);
    clearFilterButton.addEventListener('click', clearFilter);
    clearAllFiltersButton.addEventListener('click', clearAllFilters);
}




const changeColumnFormat = (columnIndex, formatFunction) => {
    // change the format of the column at columnIndex to formatFunction and store the original value in data-sort-value
    const table = document.querySelector('table');
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');
    for (let i = 0; i < rows.length; i++) {
        // if type can be converted to integer, convert it
        const value = rows[i].children[columnIndex].innerText;
        const intValue = parseInt(value);
        const formattedValue = isNaN(intValue) ? formatFunction(value) : formatFunction(intValue);
        rows[i].children[columnIndex].setAttribute('data-sort-value', value);
        rows[i].children[columnIndex].innerText = formattedValue;
    }
}



// change the format of the 'listing age' column to '<X> <unit>'s ago'
changeColumnFormat(9, formatAge);
changeColumnFormat(7, formatTimeDelta);
changeColumnFormat(6, formatPrice);

// do the work...
document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
    const table = th.closest('table');
    const tbody = table.querySelector('tbody');

    // remove previous arrows
    document.querySelectorAll('th').forEach(th => {
        th.innerHTML = th.innerHTML.replace("▲", "");
        th.innerHTML = th.innerHTML.replace("▼", "");
    });
    // add up arrow for last clicked th if ascending, down arrow if descending
    th.innerHTML += this.asc ? " &#9660;" : " &#9650;";

    // sort the table by the column of the clicked th
    Array.from(tbody.querySelectorAll('tr'))
      .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
      .forEach(tr => tbody.appendChild(tr) );
})));


// update the 10th column with the formatted value, excluding the header row
// document.querySelectorAll('tr').forEach(tr => {
//     const td = tr.children[9];
//     if (td) {
//         // take value and save it as sort value
//         const value = td.innerText;
//         td.setAttribute("data-sort-value", value);
        
//         // if type can be converted to integer, convert it
//         const days = parseInt(td.innerText);
//         if (!isNaN(days)) {
//             td.innerText = largestUnit(days);
//         }
//     }
// });


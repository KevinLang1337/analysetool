// Sort rows in table by date onclick, use i to toggle order
var i;
function sortByDate(n){
    var tbody = document.querySelector("#source_table tbody");
    var rows = [].slice.call(tbody.querySelectorAll("tr"));

    // Sorting table rows ascending
    if (i!=1){
    rows.sort(function(a,b){
        return convertDate(a.cells[n].innerHTML)-convertDate(b.cells[n].innerHTML);

    });
    i = 1;
}
    // Sorting table rows descending
    else {
        rows.sort(function(a,b){
            return convertDate(b.cells[n].innerHTML)-convertDate(a.cells[n].innerHTML);
    
        });
        i = 0;
    }
    rows.forEach(function(v){
        tbody.appendChild(v);
    })
}
// Convert date to YYYYMMDD
function convertDate(date) {
    
    var dateConverted = date.split(".");
    // If there is no date, return 0 so the source is treated as newest
    if(date==""){
        return "0" 
    }
    else return +(dateConverted[2]+dateConverted[1]+dateConverted[0]);
}
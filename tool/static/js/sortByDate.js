var i;
function sortByDate(n){
    var tbody = document.querySelector("#source_table tbody");
    var rows = [].slice.call(tbody.querySelectorAll("tr"));

    if (i!=1){
    rows.sort(function(a,b){
        return convertDate(a.cells[n].innerHTML)-convertDate(b.cells[n].innerHTML);

    });
    i = 1;
}
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

function convertDate(date) {
    
    var dateConverted = date.split(".");
    if(date==""){
        return "0" 
    }
    else return +(dateConverted[2]+dateConverted[1]+dateConverted[0]);
}
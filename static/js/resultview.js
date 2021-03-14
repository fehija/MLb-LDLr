let newQueryArray = [];
let deletedQueries = [];
document.addEventListener("DOMContentLoaded", function (event) {
    let queryIndex = sessionStorage.length;
    //Insertamos en el sessionStorage el array de queries
    for (let i = 0; i < queryArray.length; i++){
        sessionStorage.setItem('query'+ (queryIndex+i), JSON.stringify(queryArray[i]));
    }
    //Creamos un array con las query del sessionStorage para operar con él
    for(let x = 0; x < sessionStorage.length; x++){
        let dataQuery = sessionStorage.getItem('query'+x);
        newQueryArray.push(JSON.parse(dataQuery)); 
    }
    if (sessionStorage.length > 0){
        //Creamos el h2
        titleH2Div = document.createElement("div");
        titleH2Div.id = 'titleH2Div';
        titleH2Div.classList.add('titleH2Div');
        document.getElementById('list').appendChild(titleH2Div);
        let titlenoresults = document.createElement("h2");
        document.getElementById('titleH2Div').appendChild(titlenoresults);
        titlenoresults.textContent = "Executed queries:";
        //Creamos el botón de reseteo (delete all)
        let deleteAllButton = document.createElement("button");
        deleteAllButton.type = 'button';
        deleteAllButton.id = 'deleteall';
        deleteAllButton.className = 'btn btn-outline-dark btn-sm';
        deleteAllButton.textContent = 'Delete all';
        document.getElementById('titleH2Div').appendChild(deleteAllButton);
        deleteAllButton.addEventListener('click', deleteAllItems  => { 
            if (document.getElementsByClassName('result-item').length !== 0){
                //Eliminamos la búsqueda y vaciamos newQueryArray
                let deleteThisItem = document.getElementById('allResultsDiv');
                deleteThisItem.parentNode.removeChild(deleteThisItem);
                newQueryArray = [];
                noResults();
            } 
        });
        allResultsDiv = document.createElement("div");
        allResultsDiv.id = "allResultsDiv";
        document.getElementById('list').appendChild(allResultsDiv);
        for(let i = newQueryArray.length - 1; i >= 0 ; i--){
            //Creamos el div, el h3 y la lista
            let divResult = document.createElement("div");
            divResult.id = 'result' + i;
            divResult.classList.add('result-item');
            document.getElementById('allResultsDiv').appendChild(divResult);
            titleDiv = document.createElement("div");
            titleDiv.id = 'titleDiv' + i;
            titleDiv.classList.add('titleDiv');
            document.getElementById('result' + i).appendChild(titleDiv);
            let titleResult = document.createElement("h3");
            titleResult.classList.add('h5');
            titleResult.textContent = 'Query number '+ (i+1);
            document.getElementById('titleDiv' + i).appendChild(titleResult);
            let listResult = document.createElement("ul");
            listResult.id = 'list' + i;
            document.getElementById('result' + i).appendChild(listResult);
            //Creamos un li por cada valor del objeto (de la query)
            let data = newQueryArray[i];
            for (const [key, value] of Object.entries(data)) {
                let listResultItem = document.createElement("li");     
                listResultItem.textContent = key +': '+ value;
                listResult.append(listResultItem);
                document.getElementById('list' + i).appendChild(listResultItem);
            }
            //Creamos el botón de delete
            let deleteButton = document.createElement("button");
            deleteButton.type = 'button';
            deleteButton.id = i;
            deleteButton.className = 'btn btn-outline-dark btn-sm';
            deleteButton.textContent = 'Delete';
            document.getElementById('titleDiv'+i).appendChild(deleteButton);
            deleteButton.addEventListener('click', deleteItem  => { 
                //Eliminamos el elemento del DOM y lo añadimos a deletedQueries
                let deleteThisItem = document.getElementById('result'+i);
                deleteThisItem.parentNode.removeChild(deleteThisItem);
                deletedQueries.push(newQueryArray[i]);
                if (document.getElementsByClassName('result-item').length === 0){
                    noResults();
                }
            });
        }
    }
});
window.addEventListener('beforeunload', function(event) {
    //Eliminamos de newQueryArray las queries que ha eliminado el usario
    newQueryArray = newQueryArray.filter( x => !deletedQueries.includes(x) );
    //Insertamos en el sessionStorage de nuevo el array de queries
    sessionStorage.clear();
    for(let i = 0; i < newQueryArray.length; i++){
        sessionStorage.setItem('query'+ (i), JSON.stringify(newQueryArray[i])); 
    }
});
function noResults(){
    //Mostramos un párrafo con el texto '0 results' y eliminamos el botón de 'delete all'
    let paragraphnoresults = document.createElement('p');
    paragraphnoresults.textContent = '0 results.';
    document.getElementById('list').appendChild(paragraphnoresults);
    let deleteAnotherItem = document.getElementById('deleteall');
    deleteAnotherItem.parentNode.removeChild(deleteAnotherItem);
}

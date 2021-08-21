//const { SSL_OP_EPHEMERAL_RSA } = require("constants");

LICITACION_ID=null;
FILTRO_ID=null;
grupo=null;
familia=null;
articulo=null;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var typingTimer= null;
var doneTypingInterval = 5000;

function keyupFunction(){
    clearTimeout(typingTimer);
    typingTimer = setTimeout(function(){make_search_query()}, 2000);
}

function make_search_query(){
    let cookie = getCookie('csrftoken');
    var nombre = document.getElementById("search_licitacion").value;
    fetch('http://127.0.0.1:8000/account/search_licitacion_by_name?nombre='+nombre, { method: 'GET',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
    }).then(res => {
        return res.text();
    })
    .then(data => {
        var parser = new DOMParser();
        // Parse the text
        var doc = parser.parseFromString(data, "text/html"); 
        var docArticle = doc.querySelector('#main_container');
        $( "#main_container" ).replaceWith( docArticle );
    });
}

function change_status(licitacion_id, status){
    console.log("entro aqui ", status);
    if (status=="Eliminar"){
        console.log("simon aqui");
        $("#modal_boton").click();
        LICITACION_ID=licitacion_id
    }
    else{
        call_change_status_licitacion(licitacion_id, status);
    }
}

function aceptar_borrar(){
    remove_licitacion(LICITACION_ID);
}

function call_change_status_licitacion(licitacion_id, status){
    let cookie = getCookie('csrftoken');
    fetch('http://127.0.0.1:8000/account/change_status_licitacion',{ method: 'POST',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({"id": licitacion_id, 'status':status})
    }).then(res => {
        return res.text();
    })
    .then(data => {
        var parser = new DOMParser();
        // Parse the text
        var doc = parser.parseFromString(data, "text/html"); 
        var docArticle = doc.querySelector('#mis_licitaciones');
        $( "#mis_licitaciones" ).replaceWith( docArticle );
    });
}

function add_licitacion(id, description, entidad){
    let cookie = getCookie('csrftoken');
    fetch('http://127.0.0.1:8000/account/add_licitacion',{ method: 'POST',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({"valor": id, 'description':description, 'entidad':entidad})
    }).then(res => {
        return res.text();
    })
    .then(data => {
        var parser = new DOMParser();
        var doc = parser.parseFromString(data, "text/html");
        var docArticle = doc.querySelector('#r'+id.toString().split(".")[0]);
        $( '#r'+id.toString().split(".")[0] ).replaceWith( docArticle );
    });
}

function remove_licitacion(id){
    let cookie = getCookie('csrftoken');
    fetch('http://127.0.0.1:8000/account/remove_licitacion',{ method: 'POST',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({"valor": id})
    }).then(res => {
        return res.text();
    })
    .then(data => {
        $("#modal_boton").click();
        var parser = new DOMParser();
        // Parse the text
        var doc = parser.parseFromString(data, "text/html"); 
        var docArticle = doc.querySelector('#mis_licitaciones');
        $( "#mis_licitaciones" ).replaceWith( docArticle );
    });
}

function change_status_filtro(id, status){
    console.log("entro aqui ", status);
    if (status=="Eliminar"){
        console.log("simon aqui");
        $("#modal_boton").click();
        FILTRO_ID=id
    }
    else{
        call_change_status_filtro(id, status);
    }

}

function call_change_status_filtro(licitacion_id, status){
    let cookie = getCookie('csrftoken');
    fetch('http://127.0.0.1:8000/account/change_status_filtro',{ method: 'POST',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({"id": licitacion_id, 'status':status})
    }).then(res => {
        return res.text();
    })
    .then(data => {
        var parser = new DOMParser();
        // Parse the text
        var doc = parser.parseFromString(data, "text/html"); 
        var docArticle = doc.querySelector('#tabla_filtros');
        $( "#tabla_filtros" ).replaceWith( docArticle );
    });
}

function aceptar_borrar_filtro(){
    remove_filtro(FILTRO_ID);
}

function remove_filtro(id){
    let cookie = getCookie('csrftoken');
    fetch('http://127.0.0.1:8000/account/remove_filtro',{ method: 'POST',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({"valor": id})
    }).then(res => {
        return res.text();
    })
    .then(data => {
        $("#modal_boton").click();
        var parser = new DOMParser();
        // Parse the text
        var doc = parser.parseFromString(data, "text/html"); 
        var docArticle = doc.querySelector('#tabla_filtros');
        $( "#tabla_filtros" ).replaceWith( docArticle );
    });
}

function add_filtro(){
    console.log("llego al boton");
    console.log(grupo, familia, articulo)
    let cookie = getCookie('csrftoken');
    fetch('http://127.0.0.1:8000/account/add_filtro',{ method: 'POST',
    headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({grupo, familia, articulo })
    }).then((res)=>{
        return res.text();
    }).then((data)=>{
        $('.grupoAutoComplete').autoComplete('clear');
        $('.familiaAutoComplete').autoComplete('clear');
        $('.articuloAutoComplete').autoComplete('clear');
        var parser = new DOMParser();
        var doc = parser.parseFromString(data, "text/html"); 
        var docArticle = doc.querySelector('#tabla_filtros');
        $( "#tabla_filtros" ).replaceWith( docArticle );
        $("#add_filtro_btn").addClass("hide-element");
    })
}

$( document ).ready(function() {
    grupo=null;
    familia=null;
    articulo=null;
    $('.grupoAutoComplete').autoComplete({
        minLength:1,
        noResultsText: "No hay grupo con este nombre",
        queryKey:'grupo',
        resolverSettings: {
            queryKey:'grupo',
            url: 'http://127.0.0.1:8000/account/filter'
        }
    });
    $(".grupoAutoComplete").on("autocomplete.select", function(evt, item){
        grupo=item["value"];
        $("#add_filtro_btn").removeClass("hide-element");
    })

    $('.familiaAutoComplete').autoComplete({
        noResultsText: "No hay familia con este nombre",
        minLength:1,
        resolver: 'custom',
        events: {
            search: function (qry, callback){
                $.ajax(
                'http://127.0.0.1:8000/account/filter?familia='+qry+"&grupo="+grupo,
                ).done(function (res) {
                callback(res)
                });
            }
        }
    });
    $(".familiaAutoComplete").on("autocomplete.select", function(evt, item){
        familia=item["value"];
    })

    $('.articuloAutoComplete').autoComplete({
        noResultsText: "No hay articulo con este nombre",
        minLength:1,
        resolver: 'custom',
        events: {
            search: function (qry, callback){
                $.ajax(
                'http://127.0.0.1:8000/account/filter?articulo='+qry+"&grupo="+grupo+"&familia="+familia,
                ).done(function (res) {
                callback(res)
                });
            }
        }
    });
    $(".articuloAutoComplete").on("autocomplete.select", function(evt, item){
        articulo=item["value"];
    })
});



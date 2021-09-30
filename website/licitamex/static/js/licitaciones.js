//const { SSL_OP_EPHEMERAL_RSA } = require("constants");

let dependencia = 'todas';

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
function keyupFunction_mi_portal(){
    clearTimeout(typingTimer);
    typingTimer = setTimeout(function(){search_mi_portal_licitaciones()}, 2000);
}
function keyupFunction_buscar_filtro(){
    clearTimeout(typingTimer);
    typingTimer = setTimeout(function(){search_filtro_configuracion()}, 2000);

}

function search_filtro_configuracion(){
    let cookie = getCookie('csrftoken');
    var nombre = document.getElementById("search_filtro_valor").value;
    fetch('http://localhost:8000/account/search_filtro_by_name?nombre='+nombre, { method: 'GET',
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
        var docArticle = doc.querySelector('#filtros_container');
        $( "#filtros_container" ).replaceWith( docArticle );
    });

}




function search_mi_portal_licitaciones(){
    let cookie = getCookie('csrftoken');
    var nombre = document.getElementById("search_mi_portal_lcitacion").value;
    fetch('http://localhost:8000/account/search_mi_portallicitacion_by_name?nombre='+nombre, { method: 'GET',
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
        var docArticle = doc.querySelector('#mis_licitaciones');
        $( "#mis_licitaciones" ).replaceWith( docArticle );
    });

}


function seleccionar_dependencia(dependencia_valor){
    console.log("aqui");
    dependencia = dependencia_valor
    $("#dependencia-seleccionada-licitaciones").text(dependencia)
    make_search_query()
}

function make_search_query(){
    let cookie = getCookie('csrftoken');
    var nombre = document.getElementById("search_licitacion").value;
    let url = 'http://localhost:8000/account/search_licitacion_by_name?nombre='+nombre
    if(dependencia !== 'todas'){
        url = url+"&dependencia="+dependencia
    }
    fetch(url, { method: 'GET',
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
        var docArticle = doc.querySelector('#tabla_licitaciones');
        $( "#tabla_licitaciones").replaceWith( docArticle );
    });
}





function activar_licitacion(id, description, entidad){
    let cookie = getCookie('csrftoken');
    $("#activar_licitacionr"+id.toString().split(".")[0]).addClass("hide-element");
    $("#loaderr"+id.toString().split(".")[0]).removeClass("hide-element");
    fetch('http://localhost:8000/account/activate_licitacion',{ method: 'POST',
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

function desactivar_licitacion(id){
    let cookie = getCookie('csrftoken');
    $("#desactivar_licitacionr"+id.toString().split(".")[0]).addClass("hide-element");
    $("#loaderr"+id.toString().split(".")[0]).removeClass("hide-element");
    fetch('http://localhost:8000/account/inactive_licitacion',{ method: 'POST',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({"valor": id})
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



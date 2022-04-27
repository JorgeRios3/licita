grupo=null;
familia=null;
articulo=null;
FILTRO_ID=null;



function mostrar_forma_crear_usuario(){
    
}



function remove_filtro(id){
    let cookie = getCookie('csrftoken');
    fetch('https://consultalicitamex.com/remove_filtro',{ method: 'POST',
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
    fetch('https://consultalicitamex.com/add_filtro',{ method: 'POST',
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

function aceptar_borrar_filtro(){
    remove_filtro(FILTRO_ID);
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
            url: 'https://consultalicitamex.com/filter'
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
                'https://consultalicitamex.com/filter?familia='+qry+"&grupo="+grupo,
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
                'https://consultalicitamex.com/filter?articulo='+qry+"&grupo="+grupo+"&familia="+familia,
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

function DeletePermisionUser(id){
    console.log("viendo el id ",id);
    let cookie = getCookie('csrftoken');
    fetch('https://consultalicitamex.com/delete_user_permision',{ method: 'POST',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({"permiso_id":id})
    }).then(res => {
        window.location.reload()
    })
}

function validate_selection(){
    var usuario = document.getElementById("selected_usuario").value;
    var permiso = document.getElementById("selected_permiso").value;
    console.log("si entro en los 2 selects", usuario, permiso);
    if(usuario == "" || permiso == ""){
        $("#btn_agregar_permiso").addClass("hide_add_permiso");
    } else {
        $("#btn_agregar_permiso").removeClass("hide_add_permiso");
    }
}

function agregar_permisoUsuario(){
    var usuario = document.getElementById("selected_usuario").value;
    var permiso = document.getElementById("selected_permiso").value;
    console.log("en agregar", usuario, permiso);
    let cookie = getCookie('csrftoken');
    fetch('https://consultalicitamex.com/add_user_permision',{ method: 'POST',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({"usuario_id": usuario, "permiso_id":permiso})
    }).then(res => {
        window.location.reload()
    })
}

function deleteGroupUser(id){
    let cookie = getCookie('csrftoken');
    fetch('https://consultalicitamex.com/delete_group_user',{ method: 'POST',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({"id": id})
    }).then(res => {
        return res.text();
    })
    .then(data => {
        var parser = new DOMParser();
        // Parse the text
        //var doc = parser.parseFromString(data, "text/html"); 
        //var docArticle = doc.querySelector('#tabla_filtros');
        //$( "#tabla_filtros" ).replaceWith( docArticle );
    });
}

function call_change_status_filtro(licitacion_id, status){
    let cookie = getCookie('csrftoken');
    fetch('https://consultalicitamex.com/change_status_filtro',{ method: 'POST',
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
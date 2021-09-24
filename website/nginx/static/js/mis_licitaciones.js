LICITACION_ID=null;

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

function call_change_status_licitacion(licitacion_id, status){
    let cookie = getCookie('csrftoken');
    fetch('https://consultalicitamex.comaccount/change_status_licitacion',{ method: 'POST',
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


function aceptar_borrar(){
    console.log("falta chamba aqui", LICITACION_ID);
    let cookie = getCookie('csrftoken');
    fetch('https://consultalicitamex.comaccount/delete_licitacion',{ method: 'POST',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({"id": LICITACION_ID,})
    }).then(res => {
        return res.text();
    })
    .then(data => {
        var parser = new DOMParser();
        // Parse the text
        var doc = parser.parseFromString(data, "text/html"); 
        var docArticle = doc.querySelector('#mis_licitaciones');
        $( "#mis_licitaciones" ).replaceWith( docArticle );
        $("#modal_boton").click();
    });
}


function agregar_comentario(id){
    let cookie = getCookie('csrftoken');
    val = $("#new_comment").val().trim();
    if (val === ""){
        return;
    }
    fetch('https://consultalicitamex.comaccount/licitacion/'+id,{ method: 'POST',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({"id": id, "text": val})
    }).then(res => {
        return res.text();
    })
    .then(data => {
        $("#new_comment").val('');
        var parser = new DOMParser();
        var doc = parser.parseFromString(data, "text/html"); 
        var docArticle = doc.querySelector('#licitacion_container');
        $( "#licitacion_container" ).replaceWith( docArticle );
    });
}

function guardar_datos_comprador(id){
    let cookie = getCookie('csrftoken');
    comprador_nombre = $("#comprador_nombre").val();
    comprador_telefono = $("#comprador_telefono").val();
    comprador_email = $("#comprador_email").val();
    comprador_direccion = $("#comprador_direccion").val();
    fetch('https://consultalicitamex.comaccount/licitacion/'+id,{ method: 'POST',
        headers: {'X-CSRFToken': cookie},
        mode: 'same-origin',
        cache: 'default',
        body: JSON.stringify({"id": id, "nombre": comprador_nombre, "telefono":comprador_telefono, "email":comprador_email, "direccion":comprador_direccion})
    }).then(res => {
        return res.text();
    })
    .then(data => {
        var parser = new DOMParser();
        var doc = parser.parseFromString(data, "text/html"); 
        var docArticle = doc.querySelector('#comprador_container');
        $( "#comprador_container" ).replaceWith( docArticle );
        $("#modal_datos_comprador").click();
        //listo
    });
}
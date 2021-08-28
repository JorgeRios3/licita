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
    fetch('https://consultalicitamex.com/account/change_status_licitacion',{ method: 'POST',
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
    fetch('https://consultalicitamex.com/account/delete_licitacion',{ method: 'POST',
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
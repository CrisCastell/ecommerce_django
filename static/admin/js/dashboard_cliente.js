document.addEventListener('DOMContentLoaded', function() {
    // Hacer la petición a la API cuando la página haya cargado completamente
    cargarProductos()
    cargarHistorialCompras()
});



function cargarProductos(){
    fetch('/api/productos/')
    .then(response => response.json())  // Convertir la respuesta a JSON
    .then(data => {

        const productosContainer = document.getElementById('productos-list');
        if (productosContainer.innerHTML != '') productosContainer.innerHTML = "";

        data.forEach(producto => {

            const productCard = document.createElement('div');        
            productCard.classList.add('col-md-4');

            productCard.innerHTML = `
                <div class="card"">
                    <img class="producto-list-imagen" alt="${producto.nombre}" src="${producto.imagen ? producto.imagen : 'https://media.s-bol.com/mO7MJqVMgJLA/550x550.jpg'}">
                    <div class="card-body">
                        <h5 class="card-title">${producto.nombre}</h5>
                        <p class="card-text">${producto.nombre_categoria}</p>
                        <p class="card-text">$ ${producto.precio}</p>
                        <div><strong>Stock disponible:</strong> <p id="stock-seleccionado-${producto.id}">${producto.stock}</p></div>
                        <div class="d-flex justify-content-between align-items-center">
                            <a class="btn mr-2" id="detalle-producto" data-id="${producto.id}"><i class="fas fa-link"></i>Ver Producto</a>
                            <a class="btn btn-cantidad agregar-carrito" id="agregar-carrito-${producto.id}"  data-id="${producto.id}"><i class="fab fa-github"></i>Agregar</a>
                            <div id="controles-cantidad-${producto.id}" data-id="${producto.id}" class="btn-wrapper" style="display: none;">
                                <a class="btn btn-cantidad disminuir-cantidad" id="disminuir-cantidad-${producto.id}" data-id="${producto.id}"><i class="fab fa-github"></i>-</a>
                                <span id="cantidad-seleccionada-${producto.id}" data-id="${producto.id}" class="cantidad-box  p-2">0</span>
                                <a class="btn btn-cantidad aumentar-cantidad" id="aumentar-cantidad-${producto.id}"  data-id="${producto.id}"><i class="fab fa-github"></i>+</a>
                            </div>
                        </div>
                        
                        

                    </div>
                </div>
            `;

            // Añadir la tarjeta al contenedor
            productosContainer.appendChild(productCard);

            
        });

        actualizarEstadoBotonesDesdeCarrito(data);
    })
    .catch(error => {
        console.error("Error al cargar los productos:", error);
    });
}


function cargarHistorialCompras(){
    fetch('/api/compras/')
    .then(response => response.json())  // Convertir la respuesta a JSON
    .then(data => {
        const historialContainer = document.getElementById('historial-compras-list');
        if (historialContainer.innerHTML != '') historialContainer.innerHTML = "";

        data.forEach(compra => {

            const compraItem = document.createElement('li');        
            compraItem.classList.add("list-group-item");
            compraItem.classList.add("mb-2");
            compraItem.setAttribute('data-id', compra.id);

            compraItem.innerHTML = `
                <div class="compra-item d-flex justify-content-between align-items-center">
                    <div class="">
                        <h5>Compra #${compra.identificador_unico}</h5>
                        <p>${compra.fecha}</p>
                        <p>$ ${compra.total}</p>
                        <a class="btn" id="detalle-compra" data-id="${compra.id}"><i class="fas fa-link"></i>Ver Compra</a>
                    </div>
                </div>
            `;
            historialContainer.appendChild(compraItem);
        });
    })
    .catch(error => {
        console.error("Error al cargar los productos:", error);
    });
}



document.addEventListener('click', function() {
    const botonModal = event.target
    if(botonModal){
        if (botonModal.id === 'detalle-producto') {
            mostrarDetalleProducto(botonModal)
        }
        else if (botonModal.id === 'contenido-carrito') {
            
            listarCarritoEnModal()
        }

        else if (botonModal.id === 'detalle-compra') {
            
            mostrarDetalleCompra(botonModal)
        }
    }

});



function mostrarDetalleProducto(boton){
    const productId = boton.getAttribute('data-id');
    const apiUrl = `/api/productos/${productId}/`;

    // Llamar a la API para obtener los detalles del producto
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Una vez que recibimos los datos del producto, llenamos el modal
            let contenido = `
                <h5>${data.nombre}</h5>
                <p><strong>Descripción:</strong> ${data.descripcion}</p>
                <p><strong>Precio:</strong> $${data.precio}</p>
                <p><strong>Stock disponible:</strong> ${data.stock}</p>
                <img src="${data.imagen ? data.imagen : 'https://media.s-bol.com/mO7MJqVMgJLA/550x550.jpg'}" alt="${data.nombre}" class="img-fluid"/>
            `;

            // Colocamos el contenido dentro del modal
            document.getElementById('detalle-contenido').innerHTML = contenido;

            // Mostramos el modal
            let modal = new bootstrap.Modal(document.getElementById('detalleModal'));
            modal.show();


        })
        .catch(error => {
            console.error("Error al obtener los detalles del producto:", error);
            document.getElementById('detalle-contenido').innerHTML = `<p>Error al cargar los detalles del producto.</p>`;
        });

}




function mostrarDetalleCompra(boton){
    const compraId = boton.getAttribute('data-id');
    const apiUrl = `/api/compras/${compraId}/`;

    // Llamar a la API para obtener los detalles del producto
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {

            
            let compraProductos = ""

            data.productos.forEach(producto => {
                compraProductos += `<li class="list-group-item">
                                        <div class="container d-flex justify-content-between align-items-center">
                                            <img class="img-small-list" alt="${producto.nombre}" src="${producto.imagen ? producto.imagen : 'https://media.s-bol.com/mO7MJqVMgJLA/550x550.jpg'}">
                                            <p>${producto.nombre}</p>
                                            <p>${producto.nombre_categoria}</p>
                                            <p>Precio: $ ${producto.precio}</p>
                                            
                                        </div>
                                    </li>`
            })

            // Una vez que recibimos los datos del producto, llenamos el modal
            let contenido = `
                <h5>Orden Nro:</strong> ${data.identificador_unico}</h5>
                <p><strong>Fecha:</strong> ${data.fecha}</p>
                <p><strong>Costo total:</strong> $${data.total}</p>
                <ul class="list-group>${compraProductos}</ul>
                `;

            // Colocamos el contenido dentro del modal
            document.getElementById('detalle-compra-container').innerHTML = contenido;

            // Mostramos el modal
            let modal = new bootstrap.Modal(document.getElementById('detalleCompraModal'));
            modal.show();


        })
        .catch(error => {
            console.error("Error al obtener los detalles del producto:", error);
            document.getElementById('detalle-contenido').innerHTML = `<p>Error al cargar los detalles del producto.</p>`;
        });

}


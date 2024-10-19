document.addEventListener('click', function(event) {
    // Botón "Agregar al carrito"
    const boton = event.target
    const productId = boton.getAttribute('data-id');
    let cantidad = 0
    if (boton){
        if(boton.id === 'comprar-btn'){
            manejarCompra()
        }

        if (boton.classList.contains('agregar-carrito')) {
            
            cantidad = 1; // Inicializamos con 1 al agregar al carrito

            // Mostrar los controles de cantidad asociados al producto por su ID
            const controlesCantidad = document.getElementById(`controles-cantidad-${productId}`);
            controlesCantidad.style.display = 'inline-block';
            
            // Ocultar el botón "Agregar al carrito" correspondiente por su ID
            const agregarBoton = document.getElementById(`agregar-carrito-${productId}`);
            agregarBoton.style.display = 'none';

            // Actualizar la cantidad mostrada
            const cantidadElemento = document.getElementById(`cantidad-seleccionada-${productId}`);
            cantidadElemento.textContent = cantidad;

        }

        // Botón para aumentar la cantidad
        if (boton.classList.contains('aumentar-cantidad')) {
            const stock = document.getElementById(`stock-seleccionado-${productId}`).textContent;
            let cantidadElemento = document.getElementById(`cantidad-seleccionada-${productId}`);
            cantidad = parseInt(cantidadElemento.textContent);

            if (cantidad < stock) {
                cantidad++;
                cantidadElemento.textContent = cantidad;
            }
        }

        // Botón para disminuir la cantidad
        if (boton.classList.contains('disminuir-cantidad')) {
            let cantidadElemento = document.getElementById(`cantidad-seleccionada-${productId}`);
            cantidad = parseInt(cantidadElemento.textContent);

            if (cantidad > 0) {
                cantidad--;
                cantidadElemento.textContent = cantidad;

            }
        }
        if(boton.classList.contains('btn-cantidad')){
            actualizarCarrito(productId, cantidad);
            actualizarBotones(cantidad, productId);
    
        }
    }
});

// Función para actualizar el carrito en el LocalStorage
function actualizarCarrito(productId, cantidad) {
    const stock = document.getElementById(`stock-seleccionado-${productId}`).textContent;
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let productoEnCarrito = carrito.find(producto => producto.producto_id === productId);

    if (productoEnCarrito) {
        productoEnCarrito.cantidad = cantidad;
    } else {
        carrito.push({
            producto_id: productId,
            cantidad: cantidad, 
            stock: stock
        });
    }


    // Eliminar el producto si la cantidad es 0
    carrito = carrito.filter(producto => producto.cantidad > 0);
    actualizarTotalCarrito(carrito)
    localStorage.setItem('carrito', JSON.stringify(carrito));
}





function actualizarBotones(cantidad, productId) {

    const aumentarBoton = document.getElementById(`aumentar-cantidad-${productId}`);
    const agregarBoton = document.getElementById(`agregar-carrito-${productId}`);
    const controlesCantidad = document.getElementById(`controles-cantidad-${productId}`);
    const stock = document.getElementById(`stock-seleccionado-${productId}`).textContent;

    if (cantidad > 0) {
        agregarBoton.style.display = 'none';
        controlesCantidad.style.display = 'inline-block';

        // Ocultar el botón "Aumentar" si se alcanza la cantidad en stock
        aumentarBoton.style.display = (cantidad >= stock) ? 'none' : 'inline-block';
    } else {
        // Si la cantidad es 0, volver a mostrar el botón "Agregar al carrito" y ocultar los botones interectivos
        agregarBoton.style.display = 'inline-block';
        controlesCantidad.style.display = 'none';
    }
}



function actualizarEstadoBotonesDesdeCarrito(productosList) {
    // Obtener el carrito almacenado en el LocalStorage
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];

    // Iterar sobre los productos en el carrito
    carrito.forEach(itemCarrito => {
        // Buscar el producto en la lista de productos de la API
        const productoElem = productosList.find(producto => producto.id == itemCarrito.producto_id);
        const productoEnAPI = productoElem.id == itemCarrito.producto_id;

        // Si el producto existe en la lista de la API y tiene cantidad en el carrito
        if (productoEnAPI && itemCarrito.cantidad > 0) {
            // Actualizar la cantidad en los elementos del DOM y los botones interactivos
            const cantidadElemento = document.getElementById(`cantidad-seleccionada-${itemCarrito.producto_id}`);
            const agregarBoton = document.getElementById(`agregar-carrito-${itemCarrito.producto_id}`);
            const controlesCantidad = document.getElementById(`controles-cantidad-${itemCarrito.producto_id}`);
            
            if (cantidadElemento && agregarBoton && controlesCantidad) {

                cantidadElemento.textContent = itemCarrito.cantidad;

                agregarBoton.style.display = 'none';
                controlesCantidad.style.display = 'inline-block';

                actualizarBotones(itemCarrito.cantidad, itemCarrito.producto_id);
                actualizarTotalCarrito(carrito)
            }
        }
    });
}


function actualizarTotalCarrito(carrito){

    const carritoBtn = document.getElementById(`cart`);
    let cantidadTotal = 0;

    carrito.forEach(producto => cantidadTotal += producto.cantidad);
    carritoBtn.textContent = cantidadTotal;
}





function obtenerCarrito() {
    return JSON.parse(localStorage.getItem('carrito')) || [];
}







function listarCarritoEnModal() {
    const listaProductosCarrito = document.getElementById('lista-productos-carrito');
    listaProductosCarrito.innerHTML = ''; 
    const carritoModal = new bootstrap.Modal(document.getElementById('carritoModal'));
    carritoModal.show();
    let totalCompra = 0

    const carrito = obtenerCarrito();

    const csrfToken = getCsrfToken();


    if(carrito.length > 0){
        fetch('/api/productos/filtrar-productos-carrito/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  
            },
            body: JSON.stringify(carrito)
        })
        .then(response => response.json())  
        .then(data => {
            data.forEach(producto => {  
                totalCompra += producto.total;  
                const fila = `
                    <tr>
                        <td>
                            <img class="img-small-list" src="${producto.imagen ? producto.imagen : 'https://media.s-bol.com/mO7MJqVMgJLA/550x550.jpg'}" alt="${producto.nombre}" class="img-list-productos" />
                        </td>
                        <td>${producto.nombre}</td>
                        <td>${producto.cantidad}</td>
                        <td>$${producto.precio_unitario.toFixed(2)}</td>
                        <td>$${producto.total.toFixed(2)}</td>
                    </tr>
                `;
                listaProductosCarrito.insertAdjacentHTML('beforeend', fila);
                
            });
    
            // Mostrar el total de la compra
            document.getElementById('total-compra').textContent = totalCompra.toFixed(2);
            })
            .catch(error => {
                console.error('Error al enviar el carrito:', error);
        });
    }

}


function manejarCompra() {
    const carrito = obtenerCarrito();
    const listaProductosCarrito = document.getElementById('lista-productos-carrito');

    const compraData = {
        articulos: carrito.map(item => ({
            producto_id: item.producto_id,
            cantidad: item.cantidad,
        })),
    };

    const csrfToken = getCsrfToken();

    fetch('/api/compras/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  
        },
        body: JSON.stringify(compraData),
    })
    .then(response => response.json())
    .then(data => {

        localStorage.removeItem('carrito');

        const carritoModal = document.getElementById('carritoModal');
        const modalInstance = bootstrap.Modal.getInstance(carritoModal);
        if (modalInstance) {
            modalInstance.hide();
        }
        listaProductosCarrito.innerHTML = '';
        mostrarCompraExitosa(data.identificador_unico)
        cargarProductos()
        cargarHistorialCompras()

    })
    .catch(error => {
        console.error('Error al realizar la compra:', error);
    });
}


function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}


function mostrarCompraExitosa(nroCompra) {
    let nroCompraSpan = document.getElementById('nro-compra-exitosa');
    nroCompraSpan.innerHTML = nroCompra;
    let modal = new bootstrap.Modal(document.getElementById('compraExitosaModal'));
    modal.show();
  }


const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7] },
        { orderable: false, targets: [1, 6, 7] },
        { searchable: false, targets: [1, 7] }
    ], dom: 'Bfrtilp',
    buttons: [
        {
            extend: 'excelHtml5',
            text: '<i class="fas fa-file-excel"></i> ',
            titleAttr: 'Exportar a Excel',
            className: 'btn btn-success',
        },
        {
            extend: 'pdfHtml5',
            text: '<i class="fas fa-file-pdf"></i> ',
            titleAttr: 'Exportar a PDF',
            className: 'btn btn-danger',
        },
        {
            extend: 'print',
            text: '<i class="fa fa-print"></i> ',
            titleAttr: 'Imprimir',
            className: 'btn btn-info',
        },
    ],
    pageLength: 3,
    destroy: true,
    language: {
        processing: 'Procesando...',
        lengthMenu: 'Mostrar _MENU_ registros',
        zeroRecords: 'No se encontraron resultados',
        emptyTable: 'Ningún dato disponible en esta tabla',
        infoEmpty: 'Mostrando registros del 0 al 0 de un total de 0 registros',
        infoFiltered: '(filtrado de un total de _MAX_ registros)',
        search: 'Buscar:',
        infoThousands: ',',
        loadingRecords: 'Cargando...',
        paginate: {
            first: 'Primero',
            last: 'Último',
            next: 'Siguiente',
            previous: 'Anterior',
        },
        aria: {
            sortAscending: ': Activar para ordenar la columna de manera ascendente',
            sortDescending: ': Activar para ordenar la columna de manera descendente',
        },
        buttons: {
            copy: 'Copiar',
            colvis: 'Visibilidad',
            collection: 'Colección',
            colvisRestore: 'Restaurar visibilidad',
            copyKeys:
                'Presione ctrl o u2318 + C para copiar los datos de la tabla al portapapeles del sistema. <br /> <br /> Para cancelar, haga clic en este mensaje o presione escape.',
            copySuccess: {
                1: 'Copiada 1 fila al portapapeles',
                _: 'Copiadas %ds fila al portapapeles',
            },
            copyTitle: 'Copiar al portapapeles',
            csv: 'CSV',
            excel: 'Excel',
            pageLength: {
                '-1': 'Mostrar todas las filas',
                _: 'Mostrar %d filas',
            },
            pdf: 'PDF',
            print: 'Imprimir',
            renameState: 'Cambiar nombre',
            updateState: 'Actualizar',
            createState: 'Crear Estado',
            removeAllStates: 'Remover Estados',
            removeState: 'Remover',
            savedStates: 'Estados Guardados',
            stateRestore: 'Estado %d',
        },
        autoFill: {
            cancel: 'Cancelar',
            fill: 'Rellene todas las celdas con <i>%d</i>',
            fillHorizontal: 'Rellenar celdas horizontalmente',
            fillVertical: 'Rellenar celdas verticalmentemente',
        },
        decimal: ',',
        searchBuilder: {
            add: 'Añadir condición',
            button: {
                0: 'Constructor de búsqueda',
                _: 'Constructor de búsqueda (%d)',
            },
            clearAll: 'Borrar todo',
            condition: 'Condición',
            conditions: {
                date: {
                    after: 'Despues',
                    before: 'Antes',
                    between: 'Entre',
                    empty: 'Vacío',
                    equals: 'Igual a',
                    notBetween: 'No entre',
                    notEmpty: 'No Vacio',
                    not: 'Diferente de',
                },
                number: {
                    between: 'Entre',
                    empty: 'Vacio',
                    equals: 'Igual a',
                    gt: 'Mayor a',
                    gte: 'Mayor o igual a',
                    lt: 'Menor que',
                    lte: 'Menor o igual que',
                    notBetween: 'No entre',
                    notEmpty: 'No vacío',
                    not: 'Diferente de',
                },
                string: {
                    contains: 'Contiene',
                    empty: 'Vacío',
                    endsWith: 'Termina en',
                    equals: 'Igual a',
                    notEmpty: 'No Vacio',
                    startsWith: 'Empieza con',
                    not: 'Diferente de',
                    notContains: 'No Contiene',
                    notStartsWith: 'No empieza con',
                    notEndsWith: 'No termina con',
                },
                array: {
                    not: 'Diferente de',
                    equals: 'Igual',
                    empty: 'Vacío',
                    contains: 'Contiene',
                    notEmpty: 'No Vacío',
                    without: 'Sin',
                },
            },
            data: 'Data',
            deleteTitle: 'Eliminar regla de filtrado',
            leftTitle: 'Criterios anulados',
            logicAnd: 'Y',
            logicOr: 'O',
            rightTitle: 'Criterios de sangría',
            title: {
                0: 'Constructor de búsqueda',
                _: 'Constructor de búsqueda (%d)',
            },
            value: 'Valor',
        },
        searchPanes: {
            clearMessage: 'Borrar todo',
            collapse: {
                0: 'Paneles de búsqueda',
                _: 'Paneles de búsqueda (%d)',
            },
            count: '{total}',
            countFiltered: '{shown} ({total})',
            emptyPanes: 'Sin paneles de búsqueda',
            loadMessage: 'Cargando paneles de búsqueda',
            title: 'Filtros Activos - %d',
            showMessage: 'Mostrar Todo',
            collapseMessage: 'Colapsar Todo',
        },
        select: {
            cells: {
                1: '1 celda seleccionada',
                _: '%d celdas seleccionadas',
            },
            columns: {
                1: '1 columna seleccionada',
                _: '%d columnas seleccionadas',
            },
            rows: {
                1: '1 fila seleccionada',
                _: '%d filas seleccionadas',
            },
        },
        thousands: '.',
        datetime: {
            previous: 'Anterior',
            next: 'Proximo',
            hours: 'Horas',
            minutes: 'Minutos',
            seconds: 'Segundos',
            unknown: '-',
            amPm: ['AM', 'PM'],
            months: {
                0: 'Enero',
                1: 'Febrero',
                10: 'Noviembre',
                11: 'Diciembre',
                2: 'Marzo',
                3: 'Abril',
                4: 'Mayo',
                5: 'Junio',
                6: 'Julio',
                7: 'Agosto',
                8: 'Septiembre',
                9: 'Octubre',
            },
            weekdays: ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'],
        },
        editor: {
            close: 'Cerrar',
            create: {
                button: 'Nuevo',
                title: 'Crear Nuevo Registro',
                submit: 'Crear',
            },
            edit: {
                button: 'Editar',
                title: 'Editar Registro',
                submit: 'Actualizar',
            },
            remove: {
                button: 'Eliminar',
                title: 'Eliminar Registro',
                submit: 'Eliminar',
                confirm: {
                    _: '¿Está seguro que desea eliminar %d filas?',
                    1: '¿Está seguro que desea eliminar 1 fila?',
                },
            },
            error: {
                system:
                    'Ha ocurrido un error en el sistema (<a target="\\" rel="\\ nofollow" href="\\">Más información&lt;\\/a&gt;).</a>',
            },
            multi: {
                title: 'Múltiples Valores',
                info: 'Los elementos seleccionados contienen diferentes valores para este registro. Para editar y establecer todos los elementos de este registro con el mismo valor, hacer click o tap aquí, de lo contrario conservarán sus valores individuales.',
                restore: 'Deshacer Cambios',
                noMulti:
                    'Este registro puede ser editado individualmente, pero no como parte de un grupo.',
            },
        },
        info: 'Mostrando _START_ a _END_ de _TOTAL_ registros',
        stateRestore: {
            creationModal: {
                button: 'Crear',
                name: 'Nombre:',
                order: 'Clasificación',
                paging: 'Paginación',
                search: 'Busqueda',
                select: 'Seleccionar',
                columns: {
                    search: 'Búsqueda de Columna',
                    visible: 'Visibilidad de Columna',
                },
                title: 'Crear Nuevo Estado',
                toggleLabel: 'Incluir:',
            },
            emptyError: 'El nombre no puede estar vacio',
            removeConfirm: '¿Seguro que quiere eliminar este %s?',
            removeError: 'Error al eliminar el registro',
            removeJoiner: 'y',
            removeSubmit: 'Eliminar',
            renameButton: 'Cambiar Nombre',
            renameLabel: 'Nuevo nombre para %s',
            duplicateError: 'Ya existe un Estado con este nombre.',
            emptyStates: 'No hay Estados guardados',
            removeTitle: 'Remover Estado',
            renameTitle: 'Cambiar Nombre Estado',
        },
    },
    pageLength: 4,
    destroy: true

};

let dataTable;
let dataTableInit = false;

const initDatatable = async () => {
    if (dataTableInit) {
        dataTable.destroy();
    }
    await listusers();

    dataTable = $('#datatable-users').DataTable(dataTableOptions);

    dataTableInit = true;

};


const listusers = async () => {
    try {

        const response = await fetch('/listUsers/')
        const data = await response.json();
        let content = ``;
        let userType = '';
        let activo = '';
        data.user.forEach((user, index) => {
            if (data.user[index].is_superuser) {
                userType = 'Administrador';
            } else if (data.user[index].is_chef) {
                userType = 'Chef';
            } else {
                userType = 'Mesero';
            }

            activo = data.user[index].is_active ? 'Activo' : 'No activo';

            content += `
                <tr id="user-${user.id}">
                    <td>${user.id}</td>
                    <td>${activo == 'Activo' ? "<p style='color: green;'>Activo</p>" : "<p style='color: red;'>No activo</p>"}</td>
                    <td>${user.email}</td>
                    <td>${user.first_name}</td>
                    <td>${user.last_name}</td>
                    <td>${user.username}</td>
                    <td>${userType}</td>
                    <td>
                    <button class='btn btn-sm btn-primary' onclick="editUser(${user.id})"><i class='fa-solid fa-pencil'></i></button>
                        ${userType == 'Administrador' ?
                    "" :
                    `<button class='btn btn-sm btn-danger' onclick="deleteUser(${user.id})"><i class='fa-solid fa-trash-can'></i></button>`}
                        </td>
                </tr>`;
        });

        tableBody_users.innerHTML = content;

    } catch (ex) {
        alert(ex);
    }

}


const deleteUser = async (userId) => {
    try {
        const result = await Swal.fire({
            title: "¿Quieres eliminar al usuario?",
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: "Eliminar",
            confirmButtonColor: "#dc3545", // Color rojo para el botón "Eliminar"
            denyButtonText: `No eliminar`,
            denyButtonColor: "#28a745", // Color verde para el botón "No eliminar"
            cancelButtonText: 'Cancelar',
            customClass: {
                confirmButton: "btn btn-danger",
                denyButton: "btn btn-success",
                cancelButton: "btn btn-primary"
            }
        });

        if (result.isConfirmed) {
            const response = await fetch(`/deleteUser/${userId}`);

            if (response.ok) {
                $(`#user-${userId}`).remove();
                Swal.fire("Usuario eliminado correctamente", "", "success");
            } else {
                throw new Error('Failed to delete user');
            }
        } else if (result.isDenied) {
            Swal.fire("Cambios no guardados", "", "info");
        }
    } catch (ex) {
        alert(ex);
    }
};


// Función que se llama cuando el modal se abre y llena los campos
const cargarDatosUsuario = async(userId) => {
    console.log(userId);
    const response = await fetch(`/listUserPorId/${userId}`);
    
    // Verificar si la respuesta es exitosa
    if (!response.ok) {
        console.error("Error en la respuesta del servidor:", response.status);
        return;
    }
    
    // Obtener los datos JSON de la respuesta
    const usuario = await response.json();
    
    console.log("Datos del usuario:", usuario);

    // Llenar los campos con los valores del usuario
    document.getElementById('edit-user-id').value = usuario.id;
    document.getElementById('edit-user-email').value = usuario.email;
    document.getElementById('edit-user-firstname').value = usuario.first_name;
    document.getElementById('edit-user-lastname').value = usuario.last_name;
    document.getElementById('edit-user-username').value = usuario.username;
    
    // Establecer el tipo de usuario (esto se basa en tu lógica)
    document.getElementById('edit-usertype').value = usuario.is_waiter ? 'Mesero' : 'Chef';

    // Establecer el estado del usuario
    if (usuario.is_active) {
        document.getElementById('option1').checked = true;
    } else {
        document.getElementById('option2').checked = true;
    }
}

 
  

const editUser = async (userId) => {
    try {

        $('#edit-user-id').val(userId);
        cargarDatosUsuario(userId)
        $('#editUserModal').modal('show');
    } catch (ex) {
        alert(ex);
    }
};

const guardarCambios = async (userId) => {
    console.log("ID usuario editar: " + userId)
    try {
        const result = await Swal.fire({
            title: "¿Quieres guardar los datos del usuaio?",
            showDenyButton: true,
            confirmButtonText: "Guardar",
            confirmButtonColor: "#28a745",
            denyButtonText: `No guardar`,
            denyButtonColor: "#dc3545",
            customClass: {
                confirmButton: "btn btn-danger",
                denyButton: "btn btn-success",
                cancelButton: "btn btn-primary"
            }
        });

        if (result.isConfirmed) {
            const email = document.getElementById('edit-user-email').value;
            const firstName = document.getElementById('edit-user-firstname').value;
            const lastName = document.getElementById('edit-user-lastname').value;
            const username = document.getElementById('edit-user-username').value;
            const userType = document.getElementById('edit-usertype').value;
            const userStatus = document.querySelector('input[name="option"]:checked').value;

            const data = {
                email: email,
                first_name: firstName,
                last_name: lastName,
                username: username,
                userType: userType,
                user_status: userStatus
            };

            console.log(data)

            const response = await fetch(`/actulizarDatosUsuario/${userId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                Swal.fire({
                    title: "Usuario actualizado correctamente",
                    icon: "success"
                }).then(() => {
                    // Cerrar el modal
                    $('#editUserModal').modal('hide');
                    // Recargar la página
                    window.location.reload();
                });
            } else {
                Swal.fire("Error al actualizar al usuario", "", "error");
            }
        }
    } catch (ex) {
        alert(ex);
    }
};




window.addEventListener('load', async () => {
    await initDatatable();
});

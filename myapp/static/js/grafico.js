document.addEventListener("DOMContentLoaded", function() {
  // Hacer la solicitud fetch al endpoint datos_facturas
  fetch('/datos_facturas/')
    .then(response => response.json()) // Parsear la respuesta como JSON
    .then(data => {
      // Verificar los datos
      console.log("Datos recibidos:", data);
      
      // Obtener las fechas y valores de la respuesta
      const fechas = data.fechas; // Formato yyyy-mm-dd
      const valores = data.valores;
      
      // Crear un objeto para almacenar las fechas agrupadas por "Mes - Semana del mes" y sus valores sumados
      const sumaPorSemanaDelMes = {};

      // Agrupar por mes y semana del mes
      fechas.forEach((fechaStr, index) => {
        // Convertir la fecha de formato 'yyyy-mm-dd' a un objeto Date
        const fecha = new Date(fechaStr); // Esto crea una fecha válida a partir de una cadena 'yyyy-mm-dd'

        // Obtener el mes (nombre) y el año de la fecha
        const mes = fecha.toLocaleString('es-ES', { month: 'long' });
        const año = fecha.getFullYear(); // Año de la fecha

        // Obtener el día del mes
        const diaDelMes = fecha.getDate();

        // Calcular la semana del mes (dividimos el día entre 7 y redondeamos hacia arriba)
        const semanaDelMes = Math.ceil(diaDelMes / 7);

        // Crear una clave combinada 'Mes - Semana del mes'
        const clave = `${mes} Semana ${semanaDelMes} ${año}`;

        // Agrupar las ventas por 'Mes - Semana del mes'
        if (sumaPorSemanaDelMes[clave]) {
          sumaPorSemanaDelMes[clave] += valores[index];
        } else {
          sumaPorSemanaDelMes[clave] = valores[index];
        }
      });

      // Convertir el objeto agrupado en arrays para las etiquetas y valores del gráfico
      const fechasAgrupadas = [];
      const valoresSumados = [];

      // Iterar sobre las claves y agregar las etiquetas y los valores
      for (const clave in sumaPorSemanaDelMes) {
        fechasAgrupadas.push(clave);  // Ej: "Abril Semana 1 2025"
        valoresSumados.push(sumaPorSemanaDelMes[clave]);  // Ventas sumadas
      }

    
      const meseros = data.nombres_meseros;
      const ventas_meseros = data.cantidades_vendidas_meseros;
      const mesas = data.nombres_mesas;
      console.log(data.productos, data.cantidades_productos)




      function ajustarCanvasAltaResolucion(canvas) {
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;

    // Guardamos tamaño CSS actual
    const cssWidth = canvas.clientWidth;
    const cssHeight = canvas.clientHeight;

    // Ajustamos el tamaño real del canvas para mayor resolución
    canvas.width = cssWidth * dpr;
    canvas.height = cssHeight * dpr;

    // Mantener tamaño CSS para que no cambie en pantalla
    canvas.style.width = cssWidth + "px";
    canvas.style.height = cssHeight + "px";

    // Escalamos contexto para que los dibujos se vean nítidos
    ctx.scale(dpr, dpr);
}

const ids = ["histograma", "meseros", "mesas", "histogramaProductos", "histogramaDias"];

ids.forEach(id => {
    const canvas = document.getElementById(id);
    if (canvas) ajustarCanvasAltaResolucion(canvas);
});


      
      crearGrafico(fechasAgrupadas, valoresSumados);
      crearGrafico2(meseros, ventas_meseros);
      crearGrafico3(mesas, data.cantidades_vendidas_mesas, 0);
      crearGrafico4(data.productos, data.cantidades_productos);
      crearGrafico5(data.dias_semana, data.ventas_dias);



      document.getElementById('descargar-pdf').addEventListener('click', function() {
        descargarPDF('histograma', 'grafico_ventas_mes_semana.pdf', 180, 160); 
        descargarPDF('meseros', 'grafico_ventas_meseros.pdf', 180, 160 ); 
        descargarPDF('mesas', 'grafico_ventas_mesas.pdf', 180, 160); 
        descargarPDF('histogramaProductos', 'grafico_productos_mas_vendidos.pdf', 180, 160);
        descargarPDF('histogramaDias', 'grafico_dias_vendidos.pdf', 180, 160);


      });
    })
    .catch(error => {
      console.error("Error al obtener los datos:", error);
    });
});

 



const crearGrafico = (fechas, valores) => {
  const ctx = document.getElementById('histograma').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'bar', // Cambiar el tipo de gráfico a 'bar' (barras)
    data: {
      labels: fechas, // Las fechas se pasan como etiquetas en el eje X
      datasets: [{
        label: 'Total venta del día',
        data: valores, // Los valores sumados para cada fecha
        backgroundColor: 'rgba(255, 165, 0, 0.6)', // Color naranja con opacidad de las barras
        borderColor: 'rgba(255, 165, 0, 0.6)', // Color del borde de las barras (azul)
        borderWidth: 1, // Ancho del borde de las barras
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            font: {
              family: 'Arial',
              size: 14
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: 'black' // Color de los ticks del eje Y
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje Y
          },
          title: {
            display: true,
            text: 'Cantidad', // Título del eje Y
            color: 'black', // Color del título del eje Y
            font: {
              size: 16,  // Tamaño de la fuente del título
              family: 'Arial' // Fuente del título
            }
          }
        },
        x: {
          ticks: {
            color: 'black' // Color de los ticks del eje X
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje X
          },
          title: {
            display: true,
            text: 'Día', // Título del eje X
            color: 'black', // Color del título del eje X
            font: {
              size: 16,  // Tamaño de la fuente del título
              family: 'Arial' // Fuente del título
            }
          }
        }
      },
      layout: {
        padding: {
          left: 10,
          right: 10,
          top: 10,
          bottom: 10
        }
      },
      backgroundColor: '#ffffff', // Fondo blanco para el gráfico
    }
  });
};


const crearGrafico2 = (nombres, ventas) => {
  const ctx = document.getElementById('meseros').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'bar', // Tipo de gráfico: Barras
    data: {
      labels: nombres, // Las etiquetas serán los nombres de los meseros
      datasets: [{
        label: 'Venta de meseros',
        data: ventas, // Las ventas totales por mesero
        backgroundColor: 'rgba(255, 165, 0, 0.6)', // Color naranja con opacidad de las barras
        borderColor: 'rgba(255, 165, 0, 0.6)', // Color del borde de las barras (azul)
        borderWidth: 1, // Ancho del borde de las barras
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top', // Posición de la leyenda
          labels: {
            font: {
              family: 'Arial', // Tipo de fuente para la leyenda
              size: 14 // Tamaño de la fuente
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: 'black' // Color de los ticks del eje Y
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje Y
          },
          title: {
            display: true,
            text: 'Cantidad', // Título del eje Y
            color: 'black', // Color del título del eje Y
            font: {
              size: 16,  // Tamaño de la fuente del título
              family: 'Arial' // Fuente del título
            }
          }
        },
        x: {
          ticks: {
            color: 'black' // Color de los ticks del eje X
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje X
          },
          title: {
            display: true,
            text: 'Nombre de usuario', // Título del eje X
            color: 'black', // Color del título del eje X
            font: {
              size: 16,  // Tamaño de la fuente del título
              family: 'Arial' // Fuente del título
            }
          }
        }
      },
      layout: {
        padding: {
          left: 10,
          right: 10,
          top: 10,
          bottom: 10
        }
      },
      backgroundColor: '#ffffff', // Fondo blanco para el gráfico
    }
  });
};


const crearGrafico3 = (mesas, ventas_mesas, total_venta_mesas) => {
  const ctx = document.getElementById('mesas').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'pie', // Tipo de gráfico: Torta
    data: {
      labels: mesas, // Las mesas se pasan como etiquetas en el gráfico
      datasets: [{
        label: 'Total venta por mesa',
        data: ventas_mesas, // Los valores sumados para cada mesa
        backgroundColor: [
          'rgba(54, 162, 235, 1)', // Color para la primera sección
          'rgba(255, 99, 132, 1)', // Color para la segunda sección
          'rgba(255, 159, 64, 1)', // Color para la tercera sección
          'rgba(75, 192, 192, 1)', // Color para la cuarta sección
          'rgba(153, 102, 255, 1)', // Color para la quinta sección
          'rgba(255, 159, 64, 1)', // Color para más secciones
          'rgba(255, 205, 86, 1)'  // Otro color si hay más mesas
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)', // Color de borde para la primera sección
          'rgba(255, 99, 132, 1)', // Color de borde para la segunda sección
          'rgba(255, 159, 64, 1)', // Color de borde para la tercera sección
          'rgba(75, 192, 192, 1)', // Color de borde para la cuarta sección
          'rgba(153, 102, 255, 1)', // Color de borde para la quinta sección
          'rgba(255, 159, 64, 1)', // Color de borde para más secciones
          'rgba(255, 205, 86, 1)'  // Otro color de borde
        ],
        borderWidth: 1, // Ancho del borde de las secciones
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top', // Posición de la leyenda
          labels: {
            font: {
              family: 'Arial',
              size: 14
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(tooltipItem) {
              return `${tooltipItem.label}: ${tooltipItem.raw}`; // Formato de la etiqueta en el tooltip
            }
          }
        },
        title: {
          display: true, // Habilitar el título
          text: `Cantidad de ventas por mesa`, // Título dinámico con el valor de total_venta_mesas
          font: {
            size: 18, // Tamaño de la fuente del título
            family: 'Arial', // Tipo de fuente
            weight: 'bold' // Peso de la fuente
          },
          color: '#333', // Color del título
          padding: {
            top: 10,    // Espacio superior
            bottom: 20  // Espacio inferior
          }
        }
      },
      layout: {
        padding: {
          left: 10,
          right: 10,
          top: 10,
          bottom: 10
        }
      },
      cutoutPercentage: 0, // Esto asegura que sea un gráfico de torta completo (sin agujero en el medio)
      backgroundColor: '#ffffff', // Fondo blanco para el gráfico
    }
  });
};


const crearGrafico4 = (productos, cantidades) => {
  const ctx = document.getElementById('histogramaProductos').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'bar', // Cambiar el tipo de gráfico a 'bar' (barras)
    data: {
      labels: productos, // Las fechas se pasan como etiquetas en el eje X
      datasets: [{
        label: 'Total vendido por producto',
        data: cantidades, // Los valores sumados para cada fecha
        backgroundColor: 'rgba(255, 165, 0, 0.6)', // Color naranja con opacidad de las barras
        borderColor: 'rgba(255, 165, 0, 0.6)', // Color del borde de las barras (azul)
        borderWidth: 1, // Ancho del borde de las barras
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            font: {
              family: 'Arial',
              size: 14
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: 'black' // Color de los ticks del eje Y
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje Y
          },
          title: {
            display: true,
            text: 'Cantidad', // Título del eje Y
            color: 'black', // Color del título del eje Y
            font: {
              size: 16,  // Tamaño de la fuente del título
              family: 'Arial' // Fuente del título
            }
          }
        },
        x: {
          ticks: {
            color: 'black' // Color de los ticks del eje X
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje X
          },
          title: {
            display: true,
            text: 'Día', // Título del eje X
            color: 'black', // Color del título del eje X
            font: {
              size: 16,  // Tamaño de la fuente del título
              family: 'Arial' // Fuente del título
            }
          }
        }
      },
      layout: {
        padding: {
          left: 10,
          right: 10,
          top: 10,
          bottom: 10
        }
      },
      backgroundColor: '#ffffff', // Fondo blanco para el gráfico
    }
  });
};

const crearGrafico5= (dias, cantidadesDias) => {
  const ctx = document.getElementById('histogramaDias').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'bar', // Cambiar el tipo de gráfico a 'bar' (barras)
    data: {
      labels: dias, // Las fechas se pasan como etiquetas en el eje X
      datasets: [{
        label: 'Ventas diarias',
        data: cantidadesDias, // Los valores sumados para cada fecha
        backgroundColor: 'rgba(255, 165, 0, 0.6)', // Color naranja con opacidad de las barras
        borderColor: 'rgba(255, 165, 0, 0.6)', // Color del borde de las barras (azul)
        borderWidth: 1, // Ancho del borde de las barras
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            font: {
              family: 'Arial',
              size: 14
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: 'black' // Color de los ticks del eje Y
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje Y
          },
          title: {
            display: true,
            text: 'Total', // Título del eje Y
            color: 'black', // Color del título del eje Y
            font: {
              size: 16,  // Tamaño de la fuente del título
              family: 'Arial' // Fuente del título
            }
          }
        },
        x: {
          ticks: {
            color: 'black' // Color de los ticks del eje X
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje X
          },
          title: {
            display: true,
            text: 'Día', // Título del eje X
            color: 'black', // Color del título del eje X
            font: {
              size: 16,  // Tamaño de la fuente del título
              family: 'Arial' // Fuente del título
            }
          }
        }
      },
      layout: {
        padding: {
          left: 10,
          right: 10,
          top: 10,
          bottom: 10
        }
      },
      backgroundColor: '#ffffff', // Fondo blanco para el gráfico
    }
  });
};






// Interfaz base
class ExportStrategy {
    export(canvasIdOrArray, nombreArchivo, width, height) {
        throw new Error("Debes implementar el método export.");
    }
}

// Estrategia para exportar todos los gráficos en un PDF (cada uno en página diferente)
class MultiChartPDFExportStrategy extends ExportStrategy {
    export(canvasIds, nombreArchivo, maxWidth = 180, maxHeight = 160) {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        canvasIds.forEach((canvasId, index) => {
            const canvas = document.getElementById(canvasId);
            if (!canvas) {
                console.warn(`Canvas con id "${canvasId}" no encontrado.`);
                return;
            }

            const imgData = canvas.toDataURL("image/png");

            if (index > 0) doc.addPage();

            // Tamaño real del canvas
            const canvasWidth = canvas.width;
            const canvasHeight = canvas.height;

            // Calcular escala para que quepa dentro del tamaño máximo sin deformar
            const widthRatio = maxWidth / canvasWidth;
            const heightRatio = maxHeight / canvasHeight;
            const scale = Math.min(widthRatio, heightRatio, 1);

            const w = canvasWidth * scale;
            const h = canvasHeight * scale;

            // Centrar imagen en página PDF
            const pageWidth = doc.internal.pageSize.getWidth();
            const pageHeight = doc.internal.pageSize.getHeight();

            const x = (pageWidth - w) / 2;
            const y = (pageHeight - h) / 2;

            doc.addImage(imgData, "PNG", x, y, w, h);
        });

        doc.save(nombreArchivo);
    }
}


// Estrategia para exportar todos los gráficos en PNG (varios archivos, uno por gráfico)
class MultiChartPNGExportStrategy extends ExportStrategy {
    export(canvasIds, nombreArchivoBase) {
        canvasIds.forEach((canvasId) => {
            const canvas = document.getElementById(canvasId);
            if (!canvas) {
                console.warn(`Canvas con id "${canvasId}" no encontrado.`);
                return;
            }
            const img = canvas.toDataURL("image/png");

            // Crear enlace y descargar cada PNG con nombre diferente
            const link = document.createElement("a");
            link.href = img;
            link.download = `${nombreArchivoBase}_${canvasId}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }
}

// Contexto
class Exporter {
    constructor(strategy) {
        this.strategy = strategy;
    }

    setStrategy(strategy) {
        this.strategy = strategy;
    }

    export(canvasIds, nombreArchivo, width = 180, height = 160) {
        this.strategy.export(canvasIds, nombreArchivo, width, height);
    }
}

// Funciones para botones
function exportarTodosLosGraficosComoPDF() {
    const canvasIds = [
        "histograma",
        "meseros",
        "mesas",
        "histogramaProductos",
        "histogramaDias"
    ];

    const exporter = new Exporter(new MultiChartPDFExportStrategy());
    // maxWidth y maxHeight los puedes cambiar según necesites
    exporter.export(canvasIds, "todos_los_graficos.pdf", 180, 160);
}


function exportarTodosLosGraficosComoPNG() {
    const canvasIds = [
        "histograma",
        "meseros",
        "mesas",
        "histogramaProductos",
        "histogramaDias"
    ];
    const exporter = new Exporter(new MultiChartPNGExportStrategy());
    exporter.export(canvasIds, "grafico");
}
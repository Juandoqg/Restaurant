document.addEventListener("DOMContentLoaded", function() {
  // Hacer la solicitud fetch al endpoint datos_facturas
  fetch('/datos_facturas/')
    .then(response => response.json()) // Parsear la respuesta como JSON
    .then(data => {
      // Verificar los datos
      console.log("Datos recibidos:", data);
      
      // Obtener las fechas y valores de la respuesta
      const fechas = data.fechas;
      const valores = data.valores;

      // Agrupar las facturas por fecha y sumar los valores
      const fechasAgrupadas = [];
      const valoresSumados = [];

      // Crear un objeto para almacenar las fechas únicas y sus valores sumados
      const sumaPorFecha = {};

      // Agrupar por fecha
      fechas.forEach((fecha, index) => {
        if (sumaPorFecha[fecha]) {
          sumaPorFecha[fecha] += valores[index]; // Sumar el valor de las facturas del mismo día
        } else {
          sumaPorFecha[fecha] = valores[index]; // Crear una nueva entrada para la fecha
        }
      });

      // Convertir el objeto de fechas agrupadas a arreglos para las etiquetas y valores del gráfico
      for (const fecha in sumaPorFecha) {
        fechasAgrupadas.push(fecha);
        valoresSumados.push(sumaPorFecha[fecha]);
      }

      // Llamar a la función para crear el gráfico con los datos agrupados
      crearGrafico(fechasAgrupadas, valoresSumados);
    })
    .catch(error => {
      console.error("Error al obtener los datos:", error);
    });
});

const crearGrafico = (fechas, valores) => {
  const ctx = document.getElementById('histograma').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'line', // Tipo de gráfico: Línea
    data: {
      labels: fechas, // Las fechas se pasan como etiquetas en el eje X
      datasets: [{
        label: 'Total venta del dia',
        data: valores, // Los valores sumados para cada fecha
        fill: false, // Evitar el relleno bajo la línea
        borderColor: 'rgba(54, 162, 235, 1)', // Color de la línea
        borderWidth: 2, // Ancho de la línea
        tension: 0.4 // Suaviza la curva de la línea
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
          }
        },
        x: {
          ticks: {
            color: 'black' // Color de los ticks del eje X
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)' // Color de la cuadrícula en el eje X
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
      elements: {
        line: {
          borderColor: 'rgba(54, 162, 235, 1)', // línea  azul
          borderWidth: 2, 
        }
      }
    }
  });
};

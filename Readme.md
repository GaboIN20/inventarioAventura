# Ecoparque y Reserva Natural "Aventuras del Sur" (`inventarioAventura`)

Plataforma web desarrollada en **Django** y **MySQL** para la administración de experiencias al aire libre, control de acceso basado en roles y gestión de reservas[cite: 1].

## Credenciales de Prueba por Rol[cite: 1]

| Rol | Usuario | Contraseña | Nombre Completo | Permisos y Datos Cargados |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador**[cite: 1] | `admin_parque` | `admin123` | Carlos Admin | Control total: usuarios, categorías, experiencias y reservas[cite: 1]. |
| **Guía / Operador 1**[cite: 1] | `guia_juan` | `guia123` | Juan Pérez | Crea, lista y edita sus propias experiencias (4 creadas)[cite: 1]. |
| **Guía / Operador 2**[cite: 1] | `guia_ana` | `guia123` | Ana Soto | Crea, lista y edita sus propias experiencias (4 creadas)[cite: 1]. |
| **Turista / Cliente 1**[cite: 1] | `turista_pedro` | `turista123` | Pedro Gómez | Visualiza catálogo e inscribe experiencias (3 reservas)[cite: 1]. |
| **Turista / Cliente 2**[cite: 1] | `turista_maria` | `turista123` | María Rojas | Visualiza catálogo e inscribe experiencias (3 reservas)[cite: 1]. |

## Instalación y Ejecución

1. **Crear base de datos en MySQL:**
   Importar el archivo `respaldo_ecoparque.sql` incluido en este repositorio (crea automáticamente la base de datos `ecoparque_db` y carga los registros)[cite: 1].

2. **Instalar dependencias:**
   ```bash
   pip install django pymysql
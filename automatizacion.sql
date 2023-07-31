-- Crear Base de Datos
create database dbp_automatizacion_bot;
use dbp_automatizacion_bot;

-- -----------------------------------------------------
------------------ Table `tbl_prueba`-------------------
-- -----------------------------------------------------

create table tbl_prueba (
  PKUSU_NCODIGO int not null auto_increment primary key,    
  PRU_TITULO varchar(255) DEFAULT NULL,
  PRU_INTRODUCCION varchar(255) DEFAULT NULL,
  PRU_HISTORIA varchar(255) DEFAULT NULL,
  PRU_COMPONENTES varchar(255) DEFAULT NULL,
  PRU_FECHA_REGISTRO TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-------------- Table `tbl_principala`-------------------
-- -----------------------------------------------------
create table tbl_principal(
  PKUSU_NCODIGO int not null auto_increment primary key,    
  PRI_PROCESO varchar(255) DEFAULT NULL,
  PRI_DETALLE varchar(255) DEFAULT NULL,
  PRI_REGISTRO TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRI_CFECHA_MODIFICACION TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRI_CESTADO varchar(255) DEFAULT 'Activo' 
  );

-- -----------------------------------------------------
-------------------- Table `tbl_logs`-------------------
-- -----------------------------------------------------
create table tbl_logs(
  PKUSU_NCODIGO int not null auto_increment primary key,    
  LOG_TIPO_ERROR varchar(255) DEFAULT NULL,
  LOG_REGISTRO TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  LOG_FECHA_MODIFICACION TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  LOG_ESTADO varchar(255) DEFAULT 'Activo' 
  );

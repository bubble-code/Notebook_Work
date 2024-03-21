from sqlalchemy import create_engine, text, bindparam, Integer, select, func
from Conexion import MainConexion
from sqlalchemy.orm import sessionmaker
import pandas as pd

class ImportArticulos:
    def __init__(self):
        self.ruta_archivo = r'ArtFormateados2.xlsx' 
        self.hoja_excel = 'Sheet1'
        

    def getDatosArtIndustry(self, TipoArticulo =1):
        mainConexion = MainConexion()
        try:
            conn = mainConexion.Open_Conn_Industry()
            if conn:
                print("Get DatosArtIndustry")
                query = text(
                    f"SELECT MArticulo.CodigoArticulo, MArticulo.Descripcion, MArticulo.Familia, MArticulo.Subfamilia, MArticulo.UltimoPrecioCoste, MArticulo.PrecioCosteMedio, MArticulo.ProveedorHabitual, MArticulo.PlazoAprovisionam, MArticulo.PlazoSeguridad, MArticulo.SerieMinimaRentable, MArticulo.TipoArticulo, MArticulo.StockMinimo, MArticulo.StockMaximo, MArticulo.Existencia, MArticulo.UnidReservadas, MArticulo.UnidOrdenadas, MArticulo.Codigo2, MArticulo.Codigo3, MArticulo.FechaUltimaCompra, MArticulo.FechaUltimaEntrada, MArticulo.FechaUltimaSalida, MArticulo.FechaCreacion, MArticulo.PesoNeto, MArticulo.PesoBruto, MArticulo.UnidMedidaCompra, MArticulo.UnidMedidaVenta, MArticulo.UnidMedidaAlmacen, MArticulo.MultiploFabricacion, MArticulo.TipoEnvase, MArticulo.CantidadEnvase, MArticulo.NumPlano, MArticulo.CodigoMoldeMatriz, MArticulo.EstadoArticulo, MArticulo.UnidConverCompra, MArticulo.AlmacenDefecto, MArticulo.CodigoUltimoProv, MArticulo.Inventariable, MArticulo.UbicacionDefecto, MArticulo.FechaDeAlta, MArticulo.FechaUltimaModificacion, MArticulo.UsuarioAlta, MArticulo.UsuarioModificacion, MArticulo.Version, MArticulo.GuardaVersion, MArticulo.Descripcion2, MArticulo.SumatorioComponentes, MArticulo.UnidConverVenta, MArticulo.PrecioCosteStandard, MArticulo.PrecioCompra, MArticulo.PrecioCompraDivisa, MArticulo.CodigoMoneda, MArticulo.PorcIVA, MArticulo.PorcRecargo, MArticulo.ABC, MArticulo.Trazabilidad, MArticulo.CriterioAsignacionLote, MArticulo.NumeroSerie, MArticulo.DiasCuarentena, MArticulo.RevisionPlano, MArticulo.FechaUltimaRevisionPlano, MArticulo.UnidMedidasEnvase, MArticulo.MedidaEnvaseLargo, MArticulo.MedidaEnvaseAncho, MArticulo.MedidaEnvaseAlto, MArticulo.UnidVolumenEnvase, MArticulo.MedidaEnvaseVolumen, MArticulo.ClientePrincipal, MArticulo.ClienteExclusivo, MArticulo.PrecioHIFO, MArticulo.FechaPrecioHIFO, MArticulo.MultiploConsumo, MArticulo.LotificacionPropia, MArticulo.ValorNumeroSerie, MArticulo.CosteStandarMOE, MArticulo.PrecioVenta, MArticulo.IDDocumAdjuntos, MArticulo.MesesGarantia, MArticulo.SistemaDistribucionObjetivos, MArticulo.PorcComision, MArticulo.CodNomenclaturaCombinada, MArticulo.RegimenEstadisticoHabitual, MArticulo.NaturalezaTransaccionA, MArticulo.NaturalezaTransaccionB, MArticulo.CodUnidadSuplem, MArticulo.FactorConversionSuplem, MArticulo.ClaseArticulo, MArticulo.Plantilla, MArticulo.GeneradorPlantilla, MArticulo.CodigoEstructura, MArticulo.EjecucionEN15085, MArticulo.TipoImpuesto, MArticulo.TipoArticuloVariantes, MArticulo.MesesCaducidad, MArticulo.Contador, MArticulo.Generico, MArticulo.FijarCosteStandard, MArticulo.Despunte, MArticulo.PorcRecuperado, MArticulo.altCantidadPorLote, MArticulo.DiasCaducidad, MArticulo.Pantone, MArticulo.RAL, MArticulo.CodigoAdicionalIntrastat, MArticulo.ExcluirEnIntrastat, MArticulo.DiasCaducidadInterna, MArticulo.MesesCaducidadInterna, MArticulo.MinimoCompra, MArticulo.PorcIGIC, MArticulo.VersionDesc, MArticulo.AplicaRedondeo, MArticulo.DecimalesRedondeo, MArticulo.Kit, MArticulo.UltimoPrecioCosteConInd, MArticulo.ProductoECommerce, MArticulo.ProductoDestacadoECommerce, MArticulo.AplicarRedondeoAlza, MArticulo.NumOperacionesTotales, MArticulo.NumOperacionesSerieLarga, MArticulo.Notificaciones, MArticulo.CtrlLimitePrecioVenta, MArticulo.CodigoEstructura1, MArticulo.LoteEntrega, MArticulo.DiasAprovComprasMasLargo, REPLACE(MArticuloCuenta.CuentaCompras, ' ', '') + REPLACE(MArticuloCuenta.SubcuentaCompras, ' ', '') AS CCompra FROM MArticulo LEFT OUTER JOIN MArticuloCuenta ON MArticulo.CodigoArticulo = MArticuloCuenta.CodigoArticulo ")
                    # WHERE TipoArticulo = N'{TipoArticulo}'")
                result = conn.execute(query).fetchall()
                print("Completed")
                return result
        except Exception as e:
            print("Error en la consulta:", e)
        finally:
            if conn:
                conn.close()

    def CheckArticuloSolmicro(self,listArticulos):
        mainConexion = MainConexion()
        resultados = []
        try:
            conn = mainConexion.Open_Conn_Solmicro()
            if conn:
                print("Check articulo in Solmicro")
                for articulo in listArticulos:
                    print(articulo[0])
                    query = text(f"SELECT top(1) IDArticulo FROM tbMaestroArticulo WHERE IDArticulo = N'{articulo[0]}' ")
                    result = conn.execute(query).fetchone()
                    if not result:
                        resultados.append(articulo)
                conn.commit()
                conn.close()
                print("Completado")
            return resultados
        except Exception as e:
            print("Error en la consulta:", e)
            return resultados
        
    def serializer(self, datos):
        result = []
        print("Serializing")
        for linea in datos:
            result.append(
                {
                    "IDArticulo": linea[0].strip(),
                    "DescArticulo": linea[1].strip(),
                    "IDContador": "NULL",
                    "FechaAlta": "2023-12-15 00:00:00.383",
                    "IDEstado": 0,
                    "IDTipo": str(linea[10]).zfill(2) if linea[10] is not None else "04",
                    "IDFamilia": "VENTACLIEN" if linea[10] == 1 else linea[2],
                    "IDSubfamilia": linea[2] if not None and linea[10] == 1 else linea[3] if linea[3] is not None else "00",
                    "CCVenta": "70000000" if linea[10] == 1 else "NULL",
                    "CCExport": "NULL",
                    "CCCompra": linea[123] if linea[10] == 4 else "NULL",
                    "CCImport": "NULL",
                    "CCVentaRegalo": "NULL",
                    "CCStocks": "NULL",
                    "IDTipoIva": "NOR",
                    "IDPartidaEstadistica": "NULL",
                    "IDUdInterna": linea[26] if linea[26] is not None else "u.",
                    "IDUdVenta": linea[25] if linea[25] is not None else "u.",
                    "IDUdCompra": linea[24] if linea[24] is not None else "u.",
                    "PrecioEstandarA": linea[47],
                    "PrecioEstandarB": linea[47],
                    "FechaEstandar": "2023-12-15 00:00:00.383",
                    "UdValoracion": 1,
                    "PesoNeto": linea[22],
                    "PesoBruto": linea[23],
                    "TipoEstructura": 0,
                    "IDTipoEstructura": "NULL",
                    "TipoRuta": 0,
                    "IDTipoRuta": "NULL",
                    "CodigoBarras": "NULL",
                    "PuntoVerde": 0.00000000,
                    "PVPMinimo": linea[74],
                    "PorcentajeRechazo": 0,
                    "Plazo": linea[7],
                    "Volumen": 0,
                    "RecalcularValoracion": 1,
                    "CriterioValoracion": 0,
                    "GestionStockPorLotes": 0,
                    "PrecioUltimaCompraA": 0.00000000,
                    "PrecioUltimaCompraB": 0.00000000,
                    "FechaUltimaCompra": "NULL",
                    "IDProveedorUltimaCompra": "NULL",
                    "LoteMultiplo": 0,
                    "CantMinSolicitud": 0,
                    "CantMaxSolicitud": 0,
                    "LimitarPetDia": 0,
                    "IdArticuloConfigurado": "NULL",
                    "ContRadical": "NULL",
                    "IdFamiliaConfiguracion": "NULL",
                    "PrecioBase": linea[74],
                    "Configurable": 0,
                    "FechaCreacionAudi": "2023-12-15 00:00:00.383",
                    "FechaModificacionAudi": "2023-12-15 00:00:00.383",
                    "UsuarioAudi": f"favram\\a.obregon",
                    "NivelPlano": linea[30],
                    "StockNegativo": 0,
                    "PlazoFabricacion": linea[7],
                    "ParamMaterial": 3 if linea[10] == 1 else "NULL",
                    "ParamTerminado": 1 if linea[10] == 1 else "NULL",
                    "ParamTerminado": 0.00000000,
                    "AplicarLoteMRP": 0,
                    "NSerieObligatorio": 0,
                    "PuntosMarketing": 0,
                    "ValorPuntosMarketing": 0,
                    "ValorReposicionA": 0.00000000,
                    "ValorReposicionB": 0.00000000,
                    "FechaValorReposicion": "NULL",
                    "ControlRecepcion": 0,
                    "IDEstadoHomologacion": "NULL",
                    "IDArticuloFinal": "NULL",
                    "GenerarOFArticuloFinal": 0,
                    "IdDocumentoEspecificacion": "NULL",
                    "NivelModificacionPlan": "NULL",
                    "FechaModificacionNivelPlan": "NULL",
                    "TipoFactAlquiler": 0,
                    "Seguridad": 0,
                    "Reglamentacion": 0,
                    "SeguridadReglamentacion": 0,
                    "DiasMinimosFactAlquiler": 0,
                    "SinDtoEnAlquiler": 0,
                    "SinSeguroEnAlquiler": 0,
                    "NecesitaOperario": 0,
                    "IDConcepto": "NULL",
                    "CCVentaGRUPO": "NULL",
                    "CCExportGRUPO": "NULL",
                    "CCImportGRUPO": "NULL",
                    "CCCompraGRUPO": "NULL",
                    "FacturacionAsociadaMaq": 0,
                    "FactTasaResiduos": 0,
                    "NoImprimirEnFactura": 0,
                    "IDArticuloContenedor": "NULL",
                    "QContenedor": "NULL",
                    "IDArticuloEmbalaje": "NULL",
                    "QEmbalaje": "NULL",
                    "Color": "NULL",
                    "IDCaracteristicaArticulo1": "NULL",
                    "IDCaracteristicaArticulo2": "NULL",
                    "IDCaracteristicaArticulo3": "NULL",
                    "IDCaracteristicaArticulo4": "NULL",
                    "IDCaracteristicaArticulo5": "NULL",
                    "IDArticuloPadre": "NULL",
                    "TipoPrecio": "NULL",
                    "IDTipoProducto": "NULL",
                    "IDTipoMaterial": "NULL",
                    "IDTipoSubMaterial": "NULL",
                    "IDTipoEnvase": "NULL",
                    "IDComerIndus": "NULL",
                    "IDTipoIVAReducido": "NULL",
                    "IDUdInterna2": "NULL",
                    "Observaciones": "NULL",
                    "PorcenIVANoDeducible": "NULL",
                    "PrecioBaseConfigurado": "NULL",
                    "Alias": "NULL",
                    "IDCategoria": "NULL",
                    "IDAnada": "NULL",
                    "IDColorVino": "NULL",
                    "IDCategoriaVino": "NULL",
                    "IDFormato": "NULL",
                    "IDMarcaComercial": "NULL",
                    "IDEmpresa": "NULL",
                    "INFAPNecesitaOperario": "NULL",
                    "RetencionIRPF": 1,
                    "IncluirEnEMCS": 0,
                    "ClaveDeclaracion": "NULL",
                    "IDRegistroFitosanitario": "NULL",
                    "RiquezaNPK": "NULL",
                    "IDTipoAbono": "NULL",
                    "IDTipoFertilizacion": "NULL",
                    "ClaveProductoSilicie": "NULL",
                    "TipoEnvaseSilicie": "NULL",
                    "ExcluirSilicie": 0,
                    "IDCalificacion": "NULL",
                    "IDProductoVino": "NULL",
                    "IDPaisOrigen": "NULL",
                    "CodigoEstructura": "NULL",
                    "Certif31": "NULL",
                    "Ubicacion": "NULL",
                    "Codigo3": "NULL",
                    "Descripcion2": "NULL",
                    "INFAPP": "NULL",
                    "EJEN15085": "NULL",
                    "TIPO15085": "NULL",
                    "TIPO15085": "NULL",
                    "ExcluirCupos": 0,
                    "IDCampanaCupoClasificacion": "NULL",
                    "KGPlastico": "NULL",
                    "KGPlasticoNR": "NULL",
                    "ClaveProducto": "NULL",
                    "GestionContraPedidoVenta": 0,
                    "UsuarioCreacionAudi": "NULL",
                    "Espesor": "NULL",
                    "Activo": 1,
                    "Venta": 1
                }
            )
        print("End Serializado")
        return result
    
    def serializer2(self, datos):
        result = []
        print("Serializing")
        for linea in datos:
            result.append(
                {
                    "IDArticulo": linea[0],
                    "DescArticulo": linea[1],
                    "IDContador": linea[2],
                    "FechaAlta": linea[3],
                    "IDEstado": linea[4],
                    "IDTipo": linea[5],
                    "IDFamilia": linea[6],
                    "IDSubfamilia": linea[7],
                    "CCVenta": linea[8],
                    "CCExport": linea[9],
                    "CCCompra": linea[10],
                    "CCImport": linea[11],
                    "CCVentaRegalo": linea[12],
                    "CCStocks": linea[13],
                    "IDTipoIva": linea[14],
                    "IDPartidaEstadistica": linea[15],
                    "IDUdInterna": linea[16],
                    "IDUdVenta": linea[17],
                    "IDUdCompra": linea[18],
                    "PrecioEstandarA": linea[19],
                    "PrecioEstandarB": linea[20],
                    "FechaEstandar": linea[21],
                    "UdValoracion": linea[22],
                    "PesoNeto": linea[23],
                    "PesoBruto": linea[24],
                    "TipoEstructura": linea[25],
                    "IDTipoEstructura": linea[26],
                    "TipoRuta": linea[27],
                    "IDTipoRuta": linea[28],
                    "CodigoBarras": linea[29],
                    "PuntoVerde": linea[30],
                    "PVPMinimo": linea[31],
                    "PorcentajeRechazo": linea[32],
                    "Plazo": linea[33],
                    "Volumen": linea[34],
                    "RecalcularValoracion": linea[35],
                    "CriterioValoracion": linea[36],
                    "GestionStockPorLotes": linea[37],
                    "PrecioUltimaCompraA": linea[38],
                    "PrecioUltimaCompraB": linea[39],
                    "FechaUltimaCompra": linea[40],
                    "IDProveedorUltimaCompra": linea[41],
                    "LoteMultiplo": linea[42],
                    "CantMinSolicitud": linea[43],
                    "CantMaxSolicitud": linea[44],
                    "LimitarPetDia": linea[45],
                    "IdArticuloConfigurado": linea[46],
                    "ContRadical": linea[47],
                    "IdFamiliaConfiguracion": linea[48],
                    "PrecioBase": linea[49],
                    "Configurable": linea[50],
                    "FechaCreacionAudi": linea[51],
                    "FechaModificacionAudi": linea[52],
                    "UsuarioAudi": linea[53],
                    "NivelPlano": linea[54],
                    "StockNegativo": linea[55],
                    "PlazoFabricacion": linea[56],
                    "ParamMaterial": linea[57],
                    "ParamTerminado": linea[58],
                    "ParamTerminado": linea[59],
                    "AplicarLoteMRP": linea[60],
                    "NSerieObligatorio": linea[61],
                    "PuntosMarketing": linea[62],
                    "ValorPuntosMarketing": linea[63],
                    "ValorReposicionA": linea[64],
                    "ValorReposicionB": linea[65],
                    "FechaValorReposicion": linea[66],
                    "ControlRecepcion": linea[67],
                    "IDEstadoHomologacion": linea[68],
                    "IDArticuloFinal": linea[69],
                    "GenerarOFArticuloFinal": linea[70],
                    "IdDocumentoEspecificacion": None,
                    "NivelModificacionPlan": None,
                    "FechaModificacionNivelPlan": None,
                    "TipoFactAlquiler": 0,
                    "Seguridad": 0,
                    "Reglamentacion": 0,
                    "SeguridadReglamentacion": 0,
                    "DiasMinimosFactAlquiler": 0,
                    "SinDtoEnAlquiler": 0,
                    "SinSeguroEnAlquiler": 0,
                    "NecesitaOperario": 0,
                    "IDConcepto": None,
                    "CCVentaGRUPO": None,
                    "CCExportGRUPO": None,
                    "CCImportGRUPO": None,
                    "CCCompraGRUPO": None,
                    "FacturacionAsociadaMaq": 0,
                    "FactTasaResiduos": 0,
                    "NoImprimirEnFactura": 0,
                    "IDArticuloContenedor": None,
                    "QContenedor": None,
                    "IDArticuloEmbalaje": None,
                    "QEmbalaje": None,
                    "Color": None,
                    "IDCaracteristicaArticulo1": None,
                    "IDCaracteristicaArticulo2": None,
                    "IDCaracteristicaArticulo3": None,
                    "IDCaracteristicaArticulo4": None,
                    "IDCaracteristicaArticulo5": None,
                    "IDArticuloPadre": None,
                    "TipoPrecio": None,
                    "IDTipoProducto": None,
                    "IDTipoMaterial": None,
                    "IDTipoSubMaterial": None,
                    "IDTipoEnvase": None,
                    "IDComerIndus": None,
                    "IDTipoIVAReducido": None,
                    "IDUdInterna2": None,
                    "Observaciones": None,
                    "PorcenIVANoDeducible": None,
                    "PrecioBaseConfigurado": None,
                    "Alias": None,
                    "IDCategoria": None,
                    "IDAnada": None,
                    "IDColorVino": None,
                    "IDCategoriaVino": None,
                    "IDFormato": None,
                    "IDMarcaComercial": None,
                    "IDEmpresa": None,
                    "INFAPNecesitaOperario": None,
                    "RetencionIRPF": 1,
                    "IncluirEnEMCS": 0,
                    "ClaveDeclaracion": None,
                    "IDRegistroFitosanitario": None,
                    "RiquezaNPK": None,
                    "IDTipoAbono": None,
                    "IDTipoFertilizacion": None,
                    "ClaveProductoSilicie": None,
                    "TipoEnvaseSilicie": None,
                    "ExcluirSilicie": 0,
                    "IDCalificacion": None,
                    "IDProductoVino": None,
                    "IDPaisOrigen": None,
                    "CodigoEstructura": None,
                    "Certif31": None,
                    "Ubicacion": None,
                    "Codigo3": None,
                    "Descripcion2": None,
                    "INFAPP": None,
                    "EJEN15085": None,
                    "TIPO15085": None,
                    "TIPO15085": None,
                    "ExcluirCupos": 0,
                    "IDCampanaCupoClasificacion": None,
                    "KGPlastico": None,
                    "KGPlasticoNR": None,
                    "ClaveProducto": None,
                    "GestionContraPedidoVenta": 0,
                    "UsuarioCreacionAudi": None,
                    "Espesor": None,
                    "Activo": 1,
                    "Venta": 1
                }
            )
        print("End Serializado")
        return result
    
    @staticmethod
    def export_to_excel_art_desd_indus(data):
        print("Exporting")
        df = pd.DataFrame(data, columns=["IDArticulo",	"DescArticulo",	"IDContador",	"FechaAlta",	"IDEstado",	"IDTipo",	"IDFamilia",	"IDSubfamilia",	"CCVenta",	"CCExport",	"CCCompra",	"CCImport",	"CCVentaRegalo",	"CCGastoRegalo",	"CCStocks",	"IDTipoIva",	"IDPartidaEstadistica",	"IDUdInterna",	"IDUdVenta",	"IDUdCompra",	"PrecioEstandarA",	"PrecioEstandarB",	"FechaEstandar",	"UdValoracion",	"PesoNeto",	"PesoBruto",	"TipoEstructura",	"IDTipoEstructura",	"TipoRuta",	"IDTipoRuta",	"CodigoBarras",	"PuntoVerde",	"PVPMinimo",	"PorcentajeRechazo",	"Plazo",	"Volumen",	"RecalcularValoracion",	"CriterioValoracion",	"GestionStockPorLotes",	"PrecioUltimaCompraA",	"PrecioUltimaCompraB",	"FechaUltimaCompra",	"IDProveedorUltimaCompra",	"LoteMultiplo",	"CantMinSolicitud",	"CantMaxSolicitud",	"LimitarPetDia",	"IdArticuloConfigurado",	"ContRadical",	"IdFamiliaConfiguracion",	"PrecioBase",	"Configurable",	"FechaCreacionAudi",	"FechaModificacionAudi",	"UsuarioAudi",	"NivelPlano",	"StockNegativo",	"PlazoFabricacion",	"ParamMaterial",	"ParamTerminado",	"CapacidadDiaria",	"AplicarLoteMRP",	"NSerieObligatorio",	"PuntosMarketing",	"ValorPuntosMarketing",	"ValorReposicionA",	"ValorReposicionB",	"FechaValorReposicion",	"ControlRecepcion",	"IDEstadoHomologacion",	"IDArticuloFinal",	"GenerarOFArticuloFinal",	"IdDocumentoEspecificacion",	"NivelModificacionPlan",	"FechaModificacionNivelPlan",	"TipoFactAlquiler","Seguridad",	"Reglamentacion",	"SeguridadReglamentacion",	"DiasMinimosFactAlquiler",	"SinDtoEnAlquiler",	"SinSeguroEnAlquiler",	"NecesitaOperario",	"IDConcepto",	"CCVentaGRUPO",	"CCExportGRUPO",	"CCImportGRUPO",	"CCCompraGRUPO",	"FacturacionAsociadaMaq",	"FactTasaResiduos",	"NoImprimirEnFactura",	"IDArticuloContenedor",	"QContenedor",	"IDArticuloEmbalaje",	"QEmbalaje",	"Color",	"IDCaracteristicaArticulo1",	"IDCaracteristicaArticulo2",	"IDCaracteristicaArticulo3",	"IDCaracteristicaArticulo4",	"IDCaracteristicaArticulo5",	"IDArticuloPadre",	"TipoPrecio",	"IDTipoProducto",	"IDTipoMaterial",	"IDTipoSubMaterial",	"IDTipoEnvase",	"IDComerIndus",	"IDTipoIVAReducido",	"IDUdInterna2",	"Observaciones",	"PorcenIVANoDeducible",	"PrecioBaseConfigurado",	"Alias",	"IDCategoria",	"IDAnada",	"IDColorVino",	"IDCategoriaVino",	"IDFormato",	"IDMarcaComercial",	"IDEmpresa",	"RetencionIRPF",	"IncluirEnEMCS",	"ClaveDeclaracion",	"IDRegistroFitosanitario",	"RiquezaNPK",	"IDTipoAbono",	"IDTipoFertilizacion",	"ClaveProductoSilicie",	"TipoEnvaseSilicie",	"ExcluirSilicie",	"IDCalificacion",	"IDProductoVino",	"IDPaisOrigen",	"CodigoEstructura",	"Certif31",	"Ubicacion",	"Codigo3",	"Descripcion2",	"INFAPP",	"EJEN15085",	"TIPO15085",	"ExcluirCupos",	"IDCampanaCupoClasificacion",	"KGPlastico",	"KGPlasticoNR",	"ClaveProducto",	"GestionContraPedidoVenta",	"UsuarioCreacionAudi",	"Espesor",	"Activo",	"Venta"])
        df.to_excel("ImportArticulos04.xlsx", index=False)
        print("End Exportacion")


obj = ImportArticulos()
listSubfamiliaIndustry = obj.getDatosArtIndustry(TipoArticulo=4)
print(len(listSubfamiliaIndustry))
input("Continuar")
checkSubFamiliaSolmicro = obj.CheckArticuloSolmicro(listArticulos=listSubfamiliaIndustry)
print(len(checkSubFamiliaSolmicro))
input("Continuar")
articulosSerialilzados = obj.serializer(datos=checkSubFamiliaSolmicro)
input("Continuar")
obj.export_to_excel_art_desd_indus(data=articulosSerialilzados)
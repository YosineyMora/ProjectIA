
__versión__ = "1.0"


"""
El módulo *reportePDF* permite crear un reporte PDF sencillo.
"""

from sqlite3 import connect
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black, purple, white
from reportlab.pdfgen import canvas
import os
from datetime import date
from datetime import datetime


# ======================= CLASE reportePDF =========================

class reportePDF(object):
    """Exportar una lista de diccionarios a una tabla en un
       archivo PDF."""

    def __init__(self, titulo, cabecera, datos, nombrePDF):
        super(reportePDF, self).__init__()

        self.titulo = titulo
        self.cabecera = cabecera
        self.datos = datos
        self.nombrePDF = nombrePDF

        self.estilos = getSampleStyleSheet()

    @staticmethod
    def _encabezadoPiePagina(canvas, archivoPDF):
        """Guarde el estado de nuestro lienzo para que podamos aprovecharlo"""

        canvas.saveState()
        estilos = getSampleStyleSheet()

        alineacion = ParagraphStyle(name="alineacion", alignment=TA_RIGHT,
                                    parent=estilos["Normal"])

        # Encabezado
        encabezadoNombre = Paragraph(
            "IA - Sistema de detección Facial", estilos["Normal"])
        anchura, altura = encabezadoNombre.wrap(
            archivoPDF.width, archivoPDF.topMargin)
        encabezadoNombre.drawOn(canvas, archivoPDF.leftMargin, 736)

        # Día actual
        today = date.today()
        fecha = str(today.day)+"/"+str(today.month)+"/"+str(today.year)

        fechaReporte = fecha.replace("-", "de")

        encabezadoFecha = Paragraph(fechaReporte, alineacion)
        anchura, altura = encabezadoFecha.wrap(
            archivoPDF.width, archivoPDF.topMargin)
        encabezadoFecha.drawOn(canvas, archivoPDF.leftMargin, 736)

        # Pie de página
        piePagina = Paragraph(
            "Reporte generado por Andres Niño.", estilos["Normal"])
        anchura, altura = piePagina.wrap(
            archivoPDF.width, archivoPDF.bottomMargin)
        piePagina.drawOn(canvas, archivoPDF.leftMargin, 15 * mm + (0.2 * inch))

        # Suelta el lienzo
        canvas.restoreState()

    def convertirDatos(self):
        """Convertir la lista de diccionarios a una lista de listas para crear
           la tabla PDF."""

        estiloEncabezado = ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,
                                          fontSize=10, textColor=white,
                                          fontName="Helvetica-Bold",
                                          parent=self.estilos["Normal"])

        estiloNormal = self.estilos["Normal"]
        estiloNormal.alignment = TA_LEFT

        claves, nombres = zip(*[[k, n] for k, n in self.cabecera])

        encabezado = [Paragraph(nombre, estiloEncabezado)
                      for nombre in nombres]
        nuevosDatos = [tuple(encabezado)]

        for dato in self.datos:
            nuevosDatos.append(
                [Paragraph(str(dato[clave]), estiloNormal) for clave in claves])

        return nuevosDatos

    def Exportar(self):
        """Exportar los datos a un archivo PDF."""

        alineacionTitulo = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=13,
                                          leading=10, textColor=purple,
                                          parent=self.estilos["Heading1"])

        self.ancho, self.alto = letter

        convertirDatos = self.convertirDatos()

        tabla = Table(convertirDatos, colWidths=(
            self.ancho-100)/len(self.cabecera), hAlign="CENTER")
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), purple),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            # Texto centrado y alineado a la izquierda
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("INNERGRID", (0, 0), (-1, -1), 0.50, black),  # Lineas internas
            ("BOX", (0, 0), (-1, -1), 0.25, black),  # Linea (Marco) externa
        ]))

        historia = []
        historia.append(Paragraph(self.titulo, alineacionTitulo))
        historia.append(Spacer(1, 0.16 * inch))
        historia.append(tabla)

        archivoPDF = SimpleDocTemplate(self.nombrePDF, leftMargin=50, rightMargin=50, pagesize=letter,
                                       title="Reporte PDF", author="Andres Niño")

        try:
            archivoPDF.build(historia, onFirstPage=self._encabezadoPiePagina,
                             onLaterPages=self._encabezadoPiePagina,
                             canvasmaker=numeracionPaginas)

         # +------------------------------------+
            return "Reporte generado con éxito."
         # +------------------------------------+
        except PermissionError:
         # +--------------------------------------------+
            return "Error inesperado: Permiso denegado."
         # +--------------------------------------------+


# ================== CLASE numeracionPaginas =======================

class numeracionPaginas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Agregar información de la página a cada página (página x de y)"""
        numeroPaginas = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(numeroPaginas)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, conteoPaginas):
        self.drawRightString(204 * mm, 15 * mm + (0.2 * inch),
                             "Página {} de {}".format(self._pageNumber, conteoPaginas))


# ===================== FUNCIÓN generarReporte =====================


def obtenerTotal(rutaDeteccion, rutaDesconocido):
    cantDetec = len(os.listdir(rutaDeteccion))
    cantDesc = len(os.listdir(rutaDesconocido))
    contenidoTotal = cantDetec + cantDesc
    return contenidoTotal


def obtenercantDetec(rutaDeteccion):
    cantDetec = len(os.listdir(rutaDeteccion))
    return cantDetec


def obtenercantDesc(rutaDesconocido):
    cantDesc = len(os.listdir(rutaDesconocido))
    return cantDesc


datos = []


def generarGroupAllReporte():

    ruta = "Results\\Grupal\\"
    list = os.listdir(ruta)
    for i in list:
        rutaDeteccion = ruta+"\\"+i+"\\"+i
        rutaDesconocido = ruta+"\\"+i+"\\"+"Desconocido"
        contenidoTotal = obtenerTotal(rutaDeteccion, rutaDesconocido)
        cantDetec = obtenercantDetec(rutaDeteccion)
        cantDesc = obtenercantDesc(rutaDesconocido)
   

        pA = round((cantDetec/contenidoTotal)*100, 2)
        pD = round((cantDesc/contenidoTotal)*100, 2)

        datos.append({"NOMBRE": i, "ACIERTOS": cantDetec, "FALLOS": cantDesc,
                    "TOTAL": contenidoTotal, "PACIERTOS": str(pA)+"%", "PFALLOS": str(pD)+"%"})

    # conexionDB.close()

    titulo = "Informe Grupal de detecciones"

    cabecera = (
        ("NOMBRE", "NOMBRE"),
        ("ACIERTOS", "ACIERTOS"),
        ("FALLOS", "FALLOS"),
        ("TOTAL", "DETECCIONES TOTALES"),
        ("PACIERTOS", "% CORRECTOS"),
        ("PFALLOS", "% DESCONOCIDOS")
    )

    nombrePDF = "ReporteGrupal.pdf"

    reporte = reportePDF(titulo, cabecera, datos, nombrePDF).Exportar()
    print(reporte)


# ======================== LLAMAR FUNCIÓN ==========================


# generarGroupAllReporte()

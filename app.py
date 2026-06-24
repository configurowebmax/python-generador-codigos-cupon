"""
=====================================================================
 Generador de Códigos de Cupón
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_generador_codigos_cupon_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Generador de Códigos de Cupón."""

    def __init__(self, cantidad, longitud):
        self.cantidad = float(cantidad)
        self.longitud = float(longitud)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        import random, string
        n = int(self.cantidad) if self.cantidad > 0 else 1
        L = int(self.longitud) if self.longitud > 0 else 8
        chars = string.ascii_uppercase + string.digits
        codigos = []
        for _ in range(n):
            codigos.append("".join(random.choice(chars) for _ in range(L)))
        return {"codigos": codigos}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""
        return "✅ Códigos generados. Úsalos en tu campaña."


# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("cantidad"), input_float("longitud"))
    r = c.calcular()
    lista = "\n".join(r["codigos"])
    html = f"""
      <div class="result-value">🎟️ {len(r["codigos"])} códigos</div>
      <pre style="white-space:pre-wrap;background:#fff;padding:1rem;border-radius:8px;border:1px solid var(--cweb-border);">{lista}</pre>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "cantidad": input_float("cantidad"),
            "longitud": input_float("longitud"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
        if "cantidad" in datos:
            document.querySelector("#cantidad").value = datos["cantidad"]
        if "longitud" in datos:
            document.querySelector("#longitud").value = datos["longitud"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()

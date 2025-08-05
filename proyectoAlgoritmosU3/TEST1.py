import streamlit as st
from datetime import datetime

# --- ESTRUCTURA DE DATOS ---
# Cada ticket: [código, cliente, descripción, prioridad, fecha_rec, fecha_entrega, estado, tipo_equipo, precio]
if 'tickets' not in st.session_state:
    st.session_state.tickets = []

# --- FUNCIONES DE ORDENAMIENTO ---
def bubble_sort_by_priority(tickets, descending=False):
    n = len(tickets)
    for i in range(n-1):
        for j in range(n-1-i):
            if (tickets[j][3] > tickets[j+1][3]) != descending:
                tickets[j], tickets[j+1] = tickets[j+1], tickets[j]

def selection_sort_by_date(tickets, descending=False):
    n = len(tickets)
    for i in range(n):
        sel = i
        for j in range(i+1, n):
            if (tickets[j][4] < tickets[sel][4]) != descending:
                sel = j
        if sel != i:
            tickets[i], tickets[sel] = tickets[sel], tickets[i]

def bubble_sort_by_price(tickets, descending=False):
    n = len(tickets)
    for i in range(n-1):
        for j in range(n-1-i):
            if (tickets[j][8] > tickets[j+1][8]) != descending:
                tickets[j], tickets[j+1] = tickets[j+1], tickets[j]

def selection_sort_by_type(tickets, descending=False):
    n = len(tickets)
    for i in range(n):
        sel = i
        for j in range(i+1, n):
            if (tickets[j][7] < tickets[sel][7]) != descending:
                sel = j
        if sel != i:
            tickets[i], tickets[sel] = tickets[sel], tickets[i]

# --- GENERADOR DE CÓDIGO ---
def next_ticket_code():
    num = len(st.session_state.tickets) + 1
    return f"TKT-{num:03d}"

# --- INTERFAZ ---
st.title("Sistema de Tickets - Soporte Técnico")

menu = ["Ingresar ticket", "Mostrar tickets", "Ordenar tickets", "Buscar/Editar ticket"]
choice = st.sidebar.radio("Menú", menu)

if choice == "Ingresar ticket":
    st.header("Ingresar nuevo ticket")
    with st.form("form_ticket"):
        code = next_ticket_code()
        st.text_input("Código del ticket", value=code, disabled=True)
        cliente = st.text_input("Cliente")
        desc = st.text_area("Descripción del problema")
        prioridad = st.selectbox("Prioridad", ["1-Alta", "2-Media", "3-Baja"])
        fecha = st.date_input("Fecha de recepción", value=datetime.now().date())
        tipo_equipo = st.selectbox("Tipo de equipo", ["Laptop", "Celular", "Impresora", "Computadora", "Otros"])
        precio = st.number_input("Precio estimado de reparación (S/.)", min_value=0.0, step=10.0)
        enviar = st.form_submit_button("Guardar ticket")
        
        if enviar:
            if not cliente.strip() or not prioridad or not fecha or not tipo_equipo or precio == 0.0:
                st.error("Por favor, completa todos los campos obligatorios antes de continuar.")
            else:
                st.session_state.tickets.append([
                    code,
                    cliente,
                    desc,
                    int(prioridad[0]),
                    fecha,
                    None,
                    "En proceso",
                    tipo_equipo,
                    precio
                ])
                st.success(f"Ticket {code} registrado.")

elif choice == "Mostrar tickets":
    st.header("Tickets registrados")
    if not st.session_state.tickets:
        st.info("No hay tickets para mostrar.")
    else:
        for i, t in enumerate(st.session_state.tickets, start=1):
            st.markdown(
                f"**{i}. {t[0]}** | Cliente: {t[1]} | Prioridad: {t[3]} | Equipo: {t[7]} | Precio: S/ {t[8]:.2f} | "
                f"Recepción: {t[4].strftime('%d/%m/%Y')} | Estado: {t[6]}"
            )

elif choice == "Ordenar tickets":
    st.header("Ordenar tickets")
    if not st.session_state.tickets:
        st.info("No hay tickets para ordenar.")
    else:
        criterio = st.selectbox("Ordenar por:", ["Prioridad", "Fecha de recepción", "Precio", "Tipo de equipo"])
        orden = st.radio("Orden:", ["Ascendente", "Descendente"])
        descending = orden == "Descendente"

        if st.button("Ordenar"):
            if criterio == "Prioridad":
                bubble_sort_by_priority(st.session_state.tickets, descending)
            elif criterio == "Fecha de recepción":
                selection_sort_by_date(st.session_state.tickets, descending)
            elif criterio == "Precio":
                bubble_sort_by_price(st.session_state.tickets, descending)
            elif criterio == "Tipo de equipo":
                selection_sort_by_type(st.session_state.tickets, descending)
            st.success(f"Tickets ordenados por {criterio.lower()} ({orden.lower()}).")

        for t in st.session_state.tickets:
            st.write(
                f"{t[0]} | Cliente: {t[1]} | Prioridad: {t[3]} | Equipo: {t[7]} | "
                f"Precio: S/ {t[8]:.2f} | Recepción: {t[4].strftime('%d/%m/%Y')} | Estado: {t[6]}"
            )

elif choice == "Buscar/Editar ticket":
    st.header("Buscar y Editar Ticket")
    if not st.session_state.tickets:
        st.info("No hay tickets.")
    else:
        num = st.text_input("Número de solicitud (ej: 1 o 042)")
        if st.button("Buscar"):
            try:
                code_search = f"TKT-{int(num):03d}"
                encontrados = [(i, t) for i, t in enumerate(st.session_state.tickets) if t[0] == code_search]
                if encontrados:
                    idx, t = encontrados[0]
                    st.session_state.selected_ticket_idx = idx
                    st.session_state.found_ticket = True
                else:
                    st.warning("No se encontró ningún ticket con ese código.")
                    st.session_state.found_ticket = False
            except ValueError:
                st.error("Por favor ingresa un número válido.")
                st.session_state.found_ticket = False

        if st.session_state.get("found_ticket", False):
            idx = st.session_state.selected_ticket_idx
            t = st.session_state.tickets[idx]
            st.write(f"{t[0]} | Cliente: {t[1]} | Estado: {t[6]} | Precio: S/ {t[8]:.2f}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Marcar como completado"):
                    st.session_state.tickets[idx][6] = "Completado"
                    st.session_state.tickets[idx][5] = datetime.now().date()
                    st.success("Ticket marcado como completado.")
                    st.rerun()
            with col2:
                if st.button("Eliminar ticket"):
                    st.session_state.tickets.pop(idx)
                    st.success("Ticket eliminado.")
                    st.session_state.found_ticket = False
                    st.rerun()

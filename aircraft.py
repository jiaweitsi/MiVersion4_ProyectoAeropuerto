from airport import *
import matplotlib.pyplot as plt
import math

# -------------------------------------------------------
# CLASE Aircraft - Version 2 + 4
# -------------------------------------------------------

class Aircraft:
    def __init__(self, aircraft, company, origin, time, destination="", departure_time=""):
        self.aircraft = aircraft          # id del avion (string)
        self.company = company            # codigo ICAO aerolinea (3 letras)
        self.origin = origin              # aeropuerto origen (4 letras ICAO)
        self.time = time                  # hora de llegada (hh:mm)

       #===VERSIÓN 4===
        self.destination = destination    # aeropuerto destino (4 letras ICAO) - NUEVO V4
        self.departure_time = departure_time  # hora de salida (hh:mm) - NUEVO V4


# -------------------------------------------------------
# FUNCIONES VERSION 2
# -------------------------------------------------------

#===== LOAD ARRIVALS =====
def LoadArrivals(filename):
    lista_arrivals = []
    try:
        f = open(filename, "r")
        lineas = f.readlines()
        f.close()

        i = 1
        while i < len(lineas):
            partes = lineas[i].split()
            if len(partes) == 4:
                aircraft = partes[0]
                origin = partes[1]
                time = partes[2]
                company = partes[3]
                if ':' in time:
                    nuevo = Aircraft(aircraft, company, origin, time)
                    lista_arrivals.append(nuevo)
            i = i + 1

    except FileNotFoundError:
        print("No se encontro el archivo:", filename)
        return []
    return lista_arrivals

#===== PLOT ARRIVALS =====
def PlotArrivals(aircrafts):

    if len(aircrafts) == 0:
        print("No existeix la llista")
        return

    Vx = range(24)  # hores
    Vy = [0] * 24  # arribades/hora
    i = 0
    while i < len(aircrafts):
        fila = aircrafts[i]
        tiempo = fila.time
        if tiempo != "":  # saltar aviones nocturnos sin hora de llegada
            partes = tiempo.split(":")
            if len(partes) == 2 and partes[0] != "":
                hlanding = int(partes[0])
                Vy[hlanding] = Vy[hlanding] + 1
        i = i + 1

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.bar(Vx, Vy, color='skyblue', edgecolor='black')
    ax.set_title("Frecuencia de aterrizajes por hora")
    ax.set_ylabel("Número de aviones")
    ax.set_xlabel("Hora del día")
    ax.set_xticks(range(0, 24))

    return fig


#===== SAVE FLIGHTS =====
def SaveFlights(aircrafts, filename):
    if len(aircrafts) == 0:
        print("No existeix la llista")
        return False
    try:
        out = open(filename, 'w')
        out.write("Aircraft\tOrigin\tTime\tCompany\tDestination\tDeparture\n")
        i = 0
        while i < len(aircrafts):
            fila = aircrafts[i]

            aircraft = fila.aircraft if fila.aircraft != "" else "-"
            origin = fila.origin if fila.origin != "" else "-"
            arrival = fila.time if fila.time != "" else "-"
            airline = fila.company if fila.company != "" else "-"
            destination = fila.destination if fila.destination != "" else "-"
            departure = fila.departure_time if fila.departure_time != "" else "-"

            out.write(aircraft + "\t" + origin + "\t" + arrival + "\t" +
                      airline + "\t" + destination + "\t" + departure + "\n")
            i = i + 1

        out.close()
        return True
    except:
        print("No se pudo guardar el archivo")
        return False


#===== PLOT AIRLINES =====
def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("No existeix la llista")
        return

    # Primero contamos los vuelos por aerolinea (igual que antes)
    Vx = []
    Vy = []
    i = 0
    while i < len(aircrafts):
        fila = aircrafts[i]
        airline = fila.company
        if airline not in Vx:
            Vx.append(airline)
            Vy.append(1)
        else:
            encontrado = False
            x = 0
            while not encontrado and x < len(Vx):
                if Vx[x] == airline:
                    encontrado = True
                else:
                    x = x + 1
            if encontrado:
                Vy[x] = Vy[x] + 1
        i = i + 1

    # Ahora ordenamos para quedarnos solo con las 10 con mas vuelos
    # Usamos bubble sort para ordenar de mayor a menor
    n = len(Vx)
    j = 0
    while j < n - 1:
        k = 0
        while k < n - j - 1:
            if Vy[k] < Vy[k + 1]:
                # Intercambiamos vuelos
                temp_y = Vy[k]
                Vy[k] = Vy[k + 1]
                Vy[k + 1] = temp_y
                # Intercambiamos nombres
                temp_x = Vx[k]
                Vx[k] = Vx[k + 1]
                Vx[k + 1] = temp_x
            k = k + 1
        j = j + 1

    # Nos quedamos solo con las 10 primeras
    if len(Vx) > 10:
        Vx = Vx[0:10]
        Vy = Vy[0:10]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(Vx, Vy, color='orange')
    ax.set_xlabel("Aerolíneas")
    ax.set_ylabel("Número de vuelos")
    ax.set_title("Top 10 aerolíneas con más vuelos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

#===== PLOT FLIGHTS TYPE =====
def PlotFlightsType(aircrafts):
    if len(aircrafts) > 0:
        schengen = 0
        no_schengen = 0

        schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
                          'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

        i = 0
        while i < len(aircrafts):
            fila = aircrafts[i]
            origen = fila.origin
            inicio = origen[0:2]
            encontrado = False
            j = 0
            while j < len(schengen_codes) and not encontrado:
                if schengen_codes[j] == inicio:
                    encontrado = True
                else:
                    j = j + 1

            if encontrado == True:
                schengen = schengen + 1
            else:
                no_schengen = no_schengen + 1
            i = i + 1

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(['Schengen', 'No Schengen'], [schengen, no_schengen], color=['blue', 'red'])
        ax.set_title("Vuelos Schengen vs No Schengen")
        ax.set_ylabel("Cantidad de vuelos")
        return fig
    else:
        return None

#===== MAP FLIGHTS =====
def MapFlights(lista_arrivals, lista_airports):
    f = open("trayectorias.kml", "w")

    # Cabecera del archivo KML - comillas dobles obligatorias para Google Earth
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    f.write("<Document>\n")

    # Estilo para vuelos Schengen: linea verde
    f.write("  <Style id=\"schengen\">\n")
    f.write("    <LineStyle>\n")
    f.write("      <color>ff00ff00</color>\n")
    f.write("      <width>3</width>\n")
    f.write("    </LineStyle>\n")
    f.write("  </Style>\n")

    # Estilo para vuelos no Schengen: linea roja
    f.write("  <Style id=\"noschengen\">\n")
    f.write("    <LineStyle>\n")
    f.write("      <color>ff0000ff</color>\n")
    f.write("      <width>3</width>\n")
    f.write("    </LineStyle>\n")
    f.write("  </Style>\n")

    # Coordenadas de Barcelona El Prat (LEBL)
    lat_bcn = 41.297445
    lon_bcn = 2.0832941

    schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
                      'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

    i = 0
    while i < len(lista_arrivals):
        vuelo = lista_arrivals[i]

        # Buscamos el aeropuerto origen en la lista
        aeropuerto_encontrado = None
        j = 0
        while j < len(lista_airports):
            if lista_airports[j].code == vuelo.origin:
                aeropuerto_encontrado = lista_airports[j]
            j = j + 1

        # Solo dibujamos si encontramos el aeropuerto origen
        if aeropuerto_encontrado != None:

            # Comprobamos si es Schengen mirando las 2 primeras letras del codigo origen
            es_schengen = False
            k = 0
            while k < len(schengen_codes):
                if vuelo.origin[0:2] == schengen_codes[k]:
                    es_schengen = True
                k = k + 1

            if es_schengen:
                estilo = "schengen"
            else:
                estilo = "noschengen"

            f.write("  <Placemark>\n")
            f.write("    <name>" + vuelo.aircraft + " desde " + vuelo.origin + "</name>\n")
            f.write("    <styleUrl>#" + estilo + "</styleUrl>\n")
            f.write("    <LineString>\n")
            f.write("      <tessellate>1</tessellate>\n")
            f.write("      <coordinates>\n")
            # Origen: lon,lat del aeropuerto de salida
            f.write("        " + str(aeropuerto_encontrado.lon) + "," +
                    str(aeropuerto_encontrado.lat) + ",0\n")
            # Destino: lon,lat de Barcelona
            f.write("        " + str(lon_bcn) + "," + str(lat_bcn) + ",0\n")
            f.write("      </coordinates>\n")
            f.write("    </LineString>\n")
            f.write("  </Placemark>\n")

        i = i + 1

    f.write("</Document>\n")
    f.write("</kml>\n")
    f.close()
    print("Archivo trayectorias.kml generado.")

#===== LONG FLIGHT ARRIVALS =====
def LongFlightArrivals(aircrafts, lista_aeropuertos):
    vuelos_largos = []

    lat_bcn = 0
    lon_bcn = 0
    k = 0
    while k < len(lista_aeropuertos):
        if lista_aeropuertos[k].code == "LEBL":
            lat_bcn = lista_aeropuertos[k].lat
            lon_bcn = lista_aeropuertos[k].lon
        k = k + 1

    radio_tierra = 6371

    i = 0
    while i < len(aircrafts):
        vuelo = aircrafts[i]
        lat_origen = 0
        lon_origen = 0
        encontrado = False

        j = 0
        while j < len(lista_aeropuertos) and not encontrado:
            if lista_aeropuertos[j].code == vuelo.origin:
                lat_origen = lista_aeropuertos[j].lat
                lon_origen = lista_aeropuertos[j].lon
                encontrado = True
            j = j + 1

        if encontrado:
            phi1 = math.radians(lat_origen)
            phi2 = math.radians(lat_bcn)
            dphi = math.radians(lat_bcn - lat_origen)
            dlambda = math.radians(lon_bcn - lon_origen)

            a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distancia = radio_tierra * c

            if distancia > 2000:
                vuelos_largos.append(vuelo)
        i = i + 1

    return vuelos_largos


# -------------------------------------------------------
# FUNCIONES VERSION 4
# -------------------------------------------------------

#===== LOAD DEPARTURES =====
def LoadDepartures(filename):
    # Carga el archivo de salidas y devuelve lista de Aircraft
    # Solo rellena: aircraft, company, destination, departure_time
    lista_departures = []
    try:
        f = open(filename, "r")
        lineas = f.readlines()
        f.close()
    except FileNotFoundError:
        print("No se encontro el archivo:", filename)
        return lista_departures

    # Formato: AIRCRAFT DESTINATION DEPARTURE AIRLINE
    i = 1
    while i < len(lineas):
        partes = lineas[i].split()
        if len(partes) == 4:
            aircraft = partes[0]
            destination = partes[1]
            departure_time = partes[2]
            company = partes[3]
            if ':' in departure_time:
                # Solo rellenamos campos de salida, llegada vacia
                nuevo = Aircraft(aircraft, company, "", "", destination, departure_time)
                lista_departures.append(nuevo)
        i = i + 1

    return lista_departures

#===== MERGE MOVEMENTS =====
def MergeMovements(arrivals, departures):
    # Combina listas de llegadas y salidas por ID de avion
    # Si los tiempos son compatibles (llegada < salida) se fusionan
    # Aviones solo en departures = aviones nocturnos
    # Devuelve lista fusionada

    if len(arrivals) == 0 or len(departures) == 0:
        print("Error: una de las listas esta vacia")
        return []

    # Empezamos copiando todas las llegadas
    merged = []
    i = 0
    while i < len(arrivals):
        ac = arrivals[i]
        nuevo = Aircraft(ac.aircraft, ac.company, ac.origin, ac.time, ac.destination, ac.departure_time)
        merged.append(nuevo)
        i = i + 1

    # Para cada salida buscamos si hay una llegada del mismo avion compatible
    i = 0
    while i < len(departures):
        dep = departures[i]
        encontrado = False

        j = 0
        while j < len(merged) and not encontrado:
            # Mismo id de avion
            if merged[j].aircraft == dep.aircraft:
                # Comprobamos que la llegada es antes que la salida
                if merged[j].time != "" and merged[j].departure_time == "":
                    hora_arr = int(merged[j].time.split(":")[0])
                    min_arr = int(merged[j].time.split(":")[1])
                    hora_dep = int(dep.departure_time.split(":")[0])
                    min_dep = int(dep.departure_time.split(":")[1])

                    total_arr = hora_arr * 60 + min_arr
                    total_dep = hora_dep * 60 + min_dep

                    if total_dep > total_arr:
                        # Fusionamos: añadimos datos de salida al avion de llegada
                        merged[j].destination = dep.destination
                        merged[j].departure_time = dep.departure_time
                        encontrado = True
            j = j + 1

        if not encontrado:
            # Es un avion nocturno: solo tiene salida, no llegada
            nuevo = Aircraft(dep.aircraft, dep.company, "", "", dep.destination, dep.departure_time)
            merged.append(nuevo)

        i = i + 1

    return merged

#===== NIGHT AIRCRAFT =====

def NightAircraft(aircrafts):
    # Devuelve lista de aviones que solo tienen salida (sin llegada)
    # Son los que pasaron la noche en el aeropuerto

    if len(aircrafts) == 0:
        print("Error: la lista esta vacia")
        return []

    nocturnos = []
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        # Avion nocturno: sin hora de llegada pero con hora de salida
        if ac.time == "" and ac.departure_time != "":
            nocturnos.append(ac)
        i = i + 1

    return nocturnos

# -------------------------------------------------------
# FUNCIONES EXTRA
# -------------------------------------------------------

def PlotTAT(aircrafts):
    if len(aircrafts) == 0:
        print("No hay vuelos cargados")
        return None

    # Calcular TAT para cada avión que tenga llegada Y salida
    ids    = []
    minutos = []

    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        if ac.time != "" and ac.departure_time != "":
            try:
                p_arr = ac.time.split(":")
                p_dep = ac.departure_time.split(":")
                total_arr = int(p_arr[0]) * 60 + int(p_arr[1])
                total_dep = int(p_dep[0]) * 60 + int(p_dep[1])
                tat = total_dep - total_arr
                if tat > 0:           # descartamos datos inconsistentes
                    ids.append(ac.aircraft)
                    minutos.append(tat)
            except:
                pass
        i += 1

    if len(minutos) == 0:
        print("No hay aviones con llegada y salida registradas")
        return None

    # ── Top 10 ────────────────────────────────────────────────────
    # Ordenar de mayor a menor (bubble sort para no usar sorted())
    top_ids = list(ids)
    top_min = list(minutos)
    n = len(top_ids)
    j = 0
    while j < n - 1:
        k = 0
        while k < n - j - 1:
            if top_min[k] < top_min[k + 1]:
                top_min[k], top_min[k + 1] = top_min[k + 1], top_min[k]
                top_ids[k], top_ids[k + 1] = top_ids[k + 1], top_ids[k]
            k += 1
        j += 1

    if len(top_ids) > 10:
        top_ids = top_ids[:10]
        top_min = top_min[:10]

    # Convertir minutos a horas y minutos para etiquetas
    top_labels = []
    i = 0
    while i < len(top_min):
        h = top_min[i] // 60
        m = top_min[i] % 60
        top_labels.append(str(h) + "h " + str(m) + "m")
        i += 1

    # ── Figura con 2 subplots ─────────────────────────────────────
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Turnaround Time (TAT) — Tiempo en tierra",
                 fontsize=12, fontweight="bold", color="#3D2B5A")

    # — Subplot 1: histograma —
    # Calcular bins manualmente
    min_val = minutos[0]
    max_val = minutos[0]
    for v in minutos:
        if v < min_val:
            min_val = v
        if v > max_val:
            max_val = v

    num_bins = 10
    ancho = (max_val - min_val) / num_bins if max_val != min_val else 1
    bins_x  = []
    bins_y  = []
    b = 0
    while b < num_bins:
        lim_inf = min_val + b * ancho
        lim_sup = min_val + (b + 1) * ancho
        bins_x.append(lim_inf + ancho / 2)   # centro del bin
        cuenta = 0
        for v in minutos:
            if lim_inf <= v < lim_sup:
                cuenta += 1
        # último bin incluye el máximo
        if b == num_bins - 1:
            for v in minutos:
                if v == max_val:
                    cuenta += 1
        bins_y.append(cuenta)
        b += 1

    etiq_x = []
    for cx in bins_x:
        h = int(cx) // 60
        m = int(cx) % 60
        etiq_x.append(str(h) + "h" + str(m).zfill(2))

    ax1.bar(range(num_bins), bins_y,
            color="#9B7EC8", edgecolor="#5C3D8F", alpha=0.85, width=0.7)
    ax1.set_xticks(range(num_bins))
    ax1.set_xticklabels(etiq_x, rotation=45, ha="right", fontsize=7)
    ax1.set_title("Distribución de tiempos en tierra", fontsize=10)
    ax1.set_xlabel("Tiempo en tierra")
    ax1.set_ylabel("Número de aviones")
    ax1.set_facecolor("#FDFBFF")

    # Línea de media
    media = sum(minutos) / len(minutos)
    media_bin = (media - min_val) / ancho if ancho > 0 else 0
    ax1.axvline(x=media_bin, color="#E05C3A", linestyle="--",
                linewidth=1.5, label="Media: " + str(int(media // 60)) +
                "h " + str(int(media % 60)) + "m")
    ax1.legend(fontsize=8)

    # — Subplot 2: ranking top 10 —
    colores_barras = ["#5C3D8F", "#7A52B5", "#9B7EC8",
                      "#B8A0D8", "#D4C5E8", "#E4D9F5",
                      "#C8DCF0", "#A8C8EC", "#7AAEE0", "#4A8ECF"]

    barras = ax2.barh(range(len(top_ids)), top_min,
                      color=colores_barras[:len(top_ids)],
                      edgecolor="#3D2B5A", alpha=0.88)
    ax2.set_yticks(range(len(top_ids)))
    ax2.set_yticklabels(top_ids, fontsize=8)
    ax2.invert_yaxis()   # el mayor arriba
    ax2.set_title("Top " + str(len(top_ids)) +
                  " aviones con más tiempo en tierra", fontsize=10)
    ax2.set_xlabel("Minutos en tierra")
    ax2.set_facecolor("#FDFBFF")

    # Etiquetas de valor al final de cada barra
    i = 0
    while i < len(barras):
        ax2.text(top_min[i] + 1, i, top_labels[i],
                 va="center", fontsize=7, color="#3D2B5A")
        i += 1

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    return fig

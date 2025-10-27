import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio
from automobile import Automobile

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO


    marca=ft.TextField(label="Marca")
    modello=ft.TextField(label="Modello")
    anno=ft.TextField(label="Anno")

    num_posti=ft.TextField(width=100, text_size=16, border_color="white", text_align=ft.TextAlign.CENTER)

    num_posti.value=0 # contatore al centro impostato a 0

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    def handlerMinus(e):
        cVal=num_posti.value
        if cVal>0:
            cVal=cVal- 1
            num_posti.value=cVal
            num_posti.update()

    def handlerPlus(e):
        cVal=num_posti.value
        cVal=cVal+1
        num_posti.value = cVal
        num_posti.update()

    # bottoni  per aumentare e diminuire  il numero di posti
    btnMinus=ft.IconButton(icon=ft.Icons.REMOVE, icon_size=24, icon_color="Red", on_click=handlerMinus)
    btnPlus=ft.IconButton(icon=ft.Icons.ADD, icon_size=24, icon_color="Green", on_click=handlerPlus)

    # TODO


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto

    def handler_aggiungi_auto(e):
        try:
            autonoleggio.aggiungi_automobile(marca.value, modello.value, anno.value, num_posti.value)
            aggiorna_lista_auto()
            marca.value=""
            modello.value=""
            anno.value=""
            num_posti.value=0  # se metto il contatore a 0, posso riaggiungere un altra auto
            page.update()
        except Exception as e:
            alert.show_alert("ERRORE: Inserisci valore numerici per anno e numero di posti")




    pulsante_aggiungi_auto=ft.ElevatedButton(text="Aggiungi", on_click=handler_aggiungi_auto)
    #TODO


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO

        ft.Divider(),
        ft.Text("Aggiungi nuova automobile", size=20),

        ft.Row([marca, modello, anno, btnMinus,num_posti,btnPlus], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(spacing=200,
               controls=[pulsante_aggiungi_auto],
               alignment=ft.MainAxisAlignment.CENTER),


        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)

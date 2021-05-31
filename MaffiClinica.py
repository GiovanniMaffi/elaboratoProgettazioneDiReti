'''
ELABORATO DI PROGRAMMAZIONE DI RETI (TRACCIA 2)
GIOVANNI MAFFI
MATRICOLA: 0000948696
Web Server per gestioni di reparti ospedalieri
'''

#!/bin/env python
import sys, signal
import http.server
import socketserver
import threading 
import cgi

#Gestisce l'attesa senza busy waiting
waiting_refresh = threading.Event()

# Legge il numero della porta dalla riga di comando, e mette default 8080
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8080

# classe che mantiene le funzioni di SimpleHTTPRequestHandler e implementa
# il metodo get nel caso in cui si voglia fare un refresh
class ServerHandler(http.server.SimpleHTTPRequestHandler):        
    def do_GET(self):
        # Scrivo sul file AllRequestsGET le richieste dei client     
        with open("AllRequests.txt", "a") as out:
          info = "GET request,\nPath: " + str(self.path) + "\nHeaders:\n" + str(self.headers) + "\n"
          out.write(str(info))
        if self.path == '/refresh':
            resfresh_contents()
            self.path = '/'
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        
    def do_POST(self):
        try:
            # Salvo i vari dati inseriti
            form = cgi.FieldStorage(    
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'})
            
            mail = form.getvalue('email')
            password = form.getvalue('password')

            output="ACCESSO EFFETTUTATO CON LE SEGUENTI CREDENZIALI:\n\nMAIL: " + mail + "\nPASSWORD: " + password + "\n\nTorna indietro per tornare alla home"
            self.send_response(200)      
        except: 
            self.send_error(404, 'Bad request submitted.')
            return;
        
        self.end_headers()
        self.wfile.write(bytes(output, 'utf-8'))
        
        # Salvo in locale i vari messaggi in AllPOST
        with open("LoginEffettutai.txt", "a") as out:
           info = "CREDENZIALI:,\nMAIL: " + mail + "\nPASSWORD: " + password +"\n\n\n"
           out.write(info)
        
        
# ThreadingTCPServer per gestire più richieste
server = socketserver.ThreadingTCPServer(('127.0.0.1',port), ServerHandler)

# la parte iniziale è identica per tutti i giornali
header_html = """
<html>
    <head>
        <style>
            h1 {
                text-align: center;
                margin: 0;
            }
            table {width:70%;}
            img {
                max-width:300;
                max-height:200px;
                width:auto;
            }
            td {width: 33%;}
            p {text-align:justify;}
            td {
                padding: 20px;
                text-align: center;
            }
            .topnav {
  		        overflow: hidden;
  		        background-color: #808080;
  		    }
            .topnav a {
  		        float: left;
  		        color: #f2f2f2; 
  		        text-align: center;
  		        padding: 14px 16px;
  		        text-decoration: none;
  		        font-size: 17px;
  		    }        
  		    .topnav a:hover {
  		        background-color: #808080;
  		        color: green;
  		    }        
  		    .topnav a.active {
  		        background-color: #4CAF50;
  		        color: white;
  		    }
        </style>
    </head>
    <body>
        <title>Maffi Ospedale</title>
"""

# la barra di navigazione è identica per tutti i giornali
navigation_bar = """
        <br>
        <br>
        <br>
        <div class="topnav">
            <a href="http://127.0.0.1:{port}">Home</a>
  		    <a href="http://127.0.0.1:{port}/Cardiologia.html">|Cardiologia|</a>
            <a href="http://127.0.0.1:{port}/Centro_Ustioni.html">|Centro Ustioni e Chiururgia Plastica|</a>
            <a href="http://127.0.0.1:{port}/Ostetricia.html">|Ostetricia|</a>
            <a href="http://127.0.0.1:{port}/Oculista.html">|Oculista|</a>
            <a href="http://127.0.0.1:{port}/CTMO.html">|CTMO|</a>
            <a href="http://127.0.0.1:{port}/Radioterapia.html">|Radioterapia|</a>
  		    <a href="http://127.0.0.1:{port}/refresh" style="float: right">|Refresh|</a>
            <a href="http://127.0.0.1:{port}/Login.html" style="float: right">|Login|</a>
  		</div>
        <br><br>
        <table align="center">
""".format(port=port)

# parte inferiore uguale per tutte le pagine
footer_html= """
        </table>
    </body>
</html>
"""

home_page = """
    <a href="http://127.0.0.1:{port}">QUI </a>

"""

#Creo le textbox per inserire email e password, utilizzate per il login
login = """
		<form action="http://127.0.0.1:{port}/login" method="post" style="text-align: center;">
		  <h2>Login</h2><br>
		  <label for="email">Email:</label>
		  <input type="text" id="mail" name="email"><br><br>
		  <label for="password">Password:</label>
		  <input type="text" id="password" name="password"><br><br>
		  <input type="submit" value="Login">
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#lista dei reparti di cardiologia
reparti ="""
    <ul>
        <li>Servizio di cardiologia, il reparto base, dove si presta servizio ambulatoriale e gestiscono i ricoverati altri reparti.</li>
        <li>Cardiologia di degenza, dove vengono ricoverati i pazienti meno gravi.</li>
        <li>Unita' terapia intensiva coronarica (UTIC), il reparto intensivo specializzato di cardiologia.</li>
        <li>Sala emodinamica, ambiente sterile dove vengono effettuati determinati esami quali la coronarografia e l'angioplastica.</li>
        <li>Sala dell'elettrofisiologia, ambiente sterile dove vengono effettuati determinati interventi come ablazioni e impianti di pacemaker.</li>
    </ul>
    <br><br>
"""


# creazione di tutte le pagine
def resfresh_contents():
    print("updating all contents")
    create_page_Login()
    create_page_Cardiologia()
    create_page_Centro_Ustioni_Chirurgia()
    create_page_Ostetricia()
    create_page_Oculista()
    create_page_CTMO()
    create_page_Radioterapia()
    create_index_page()
    print("finished update")
    
#creazione della pagina di login
def create_page_Login():
    f = open('Login.html','w', encoding="utf-8")
    f.write(header_html + " <h1>LOGIN</h1> " + navigation_bar + "</table>" + login)
    f.close()

# metodo per creare la pagina Centro Ustioni e chirurgia plastica
def create_page_Centro_Ustioni_Chirurgia():
   message = header_html + "<h1>Maffi Ospedale</h1>" + navigation_bar
   message = message + "<h2>CENTRO USTIONI E CHIRURGIA:</h2>" + "<br>"  
   message = message + "<h3>RICOVERI:</h3>" 
   message = message + "<h4>-CHIRURGIA PLASTICA: </h4>" + "   Il ricovero urgente e' deciso dal medico di Pronto soccorso, in accordo con lo specialista della struttura complessa. Il ricovero programmato e' deciso dallo specialista dopo la visita; l'ingresso avviene secondo l'ordine di prenotazione e le priorita' legate alla patologia, nel rispetto dei tempi di attesa regionali. Eventuali variazioni vengono comunicate dai professionisti della struttura complessa. Il ricovero puo' avvenire anche su trasferimento da un'altra struttura." + "<br>"
   message = message + "<h4>-CENTRO USTIONI:</h4>" + "   L'accoglienza avviene attraverso il Pronto soccorso e la Centrale operativa 118 (tramite la quale il Centro ustioni è collegato a tutta la regione e a tutto il territorio nazionale) o su richiesta del medico di famiglia" + "<br><br><br>"
   message = message + "<h3>CENTRO LASER:</h3>" + "Nell'ambulatorio si eseguono trattamenti laser previo test. In particolare: macchie cutanee, neoformazioni benigne, capillari, angiomi, verruche, cicatrici patologiche, rigonfiamento cutaneo." + "<br><br><br><br>"
   message = message + '<img src="https://www.ao.pr.it/wp-content/uploads/2012/06/54.jpg" alt="ChirurgiaEPlasticaImg">' + "<br><br><br>"
   message = message + '<br><br><a href="https://www.ao.pr.it/curarsi/reparti-e-servizi-sanitari/chirurgia-plastica-e-centro-ustioni/">Clicca qui per maggiori informazioni</a>'
   message = message + footer_html
   f = open('Centro_Ustioni.html','w', encoding="utf-8")
   f.write(message)
   f.close()

# metodo per creare la pagina Ostetricia
def create_page_Ostetricia():
    message = header_html + "<h1>Maffi Ospedale</h1>" + navigation_bar
    message = message + "<h2>OSTETRICIA:</h2>" + "L'ostetricia e' una branca della scienza medica che si occupa dell'assistenza alla donna durante la gravidanza, il parto ed il puerperio. Si occupa inoltre di tutte le condizioni patologiche che possono insorgere a carico della madre e del sistema feto-placentare." + "<br><br>"  
    message = message + "<h3>NIPT TEST</h3>"+ "Non Invasive Prenatal Test (NIPT) e' un test prenatale di screening innovativo, non invasivo, che si esegue nella fase iniziale della gravidanza e si basa sull'analisi del DNA fetale presente nel plasma materno. Con un semplice prelievo di sangue, questo esame consente di prevedere con grande attendibilita' alcune anomalie dei cromosomi gia' dalla decima settimana di gestazione, in particolare la trisomia 21 (sindrome di Down) e le trisomie 18 (sindrome di Edwards) e 13 (sindrome di Patau)" + "<br><br><br><br>"
    message = message + '<img src="https://cdn.gvmnet.it/admingvm/media/immagininews/cuoreevasi/Ostetricia.jpg" alt="OstetriciaImg">' + "<br><br><br>"
    message = message + '<br><br><a href="https://www.ao.pr.it/curarsi/reparti-e-servizi-sanitari/ostetricia-e-ginecologia/">Clicca qui per maggiori informazioni</a>'
    message = message + footer_html
    f = open('Ostetricia.html','w', encoding="utf-8")
    f.write(message)
    f.close()

# metodo per creare la pagina Cardiologia
def create_page_Cardiologia():
    message = header_html + "<h1>Maffi Ospedale</h1>" + navigation_bar 
    message = message + "<h2>CARDIOLOGIA:</h2>" + "La cardiologia studia la diagnosi e la cura (farmacologica e/o invasiva) delle malattie cardiovascolari acquisite o congenite.Chi si occupa di tale branca della medicina, come medico specialista, viene chiamato cardiologo. La cardiologia e' una disciplina che negli anni piu' recenti si e' molto evoluta e al suo interno si sono sviluppate specialita' come l'emodinamica e l'elettrofisiologia." + "<br><br>"  
    message = message + "<h3>Reparto di cardiologia:</h3>" + "Il reparto di cardiologia lo si trova in quasi tutti gli ospedali di importanza almeno regionale ed e' costituito da:"  + reparti
    message = message + "<h3>Quando rivolgersi al cardiologo:</h3>"+ "E' bene rivolgersi al cardiologo, quando si hanno disturbi legati alla zona del cuore, o nello specifico caso di colesterolo alto, pressione alta, diabete ma anche dolore toracico e affanno, specialmente se associati a nausea o vomito, svenimenti, capogiri o palpitazioni"+ "<br><br><br><br>"
    message = message + '<img src="https://www.ao.pr.it/wp-content/uploads/2012/06/DSC_0476.jpg" alt="CardiologiaImg" >' + "<br><br><br>"
    message = message + '<br><br><a href="https://www.ao.pr.it/curarsi/reparti-e-servizi-sanitari/cardiologia/">Clicca qui per maggiori informazioni</a>'
    message = message + footer_html
    f = open('Cardiologia.html','w', encoding="utf-8")
    f.write(message)
    f.close()    
        
# metodo per creare la pagina Oculista
def create_page_Oculista():
    message = header_html + "<h1>Maffi Ospedale</h1>" + navigation_bar  
    message = message + "<h2>OCULISTA:</h2>" + "L'Oculistica pratica la chirurgia della cataratta, la chirurgia vitreoretinica mini-invasiva 23g, la laser terapia, l'ortottica, la chirurgia del glaucoma nell'adulto (trabeculectomia, non perforante, valvole, gold shunt, canaloplastica), la chirurgia del glaucoma congenito nel bambino (trabeculotomia), l'elettrofisiologia, il trapianto di cornea (cheratoplastica perforante, lamellare, endoteliale), la diagnosi e il trattamento delle malattie infiammatorie e autoimmuni oculari oltre che delle malattie della retina e delle malattie rare legate all'apparato visivo, la neuroftalmologia, la chirurgia plastica e ricostruttiva oculare." + "<br><br>"  
    message = message + "<h3>Diagnosi e terapia</h3>"+ "Delle malattie oculari con specifici campi di interesse relativi a: cataratta, glaucoma, patologie vitreoretiniche di interesse chirurgico, oftalmologia pediatrica, strabismo, neuroftalmologia, oftalmopatia tiroidea, patologia oculare autoimmune, elettrofisiologia, oncologia oculare, malattie rare legate all'apparato visivo, malattie della cornea, cheratocono, retinopatia diabetica, maculopatia senile." + "<br><br><br><br>"
    message = message + '<img src="https://www.occhiali24.it/hubfs/Blog%20Photos/IT%20Blog%20Photos/Ottico-optometrista-oculista-oftalmologo-ortottista-quale-differenza.jpg" alt="Oculista1" >'+ '<img src="https://www.sadimedical.it/wp-content/uploads/2019/04/GN4_DAT_4376657.jpg-visita_oculistica__tra_dieci_mesi.jpg" alt="Oculista2">' + "<br><br><br>"
    message = message + '<a href="https://www.ao.pr.it/curarsi/reparti-e-servizi-sanitari/oculistica/">Clicca qui per maggiori informazioni</a>'
    message = message + footer_html
    f = open('Oculista.html','w', encoding="utf-8")
    f.write(message)
    f.close()
        
# metodo per creare la pagina CTMO
def create_page_CTMO():
    message = header_html + "<h1>Maffi Ospedale</h1>" + navigation_bar
    message = message + "<h2>CTMO:</h2>" + "Attivita' assistenziale specialistica per pazienti affetti da malattie ematologiche maligne (leucemie acute e croniche, mielodisplasie, linfomi di Hodgkin e linfomi non Hodgkin, gammopatie monoclonali e mielomi) e non maligne (anemie congenite e acquisite, piastrinopenie, alterazioni dei neutrofili e degli eosinofili, malattie del sistema immunitario) in regime di ricovero, di day hospital e ambulatoriale con garanzia delle prestazioni urgenti, delle prestazioni in urgenza differita e di quelle programmate." + "<br><br>"  
    message = message + "<h3>percorso diagnostico</h3>"+ " include prelievi del sangue, prelievo del midollo osseo tramite agoaspirato e agobiopsia,  test diagnostici specialistici di morfologia, citofluorimetria, citogenetica e biologia molecolare delle malattie ematologiche" + "<br><br><br><br>"
    message = message + '<img src="https://www.ao.pr.it/wp-content/uploads/2012/09/DSC_1952.jpg" alt="CTMO1" >' + '<img src="https://www.ao.pr.it/wp-content/uploads/2012/09/DSC_1969.jpg" alt="CTMO2">' + "<br><br><br>"
    message = message + '<br><br><a href="https://www.ao.pr.it/curarsi/reparti-e-servizi-sanitari/ematologia-e-centro-trapianti-midollo-osseo/">Clicca qui per maggiori informazioni</a>'
    message = message + footer_html
    f = open('CTMO.html','w', encoding="utf-8")
    f.write(message)
    f.close()
        
# metodo per creare la pagina Radioterapia
def create_page_Radioterapia():
    message = header_html + "<h1>Maffi Ospedale</h1>" + navigation_bar
    message = message + "<h2>RADIOTERAPIA:</h2>" + " La radioterapia e' utilizzata soprattutto nel trattamento di forme di tumore, infatti utilizza un fascio di fotoni penetranti, di 5-10 MeV di energia, per danneggiare il patrimonio genetico delle cellule malate e impedire cosi' che proliferino, mentre e' poco impiegata in patologie non oncologiche. La radioterapia puo' essere curativa in un certo numero di tipi di cancro, se confinati in una zona del corpo sulla base della classificazione TNM della lesione stessa. E' prassi comune combinare la radioterapia con la chirurgia, con la chemioterapia, con l'ormonoterapia e l'immunoterapia. Lo scopo esatto del trattamento dipendera' dal tipo di tumore, dalla posizione e stadio, nonche' dalla salute generale del paziente." + "<br><br>"  
    message = message + "<h3>Due importanti modalita' radioterapeutiche:</h3>"
    message = message + "<h4>TBI:</h4>"+ "La radiazione corporea totale, e' l'irradiazione totale e simultanea del corpo (in una o piu' frazioni) utilizzando fasci di fotoni ad alta energia. Consiste in una particolare tecnica radioterapica utilizzata per preparare il paziente a ricevere un trapianto di midollo osseo." 
    message = message + "<h4>TSEBI:</h4>"+ "Con Total Skin Electron Beam Irradiation, viene indicata l'irradiazione cutanea totale effettuata con fasci di elettroni. Si tratta di una terapia impiegata nel caso di neoplasie cutanee diffuse o in pazienti affetti da micosi fungoide" + "<br><br><br><br>"
    message = message + '<img src="https://www.auslromagna.it/media/k2/items/cache/602194768a8e459c848a96abe269a0b9_XL.jpg" alt="Radioterapia1">' + '<img src="https://www.ao.pr.it/wp-content/uploads/2012/09/DSC_1969.jpg" alt="Radioterapia2">' + "<br><br>"
    message = message + '<br><br><a href="https://www.ao.pr.it/curarsi/reparti-e-servizi-sanitari/radioterapia/">Clicca qui per maggiori informazioni</a>'
    message = message + footer_html
    f = open('Radioterapia.html','w', encoding="utf-8")
    f.write(message)
    f.close()
    
# metodo per creare la pagina iniziale index.html
def create_index_page():
    f = open('index.html','w', encoding="utf-8")
    message = header_html + "<h1>Maffi Ospedale</h1>" + navigation_bar
    message = message + '<h2>Reparti</h2>' + '<br><br>'
    message = message + '<a href="http://127.0.0.1:8080/Cardiologia.html">-CARDIOLOGIA</a>' + "<br>"
    message = message + '<a href="http://127.0.0.1:8080/Centro_Ustioni.html">-CENTRO USTIONI</a>' + "<br>"
    message = message + '<a href="http://127.0.0.1:8080/Ostetricia.html">-OSTETRICIA</a>' + "<br>"
    message = message + '<a href="http://127.0.0.1:8080/Oculista.html">-OCULISTA</a>' + "<br>"
    message = message + '<a href="http://127.0.0.1:8080/CTMO.html">-CTMO</a>' + "<br>"
    message = message + '<a href="http://127.0.0.1:8080/Radioterapia.html">-RADIOTERAPIA</a>' + "<br>"
    message = message + '<th colspan="4"><h3><a href="/info.pdf" download="info.pdf">Scarica PDF</a></h3></th>' #funziona solo dopo aver effettuato il refresh
    message = message + footer_html
    f.write(message)
    f.close()


    
# definiamo una funzione per permetterci di uscire dal processo tramite Ctrl-C
def signal_handler(signal, frame):
    print( 'Chiusura http server (Ctrl+C premuto)')
    try:
      if(server):
        server.server_close()
    finally:
      waiting_refresh.set()
      sys.exit(0)
      
# metodo che viene chiamato al "lancio" del server
def main():
    #create_page_login()
    resfresh_contents()
    #Assicura che da tastiera usando la combinazione di tasti Ctrl+C termini in modo pulito tutti i thread generati
    server.daemon_threads = True 
    #il Server acconsente al riutilizzo del socket anche se ancora non e' stato rilasciato quello precedente, andandolo a sovrascrivere
    server.allow_reuse_address = True  
    #interrompe l'esecuzione se da tastiera arriva la combinazione CTRL + C
    signal.signal(signal.SIGINT, signal_handler)
    # cancella i dati get ogni volta che il server viene attivato
    f = open('AllRequests.txt','w', encoding="utf-8")
    f.close()
    try:
      while True:
        server.serve_forever()
    except KeyboardInterrupt:
      pass
    #Chiude il server socket
    server.server_close()

if __name__ == "__main__":
    main()

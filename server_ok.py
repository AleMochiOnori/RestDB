from flask import Flask, jsonify, request
from myjson import JsonDeserialize, JsonSerialize
import dbclient as db
import sys 


api = Flask(__name__)

cur = db.connect()
if cur is None :
    sys.exit()


file_path = "anagrafe.json"
cittadini = JsonDeserialize(file_path)

file_path_users = "utenti.json"
utenti = JsonDeserialize(file_path_users)



@api.route('/login', methods=['POST'])
def GestisciLogin():
    global cur
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        #{"username":"pippo", "password":"pippo"}
        jsonReq = request.json
        sUsernameInseritoDalClient = jsonReq["username"]
        sPasswordInseritaDalClient = jsonReq["password"]
        squery  ="select privilegi from utenti where mail = '" + sUsernameInseritoDalClient + "' AND password ='" + sPasswordInseritaDalClient + "';"
        iNumRows = db.read_in_db(cur,squery)
        print(squery)
        if iNumRows == 1 :
            lRow = db.read_next_row(cur)
            sPriv = lRow[1][0]
            print("privilegio" + sPriv)
            return jsonify({"Esito": "000", "Msg": "Utente registrato", "Privilegio":sPriv}), 200
    else:
        return jsonify({"Esito": "002", "Msg": "Formato richiesta errato"}) 
                                             

@api.route('/add_cittadino', methods=['POST'])
def GestisciAddCittadino():
    global cur
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        jsonReq = request.json
        
        #prima di tutto verifico utente, password e privilegio 
        #dove utente e password me l'ha inviato il client
        #mentre il privilegio lo vado a leggere nel mio file  (utenti.json)

        
        codice_fiscale = jsonReq.get('codFiscale')
        nome = jsonReq.get('nome')
        cognome = jsonReq.get('cognome')
        dataNascita = jsonReq.get("dataNascita") 
        print(sQuery)
        sQuery = "insert into anagrafe(codice_fiscale,nome,cognome,data_nascita) Values ("
        sQuery += "'" + codice_fiscale + "','" + nome + "','" + cognome + "','" + dataNascita
        codice_fiscale = jsonReq.get('codFiscale')
        iRet = db.write_in_db(cur,sQuery)
        if iRet  == "duplicato":
            return jsonify({"Esito": "001", "Msg": "Cittadino già esistente"}), 200
        elif iRet == "aggiunto":
            return jsonify({"Esito": "000", "Msg": "Cittadino aggiunto con successo"}), 200
        else : 
          return jsonify({"Esito": "002", "Msg": "Formato richiesta non valido"}), 200   
    else:
        return jsonify({"Esito": "002", "Msg": "Formato richiesta non valido"}), 200




@api.route('/read_cittadino/<codice_fiscale>', methods=['GET'])
def read_cittadino(codice_fiscale):

    #prima di tutto verifico utente, password e privilegio 
    #dove utente e password me l'ha inviato il client
    #mentre il privilegio lo vado a leggere nel mio file  (utenti.json)

    cittadino = cittadini.get(codice_fiscale)
    if cittadino:
        return jsonify({"Esito": "000", "Msg": "Cittadino trovato", "Dati": cittadino}), 200
    else:
        return jsonify({"Esito": "001", "Msg": "Cittadino non trovato"}), 200






@api.route('/update_cittadino', methods=['PUT'])
def update_cittadino():

    #prima di tutto verifico utente, password e privilegio 
    #dove utente e password me l'ha inviato il client
    #mentre il privilegio lo vado a leggere nel mio file  (utenti.json)

    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        jsonReq = request.json
        codice_fiscale = jsonReq.get('codFiscale')
        if codice_fiscale in cittadini:
            cittadini[codice_fiscale] = jsonReq
            JsonSerialize(cittadini, file_path)  
            return jsonify({"Esito": "000", "Msg": "Cittadino aggiornato con successo"}), 200
        else:
            return jsonify({"Esito": "001", "Msg": "Cittadino non trovato"}), 200
    else:
        return jsonify({"Esito": "002", "Msg": "Formato richiesta non valido"}), 200






@api.route('/elimina_cittadino', methods=['DELETE'])
def elimina_cittadino():

    #prima di tutto verifico utente, password e privilegio 
    #dove utente e password me l'ha inviato il client
    #mentre il privilegio lo vado a leggere nel mio file  (utenti.json)
    
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        cod = request.json.get('codFiscale')
        if cod in cittadini:
            del cittadini[cod]
            JsonSerialize(cittadini, file_path)  
            return jsonify({"Esito": "000", "Msg": "Cittadino rimosso con successo"}), 200
        else:
            return jsonify({"Esito": "001", "Msg": "Cittadino non trovato"}), 200
    else:
        return jsonify({"Esito": "002", "Msg": "Formato richiesta non valido"}), 200

api.run(host="127.0.0.1", port=8080)


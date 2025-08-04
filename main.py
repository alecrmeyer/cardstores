
from app import app
import aiohttp
from flask import Flask, request, render_template

import stores.boarshat 
import stores.nrg
import stores.pastimes
# Flask constructor
app = Flask(__name__, static_url_path='/static', static_folder='static' )
  
nrg = stores.nrg.NRG()
pt = stores.pastimes.Pastimes()
bh = stores.boarshat.BoarsHat()

nrg_storage = {
   "id": "nrg",
   "Name": "Nerd Rage Gaming",
   "obj": nrg,
}
pt_storage = {
   "id": "pt",
   "Name": "Pastimes",
   "obj": pt,
}
bh_storage = {
   "id": "bh",
   "Name": "Boars Hat",
   "obj": bh,
}

store_list = [nrg_storage, pt_storage, bh_storage]

@app.route('/', methods =["GET", "POST"])
async def cardstores():

   if request.method == "POST":
      chosen_stores = request.form.getlist("cardstore")
      card = request.form.get("card")
      for store in store_list:
         if store["id"] in chosen_stores:
            store["quant"] = await store["obj"].get_card(card)
         else:
            store["quant"] = -1 

         
      return render_template("output.html", store_list=store_list, card=card)    
   return render_template("form.html")

if __name__=='__main__':
   app.run(debug=True, use_reloader=True)







import MySQLdb

fruits = "Abricot,Airelle,Alkékenge,Amande,Amélanche,Ananas,Arbouse,Asimine,Banane,Bergamote,Bigarade,Canneberge,Cassis,Cerise,Châtaigne,Citron,Clémentine,"\
"Coing,Cornouiller du Canada,Cynorrhodon,Datte,Épine-vinette,Feijoa,Figue,Figue de barbarie,Fraise,Framboise,Grenade,Griotte,Groseille,Jujube,Kaki,Kiwaï,Kiwi,Lime,"\
"Mandarine,Marron,Melon,Mûre,Myrte,Myrtille,Nèfle,Nèfle du Japon,Noisette,Noix,Orange,Pamplemousse,Pastèque,Pêche,Brugnon,Nectarine,Pavie,Physalis ou Coqueret du Pérou,"\
"Pistache,Plaquebière ou Chicouté,Poire,Pomme,Pomélos,Prunes,Pruneaux,Mirabelle,Quetsche,Reine-claude,Raisin"

legumes = "Ail,Artichaut,Asperge,Aubergine,Avocat,Bette,Betterave,Blette,Brocoli,Carotte,Catalonia,Céleri,Champignon,Choux,Citrouille,Concombre,Courge,Courgette,Cresson,"\
"Dachine,Daikon,Échalote,Endive,Épinard,Fenouil,Fève,Flageolet,Giromon,Haricot,Igname,Kancon,Konbu,Laitue,Lentille,Mâche,Maïs,Manioc,Navet,Oignon,Olive,Oseille,Panais,Patate,"\
"Pâtisson,Poireau,Poivron,Potimarron,Potiron,Radis,Rhubarbe,Roquette,Rutabaga,Salade,Salsifi,Salsifis,Tétragone,Tomate,Topinambour,Udo,Vitelotte,Wakame,Wasabi,Yin Tsoï"

articles = "Gel douche,Dentifrice,Cotons-tiges,Shampoing homme,Shampoing femme,Lessive liquide,Lessive en poudre,Nettoyant machine à laver,Essuite-tout,Papier toillette"\
""

alimentaire = "Crème fraiche,Fromage rapé,Babybel,Pâte à tartiner,Pâte feuilletée,Gâteaux,Café,Eau,Eau pétillante,Yahourt,Soupe,"\
"Légumes surgelés,Pain,Pain au chocolat,Pain au lait,Cracottes,Biscottes,Pain de mie,Pain hot dog,Eclairs au chocolat,Gauffres,Crêpes,Beignets,Muffins,Donuts,Flanc,Pain burger" \
"Toasts,Pain suédois,Brownies,Madelaines,Chocolat blanc,Chocolat noir,Chocolat au lait,Crêpes fourrées,Pancakes,Brioches fourrées,Lait écremé,Lait demi-écremé,Lait entier" \
"Lait concentré,Lait chocolaté,Lait amande,Lait de soja,Oeufs,Beurre,Beurre demi-sel,Margarine,Crème entière,Crème liquide,Crème épaisse,Sauce béchamel,Fromage raclette," \
"Fromage de chèvre,Apéritif fromage,Brie,Camembert,Comté,Emmental,Fromage bleu,Gouda,Roquefort,Saint-Agur,Mimolette,Morbier,Saint-Nectaire,Port Salut,Fromage,Edam,Tomme," \
"Fromage Abondance,Cheddar,Parmesan,Emmental rapé,Fromage de brebis,Fromage hamburger,Fromage ail et fines herbes,Fromage à tartiner,Pizza,Sandwich,Pastabox"

viandes = "Saucisses,Merguez,Chorizo,Burger,Steak haché,Saucisson,Jambon,Boulettes de viande,Onglet de boeuf,Faux filet de boeuf,Boeuf,Bifteck de boeuf,Pavé de boeuf," \
"Bavette de boeuf,Entrecôte de boeuf,Tournedos de boeuf,Carpaccio,Viande hachée,Andouillettes,Sauce roquefort,Cuisses de poulet,Escalope de poulet,Poulet fermier,Cordons bleus" \
"Manchons de poulet,Aiguillettes de poulet,Filet de poulet,Beignets au poulet,Nuggets de poulet,Escalope de dinde,Nuggets de dinde, Rillettes,Jambon cru,Mortadelle,Bacon," \
"Coppa,Salami,Rosette,Boudin blanc,Boudin noir,Chiffonade,Rôti de poulet,Blanc de dinde,Lardons"

poissons = "Crevettes,Saumon fumé,Saumon pavé,Rouille,Anchois,Poulpe,Soupe de poisson,Filet de saumon,Gambas,Filet de colin,Filet de limande,Filet merlu blanc,Filet de morue" \
"Croutons,Maquereau,Haddock,Harang fumé,Moules,Tartare de saumon,Truite fumée,Surimi,Brandade de morue,Oeufs de truite,Oeufs de cabillaud,Tarama,Rillettes de saumon" \
"Rillettes au crabe"

apero = "Chips,Bières,Vin rouge,Vin blanc,Vin rosé,Olives vertes,Olives noires,Blinis,Houmous,Tzatziki,Ice tea,Coca-Cola,Fanta,Orangina,Jus de pomme,Jus d'orange,Jus de raisin" \
"Jus multi-fruits,Sirop,Eau aromatisée,Champagne,Cidre,"

categories = [fruits, legumes, articles, alimentaire, viandes, poissons, apero]

db = MySQLdb.connect(host="renaudcosta.mysql.pythonanywhere-services.com", user="renaudcosta", passwd="elimelimelim", db="renaudcosta$podocollect")

cur = db.cursor()
cur.execute("DELETE FROM articles;")
cur.execute("ALTER TABLE articles AUTO_INCREMENT = 1;")
db.commit()

count = 0
for categorie in categories:
    for article in categorie.split(","):
        if article != "":
            cur.execute('INSERT INTO articles (nom) VALUES ("'+article.strip()+'");')
            count += 1
db.commit()

db.close()

print("Entered "+str(count)+" articles")
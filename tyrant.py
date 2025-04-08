import os
import glob
import re
import xml.etree.ElementTree as ET

# Define base fusion materials
BlooBaseFusionMaterials = ["Draconian Queen", "Smog Tank", "Blight Crusher", "Blood Pool", "Sinew Feeder", "Malgoth"]
ImpeBaseFusionMaterials = ["Tiamat", "Aegis", "Windreaver", "Absorption Shield", "Blackrock", "Nimbus"]
RaidBaseFusionMaterials = ["Havoc", "Bulldozer", "Iron Maiden", "Missile Silo", "Demon of Embers", "Omega"]
RighBaseFusionMaterials = ["Vigil", "Contaminant Scour", "Equalizer", "Sanctuary", "Falcion", "Benediction"]
XenoBaseFusionMaterials = ["Dreadship", "Xeno Mothership", "Daemon", "Genetics Pit", "Lurker Beast", "Apex"]
VindBaseFusionMaterials = ["Vindicator Reactor"]

# Check if necessary files exist
if glob.glob("cards_section*.xml") and os.path.exists("json.txt"):
   
   
###### append of all xmls #############    
    xmlcardslist = []
    for xml_file in glob.glob("cards_section*.xml"):
        tree = ET.parse(xml_file)
        xmlcardslist.append(tree)

##### go through the appended xmls and create a 'carddata' dictionnary of cards ID and Names : {1: 'Infantry-1', 2: 'Infantry-2'...   )
    carddata = {}
    for tree in xmlcardslist:
        root = tree.getroot()
        for unit in root.findall('.//unit'):
            name = unit.find('name').text
            card_id = int(unit.find('id').text)
            carddata[card_id] = f"{name}-1"
            upgrades = unit.findall('upgrade')
            if upgrades:
                for upg in upgrades:
                    upg_id = int(upg.find('card_id').text)
                    level = upg.find('level').text
                    carddata[upg_id] = f"{name}-{level}"
    #debug output file 
    #with open("carddata.txt", "w") as file:
    #    file.write(f"{carddata}\n")



    # Remove old files
    for filename in ["ownedcards.txt", "_ownedcards.txt", "_BlooBaseFusionMaterials.txt", "_ImpeBaseFusionMaterials.txt",
                     "_RaidBaseFusionMaterials.txt", "_RighBaseFusionMaterials.txt", "_XenoBaseFusionMaterials.txt",
                     "_VindBaseFusionMaterials.txt"]:
        if os.path.exists(filename):
            os.remove(filename)

    # Create new files with headers
    with open("_BlooBaseFusionMaterials.txt", "a", encoding="ascii") as f:
        f.write("\n//Bloodthirsty base fusion cards\n")
    with open("_ImpeBaseFusionMaterials.txt", "a", encoding="ascii") as f:
        f.write("\n//Imperial base fusion cards\n")
    with open("_RaidBaseFusionMaterials.txt", "a", encoding="ascii") as f:
        f.write("\n//Raider base fusion cards\n")
    with open("_RighBaseFusionMaterials.txt", "a", encoding="ascii") as f:
        f.write("\n//Righteous base fusion cards\n")
    with open("_XenobaseFusionMaterials.txt", "a", encoding="ascii") as f:
        f.write("\n//Xeno base fusion cards\n")
    with open("_VindBaseFusionMaterials.txt", "a", encoding="ascii") as f:
        f.write("\n//Vindicator Reactors\n")

    #### Read JSON data
    with open("json.txt", "r", encoding="utf-8") as f:
        x = f.read()

    #### Process json to isolate card inventory into a string
    user_cards_index = x.index("user_cards")
    #com_sp_mult_index = x.index("com_sp_mult")
    user_decks_index = x.index("user_decks")
    cards = x[user_cards_index-2:user_decks_index]

    #### Process card inventory to make a flat list ['', '"user_cards":', '"1":', '"num_owned":"45"', '"num_used":"1"', '"2":', '"num_owned":"34"', '"num_used":"0"',
    cards = cards.split("},") #split the string in a list based on a delimiter
    cards = [item.split(",") for item in cards] # split each item into a list based on a delimiter
    cards = [subitem.split("{") for item in cards for subitem in item] #split each sublist subitem based on a delimiter. We end up with a list of list of list.
    cards = [item for sublist in cards for item in sublist] #flatten the list of list of list

    #### Loop to create the 3 interesting variables : the card ID, number owned
    index = 2
    while index < (len(cards)-3) and cards[index]:
        card_id = int(cards[index].split('"')[1])
        num_owned = int(cards[index+1].split('"')[3])
        #num_used = int(cards[index+2].split('"')[3])
        if cards[index+3] == '"is_locked":true':
            index = index+4
        else: index = index+3
    
        ### if else to check if we owne that card and if yes, replace the ID by the name and them dispatch between faction base material and the rest.
        if num_owned > 0:
            line = carddata.get(card_id, "") #find in the "carddata" library the corresponding name and level for the ID.
            if num_owned > 1:
                line += f" ({num_owned})"
            line = line.replace("-6", "")
            if any(line.startswith(material) for material in BlooBaseFusionMaterials):
                with open("_BlooBaseFusionMaterials.txt", "a", encoding="ascii") as f:
                    #f.write("IS THIS IF WORKING?\n") #test to troubleshoot
                    f.write(line + "\n")
            elif any(line.startswith(material) for material in ImpeBaseFusionMaterials):
                with open("_ImpeBaseFusionMaterials.txt", "a", encoding="ascii") as f:
                    f.write(line + "\n")
            elif any(line.startswith(material) for material in RaidBaseFusionMaterials):
                with open("_RaidBaseFusionMaterials.txt", "a", encoding="ascii") as f:
                    f.write(line + "\n")
            elif any(line.startswith(material) for material in RighBaseFusionMaterials):
                with open("_RighBaseFusionMaterials.txt", "a", encoding="ascii") as f:
                    f.write(line + "\n")
            elif any(line.startswith(material) for material in XenoBaseFusionMaterials):
                with open("_XenobaseFusionMaterials.txt", "a", encoding="ascii") as f:
                    f.write(line + "\n")
            elif any(line.startswith(material) for material in VindBaseFusionMaterials):
                with open("_VindBaseFusionMaterials.txt", "a", encoding="ascii") as f:
                    f.write(line + "\n")
            else:
                with open("_ownedcards.txt", "a", encoding="ascii") as f:
                    f.write(line + "\n")

    # Combine files into ownedcards.txt
    with open("ownedcards.txt", "w", encoding="ascii") as outfile:
        for filename in ["_VindBaseFusionMaterials.txt", "_BlooBaseFusionMaterials.txt", "_ImpeBaseFusionMaterials.txt",
                         "_RaidBaseFusionMaterials.txt", "_RighBaseFusionMaterials.txt", "_XenobaseFusionMaterials.txt",
                         "_ownedcards.txt"]:
            if os.path.exists(filename):
                with open(filename, "r", encoding="ascii") as infile:
                    outfile.write(infile.read())
                os.remove(filename)

    # Process buyback data
                
    #write a header in the ownedcard file
    with open("ownedcards.txt", "a", encoding="ascii") as f:
        f.write("\n//Cards from restore\n")
    
    #create the list to go through and extract the data to write in ownedcard.txt
    buyback_data_index = x.index("buyback_data")
    request_index = x.index("request")
    buyback_cards = x[buyback_data_index-2:request_index]    
    buyback_cards = buyback_cards.split("},") #split the string in a list based on a delimiter
    buyback_cards = [item.split(",") for item in buyback_cards] # split each item into a list based on a delimiter
    buyback_cards = [subitem.split("{") for item in buyback_cards for subitem in item] #split each sublist subitem based on a delimiter. We end up with a list of list of list.
    buyback_cards = [item for sublist in buyback_cards for item in sublist] #flatten the list of list of list
    
    #loop to write cards in txt one by one
    index = 7
    while index < len(buyback_cards) and cards[index]:
        card_id = buyback_cards[index-4].replace('"card_id":',"") #removing text before ID
        card_id = card_id.replace('"',"") #removing text after id
        card_name = carddata.get(int(card_id))    #replace card ID by card name by looking at carddata dictionary 
        total_salvaged = buyback_cards[index-2].replace('"total_salvaged":',"") #removing text before number salvaged
        total_salvaged = total_salvaged.replace('"',"") #removing text after number salvaged
        
        if int(total_salvaged) > 1:
            with open("ownedcards.txt", "a", encoding="ascii") as f:
                f.write(card_name + " (" +total_salvaged+")" + "\n")
        index +=7
    
    


    #### Process current decks
    
    # create the list to go through and extract the data to write in currentdeck.txt
    user_decks_index = x.index("user_decks")
    com_sp_mult_index = x.index("com_sp_mult")
    decks = x[user_decks_index-2:com_sp_mult_index] 
    decks = decks.replace('"user_decks":{','').replace('}','')
    decksplit = decks.split(',')

    #remove old file
    if os.path.exists("currentdecks.txt"):
        os.remove("currentdecks.txt")
     
    #loop to write current deck content in txt one by one 
    index = 0    
    while index < len(decksplit):     
        if "deck_id" in decksplit[index]: #start of a new deck
            decknumber = decksplit[index][1]
            with open("currentdecks.txt", "a", encoding="ascii") as f:
                f.write( decknumber + ": ")
        elif "name" in decksplit[index]:
            index +=1
            continue
        elif "commander_id" in decksplit[index]: # commander of deck
            commanderid = decksplit[index].replace('"commander_id":"','')[:-1]
            commandername = carddata.get(int(commanderid))
            with open("currentdecks.txt", "a", encoding="ascii") as f:
                f.write( commandername + ",")
        elif "cards" in decksplit[index]: #first card in the deck
            cardid = decksplit[index].replace('"cards":{"',"")[:-5]
            cardname = carddata.get(int(cardid))
            cardnumber = decksplit[index][-2]
            if int(cardnumber) > 1:
                with open("currentdecks.txt", "a", encoding="ascii") as f:
                    f.write( cardname + " #"+cardnumber+',')
            else: 
                with open("currentdecks.txt", "a", encoding="ascii") as f:
                    f.write( cardname + ",")
        elif "dominion_id" in decksplit[index]: # dominion of deck
            dominionid = decksplit[index].replace('"dominion_id":"',"")[:-1] 
            dominionname = carddata.get(int(dominionid))
            print(dominionname)
            with open("currentdecks.txt", "a", encoding="ascii") as f:
                f.write( dominionname + "\n")
        elif re.match(r'"\d+":"\d+"',decksplit[index]): # cards of the deck (but not the first one), using regex just in case there is something else in the list.
            match = re.search(r'"(\d+)":"(\d+)"', decksplit[index])
            cardid = match.group(1)
            cardname = carddata.get(int(cardid))
            cardnumber = match.group(2)
            if int(cardnumber) > 1:
                with open("currentdecks.txt", "a", encoding="ascii") as f:
                    f.write( cardname + " #"+cardnumber+',')
            else: 
                with open("currentdecks.txt", "a", encoding="ascii") as f:
                    f.write( cardname + ",")     
        index +=1  
    
else:
    print("Please run this script in TUO data folder according to instructions!")
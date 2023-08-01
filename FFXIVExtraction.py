import asyncio
from email import message
import logging
import api_keys

import pandas as pd

import aiohttp
import pyxivapi 
from pyxivapi.models import Filter, Sort


class FFXIVExtraction:
    hotdog_id="9234208823458267779"
    client = pyxivapi.XIVAPIClient(api_key=api_keys.FFXIV)
    character_columns = ["charId","Name","ClassJobsBozjan","ClassJobsElemental","DC","GrandCompany","Gender","Deity","Race","Nameday","Server","Title","TitleTop","Town","Tribe","Bio"]
    item_columns = ["charId","name","wear_loc","item"]
    classjobs_columns=["charId","name","job","level","specialized","class","category","abbreviation","active"]
    minion_columns = ["charId","c_name","m_name","type"]
    character_df = pd.DataFrame(columns=character_columns)
    items_df = pd.DataFrame(columns=item_columns)
    minion_df = pd.DataFrame(columns=minion_columns)
    classjobs_df = pd.DataFrame(columns=classjobs_columns)

    def run_full(self):
        logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')

        loop = asyncio.get_event_loop()
        loop.run_until_complete(test.fetch_example_results())

    async def fetch_example_results(self):

        '''freecompany = await client.freecompany_search(
            world="Ultros",
            name="hotdog"
        )

        companyData = await client.freecompany_by_id(
            lodestone_id="9234208823458267779",
            extended=True,
            include_freecompany_members=True
            )

        member_list = list(companyData.values())[1]'''

        await self.update_freecompany_pdata(self.hotdog_id)
        

        await self.client.session.close()

        '''member_list = list(companyData.values())[1]
        print(member_list)
        for member in member_list:
            print(f'Name: {member["Name"]}, ID: {member["ID"]}, Rank:{member["Rank"]}')'''


    async def update_freecompany_pdata(self,freecompany_id):
        character_id_list = ["12902234","35210768","36173485","20833237","36137423"]
        for character in character_id_list:
            character_dat_full = await self.fetch_character_data(character)
            character_dat = character_dat_full["Character"]
            self.update_character_df(character_dat)
            self.update_minionmount_df(character_dat_full)
            self.update_classjobs_df(character_dat)
            self.update_equipment_df(character_dat)
        self.write_freecompany_to_csv()
           

    async def fetch_character_data(self, character_id):
        characterData = await self.client.character_by_id(
            lodestone_id=character_id,
            extended=True,
            include_classjobs=True,
            include_minions_mounts=True,
            include_achievements=True
        )
        return characterData

    def update_character_df(self, character_data):
        self.character_df = self.character_df._append(
            {"charId":character_data["ID"], "Name":character_data["Name"], "ClassJobsBozjan":str(character_data["ClassJobsBozjan"]),
            "ClassJobsElemental":str(character_data["ClassJobsElemental"]),"DC":character_data["DC"],"GrandCompany":str(character_data["GrandCompany"]),
            "Gender":character_data["Gender"],"GuardianDeity":str(character_data["GuardianDeity"]),"Race":str(character_data["Race"]),
            "Nameday":character_data["Nameday"],"Server":character_data["Server"],"Title":str(character_data["Title"]),
            "TitleTop":character_data["TitleTop"],"Town":str(character_data["Town"]),"Tribe":str(character_data["Tribe"]),"Bio":character_data["Bio"]},
            ignore_index=True
        )

    def update_minionmount_df(self,character_data):
        for minion in character_data["Minions"]:
            self.minion_df = self.minion_df._append({"charId":character_data["Character"]["ID"],"c_name":character_data["Character"]["Name"],"m_name":minion["Name"],"type":"Minion"}, ignore_index=True)
        for mount in character_data["Mounts"]:
            self.minion_df = self.minion_df._append({"charId":character_data["Character"]["ID"],"c_name":character_data["Character"]["Name"],"m_name":mount["Name"],"type":"Mount"}, ignore_index=True)

    def update_equipment_df(self,character_data):
        for item_loc in character_data["GearSet"]["Gear"]:
            self.items_df = self.items_df._append(
                {"charId":character_data["ID"],"name":character_data["Name"],"wear_loc":item_loc,"item":str(character_data["GearSet"]["Gear"][item_loc])},
                ignore_index=True
                )

    def update_classjobs_df(self, characterdata):
        active_class = characterdata["ActiveClassJob"]["Class"]["Name"]
        for curr_class in characterdata["ClassJobs"]:
            self.classjobs_df = self.classjobs_df._append(
                {"charId":characterdata["ID"],"name":characterdata["Name"],
                "job": curr_class["Job"]["Name"] if curr_class["IsSpecialised"] else curr_class["Class"]["Name"],
                "level":curr_class["Level"],"specialized":curr_class["IsSpecialised"],"class":curr_class["Class"]["Name"],
                "category":curr_class["Class"]["ClassJobCategory"], "active":active_class==curr_class["Class"]["Name"],
                "abbreviation":curr_class["Job"]["Abbreviation"] if curr_class["IsSpecialised"] else curr_class["Class"]["Abbreviation"]},
                ignore_index=True
            )
     
    def write_freecompany_to_csv(self):
        self.write_characters_to_csv()
        self.write_classjobs_to_csv()
        self.write_items_to_csv()
        self.write_minionmounts_to_csv()
        #character_frame = pd.DataFrame.from_dict(character_data)
        print (self.character_df.head())

    def write_characters_to_csv(self):
        self.character_df.to_csv("data/ffxiv_characters.csv")

    def write_minionmounts_to_csv(self):
        self.minion_df.to_csv("data/ffxiv_minionmounts.csv")

    def write_items_to_csv(self):
        self.items_df.to_csv("data/ffxiv_items.csv")

    def write_classjobs_to_csv(self):
        self.classjobs_df.to_csv("data/ffxiv_classjobs.csv")


test = FFXIVExtraction()
test.run_full()


        
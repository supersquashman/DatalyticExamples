import pandas as pd
import seaborn as seas
import matplotlib.pyplot as plt


class FFXIVAnalysis:

    def loadAll(self):
        self.load_characters()
        self.load_classes()
        self.load_items()
        self.load_minionmounts()

    def load_characters(self):
        self.characters_df = pd.read_csv(r"data/ffxiv_characters.csv")

    def load_items(self):
        self.items_df = pd.read_csv(r"data/ffxiv_items.csv")

    def load_minionmounts(self):
        self.minionmounts_df = pd.read_csv(r"data/ffxiv_minionmounts.csv")

    def load_classes(self):
        self.classes_df = pd.read_csv(r"data/ffxiv_classjobs.csv")

    def compare_minionmounts(self):
        #print(self.minionmounts_df)
        seas.displot(data=self.minionmounts_df, x="c_name",hue="type",palette="viridis",multiple="stack")
        plt.xticks(rotation=295)
        plt.show()

    def compare_all_classes(self):
        smaller_df= self.classes_df.loc[:, ["name","level","class"]]
        seas.displot(data=smaller_df,x="name",hue="class",multiple="stack")
        plt.xticks(rotation=295)
        plt.show()

test = FFXIVAnalysis()
#test.load_minionmounts()
#test.compare_minionmounts()
test.load_classes()
test.compare_all_classes()
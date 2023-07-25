from operator import contains
from re import T
import numpy as np
import pandas as pd
import seaborn as seas
import matplotlib.pyplot as plt


class DnDAnalytics:
    #df=pd.DataFrame()
    class_list = pd.DataFrame(columns=["class","sp_lev"])
    class_spell_list = pd.DataFrame(columns=["class","sp_lev","counted"])

    def __init__(self):
        self.intake()
        self.levels_by_class()

    #Create and draw line graph of number of total available spells per class
    def spells_avail_line(self):
        #need to apply some aggregation and transformation to the data present first
        self.df['classes'].apply(self.parse_spell_distribution)
        seas.lineplot(data=self.class_spell_list,hue="class", x="sp_lev", y="counted")
        #spell levels range from 0 (cantrips) to 9th level spells
        plt.xlim(0,9)
        plt.show()

    def levels_by_class(self):
        #levClass = pd.DataFrame()
        self.df['classes'].apply(self.parse_spell_distribution)
        
        
    def parse_spell_distribution(self,class_entry):
        #tighter aggregation, good for text viewing results of processing
        for cl in class_entry.split(','):
            #tighter aggregation, good for text viewing results of processing
            if cl.strip() not in self.class_list['class'].values:
                self.class_list = self.class_list._append(
                    {"class":cl.strip(),"sp_lev":self.df['level'].where(self.df['classes'].str.contains(cl.strip())).value_counts().sort_index(ascending=True)}
                    , ignore_index=True)
            
            #flatter data for easier presentation via visualizations
            if cl.strip() not in self.class_spell_list['class'].values:
                for ind, coun in enumerate(self.df['level'].where(self.df['classes'].str.contains(cl.strip())).value_counts().sort_index(ascending=True)):
                    self.class_spell_list = self.class_spell_list._append(
                        {"class":cl.strip(), "sp_lev": ind, "counted":coun}, ignore_index=True
                    )
        self.class_list=self.class_list.sort_values(by='class')

    def intake(self):
        self.df = pd.read_csv(r"data/dnd-spells.csv")

    def describe(self):
        print("Head:")
        print(self.df.head())
        print("Class List:")
        print(self.class_list)
        print("class spell list:")
        print(self.class_spell_list)
        
    def graph_unique_spell_count(self):
        #self.df['classes'].apply(self.parse_unique_spells_by_class)
        #print(self.df['classes'][self.df['classes'].str.split(",").str.len() == 1].value_counts())
        #unique_dist_cl_df = self.df['classes'][self.df['classes'].str.split(",").str.len() == 1].value_counts().reset_index()

        unique_dist_cl_df = self.df['classes'][self.df['classes'].str.split(",").str.len() == 1].reset_index()
        print(unique_dist_cl_df)
        #print(self.df[['classes','level']][self.df['classes'].str.split(",").str.len() == 1].value_counts())
        unique_dist_cl_spl_df = self.df[['classes','level']][self.df['classes'].str.split(",").str.len() == 1].value_counts().reset_index()
        seas.lineplot(data=unique_dist_cl_spl_df, hue="classes", x="level", y="count")
        plt.xlim(0,9)
        #plt.show()
        unique_dist_graph = seas.displot(data=unique_dist_cl_df.sort_values("classes"),hue="classes", x="classes",bins=unique_dist_cl_df['classes'].count()+1)
        unique_dist_graph.set(yticks=[5,10,15,20,25,30,35,40,45,50,55,60,65])
        unique_dist_graph.set_titles('a rguglar title')
        plt.ylim(0,unique_dist_cl_df['classes'].value_counts().max()+5)
        plt.xticks(rotation=295)
        plt.show()
    
    def show(self):
        plt.show()
    

analyzer = DnDAnalytics()
#analyzer.spells_avail_line()
analyzer.describe()
#analyzer.graph_unique_spell_count()
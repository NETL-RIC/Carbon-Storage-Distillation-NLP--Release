# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 14:30:55 2019

@author: sabbatim
"""

# -*- coding: utf-8 -*-
"""
This loops through docuemnts in a folder and 
classified the doc by 5 topics
"""
#import modules
import gensim.corpora as corpora
import gensim
import PDFtoDatabase
from PDFtoDatabase import cleanupdocuments #custom cleanup module
import os

#scan through folder and collect new document text
#these documents will be classified into the topics
# Old test topic names topic_names = [[0, "Data Science"],[1, "Economic Geology"], [2, "Offshore Regulatory"], [3, "Oil Spill Modeling"], [4, "Volcanology"]]

#User inputs
#New topic names from Paige
topic_names = [[1, 'Field Injection and Monitoring'], [2, 'NatCarb RCSP Documents'],
               [3, 'CCS Project Research and Site Analysis'], [4, 'Sandstone Reservoir Projects'],
               [5, 'Sampling and Sample Testing'], [6, 'Permitting and Environmental Regulation'],
               [7, 'Methods and Analysis of Injection'], [8, 'Data Logging and Subsurface Analysis (Seismic)'],
               [9, 'Data Use, Authorization and EDX']]
LDAModelLocation = r'E:\NATCARB\NLP2-11-20\LDA Models_2_10_2020\9topicLDAModel.gensim'
dictionaryLocation = r'E:\NATCARB\NLP2-11-20\LDA Models_2_10_2020\dictionary.gensim'
#need to add a folder where you have new docs to classify in topics 
doclocation = r'E:\NATCARB\NLP2-11-20\NATCARB Corpus Dump\SampleDocs'

#collect text from documents in doclocation folder
list = os.walk(doclocation)
collectfiles = []
for path, dir, filenames in list:
    for file in filenames:
        if '.pdf' in file:
            paperloc = os.path.join(path, file)
            doctext, metadata = TikaTest.readpdfRaw(paperloc)
            collectfiles.append([file, doctext])

# old model location lda_model5 = gensim.models.ldamodel.LdaModel.load('All_LDA_5.gensim')
lda_model5 = gensim.models.ldamodel.LdaModel.load(LDAModelLocation)
dictionary = corpora.Dictionary.load(dictionaryLocation)
print("loaded")


#%%
#this section loops through the new papers and plots a pie chart
#newdoc = ['The deposit of an exceptionally large volcanic debris avalanche underlies the southwestern part of Shasta Valley in north-central California (Fig. 1). The lithology of the deposit shows that it was derived chiefly from a large andesitic volcano at the site of, and presumed to be an ancestor of, the present Mount Shasta volcano. The surface of the deposit is marked by hundreds of mounds, hills, and ridges and closely resembles the topography of debris avalanches from other volcanoes (Fig. 2). The mounds and hills of Shasta Valley have puzzled geologists for more than half a century. Diller and others (1915) noted that the hills consist of volcanic rock and stated they they appear to be, in part at least, the products of minor and local eruptions that broke through the Cretaceous beds, each vent contributing its little pile of material. Fenner (1923) proposed that a shallow sill had been intruded beneath Shasta Valley and that small bodies of magma from the sill rose to the surface to form the individual hills. Williams (1949) mapped the hills and ridges between the base of the volcano and Lake Shastina as moraines left by a glacier of Tioga age that moved into Shasta Valley from the slopes of Mount Shasta, and his geologic map shows a flat area to the west as glaciofluvial deposits. Williams believed that the hills and ridges north of Lake Shastina are products of stream dissection in volcanic rocks of Tertiary age, the Western Cascade Series. Mack (1960) agreed with Williamss interpretations; his geologic map shows the southern part of the debris-avalanche deposit as morainal deposits, and the hills to the north as volcanic rocks of the western Cascades. The map shows most flat areas between hills and ridges as younger alluvium of Recent age, although terraces northwest of Weed are shown as fluvioglacial deposits. Mack (1960, p. 44) described an outcrop in the ridge immediately west of Lake Shastina dam as deposits of GEOLOGY, v. 12, p. 143-146, March 1984 143 Downloaded from https://pubs.geoscienceworld.org/gsa/geology/article-pdf/12/3/143/3507371/i0091-7613-12-3-143.pdf by Baylor University user on 02 August 2019 stratified drift which were probably laid down in contact with the wasting glacial ice. Christiansen (1982) briefly mentioned the unusual topography of Shasta Valley and suggested that it resulted from a large debris avalanche from Mount Shasta. During field work in 1982, we (Crandell et al., 1983) verified the debris-avalanche origin of the topography and discovered details that are described here. TOPOGRAPHIC AND GEOLOGIC SETTING OF THE DEBRIS AVALANCHE The debris-avalanche deposit underlies the western two-thirds of Shasta Valley, which is a broad depression between the Klamath Mountains on the west and the Cascade Range on ::he east. The valley is drained by the Shasta River, which meanders northward across the surface of the avalanche deposit and basaltic lavas of Quaternary age. The floor of Shasta Valley slopes northward from an altitude of a little over 900 m near Weed to about 760 m near Montague. Mount Shasta volcano, which has a summit altitude of 4,316 m and an estimated volume of about 335 km3  (Williams, 1932), lies at the south end of the valley. Shasta Valley is flanked on the west and north by ultramafic and metamorphic rocks of pre-Cretaceous age and by eastward-dipping marine sandstone and conglomerate of the Upper Cretaceous Hornbrook Formation (Peck et al., 1956). Volcanic rocks of Tertiary age border the valley on the north and east and also form a few hills that rise above the central part of the valley floor, such as Gregory Mountain, Steamboat Mountain, and Owls Head. The avalanche deposit is overlain on the east by basaltic lavas. MORPHOLOGY OF THE DEBRIS AVALANCHE The most conspicuous features of the debris avalanche are hundreds of scattered mounds, hills, and ridges that are separated by flat areas. Although most of the hills are of round or irregular shape in plan view, prominent ridges are present near Lake Shastina and southwest of Weed. The largest ridge borders the northwest side of the lake (Fig. 3) and has a sinuous northeasterly trend transverse to the direction in which the avalanche moved. This ridge is 8-9 km long and as much as 1.5 km wide, and its highest point is about 210 m above the adjacent flat area to the north. The hills decrease in number as well as in basal area and height toward the northwest. Hills 2-10 km northwest of Lake Shastina include some with basal areas of as much as 2 km2  and heights of as much as 180 m. Near Montague, in contrast, most hills have basal areas of less than 0.06 km2  and heights of less than 30 m. The Shasta River has cut down only 9 m into the debris-avalanche deposit near Edgewood, and less than 30 m west of Montague. The lack of deep dissection of the deposit is largely due to a resistant bedrock threshold near the upper end of the Shasta River gorge (Fig. 1). DESCRIPTION OF THE DEBRIS-AVALANCHE DEPOSIT The debris-avalanche deposit consists of two lithologically distinct parts, which we refer to as the matrix facies and the block facies. The matrix facies consists of an unsorted and unstratified mixture of pebbles, cobbles, and boulders in compact sandy silt; texturally it resembles a mudflow. Virtually all boulders and most cobbles are pyroxene andesites similar to rocks that make up the present Mount Shasta volcano. At one locality northwest of Montague, the matrix facies overlies an unconsolidated deposit of oxidized sand and gravel that probably is part of an alluvial fan along the west flank of Shasta Valley. At this locality, the matrix facies contains masses several metres in diameter of similar sand and gravel. Smaller fragments in the matrix facies include sandstone and conglomerate derived from the Hornbrook Formation as well as metamorphic rocks. A few clasts at this and other localities consist of diatomite and laminated silt. The matrix facies at this locality and some others contains fossils of aquatic organisms, described below. The fine-grained component of the matrix evidently is made up of several constituents, including sedimentary rock from the Hornbrook Formation, volcanic rock that was pulverized during movement of the debris avalanche, and fine-grained alluvial and lacustrine sediments incorporated by the avalanche as it traversed the floor of Shasta Valley. The matrix facies underlies flat areas between hills and extends beyond the outermost extent of the hills and mounds to the west side of Shasta Valley. The flat areas slope northwestward about 5 m/km and border the Shasta River as far as the upper end of the Shasta River gorge. The block facies forms the mounds, hills, and ridges of the debris avalanche. The block facies includes individual andesite blocks ranging in size from tens to hundreds of metres in maximum dimension, many of which are brecciated, as well as masses of coherent but unconsolidated volcaniclastic deposits of similar size. Some hills consist of one or more large blocks of a single rock type, although the slopes of most such hills are veneered with smaller rock fragments of varied rock types, mostly derived from ancestral Mount Shasta but locally including pebbles and cobbles of metamorphic rock. Other hills are formed by lithologically dissimilar blocks, some of which are parts of continuous stratigraphic successions and probably were transported by the avalanche in the same relative positions that they had within the volcano. Still other hills and ridges contain unconsolidated volcaniclastic deposits that are in their original stratigraphic succession.']
#loop through collected papers
for paper in collectfiles:
    #get text of paper
    newdoc = paper[1]
    #cleanup paper
    new_doc = cleanupdocuments([newdoc])
    #create bag of words from paper
    new_doc_bow = dictionary.doc2bow(new_doc[0])
    #list paper topics and print percentage of paper per topic
    paper_topics = lda_model5.get_document_topics(new_doc_bow)
    print(paper_topics)
    topicplot = []
    #add topic name to topic percentage calculated
    for i, topic in enumerate(paper_topics):
        for x, name in enumerate(topic_names):
            if topic[0] == name[0]:
                topicplot.append([topic[1]*100,name[1]])           
    print(topicplot)
    #split list into labels and sizes
    sizes = []
    labels = []
    for row in topicplot:
        sizes.append(row[0])
        labels.append(row[1])
        
    #Create pie chart
    import matplotlib.pyplot as plt
    #%matplotlib inline
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,  labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90, radius=500)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #add title based on orignal doc file name
    plt.suptitle(paper[0].split("\\")[-1])
    #save plot to png in this folder
    plt.savefig(paper[0].split("\\")[-1].split(".")[0]+'piechart.png', dpi=300)
    plt.show()
print("done")


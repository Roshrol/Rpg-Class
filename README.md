# Rpg-Class

Group Members:
Layla and Edy

Abstract
We want to build a machine learning model whose purpose is to solve which class a character is in based on their stat distribution in Role-Playing Games. By learning patterns in how stats like strength, dexterity, intelligence, and stamina relate to a character’s play-style, the model should be able to classify builds automatically instead of requiring a player to choose a class upfront. We will evaluate the model using accuracy, some sort of per-class accuracy, and a confusion matrix. A successful project in our opinion will be a model that has an accuracy of around 40-50% as a baseline. 

Motivation and Question
We have user information for which our predictive models would help us classify character types, in doing so we hope to answer the question of what stat distribution would belong to what class (ig. Warrior, mage, healer). We hope to bring an opposite character developing feature to gaming. Role-playing games like Elder Scroll’s or Baldur’s Gate III have the function of basing originally made characters stats like strength, magic, and stamina on what class is recommended. We would love to have this functionality help those new into the gaming and D&D world where making original characters can be intimidating for many especially with a lack of knowledge.

Planned Deliverables
Github repository including all packages and README file
A Python Package containing all code
One Jupyter notebook illustrating the use of the package to analyze data
Folder of data collected and instead of web scraping it will be maunua;lly collected on numerous information sites
Written blog post on project

Full success in terms of our model specifically, would include a 40-50% accuracy rate given through the Jupyter notebook. Even higher while not our baseline would be an exceeding performance and a future aim. Our model would be able to accurately categorize character types to fluctuating stat distributions based on player’s preferences. Also determining if the player would have a better experience with a “type” that does not fall in the already established class types.

Full success to use personally would be having both a working model/code repository that showcases machine learning. Also we would hope to have the base to a future project such as a training model that could be used for future applications such as polishing this generator and making it usable for game functions.

Partial success in terms of our model specifically, would be falling below the baseline but at least having some semblance of pattern recognition. One of the things that we have to tackle is helping our model learn how to weigh the distributions so that our model doesn't get stuck guessing the same category every time.

Partial success personally would be a successful algorithm that showcases what we have learned in class. 

Resources Required
For our project we will definitely need data as it is the basis for the RPG class classification. In this case if we decide to do oblivion certain races are inclined or have a bias towards certain stats which will affect our algorithm. 

Oblivion class attributes:
https://www.scribd.com/document/836934195/Oblivion

This will likely be our main dataset, it contains the features and classes necessary to conduct our research on which rpg class the person is. It is a database of various characters made thus it will be a great basis for our research.
Dataset/Database:
https://www.elderstats.com/stats/db/oblivion

We will also need a copy of the game Oblivion (which Edy does own) for any extra cases.

We will likely use the gpu provided by google colab.

What You Will Learn

Edy intends to learn how to gather a data-set, and parse it into a spread sheet for us and the machine to read. In addition he wants to learn the best ways to think about features, classes and any other attributes as this project will include various different ways to weigh certain things. For example a warrior might value strength more than a mage but that doesn’t really take into account classes that are more hybrid. Generally he wishes to practice more with the tools that we have learnt in class and applying it in an application driven model. 

Layla intends to deepen her understanding of machine learning and its applications. She intends to strengthen her skills on feature engineering and model selection as we’ve been taught a few in class already. As the project continues she also aims to gain practical experience working with programming tools such as Python based ML frameworks and data preprocessing. As well as improving her teamworking, project management, and communication skills. We aim to work collaboratively on a project that we are both passionate about and hope to help other gamers who may find the character building feature overwhelming at first.

Risk Statement
One concern of ours is that while we think the idea is quite interesting, we might not be able to find the proper data sets we need. While there are many rpgs we can take inspiration from, there comes the issue of documentation for many of them. Additionally even if we do find some information, how can we get it into a data sheet? What will our criteria be, thresholds for certain stats, ect? How will we determine hybrid classes/stat distribution ect, it is a lot to think about despite the concept being quite simple. 


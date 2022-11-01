# Mining Arguments in Political Domain with Transformer Language Models 

## Project description 

This repository was developed as part of the Master's individual research project carried out at the University of Potsdam, Germany. Please find our detailed report [here](https://github.com/a-moi/political-argument-mining/blob/main/IM-final-report.pdf). 

**Abstract**


This project is focused on argumentation
mining framed through the tasks of argument
detection (predict whether the utterance
is an argument or not) and argument
component identification (predict whether
the argumentative utterance is a claim or
a premise). We implementing BERT and
RoBERTa models and approach both tasks
on the sentence-level. The second task,
component identification, is also modelled
on the argumentative discourse unit level.
To train and test our models, we use a
large-scale corpus of the US presidential
debates data (Haddadan et al., 2019). Additionally,
we study models’ generalizability
to the data within the same domain.
For that, we collect and manually annotate
a novel dataset of diplomatic speeches
presented in the United Nations Security
Council.


## Corpora 

For our experiments, we use two corpora. 

1. [USElecDeb](https://github.com/a-moi/political-argument-mining/tree/main/ElecDeb60To16) contains speeches of presidential debates in the US from the years 1960 to 2016. The corpus is annotated according to argumentative structure of speeches and contains such labels as claims and premises. The dataset was introduced in this [paper](https://aclanthology.org/P19-1463/). For the sentence-level experiments, we used only `sentence_db_candidate.csv` file as it provides all the necessary texts along with labels ans the original train, test and validation splits. 

2. [UC-UNSC](https://github.com/a-moi/political-argument-mining/tree/main/UC-UNSC) As part of the project, we develop a novel corpus of argument annotations. We retrive diplomatic speeches given during gatherings of the UNSC. We select 144 speeches from 2014 to 2018, dedicated to the conflict in Ukraine. We name it UC(Ukraine Conflict)-UNSC. The speeches were annotated analogically to USElecDeb and the labels include claims, premises or none of these. 

We provide 144 pairs of raw data: original .txt files and .xmi files with their respective annotations, retrived from Inception. Additionally, we provide two ready-to-use datasets. The file `sentence_full.csv` contains the following columns: sentences, final labels (claims or premises or none) and detailed labels, i.e., per each sentence, we list all its components along with their length. This length measure was used to give the final label to a sentence, since some sentences contain both a claim and a premise, and we made the decision in favor of the longer component. The file `component_full.csv` includes two columns: the component (original span, not always a sentence) and its label. 

Two python [functions](https://github.com/a-moi/political-argument-mining/blob/main/annotation2df.py) were developed to map .xmi files from Inception and the original .txt files. The outputs are labelled ready-to-use .csv files. 

## Reproduction and running on your data 

We use `bert-for-sequence-classification` Python [framework](https://pypi.org/project/bert-for-sequence-classification/) to fine-tune BERT and RoBERTa models. We attach three Python notebooks, each representing a different problem setting: 1) classification of arg vs non-arg the sentence-level; 2) classification of claims and premises on the sentence-level; 3) classification of claims and premises on the ADU-level. 

To reproduce the models, we recommend using Google Colab which enables free GPU unit. Load a notebook into your Colab env, then load and prepare the data.
To change RoBERTa to BERT, simply amend the config by selecting a model you want to use. We used `chkla/roberta-argument`, `roberta-base` and `bert-base-uncased`. We also attach `hyperparams.csv` with all the parameters and settings we used at each experiment, to facilitate reproduction. 

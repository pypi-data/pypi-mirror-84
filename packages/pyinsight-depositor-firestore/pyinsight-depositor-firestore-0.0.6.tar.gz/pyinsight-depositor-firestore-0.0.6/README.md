# Insight Module Firestore Depositor
This is a Depositor Plug-in of Insight Module
## Depositor Introduction
Depositor is one kind of worker in Insight Module
* Depositore store received data and merge it
* Once Package process 
* Any Depositor Module should be able to store data without table structure predefintion
## Firestore Depositor Introduction
Google Cloud Firestore based implementation with the following advantage
## How to use
Depositor is used in an Insight Action (Receiver, Merger, Packager, etc...)
An Insight Application is a workflow of multiple Insight Action
## How to test
Before running pytest, please:
1. Set the needed GCP credential in the environnement variables
2. Running init_topic to create needed index

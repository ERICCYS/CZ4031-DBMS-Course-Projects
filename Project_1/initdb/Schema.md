# Tables and Schemas

## PERSON

| Field | Type |
| :-----: | :-----: |
| personId | INT |
| personFullName | VARCHAR(100) |

## AUTHORSHIP

| Field | Type |
| :-----: | :-----: |
| pubKey | VARCHAR(150) |
| personFullName | VARCHAR(100) |

## EDITORSHIP

| Field | Type |
| :-----: | :-----: |
| pubKey | VARCHAR(150) |
| personFullName | VARCHAR(100) |

## PUBLICATION

| Field | Type |
| :-----: | :-----: |
| pubId | INT | 
| pubMdate | DATE |
| pubKey | VARCHAR(150) |
| pubTitle | VARCHAR(1000) |
| pubYear | SMALLINT |
| pubEE | VARCHAR(200) |
| pubSubType | VARCHAR(50) |
| pubType | VARCHAR(50) |
| confName | VARCHAR(300) |

## ARTICLE

| Field | Type |
| :-----: | :-----: |
| pubkey | VARCHAR(150) | 
| articleJournal | VARCHAR(200) |
| articleVolume | VARCHAR(100) |
| articleNumber | VARCHAR(50) |
| articlePages | VARCHAR(100) |
| articleUrl | VARCHAR(200) |
| articleBooktitle | VARCHAR(400) |
| articleCrossref | VARCHAR(200) |

## INPROCEEDING

| Field | Type |
| :-----: | :-----: |
| pubkey | VARCHAR(150) |
| inproBooktitle | VARCHAR(400) |
| inproPages | VARCHAR(100) |
| inproUrl | VARCHAR(200) |
| inproCrossref | VARCHAR(200) |


## PROCEEDING

| Field | Type |
| :-----: | :-----: |
| pubkey | VARCHAR(150) |
| proceedBooktitle | VARCHAR(400) |
| proceedVolume | VARCHAR(100) |
| proceedSeries | VARCHAR(300) |
| proceedPages | VARCHAR(100) |
| proceedUrl | VARCHAR(200) |
| proceedCrossref | VARCHAR(200) |

## BOOK

| Field | Type |
| :-----: | :-----: |
| pubkey | VARCHAR(150) |
| bookBooktitle | VARCHAR(400) |
| bookSeries | VARCHAR(300) |
| bookPages | VARCHAR(100) |
| bookUrl | VARCHAR(200) |
| bookCrossref | VARCHAR(200) |

## INCOLLECTION

| Field | Type |
| :-----: | :-----: |
| pubkey | VARCHAR(150) |
| incolBooktitle | VARCHAR(400) |
| incolNumber | VARCHAR(50) |
| incolPages | VARCHAR(100) |
| incolUrl | VARCHAR(200) |
| incolCrossref | VARCHAR(200) |

## WWW

| Field | Type |
| :-----: | :-----: |
| pubkey | VARCHAR(150) |
| wwwBooktitle | VARCHAR(400) |
| wwwUrl | VARCHAR(200) |

## MASTERTHESIS

| Field | Type |
| :-----: | :-----: |
| pubkey | VARCHAR(150) |
| masterthesisSchool | VARCHAR(300) |

## PHDTHESIS

| Field | Type |
| :-----: | :-----: |
| pubkey | VARCHAR(150) |
| phdthesisVolume | VARCHAR(100) |
| phdthesisSeries | VARCHAR(300) |
| phdthesisPages | VARCHAR(100) |
| phdthesisSchool | VARCHAR(300) |
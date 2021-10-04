# User Story

## Users

### Tourists

As a tourist, I want to explore the city. I wish to attend events that fits my interest. I want a tool that can help me to locate these interesting events, so that I could go check them out.

### Locals

As a local citizen living here, I wish to know what is going on in my city. I wish to join events that fits my interest, while also avoiding places that are crowded. I want a tool that can tell me what is happening in the city so I could plan my day around it.

### Businesses

As a business, I wish more people to buy/use my product. I wish to deploy advertising or organise promotional events to boost my product popularity. I wish to maximize the effectveness of such efforts. I want a tool that could tell me what events is happening in the city so I could plan my marketing strategy accordingly.

### Public services

As the city's public services, we wish to deploy our resource in the benefit of our citizens. We wish to reduce waste and increase the efficiency of our servies so that we could benefit more people. We want a tool that can tell us the events in teh city so we could deploy our reseources accordingly.

## Minimum Valued Product (MVP)

    - Able to collect tweets from within specified area
    - Able to analyse the tweets and extract a) sentiment and b) events and other keywords
    - Able to visualize the general mood of a given area using a map
    - Able to provide more specific information such as keywords when choosing an location on map

## Modules

| Modules       |                                                                     | Tools                         |
| ------------- | ------------------------------------------------------------------- | ----------------------------- |
| twitter_api   | Get tweets from a specific area                                     | Tiwtter API, Tweepy           |
| geocoder_api  | Get geocodes and address from a location name                       | Geopy, Nominatim              |
| language_api  | Perform NLP tasks, such as sentiment analysis and entity extraction | Google Could Natural Language |
| visualization | UI and visualize information extracted from tweets                  | Folium                        |

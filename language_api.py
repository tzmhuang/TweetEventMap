from google.cloud import language_v1


class LanguageAPI():
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()

    def get_sentiment_from_text(self, text):
        doc = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = self.client.analyze_sentiment(
            request={'document': doc})
        print(response)
        return response.document_sentiment.score

    def get_entities_from_text(self, text):
        doc = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = self.client.analyze_entities(request={'document': doc})
        # print(response)
        return response.entities


if __name__ == "__main__":
    api = LanguageAPI()
    text = "Hi, this is a test case for language api!.. This is another sentence"
    sentiment = api.get_sentiment_from_text(text)
    entities = api.get_entities_from_text(text)
    print("Input: {}".format(text))
    print("Sentiment: {}".format(sentiment))
    print("="*20)
    print("Entities: ")
    for entity in entities:
        print("{}, salience: {}, Type: {}".format(entity.name,
              entity.salience, language_v1.Entity.Type(entity.type_).name))

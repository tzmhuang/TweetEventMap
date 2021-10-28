from google.cloud import language_v1


class LanguageAPI():
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()

    def get_sentiment_from_text(self, text):
        doc = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = self.client.analyze_sentiment(
            request={'document': doc})
        # print(response)
        return response.document_sentiment.score, response.document_sentiment.magnitude

    def get_entities_from_text(self, text):
        doc = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = self.client.analyze_entities(request={'document': doc})
        # print(response.entities[0])
        return response.entities, response.entities.__str__()


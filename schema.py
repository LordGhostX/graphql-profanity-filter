import graphene
from better_profanity import profanity


class Result(graphene.ObjectType):
    sentence = graphene.String()
    is_profane = graphene.Boolean()
    censored_sentence = graphene.String()


class Query(graphene.ObjectType):
    detect_profanity = graphene.Field(Result, sentence=graphene.String(
        required=True), character=graphene.String(default_value="*"))

    def resolve_detect_profanity(self, info, sentence, character):
        is_profane = profanity.contains_profanity(sentence)
        censored_sentence = profanity.censor(sentence, character)
        return Result(
            sentence=sentence,
            is_profane=is_profane,
            censored_sentence=censored_sentence
        )


profanity.load_censor_words()
schema = graphene.Schema(query=Query)

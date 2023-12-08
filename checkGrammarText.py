'''Grammar main class'''
# import language_tool_python
# from deepmultilingualpunctuation import PunctuationModel


class CheckGrammar:

    @classmethod
    def checkGrammar(cls, text, language):
        # tool = language_tool_python.LanguageToolPublicAPI(language)
        # return tool.correct(text)
        return text


    @classmethod
    def checkPuntuaction(cls, text):

        return True
        # model = PunctuationModel("kredor/punctuate-all")
        # return model.restore_punctuation(text)


    @classmethod
    def cleanStartAndEnd(cls, text):

        while text[0] in '.,: ':
            text = text[1:]

        while text[-1] in '.,: ':
            text = text[:-1]

        return text

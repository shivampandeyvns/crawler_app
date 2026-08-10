class DocumentProfiler:

    def profile(self,text):

        words=text.split()

        return{

            "Words":len(words),

            "Characters":len(text),

            "Average Word Length":

            round(

                sum(len(w) for w in words)

                /len(words),

                2

            )

        }
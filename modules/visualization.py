import matplotlib.pyplot as plt

from wordcloud import WordCloud


def wordcloud_plot(text):

    wc=WordCloud(

        width=1000,

        height=500,

        background_color="white"

    ).generate(text)

    fig,ax=plt.subplots()

    ax.imshow(wc)

    ax.axis("off")

    return fig
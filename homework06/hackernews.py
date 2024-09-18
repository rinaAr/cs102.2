from bottle import route, run, template, request, redirect

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/", method="POST")
def add_label():
    news_id = request.forms.get("id")
    label = request.forms.get("label")
    
    if news_id and label:
        s = session()
        news_item = s.query(News).filter(News.id == news_id).first()
        if news_item:
            news_item.label = label
            s.commit()
        s.close()
    
    redirect("/news")



@route("/update")
def update_news():
    s = session()
    
    # Assuming get_news() returns a list of dictionaries with 'title' and 'content'
    news_list = get_news()
    
    for news in news_list:
        # Check if the news already exists in the database by title or content
        exists = s.query(News).filter(News.title == news['title']).first()
        if not exists:
            # Add the new news item to the database
            new_news = News(title=news['title'], content=news['content'])
            s.add(new_news)
    
    s.commit()
    s.close()
    
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    classifier = NaiveBayesClassifier()  # Assuming it's already trained
    
    # Fetch all unlabeled news
    unlabeled_news = s.query(News).filter(News.label == None).all()
    
    for news in unlabeled_news:
        # Classify the content using Naive Bayes
        predicted_label = classifier.classify(news.content)
        news.label = predicted_label
    
    s.commit()
    s.close()
    
    redirect("/news")



if __name__ == "__main__":
    run(host="localhost", port=8080)


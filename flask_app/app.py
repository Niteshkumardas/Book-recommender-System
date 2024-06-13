from flask import Flask, render_template,request
import pickle
import numpy as np

popular_df= pickle.load(open('D:/Fuse_machine/book_recommender_system/popular.pkl','rb'))
pivot_table= pickle.load(open('D:/Fuse_machine/book_recommender_system/pivot_table.pkl','rb'))
books= pickle.load(open('D:/Fuse_machine/book_recommender_system/books.pkl','rb'))
similarity_scores= pickle.load(open('D:/Fuse_machine/book_recommender_system/similarity_scores.pkl','rb'))

app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-S'].values),
                           votes=list(popular_df['Num_of_ratings'].values),
                           rating=list(popular_df['avg_of_ratings'].values),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input= request.form.get('user_input')
    index = np.where(pivot_table.index==user_input)[0][0]
    similar_items= sorted(list(enumerate(similarity_scores[index])),key= lambda x :x[1], reverse=True)[1:6]

    data=[]
    for i in similar_items:
        items=[]
        temp_df= books[books['Book-Title']== pivot_table.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-S'].values))

        data.append(items)

        
    return render_template('recommend.html', data=data)


if __name__=="__main__":
    app.run(debug= True)
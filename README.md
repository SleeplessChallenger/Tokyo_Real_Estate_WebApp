<h2>Full-Stack Django app with ML prediction feature</h2>

**Deployed with Docker**: `docker pull enoshima/tokyo_project:latest` <br>

 - after that command, run: `docker run --name tokyo_container -d -p 8085:8080 enoshima/tokyo_project:latest`
 - If current ports are already used, then: **first** one is port which will be displayed and **second** one is the<br>
   port specified in the `Dockerfile`. Hence change <ins>first</ins> one to match to another port.

<hr>

This is a project that resembles real-estate site.<br>
It's built:
 - with Django on backend
 - dynamic templates with Bootstrap/HTML/CSS on the frontend
 - as a DB I used Sqlite and for model creation: in-built Django-ORM
 - considering Machine Learning part, I used Sklearn to build 2 models

<h3>Features</h3>

<ul>
  <li>CRUD for users/posts/APIs</li>
  <li>Custom data loader from pandas to inject data from exisitng file</li>
  <li>2 ML models to predict price from prefilled or bare form</li>
  <li>Special form for posts bulk delete</li>
  <li>APIs for users/posts/profile</li>
  <li>Myraid of Unit Tests to improve quality</li>
</ul>

 
<h3>Structure</h3>

1. `general` is the base folder that has base template and code to handle CRUD for posts
2. `users` has CRUD for users with signals to create <ins>Profile</ins>
3. `prediction_price` has code to enable prediction and here deployed <ins>ML models</ins> <br>
are implemented via Interface and Composition
4. `data_loader` is a folder with mine-created tool to load data from Pandas into the model
5. `ML_models` is a folder where you can find:
   - 2 `.bin` models for production
   - notebooks where I did all the data preparation and machine learning
   - datasets

<h4>More about structure</h4>

1. Machine Learning models are done via Sklearn where first model is `Ridge()` and second is `Decision Tree Regressor()`

2. Models are done via `MainInterface()` to enable loose-coupling and easy addition of other models. <br>
  Two models, in turn, are augmeneted via <ins>Composition</ins> by `Regression()` class.<br>
  Also in these 2 classes there are model unpacking and function to trigger prediction which is done in that `Regression()` class.

3. `Regression()` class will do data transformation and prediction itself

4. In `Jupyter notebooks` you can observe model creation. In `real_estate_sklearn.ipynb` there is linear regression<br>
  implemented via a) bare numpy & python b) Sklearn. In `real_estate_dt_rf.ipynb` there is `DTR` via Sklearn.
  
5. I left on purpose `.env` (as it's not a production level) where you can find `secret_key` required for app to work.
 

<h3>Data</h3>

<ul>
  <li>For the base I used this dataset: https://www.kaggle.com/nishiodens/japan-real-estate-transaction-prices</li>
  <li>Then I trimmed it and did all the preparations. Processed dataset can be seen in ML_models both "zipped" and ".csv" </li>
</ul>


```bash
.
├── ML_models
│   ├── decision_tree_model.bin
│   ├── real_estate_dt_rf.ipynb
│   ├── real_estate_processed.csv
│   ├── real_estate_processed.csv.zip
│   ├── real_estate_sklearn.ipynb
│   └── regression_model.bin
├── README.md
├── api
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_view.py
│   ├── urls.py
│   └── views.py
├── data_loader
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── injection_class.py
│   ├── migrations
│   │   ├── __init__.py
│   ├── models.py
│   ├── static
│   │   └── data_loader
│   │       └── make_load.css
│   ├── templates
│   │   └── data_loader
│   │       └── make_load.html
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_view.py
│   └── views.py
├── db.sqlite3
├── general
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_propertyclass_can_add_posts.py
│   │   ├── 0003_auto_20210830_1043.py
│   │   ├── 0004_propertyclass_age.py
│   │   ├── 0005_alter_propertyclass_age.py
│   │   ├── 0006_alter_propertyclass_image.py
│   │   ├── 0007_auto_20210907_1102.py
│   │   ├── __init__.py
│   ├── models.py
│   ├── static
│   │   ├── favicon
│   │   │   ├── android-chrome-192x192.png
│   │   │   ├── android-chrome-512x512.png
│   │   │   ├── apple-touch-icon.png
│   │   │   ├── browserconfig.xml
│   │   │   ├── favicon-16x16.png
│   │   │   ├── favicon-32x32.png
│   │   │   ├── favicon.ico
│   │   │   ├── mstile-150x150.png
│   │   │   ├── safari-pinned-tab.svg
│   │   │   └── site.webmanifest
│   │   └── general
│   │       ├── all_properties.css
│   │       ├── delete_all_posts.css
│   │       ├── delete_post.css
│   │       ├── form_css.css
│   │       ├── main.css
│   │       ├── pages_img
│   │       │   ├── delete_page.jpg
│   │       │   └── sunflower.jpg
│   │       └── update_post.css
│   ├── templates
│   │   └── general
│   │       ├── all_properties.html
│   │       ├── create_post.html
│   │       ├── delete_all_posts.html
│   │       ├── delete_post.html
│   │       ├── single_post.html
│   │       ├── start_page.html
│   │       ├── update_post.html
│   │       └── user_posts.html
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_forms.py
│   │   ├── test_model.py
│   │   └── test_views.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── media
│   ├── avatar.jpg
│   ├── default_property.jpg
│   ├── propery_photo
│   │   ├── 8183BF8F-F393-4B12-9B6F-4147A616FFF9.JPG
│   │   ├── 8183BF8F-F393-4B12-9B6F-4147A616FFF9_s69UNqa.JPG
│   └── user_photo
│       ├── 6pu7Us-dDlk.jpg
├── notes.txt
├── prediction_price
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations
│   │   ├── __init__.py
│   ├── models.py
│   ├── prediction_interface.py
│   ├── prediction_model.py
│   ├── static
│   │   └── prediction_price
│   │       ├── form_css.css
│   │       └── price_result.css
│   ├── templates
│   │   └── prediction_price
│   │       ├── prediction_result.html
│   │       └── price_prediction.html
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_form.py
│   │   └── test_view.py
│   └── views.py
├── requirements.txt
├── tokyo_real_estate
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── decorators.py
    ├── forms.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_auto_20210830_1016.py
    │   ├── 0003_profile_can_add_posts.py
    │   ├── 0004_alter_profile_id.py
    │   ├── __init__.py
    ├── models.py
    ├── signals.py
    ├── static
    │   └── users
    │       ├── delete_acc.css
    │       ├── login.css
    │       ├── logout.css
    │       ├── pages_img
    │       │   ├── delete_account.jpg
    │       │   ├── logout_page.jpg
    │       │   └── profile_page.jpg
    │       ├── password_reset.css
    │       ├── profile.css
    │       └── register.css
    ├── templates
    │   └── users
    │       ├── all_users.html
    │       ├── delete_account.html
    │       ├── login.html
    │       ├── logout.html
    │       ├── password_reset.html
    │       ├── profile_page.html
    │       └── register.html
    ├── tests
    │   ├── __init__.py
    │   ├── test_decorators.py
    │   ├── test_form.py
    │   ├── test_model.py
    │   ├── test_signals.py
    │   └── test_views.py
    └── views.py
```

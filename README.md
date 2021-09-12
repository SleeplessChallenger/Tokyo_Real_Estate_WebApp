**Under development**

<h2>Full-Stack Django app with ML prediction feature</h2>

In this project I'm doing a Web-app with ML

<h3>Features</h3>

<ul>
  <li>CRUD for account & posts</li>
  <li>Custom data loader from pandas</li>
  <li>2 ML models to predict price from prefilled or bare form</li>
  <li>Form for posts bulk delete</li>
 </ul>
 
<h3>Structure</h3>

1. `general` is the base folder that has base template and code to handle CRUD for posts
2. `users` has CRUD for users with signals to create <ins>Profile</ins>
3. `prediction_price` has code to enable prediction and here deployed <ins>ML models</ins> <br>
are implemented via Interface and Composition
4. `data_loader` is a folder with mine-created tool to load data from Pandas into the model
5. `ML_models` is a folder where you can find notebooks where I did all the data preparation and machine learning
  + there you can see datasets (only preprocessed version as original one is too large)

<h3>Further description</h3>

1. Data
<ul>
  <li>For the base I used this dataset: https://www.kaggle.com/nishiodens/japan-real-estate-transaction-prices</li>
  <li>Then I trimmed it and did all the preparations. Processed dataset can be seen in repo. It's zipped</li>
</ul>

2. Models
<ul>
  <li>at first I did regression with numpy and bare python</li>
  <li>then I used sklearn to unleash regressions of various kinds: from Ridge() to RandomForestRegressor</li>
</ul>


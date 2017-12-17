# ------------Getting and processing the data-------------------
from builtins import print

print('------------Getting and processing the data-------------------')

from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName('MyFirstStandaloneApp')
sc = SparkContext(conf=conf)

# define download locations
print('---------------------------------------')
print('define download locations...')
print('---------------------------------------')
###########
###########
import os

datasets_path = os.path.join('..', 'datasets')
###########
###########


# not usefull since its already downloaded and extracted

# let's load the raw ratings data. We need to filter out the header, included in each file
###########
###########
print('---------------------------------------')
print('filtering out the header, included in each file...')
print('---------------------------------------')
small_ratings_file = os.path.join(datasets_path, 'ml-latest-small', 'ratings.csv')
small_ratings_raw_data = sc.textFile(small_ratings_file)
small_ratings_raw_data_header = small_ratings_raw_data.take(1)[0]
###########
###########


# Now we can parse the raw data into a new RDD
###########
###########
print('---------------------------------------')
print('parsing the raw data into a new RDD...')
print('---------------------------------------')
small_ratings_data = small_ratings_raw_data.filter(lambda line: line != small_ratings_raw_data_header) \
    .map(lambda line: line.split(",")).map(lambda tokens: (tokens[0], tokens[1], tokens[2])).cache()

###########
###########

print(small_ratings_data.take(3))

# We proceed in a similar way with the movies.csv file
###########
###########
print('---------------------------------------')
print('now all the above for movies...')
print('---------------------------------------')
small_movies_file = os.path.join(datasets_path, 'ml-latest-small', 'movies.csv')

small_movies_raw_data = sc.textFile(small_movies_file)
small_movies_raw_data_header = small_movies_raw_data.take(1)[0]

small_movies_data = small_movies_raw_data.filter(lambda line: line != small_movies_raw_data_header) \
    .map(lambda line: line.split(",")).map(lambda tokens: (tokens[0], tokens[1])).cache()
###########
###########
print('---------------------------------------')
print(small_movies_data.take(3))
print('---------------------------------------')
# --------------------Collaborative Filtering ---------------------

# The underlying assumption is that if a user A has the same
# opinion as a user B on an issue, A is more likely to have B's
# opinion on a different issue x than to have the opinion on x of a user
# chosen randomly. selecting ALS parameters using the small dataset
print('--------------------Collaborative Filtering ---------------------')
print('---------------------------------------')
print('---------------------------------------')
print('splitting data into training, validation and test datasets...')
print('---------------------------------------')
# We need first to split it into
# -------train-------------------
# -------validation--------------
# -------and test datasets-------
###########
###########
training_RDD, validation_RDD, test_RDD = small_ratings_data.randomSplit([6, 2, 2], seed=0)
validation_for_predict_RDD = validation_RDD.map(lambda x: (x[0], x[1]))
test_for_predict_RDD = test_RDD.map(lambda x: (x[0], x[1]))
###########
###########


# Now we can proceed with the

# --------training---------

# phase
###########
###########
print('---------------------------------------')
print('training...')
print('---------------------------------------')
from pyspark.mllib.recommendation import ALS
import math

seed = 5
iterations = 10
regularization_parameter = 0.1
ranks = [4, 8, 12]
errors = [0, 0, 0]
err = 0
tolerance = 0.02

min_error = float('inf')
best_rank = -1
best_iteration = -1
for rank in ranks:
    model = ALS.train(training_RDD, rank, seed=seed, iterations=iterations,
                      lambda_=regularization_parameter)
    predictions = model.predictAll(validation_for_predict_RDD).map(lambda r: ((r[0], r[1]), r[2]))
    rates_and_preds = validation_RDD.map(lambda r: ((int(r[0]), int(r[1])), float(r[2]))).join(predictions)
    error = math.sqrt(rates_and_preds.map(lambda r: (r[1][0] - r[1][1]) ** 2).mean())
    errors[err] = error
    err += 1
    print('For rank %s the RMSE is %s' % (rank, error))
    if error < min_error:
        min_error = error
        best_rank = rank
print('---------------------------------------')
print('The best model was trained with rank %s' % best_rank)
print('---------------------------------------')
###########
###########


# for three rows, for each row rating for that movie and user, as 'the predicted' by our ALS model as:
###########
###########
print("   for three rows, for each row rating for that movie and user, as 'the predicted' by our ALS model as:",
      predictions.take(3))
###########
###########


# Then we join these with our

# -------validation--------

#  data (the one that includes ratings) and the result looks as follows:
###########
###########
print('---------------------------------------')
print('validating...')
print('---------------------------------------')
print('---------------------------------------')
print('Then we join these with our validation data (the one that includes ratings) and the result looks as follows:'
      , rates_and_preds.take(3))
print('---------------------------------------')
###########
###########


# To that, we apply a squared difference and then we use the mean() action to get the MSE and apply sqrt
###########
###########
print('---------------------------------------')
print('applying a squared difference and then the mean() action to get the MSE and apply sqrt on the above...')
print('---------------------------------------')
model = ALS.train(training_RDD, best_rank, seed=seed, iterations=iterations,
                  lambda_=regularization_parameter)
predictions = model.predictAll(test_for_predict_RDD).map(lambda r: ((r[0], r[1]), r[2]))
rates_and_preds = test_RDD.map(lambda r: ((int(r[0]), int(r[1])), float(r[2]))).join(predictions)
error = math.sqrt(rates_and_preds.map(lambda r: (r[1][0] - r[1][1]) ** 2).mean())
###########
###########


# Finally we

# -------test-------

# the selected model.
###########
###########
print('---------------------------------------')
print('testing...')
print('---------------------------------------')
print('---------------------------------------')
print('For testing data the RMSE is %s' % (error))
print('---------------------------------------')
###########
###########


# ---------------Using the complete dataset to build the final model-----------------------
# -----------------------------------------------------------------------------------------

print('---------------Using the complete dataset to build the final model-----------------------')

# Using the complete dataset to build the final model

# Load the complete dataset file
###########
###########
print('---------------------------------------')
print('Loading the complete dataset (ratings.csv) file...')
print('---------------------------------------')
complete_ratings_file = os.path.join(datasets_path, 'ml-latest', 'ratings.csv')
complete_ratings_raw_data = sc.textFile(complete_ratings_file)
complete_ratings_raw_data_header = complete_ratings_raw_data.take(1)[0]
###########
###########


# Parse
print('---------------------------------------')
print('parsing the complete dataset...')
print('---------------------------------------')
###########
###########
complete_ratings_data = complete_ratings_raw_data.filter(lambda line: line != complete_ratings_raw_data_header) \
    .map(lambda line: line.split(",")).map(lambda tokens: (int(tokens[0]), int(tokens[1]), float(tokens[2]))).cache()

print('---------------------------------------')
print("There are %s recommendations in the complete dataset" % (complete_ratings_data.count()))
print('---------------------------------------')

###########
###########


# Now we are ready to train the recommender model.
###########
###########
print('---------------------------------------')
print('training the recommender model for the complete dataset....')
print('---------------------------------------')
training_RDD, test_RDD = complete_ratings_data.randomSplit([7, 3], seed=0)

complete_model = ALS.train(training_RDD, best_rank, seed=seed,
                           iterations=iterations, lambda_=regularization_parameter)
###########
###########


# print('testing on testing set....')
# #Now we test on our testing set.
# ###########
# ###########
# test_for_predict_RDD = test_RDD.map(lambda x: (x[0], x[1]))
#
# predictions = complete_model.predictAll(test_for_predict_RDD).map(lambda r: ((r[0], r[1]), r[2]))
# rates_and_preds = test_RDD.map(lambda r: ((int(r[0]), int(r[1])), float(r[2]))).join(predictions)
# error = math.sqrt(rates_and_preds.map(lambda r: (r[1][0] - r[1][1]) ** 2).mean())
#
# print('For testing data the RMSE is %s' % (error))
# print ('Note: We can see how we got a more accurate recommender when using a much larger dataset (rating.csv).')
# #We can see how we got a more accurate recommender when using a much larger dataset.
# ###########
# ###########


# How to make recommendations
print('---------------------------------------')
print('Its time for recommendations. Now loading movies.csv ...')
print('---------------------------------------')
# let's first load the movies complete file for later use
###########
###########
complete_movies_file = os.path.join(datasets_path, 'ml-latest', 'movies.csv')
complete_movies_raw_data = sc.textFile(complete_movies_file)
complete_movies_raw_data_header = complete_movies_raw_data.take(1)[0]
###########
###########

# Parse
###########
###########
print('---------------------------------------')
print('parsing the loaded movies dataset...')
print('---------------------------------------')
complete_movies_data = complete_movies_raw_data.filter(lambda line: line != complete_movies_raw_data_header) \
    .map(lambda line: line.split(",")).map(lambda tokens: (int(tokens[0]), tokens[1], tokens[2])).cache()

complete_movies_titles = complete_movies_data.map(lambda x: (int(x[0]), x[1]))
print('---------------------------------------')
print
"There are %s movies in the complete dataset" % (complete_movies_titles.count())
print('---------------------------------------')
###########
###########


# we want to give recommendations of movies with a certain minimum
# number of ratings. For that, we need to count the number of ratings per movie
###########
###########
print('---------------------------------------')
print('counting the number of ratings per movie...')
print('---------------------------------------')


def get_counts_and_averages(ID_and_ratings_tuple):
    nratings = len(ID_and_ratings_tuple[1])
    return ID_and_ratings_tuple[0], (nratings, float(sum(x for x in ID_and_ratings_tuple[1])) / nratings)


movie_ID_with_ratings_RDD = (complete_ratings_data.map(lambda x: (x[1], x[2])).groupByKey())
movie_ID_with_avg_ratings_RDD = movie_ID_with_ratings_RDD.map(get_counts_and_averages)
movie_rating_counts_RDD = movie_ID_with_avg_ratings_RDD.map(lambda x: (x[0], x[1][0]))
###########
###########

# ----------------------------------
# the big question
# ----------------------------------

# Adding new user ratings
# Now we need to rate some movies for the new user.
# We will put them in a new RDD and we will use the user ID 99991,
# 999992, 999993, that is not assigned in the MovieLens dataset.
###########
###########
print('---------------------------------------')
print('creating user 99999991 ...')
print('---------------------------------------')
new_user_1_ID = 99999991

# The format of each line is (userID, movieID, rating)
print('---------------------------------------')
print('adding 15 movie ratings for user 99999991 ...')
print('---------------------------------------')
new_user_1_ratings = [
    (new_user_1_ID, 33, 3),  # Wings of Courage (1995)
    (new_user_1_ID, 34, 7),  # Babe (1995)
    (new_user_1_ID, 35, 8),  # Carrington (1995)
    (new_user_1_ID, 36, 3),  # Dead Man Walking (1995)
    (new_user_1_ID, 37, 5),  # Across the Sea of Time (1995)
    (new_user_1_ID, 38, 9),  # It Takes Two (1995)
    (new_user_1_ID, 39, 3),  # Clueless (1995)
    (new_user_1_ID, 40, 3),  # Cry, the Beloved Country (1995)
    (new_user_1_ID, 41, 4),  # Sinivalkoinen valhe (2012)
    (new_user_1_ID, 42, 5),  # Dead Presidents (1995)
    (new_user_1_ID, 43, 6),  # Restoration (1995)
    (new_user_1_ID, 44, 7),  # Mortal Kombat (1995)
    (new_user_1_ID, 45, 8),  # To Die For (1995)
    (new_user_1_ID, 46, 9),  # How to Make an American Quilt (1995)
    (new_user_1_ID, 47, 1)   # Seven (a.k.a. Se7en) (1995)
]
new_user_1_ratings_RDD = sc.parallelize(new_user_1_ratings)
print('---------------------------------------')
print('New user ratings: %s' % new_user_1_ratings_RDD.take(15))
print('---------------------------------------')
###########
###########



###########
###########

print('---------------------------------------')
print('creating user 99999992 ...')
print('---------------------------------------')
new_user_2_ID = 99999992

# The format of each line is (userID, movieID, rating)
print('---------------------------------------')
print('adding 15 movie ratings for user 99999992 ...')
print('---------------------------------------')
new_user_2_ratings = [
    (new_user_2_ID, 16, 8),  # Casino (1995)
    (new_user_2_ID, 17, 6),  # Sense and Sensibility (1995)
    (new_user_2_ID, 18, 4),  # Four Rooms (1995)
    (new_user_2_ID, 19, 3),  # Ace Ventura: When Nature Calls (1995)
    (new_user_2_ID, 20, 2),  # Money Train (1995)
    (new_user_2_ID, 21, 4),  # Get Shorty (1995)
    (new_user_2_ID, 22, 5),  # Copycat (1995)
    (new_user_2_ID, 23, 6),  # Assassins (1995)
    (new_user_2_ID, 24, 5),  # Powder (1995)
    (new_user_2_ID, 25, 7),  # Leaving Las Vegas (1995)
    (new_user_2_ID, 26, 9),  # Othello (1995)
    (new_user_2_ID, 27, 4),  # Now and Then (1995)
    (new_user_2_ID, 28, 1),  # Persuasion (1995)
    (new_user_2_ID, 29, 6),  # City of Lost Children, The (CitÃ© des enfants perdus, La) (1995)
    (new_user_2_ID, 30, 8)   # Shanghai Triad (Yao a yao yao dao waipo qiao) (1995)
]
new_user_2_ratings_RDD = sc.parallelize(new_user_2_ratings)
print('---------------------------------------')
print('New user ratings: %s' % new_user_2_ratings_RDD.take(15))
print('---------------------------------------')
###########
###########



###########
###########
print('---------------------------------------')
print('creating user 99999993 ...')
print('---------------------------------------')
new_user_3_ID = 99999993

# The format of each line is (userID, movieID, rating)
print('---------------------------------------')
print('adding 15 movie ratings for user 99999993 ...')
print('---------------------------------------')
new_user_3_ratings = [
    (new_user_3_ID, 1, 5),  # Toy Story (1995)
    (new_user_3_ID, 2, 3),  # Jumanji (1995)
    (new_user_3_ID, 3, 4),  # Grumpier Old Men (1995)
    (new_user_3_ID, 4, 3),  # Waiting to Exhale (1995)
    (new_user_3_ID, 5, 6),  # Father of the Bride Part II (1995)
    (new_user_3_ID, 6, 7),  # Heat (1995)
    (new_user_3_ID, 7, 8),  # Sabrina (1995)
    (new_user_3_ID, 8, 9),  # Tom and Huck (1995)
    (new_user_3_ID, 9, 2),  # Sudden Death (1995)
    (new_user_3_ID, 10, 4),  # GoldenEye (1995)
    (new_user_3_ID, 11, 3),  # American President, The (1995)
    (new_user_3_ID, 12, 5),  # Dracula: Dead and Loving It (1995)
    (new_user_3_ID, 13, 6),  # Balto (1995)
    (new_user_3_ID, 14, 7),  # Nixon (1995)
    (new_user_3_ID, 15, 8)   # Cutthroat Island (1995)
]
new_user_3_ratings_RDD = sc.parallelize(new_user_3_ratings)
print('---------------------------------------')
print('New user ratings: %s' % new_user_3_ratings_RDD.take(15))
print('---------------------------------------')
###########
###########




#user 1--------------------------------------------------------------------------------------------





# Now we add them to the data we will use to train our recommender model.
# We use Spark's union() transformation for this.
###########
###########
print('---------------------------------------')
print("adding user 99999991's rated movies to train the recommender model...")
print('---------------------------------------')
complete_data_1_with_new_ratings_RDD = complete_ratings_data.union(new_user_1_ratings_RDD)
###########
###########


# And finally we
# -----train-----
# the ALS model using all the parameters we selected before ( i.e. when using the small dataset).
###########
###########
print('---------------------------------------')
print('training the ALS model using all the parameters selected in the small dataset...')
print('---------------------------------------')
from time import time

t0 = time()
new_ratings_1_model = ALS.train(complete_data_1_with_new_ratings_RDD, best_rank, seed=seed,
                              iterations=iterations, lambda_=regularization_parameter)
tt = time() - t0

print('---------------------------------------')
print("New model trained in %s seconds" % round(tt, 3))
print('---------------------------------------')
# It took some time. We will need to repeat that every time a user
# adds new ratings. Ideally we will do this in batches, and not for every
# single rating that comes into the system for every user.
###########
###########

# Getting top recommendations
# Let's now get some recommendations! For that we will get an
# RDD with all the movies the new user hasn't rated yet. We will join them together with the model to predict ratings.
###########
###########
print('---------------------------------------')
print('Recommendation time !!! ')
print('---------------------------------------')
print('---------------------------------------')
print('Getting all the RDD with all the movies user 99999991 has not rated yet ...')

new_user_1_ratings_ids = map(lambda x: x[1], new_user_1_ratings)  # get just movie IDs
# keep just those not on the ID list
new_user_1_unrated_movies_RDD = (
    complete_movies_data.filter(lambda x: x[0] not in new_user_1_ratings_ids).map(lambda x: (new_user_1_ID, x[0])))
###########
###########


# Use the input RDD, new_user_unrated_movies_RDD, with new_ratings_
# model.predictAll() to predict new ratings for the movies
###########
###########
print('---------------------------------------')
print('Using the input RDD of unrated movies for user 99999991 and input RDD ')
print('to predict new ratings for the movies user 99999991 rated... ')

new_user_1_recommendations_RDD = new_ratings_1_model.predictAll(new_user_1_unrated_movies_RDD)

###########
###########


# We have our recommendations ready. Now we can print out the 15
# movies with the highest predicted ratings. And join them with the movies
# RDD to get the titles, and ratings count in order to get movies with a minimum number of counts.

# First we will do the join and see what the result looks like.


# Transform new_user_recommendations_RDD into pairs of the form (Movie ID, Predicted Rating)
###########
###########
print('---------------------------------------')
print('Transforming new_user_1_recommendations_RDD into ')
print('pairs of the form (Movie ID, Predicted Rating...')
print('---------------------------------------')
new_user_1_recommendations_rating_RDD = new_user_1_recommendations_RDD.map(lambda x: (x.product, x.rating))
new_user_1_recommendations_rating_title_and_count_RDD = \
    new_user_1_recommendations_rating_RDD.join(complete_movies_titles).join(movie_rating_counts_RDD)
new_user_1_recommendations_rating_title_and_count_RDD.take(3)
###########
###########


# So we need to flaten this down a bit in order to have (Title, Rating, Ratings Count).
###########
###########
print('---------------------------------------')
print(' (user: 99991) flattening the transformation down ')
print('a bit in order to have (Title, Rating, Ratings Count) ...')

new_user_1_recommendations_rating_title_and_count_RDD = \
    new_user_1_recommendations_rating_title_and_count_RDD.map(lambda r: (r[1][0][1], r[1][0][0], r[1][1]))
###########
###########


# Finally, get the highest rated recommendations for the new user (99999991),
# filtering out movies with less than 15 ratings.
###########
###########
print('---------------------------------------')
print("getting the highest rated recommendations for user (user: 99999991), ")
print('filtering out movies with less than 15 ratings ...')

top_movies_1 = new_user_1_recommendations_rating_title_and_count_RDD.filter(lambda r: r[2] >= 15).takeOrdered(15, key=lambda
    x: -x[1])


print('collecting top recommended movies of user 1 (with more than 15 reviews):\n%s' %
      '\n'.join(map(str, top_movies_1)))

###########
###########



#user 2--------------------------------------------------------------------------------------------






# Now we add them to the data we will use to train our recommender model.
# We use Spark's union() transformation for this.
###########
###########
print('---------------------------------------')
print("adding user 99999992's rated movies to train the recommender model...")
print('---------------------------------------')
complete_data_2_with_new_ratings_RDD = complete_ratings_data.union(new_user_2_ratings_RDD)
###########
###########




# And finally we
# -----train-----
# the ALS model using all the parameters we selected before ( i.e. when using the small dataset).
###########
###########
print('---------------------------------------')
print('training the ALS model using all the parameters selected in the small dataset...')
print('---------------------------------------')
from time import time

t0 = time()
new_ratings_2_model = ALS.train(complete_data_2_with_new_ratings_RDD, best_rank, seed=seed,
                                iterations=iterations, lambda_=regularization_parameter)
tt = time() - t0

print('---------------------------------------')
print("New model trained in %s seconds" % round(tt, 3))
print('---------------------------------------')
# It took some time. We will need to repeat that every time a user
# adds new ratings. Ideally we will do this in batches, and not for every
# single rating that comes into the system for every user.
###########
###########



# Getting top recommendations
# Let's now get some recommendations! For that we will get an RDD with
# all the movies the new user hasn't rated yet. We will join them together with the model to predict ratings.
###########
###########


print('Getting all the RDD with all the movies user 99999992 has not rated yet ...')

new_user_2_ratings_ids = map(lambda x: x[1], new_user_2_ratings)  # get just movie IDs
# keep just those not on the ID list
new_user_2_unrated_movies_RDD = (
    complete_movies_data.filter(lambda x: x[0] not in new_user_2_ratings_ids).map(lambda x: (new_user_2_ID, x[0])))
###########
###########






# Use the input RDD, new_user_unrated_movies_RDD, with new_
# ratings_model.predictAll() to predict new ratings for the movies
###########
###########

print('Using the input RDD of unrated movies for user 99999992 and input RDD ')
print('to predict new ratings for the movies user 99999992 rated... ')
new_user_2_recommendations_RDD = new_ratings_2_model.predictAll(new_user_2_unrated_movies_RDD)

###########
###########


# Transform new_user_recommendations_RDD into pairs of the form (Movie ID, Predicted Rating)
###########
###########
print('---------------------------------------')
print('Transforming new_user_2_recommendations_RDD into ')
print('pairs of the form (Movie ID, Predicted Rating...')
print('---------------------------------------')
new_user_2_recommendations_rating_RDD = new_user_2_recommendations_RDD.map(lambda x: (x.product, x.rating))
new_user_2_recommendations_rating_title_and_count_RDD = \
    new_user_2_recommendations_rating_RDD.join(complete_movies_titles).join(movie_rating_counts_RDD)
new_user_2_recommendations_rating_title_and_count_RDD.take(3)
###########
###########

# So we need to flaten this down a bit in order to have (Title, Rating, Ratings Count).
###########
###########
print(' (user: 99992) flattening the transformation down ')
print('a bit in order to have (Title, Rating, Ratings Count) ...')
new_user_2_recommendations_rating_title_and_count_RDD = \
    new_user_2_recommendations_rating_title_and_count_RDD.map(lambda r: (r[1][0][1], r[1][0][0], r[1][1]))
###########
###########

# Finally, get the highest rated recommendations for the new user (99999992),
# filtering out movies with less than 15 ratings.
###########
###########

print("get the highest rated recommendations for user (user: 99999992), ")
print('filtering out movies with less than 15 ratings ...')

top_movies_2 = new_user_2_recommendations_rating_title_and_count_RDD.filter(lambda r: r[2] >= 15).takeOrdered(15, key=lambda
    x: -x[1])


print('collecting top recommended movies of user 2 (with more than 15 reviews):\n%s' %
      '\n'.join(map(str, top_movies_2)))

###########
###########





#user 3--------------------------------------------------------------------------------------------






# Now we add them to the data we will use to train our recommender
# model. We use Spark's union() transformation for this.
###########
###########
print('---------------------------------------')
print("adding user 99999993's rated movies to train the recommender model...")
print('---------------------------------------')
complete_data_3_with_new_ratings_RDD = complete_ratings_data.union(new_user_3_ratings_RDD)
###########
###########



# And finally we
# -----train-----
# the ALS model using all the parameters we selected before ( i.e. when using the small dataset).
###########
###########
print('---------------------------------------')
print('training the ALS model using all the parameters selected in the small dataset...')
print('---------------------------------------')
from time import time

t0 = time()
new_ratings_3_model = ALS.train(complete_data_3_with_new_ratings_RDD, best_rank, seed=seed,
                                iterations=iterations, lambda_=regularization_parameter)
tt = time() - t0

print('---------------------------------------')
print("New model trained in %s seconds" % round(tt, 3))
print('---------------------------------------')
# It took some time. We will need to repeat that every time a user
# adds new ratings. Ideally we will do this in batches, and not for every
# single rating that comes into the system for every user.
###########
###########




# Getting top recommendations
# Let's now get some recommendations! For that we will get an
# RDD with all the movies the new user hasn't rated yet. We will join them together with the model to predict ratings.
###########
###########


print('Getting all the RDD with all the movies user 99999993 has not rated yet ...')
print('---------------------------------------')
new_user_3_ratings_ids = map(lambda x: x[1], new_user_3_ratings)  # get just movie IDs
# keep just those not on the ID list
new_user_3_unrated_movies_RDD = (
    complete_movies_data.filter(lambda x: x[0] not in new_user_3_ratings_ids).map(lambda x: (new_user_3_ID, x[0])))
###########
###########




# Use the input RDD, new_user_unrated_movies_RDD, with new_ratings_
# model.predictAll() to predict new ratings for the movies
###########
###########
print('Using the input RDD of unrated movies for user 99999993 and input RDD ')
print('to predict new ratings for the movies user 99999993 rated... ')
new_user_3_recommendations_RDD = new_ratings_3_model.predictAll(new_user_3_unrated_movies_RDD)
print('---------------------------------------')
###########
###########



# Transform new_user_recommendations_RDD into pairs of the form (Movie ID, Predicted Rating)
###########
###########
print('---------------------------------------')
print('Transforming new_user_3_recommendations_RDD into ')
print('pairs of the form (Movie ID, Predicted Rating...')
print('---------------------------------------')
new_user_3_recommendations_rating_RDD = new_user_3_recommendations_RDD.map(lambda x: (x.product, x.rating))
new_user_3_recommendations_rating_title_and_count_RDD = \
    new_user_3_recommendations_rating_RDD.join(complete_movies_titles).join(movie_rating_counts_RDD)
new_user_3_recommendations_rating_title_and_count_RDD.take(3)
###########
###########


# So we need to flaten this down a bit in order to have (Title, Rating, Ratings Count).
###########
###########
print(' (user: 99993) flattening the transformation down ')
print('a bit in order to have (Title, Rating, Ratings Count) ...')
print('---------------------------------------')
new_user_3_recommendations_rating_title_and_count_RDD = \
    new_user_3_recommendations_rating_title_and_count_RDD.map(lambda r: (r[1][0][1], r[1][0][0], r[1][1]))
###########
###########



# Finally, get the highest rated recommendations for the new user (99999993),
# filtering out movies with less than 15 ratings.
###########
###########

print("get the highest rated recommendations for user (user: 99999993), ")
print('filtering out movies with less than 15 ratings ...')

top_movies_3 = new_user_3_recommendations_rating_title_and_count_RDD.filter(lambda r: r[2] >= 15).takeOrdered(15, key=lambda
    x: -x[1])


print('collecting top recommended movies of user 3 (with more than 15 reviews):\n%s' %
      '\n'.join(map(str, top_movies_3)))
print('---------------------------------------')
###########
###########


















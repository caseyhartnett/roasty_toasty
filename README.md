# Roasty Toasty

This project was not possible in the end with data available on roastme and toastme at the moment. Could not find enough similar roasts or toasts to perform Deep Learning on the images. Will consider other possible projects associated but currently dead. 

### Goals:

1. Extract images and text from the RoastMe and ToastMe subreddits.
2. Develop a machine learning model to perform automatic roasts or toasts.

### File Structure

```
├── Pipfile // Dependencies for python
├── Pipfile.lock
├── README.md // Markdown documentation
├── dvc // Store dvc files for data version controled pipeline
├── data  // Data and images scraped
|   ├── images // Storage of submission image
|   |      ├── roastme // roastme subreddit post images
|   |      ├── toastme // toastme subreddit post images
|   ├── queries // SQL queries in *.sql files to retrieve data from database
|   └── *.py // source code for use in this project
├── src 
|   └── *.py // source code for use in this project
```


### Collect Data

Starting with two data collection steps of 5000 each from RoastMe and ToastMe subreddits. 

TODO: Once finalize run for 5000 using just 5 to test.

###### RoastMe Data

```
dvc run -f dvc/collect_roastme.dvc \
        -d src/scrape.py \
        --outs-persist data/images/roastme -o data/top_posts_roastme.csv \
        python src/scrape.py roastme 5
```

###### ToastMe Data

```
dvc run -f dvc/collect_toastme.dvc \
        -d src/scrape.py \
        --outs-persist data/images/toastme -o data/top_posts_toastme.csv \
        python src/scrape.py toastme 5
```

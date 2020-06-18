# Roasty Toasty

### Goals:

1. Extract images and text from the RoastMe and ToastMe subreddits.
2. Develop a machine learning model to perform automatic roasts or toasts.

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
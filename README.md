# FIXME

  *Add website URL in couple places below.
  *

# Anime Text Analytics
  
  This is a Course Project for UIUC CS 410: Text Information Systems (Fall 2020).
  
  To view the output of this project, please visit <<.<INSERT URL HERE, AND BELOW>.>>

## Team
  
  *Produced by Team Nani (何 !?)*:
  * Karan Bokil [@bokilenator](https://github.com/bokilenator)
  * Mihir Yerande [@mihiryerande](https://github.com/mihiryerande)

## Explanation
  
  Anime shows are already categorized into various genres, such as *Shо̄nen* or *Mecha*, for example.
  
  This project attempts to use the **Latent Dirichlet Allocation** (LDA) algorithm to determine such genres from text data.
  
  Given some input text data, LDA works by training a model on text data to obtain *topics* and *topic coverages*.
  
  We use text data, scraped and cleaned, from *myanimelist.com*, where there are short synopses of anime shows.
  
  The *topics* produced by our LDA model are referred to as *LDA genres*.
  
  Each genre is a probabilistic distribution over words, which would ideally reflect a genre understandable to humans.
  
  In addition, each anime show can be assigned a *topic coverage* (i.e. *genre breakdown*).
  
  For example, we might determine that a show is 71% *Shо̄nen* and 29% *Mecha*.

## Website
  
  The output of the project has been published to a website, which can be found here: <<<INSERT URL HERE,>>>

# Implementation
  
  This section steps through the implementation of the project from start to finish.

## Scraper
  
  The raw text data is scraped from *myanimelist.net*, specifically from the list beginning [here](https://myanimelist.net/topanime.php?type=tv).
  
  The output has already been written to [*scraped.jl*](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/source_code/scraper/scraped.jl).
  
  The scraper is implemented in Python using the *scrapy* framework.
  See [*animespider.py*](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/source_code/scraper/animespider.py).
  
  To run the scraper, navigate to the containing directory, and run the following command:
  ```
  scrapy runspider animespider.py -o scraped.jl
  ```
  
  The spider's log will automatically write to *spider_log.txt*, in the same directory.

## LDA Input
  
  In order to run LDA, the raw text must be tokenized and cleaned.
  
  The output of this step has already been written to [*lda_input.jl*](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/source_code/lda_input/lda_input.jl).
  
  See [*write_lda_input.py*](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/source_code/lda_input/write_lda_input.py) for the implementation.
  
  To run the text cleaning, navigate to the containing directory, and run the following command:
  ```
  python write_lda_input.py
  ```
  
  Print-out should appear in the console as each show's raw text is cleaned.
  
## LDA Model
  
  After cleaning the raw text, we can now train our LDA model.
  
  The trained LDA model has already been saved to [*lda_model*](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/source_code/lda_model/).
  
  See [*write_lda_model.ipynb*](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/source_code/write_lda_model.ipynb) for further explanation.

## LDA Output
  
  After training the LDA model, we can obtain the desired output about *genres*.
  
  The output of this step has already been written to [*lda_output*](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/source_code/lda_output/).
  
  See [*write_lda_output.ipynb*](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/source_code/write_lda_output.ipynb) for further explanation.

## LDA Distances
  
  After obtaining the genre-breakdowns, we can determine similarity between anime shows based on their respective breakdowns.
  
  We use the Hellinger distance utilities provided in *gensim*, as described [here](https://radimrehurek.com/gensim_3.8.3/auto_examples/tutorials/run_distance_metrics.html#hellinger).
  
  As this step produces very large files, the **output has not been stored** here.
  
  See [*write_lda_distance.ipynb*](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/source_code/write_lda_distance.ipynb) for further explanation.

# Q-RAN STUFF

Website / Database stuff.

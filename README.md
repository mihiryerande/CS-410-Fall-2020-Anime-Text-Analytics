# FIXME

  *Add website URL in couple places below.
  *

# Anime Text Analytics
  
  This is a Course Project for UIUC CS 410: Text Information Systems (Fall 2020).
  
  To view the output of this project, please visit <<.<INSERT URL HERE, AND BELOW>.>>

## Team
  
  *Produced by Team Nani (何 !?)*:
  * Karan Bokil (karanb2) [@bokilenator](https://github.com/bokilenator)
  * Mihir Yerande (yerande2) [@mihiryerande](https://github.com/mihiryerande)

## Explanation
  
  Anime shows are categorized into various genres, such as *Shо̄nen* or *Mecha*, for example.
  
  This project attempts to use the **Latent Dirichlet Allocation** (LDA) algorithm to determine such genres from text data.
  
  LDA works by training a model on input text data to obtain *topics* and *topic coverages*.
  
  We use text data, scraped and cleaned, from *myanimelist.com*, where there are short synopses of anime shows.
  
  The *topics* produced by our LDA model are referred to as *LDA genres*.
  
  Each genre is a probabilistic distribution over words, which would ideally reflect a genre understandable to humans.
  
  In addition, each anime show can be assigned a *topic coverage* (i.e. *genre breakdown*).
  
  For example, we might determine that a show is 71% *Shо̄nen* and 29% *Mecha*.

## Website
  
  The output of the project has been published to a website, which can be found here: <<<INSERT URL HERE,>>>

# LDA Implementation
  
  This section steps through the implementation of the project from start to finish.
  
  The LDA code and output is all stored in the [*source_code*](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/tree/main/source_code) directory.

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
  
  The output of this step has already been written to [*lda_distance*](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/source_code/lda_distance/).
  
  See [*write_lda_distance.ipynb*](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/source_code/write_lda_distance.ipynb) for further explanation.

## Database
Due to the size of our dataset, we did not feel processing Just in Time from a website performance perspective would be good.  Thus, we preprocessed most of the data from the aforementioned steps and converted into a relational database for easy access by the web framework.
After attempting to utilize [Azure CosmosDB](https://azure.microsoft.com/en-us/free/cosmos-db/search/?OCID=AID2100131_SEM_6db6c4e0b89d1beae54c9b3675385867:G:s&ef_id=6db6c4e0b89d1beae54c9b3675385867:G:s&msclkid=6db6c4e0b89d1beae54c9b3675385867 "Azure CosmosDB") as well as [Azure SQL](https://azure.microsoft.com/en-us/free/sql-database/search/?OCID=AID2100131_SEM_dde51af6bf4d19b47106452072f042e0:G:s&ef_id=dde51af6bf4d19b47106452072f042e0:G:s&msclkid=dde51af6bf4d19b47106452072f042e0 "Azure SQL"), we ended up choosing to go with a [SQLite](https://sqlite.org/index.html "SQLite") database because it is light, easy to iterate testing on, and can easily be included as part of the repo, being only 5MB and self contained.
Our attempts at using CosmosDB and Azure SQL were hindered by slow upload times, as we had to parse from json and upload around 50,000 records, which would have taken several hours. The Azure Stack would have provided us some ecosystem advantages such as use of their BM25 ranking solution, [Azure Cognitive Search](https://azure.microsoft.com/en-us/services/search/?OCID=AID2100131_SEM_d7b98289b8b81cfe7fe8dd5f75c5bec1:G:s&ef_id=d7b98289b8b81cfe7fe8dd5f75c5bec1:G:s&msclkid=d7b98289b8b81cfe7fe8dd5f75c5bec1 "Azure Cognitive Search"), but nevertheless, we were able to find a different avenue for full text search.
The database can be initialized simply by running `python init.py` from the root of the repo.  This file will delete the former tables, create the new tables, parse the JSON and populate the Database alongside the relationships between the various tables.

## Text Retreival Model
After researching different libraries for text retrieval models, we settled on utilizing the [MSearch](https://github.com/honmaple/flask-msearch "MSearch") library, as it has the most integrated support with our web framework Flask.  MSearch serves as a wrapper around [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html "Whoosh"), a pure Python search engine library that capitalizes on [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25 "Okapi BM25") ranking function. Within [app.py](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/app.py "`app.py`"), we have marked fields in the various tables with `__searchable__` and created a custom route and view to collect and see the results of a query. The search thus exceeds the utility of normal database queries, facilitating results across different tables with ranking.  The inverted index is created during the data population phase in [init.py](https://github.com/mihiryerande/CS-410-Fall-2020-Anime-Text-Analytics/blob/main/init.py "init.py").

## Web Development and Hosting
The website is made using [Flask](https://flask.palletsprojects.com/en/1.1.x/ "Flask"), a lightweight web framework in Python.  It utilizes a standard MVC architecture and communicates cleanly with the Database via [SQLAlchemy](https://www.sqlalchemy.org/ "SQLAlchemy").  The site is hosted and deployed on Microsoft Azure using [Azure Web Apps](https://azure.microsoft.com/en-us/services/app-service/web/ "Azure Web Apps").  The frontend Javascript and CSS components is all developed utilizing the [Materialize](https://materializecss.com/ "Materialize") framework.
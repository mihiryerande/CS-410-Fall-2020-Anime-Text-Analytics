# FIXME

Add website URL in couple places below.

# Animé Text Analytics

To view the output of this project, please visit <<<INSERT URL HERE, AND BELOW>.>>
  
## Information

This is a Course Project for UIUC CS 410: Text Information Systems (Fall 2020).

*Produced by "Team Nani (何 !?)"*:
* Karan Bokil [@kabokil](https://github.com/bokilenator)
* Mihir Yerande [@mihiryerande](https://github.com/mihiryerande)

@github/bokilenator

### Intuition

Animé shows are already categorized into various genres, such as *Shо̄nen* or *Mecha*, for example.

This project attempts to use the **Latent Dirichlet Allocation** (LDA) algorithm to determine such genres from text data.

Given some input text data, LDA works by training a model on text data to obtain *topics* and *topic coverages*.

We use text data, scraped and cleaned, from *myanimelist.com*, where short synopses of animé shows can be found.

The *topics* produced by our LDA model are referred to as *LDA genres*.

Each genre is a probabilistic distribution over words, which would ideally reflect a genre understandable to humans.

In addition, each animé show can be assigned a *topic coverage* (i.e. *genre breakdown*), so we might say a show is 71% *Shо̄nen* and 29% *Mecha*, for example.

### Website

The output of the project has been published to a website, which can be found here: <<<INSERT URL HERE>>>

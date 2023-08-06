# Skeptic

A library for easy usage of predictive-power based statistics.

## Why use predictive power statistics ?

Predictive power based statistics are [arguably] better for modeling reality as well as more intuitive for certain problems.

When faced with high-dimensionality non-linear problems (e.g. correlation of a set of FMRIs with the presence and severity of brain cancer), "standard" statistical tests can't be used. However, this doesn't mean we can't say anything statistically significant about the above data, it just means we need to use more advanced methods, currently dubbed under machine learning, to find the correlation and assign a p-value to our finding being non-random.

When the validity of scientific claims must be explained to a mathematically layman audience, things like the T-test aren't necessarily intuitive to grasp, and make some heavy-handed assumptions about the data. Arguably, at least for some types of problems, predictive power based conclusions are much more intuitive to grasp.

## Functionality (why you should use this library)

This library attempts to provide said predictive power based statistics and in the process tries to abstract away a few things:

1. The process of finding the "best possible model" for a problem, given the amount of compute the researcher has on hand.
2. The process of efficient k-fold cross validation using said predictive model.
3. The process of finding an calculating meaningful errors/accuracy functions based on which to yield a predictive-power correlation (partially abstracted away)
4. The process of cleaning data (e.g. going from a csv file to a pandas dataframe with the correct types assigned to each column), in part.
5. Computing a "p value" analog based on the data and (optionally) input from the researcher about the statistical significance test they would normally attempt to use with the dataset.

Various other things that I might add if I find the time and there's some interest in the project:
* Embedding based techniques for deconfounding
* Operating under assumptions about the global distribution
* Operating under assumptions about the "expected" shape of the sample distribution
* ???

## Roadmap

Roadmap for the feature from the heading above

1 -- WIP - prototype done
2 -- WIP - prototype done
3 -- WIP - prototype done
4 -- WIP - prototype done
5 -- Not started yet

## Why make this library

Because every alternative for this on the market seems to be:
* Mixing in too many classic statistic assumptions, thus making the tool wider-reaching but diluting it's usefulness for the cases when predictive power is potentially superior.
* A complex and convoluted mess.
* Closed source and sometimes paid-for.
* Too kosher in the machine learning model being used, yielding less than ideal results.

## How to use this library

The documentation is not ready yet, but please see [the integration tests](tests/integration) for some examples of usage.

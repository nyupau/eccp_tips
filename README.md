# Tips for Custom Cloud Models with ECCP

This repo is intended to provide tips and Python code snippets to do various things inside Epic's Cognitive Computing Platform (ECCP). 

The [example_model.py](https://github.com/nyupau/eccp_tips/blob/master/example_model.py) includes several optional modifications to the base template you can download from Epic's Galaxy.
Notably:
* Flipping of scores for consistency with other scores where high score = red = bad vs. low score = green = good. 
  * This is simply a substraction from 100, see [line 36](https://github.com/nyupau/eccp_tips/blob/master/example_model.py#L36) for the score and [line 45](https://github.com/nyupau/eccp_tips/blob/master/example_model.py#L45) for the contributions
* Limiting the output from python to the top nine (or n) contributing features to aid explanation to users. 
  * This is relevant because Epic only shows the largest contributing features (note that small valued positive contributions are greater than very large but negative ones) and a maximum of nine factors.
  * We limit the output by arranging contributions by absolute magnitude, leaving the top nine and zeroing out the remainder, see [line 66](https://github.com/nyupau/eccp_tips/blob/master/example_model.py#L66). Epic does not display variables with zero contibution and they do not clutter the hover bubble. 
* Adding a "Missing data" placeholder when any piece of data is missing and a score cannot be created.
  * By default, a "N/A" is shown if no score is returned from Python, the same as if the patient is ineligible. This is confusing to users.
  * We apply logic in Python to check for NAs due to missing data and either coerce (rounded) scores to string outputs or return "Missing data" if applicable. See [line 33](https://github.com/nyupau/eccp_tips/blob/master/example_model.py#L33)
* Enabling a randomized controlled trial by replacing scores by a "Hidden" placeholder when allocated to the control group.
  * By passing a patient identifier as a variable into Python, we can coerce that ID into two 50:50 groups for example.
  * See [line 79](https://github.com/nyupau/eccp_tips/blob/master/example_model.py#L79) for a function that should work for MRN, CSN, Patient ID, or Enterprise ID. 

Note that the latter two require an adaptation in the epic parcel code to **not** coerce returned scores to floats (as "Missing data" or "Hidden" would become NAs).

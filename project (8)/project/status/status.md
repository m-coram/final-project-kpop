# Status Report

#### Your name

Megan Coram

#### Your section leader's name

Phyllis Zhang

#### Project title

K-pop Album Guide

***

Short answers for the below questions suffice. If you want to alter your plan for your project (and obtain approval for the same), be sure to email your section leader directly!

#### What have you done for your project so far?

I have created the database and a basic website with functional (as far as I can tell) pages for Albums, Artists, Songs, Search, and Add.

#### What have you not done for your project yet?

I have not yet perfected the CSS of the website, and I have not yet added all the albums that I wish to.

#### What problems, if any, have you encountered?

I realized storing images in a database is a mess, so I found a website (https://postimages.org/) to turn them into urls that I can store more easily.
I ran into a temporary issue trying to use "?" or "%s" placeholders for column names with a LIKE query, but I fixed it using concatenation and string syntax.
I had issues for a while accessing the data that my SELECT statements returned until I realized it was an array of dictionaries I needed to index into.
I had a temporary issue when using titles as the variable linking albums to versions because the space characters caused premature termination, but I fixed it by using the ids instead.
I haven't tried dealing with non-ascii characters yet, and I'm going back and forth on whether to do so or not, since the Add page is already quite long.
Organizing all the inputs from the add page was difficult and required a lot of troubeshooting, especially the loops for songs and versions.
The CSS has been driving me crazy (for example, Bootstrap Media Objects reverting to top-aligned when I ordered center-aligned).
I'm still deciding what elements should be links versus plain informational text on each page because I don't want the pages to become too busy.
It is taking even longer than I expected to research all the different versions of the albums and organize all the photos.
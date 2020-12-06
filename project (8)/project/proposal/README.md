# Proposal

## What will (likely) be the title of your project?

K-pop Album Guide

## In just a sentence or two, summarize your project. (E.g., "A website that lets you buy and sell stocks.")

A website that lets you browse all the different versions of various kpop albums from various artists. There are many websites out there listing the tracklists of albums, but none I could find that help the user figure out which version is which (there are so many versions, it's absolutely crazy).

## In a paragraph or more, detail your project. What will your software do? What features will it have? How will it be executed?

My project will be a web-based application using html/flask/css/sql. It will be somewhat visually similar to my homepage pset, but with many more pages and more functionality. From the index page, users will be able to navigate to pages where they can browse artists, albums, or songs, and each of those pages will be linked to the others whenever useful. The individual album pages will be the main focus, and they will include tracklists as well as subsections for each of the different editions of the album with descriptions and photos. I am not planning to create pages about the artists, since there are plenty of websites out there that do that already. I am also planning to implement a search page where users can search artists, albums, and songs using a text box and dropdown menu. Ideally, there will also be a page where users can help to build up the database themselves because there are simply too many kpop groups out there for me to include them all in my beginning implementation. Users would submit info (artist name, album name, tracklist, and album versions with photos and descriptions, etc.) using an admittedly long form. Hopefully, I will be able to make this form responsive (for example, using a dropdown menu for artists that are already in the database, or otherwise having a text box for new input). To keep all of the information that this website needs, I will be using an SQL database with several tables: artists (id, name, cover photo), albums (id, artist_id, name, song1_id, song2_id, etc.), songs (id, artist_id, album_id), versions (id, album_id, description, photo1_id, photo2_id, etc.), and photos (id).

## If planning to combine CS50's final project with another course's final project, with which other course? And which aspect(s) of your proposed project would relate to CS50, and which aspect(s) would relate to the other course?

I am not planning to combine this project with any other.

## If planning to collaborate with 1 or 2 classmates for the final project, list their names, email addresses, and the names of their assigned TFs below.

I am not planning to collaborate with anyone.

## In the world of software, most everything takes longer to implement than you expect. And so it's not uncommon to accomplish less in a fixed amount of time than you hope.

### In a sentence (or list of features), define a GOOD outcome for your final project. I.e., what WILL you accomplish no matter what?

My baseline goal is to create a functional, aesthetically pleasing, intuitively navigatable website with a few albums for which I have put the information into the database myself.

### In a sentence (or list of features), define a BETTER outcome for your final project. I.e., what do you THINK you can accomplish before the final project's deadline?

My next goals are to have a functional search page, then to have a functional user input page, and to add more albums.

### In a sentence (or list of features), define a BEST outcome for your final project. I.e., what do you HOPE to accomplish before the final project's deadline?

Ideally, I will have a responsive user input page and a big database full of detailed listings.

## In a paragraph or more, outline your next steps. What new skills will you need to acquire? What topics will you need to research? If working with one of two classmates, who will do what?

I know most of what I need to already to implement this project thanks to the last two psets, but I will need to do some research on how to receive photo inputs, how to store photos in a database (if that's possible), and how to make interactive forms. I have a good deal of research ahead of me in terms of the albums themselves, too, since the album info isn't very centralized (which is why I'm making this website in the first place). Since the pages are going to be heavily interconnected, I'm going to need to learn how to keep track of lots of variables in between different pages and how to create complex SQL queries based on user input. I will also need to learn more about Unicode in order to be able to display the original Korean titles of the albums and songs alongside the English translations.


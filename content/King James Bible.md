---
title: King James Bible Text
draft: false
tags:
---

My [King James Text Git Repository](https://github.com/simulacra10/kjv-text)

I have a project that I am working on that if I finish it (a big if right now) will use the King James Bible. The text needs to be plain text so that it is searchable. In order to help me accomplish the goal and save a bunch of time I decided to use ChatGPT to code the scripts to clean it up and convert the text. 

[Project Gutenberg - King James Bible](https://www.gutenberg.org/cache/epub/10/pg10.txt) is where I got the original text from. 

What was interesting about using ChatGPT to do the code was how incredibly easy it made it to accomplish. I manually copied the file to a working copy and then deleted the preamble and epilogue. After that I uploaded the text in a new prompt and then asked it write a script that kept the book names and then altered the text so that everything was on a single line. 

It took about six tries, each time it would either throw an error in Python or it wouldn't do precisely what I was asking it to do. If you have ever done any type of programming, you know that on any project about half of your time is debugging. Using ChatGPT to debug made it simple. Every time Python threw an error, I just copied that error into the prompt and then told ChatGPT that the code threw the error and to fix it. And each time it politely apologized for the error and then corrected it. 

Blown away!!!

After cleaning up the text I had it transform it into a SQLite3 database. Same thing happened. A few errors, a few corrections and then presto, we have a database!

This was a lot of fun and really informative. I can see the way of the future for programming and it is AI all the way. If you break a large project down into little bits and ask it in a way that is very clear, the AI does an amazing job of getting it done.



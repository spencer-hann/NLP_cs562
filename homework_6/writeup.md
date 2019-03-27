Part 1:

To run my Part 1 code simply use `python pcfg.py`, everything is set to run in the `if __name__ == "__main__"` section. The only other conisderation is to make sure that `wsj-normalized.psd` exists in the same directory and the python script.

> spencer@rBS:~/ohsu/562/homework_6$ python pcfg.py
> TOP -> NP VP . 1.0
> NP -> DT NN 0.3333333333333333
> NP -> NN PP 0.3333333333333333
> NP -> DT NN NN 0.3333333333333333
> DT -> the 1.0
> NN -> teacher 0.25
> NN -> today 0.25
> NN -> lecture 0.25
> NN -> hall 0.25
> VP -> MD VP 0.5
> VP -> VB NP 0.5
> MD -> will 1.0
> VB -> lecture 1.0
> PP -> IN NP 1.0
> IN -> in 1.0
> . -> . 1.0
> Count number of rules in wsj-normalized.psd
> 27290
> 27290

For this problem, I took a recursive approach, as this is normally appropriate with tree data structures. The core of the problem was relatively simple, and similar to what we had already done in homework 5. What took me the most time was figuring out an efficient way to write my function so that it could take in a single tree or many. Originally, I had the function set up to take in a tree and convert it to a tree. Ultimately, I found that the simplest way was for the function to expect an actual Tree object or an iterable object of Trees (like the generator created by Tree.from_stream).
By looping through the outer dict and summing the number of entries in each inner dict in my probabalistic CFG production rules, I get the number of rules in the untransformed trees in `wsj-normalized.psd` is 27,290.

Part 2:

I tried three different versions of the CYK algorithm. All continued to have the same bug. The backpointer table would be filled with zeros/None at the end of the function, and the cyk_matrix would be mostly empty as well. I think this has something to do with the cells not being filled in the correct order, or the wrong cells being checked, but I was unable to figure out why. As best I can tell my code should follow the pseudo code in the text book, as well as the two other versions of the algorithm I found on Wikipedia and YouTube. I also checked the two dicts I use for production rules, and they seem to be working properly, so I don't think that is the issue. It seems that for some reason, a few cells are activated at the top of the function and then the table never gets updated during the inner loop, even though it should.

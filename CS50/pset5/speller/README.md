# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

Pneumonoultramicroscopicsilicovolcanoconiosis is, according to the Oxford English Dictionary, "a factitious word alleged to mean 'a lung disease caused by the inhalation of very fine silica dust, causing inflammation in the lungs." 

## According to its man page, what does `getrusage` do?

getrusage() returns resource usage measures for who, which can be one of the following:

       RUSAGE_SELF
              Return  resource usage statistics for the calling process, which is the sum of resources used by
              all threads in the process.

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Because the prototype of 'struct rusage' expects a pointer. And it is more efficient than passing by value.  

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

The main function declare 3 integers (index, misspellings and words) and an array of characters (word) with a capacity of LENGTH (define in dictionary.h). 
Then it spell-checks each word in text with 'fgetc()' function, until it gets the end of the file. 'fgetc()' gets the next character from the file and advances the position counter (index). 
If the character is an alphabetical character or apostrophes (not in the first position of the word), the character is append to the word array to compose a complete word. 
The words which are too longs or with numbers are ignored. When the character is '\0', it indicate that the word is finished. 
So, the counter words is update. The finding word is check with the dictionary. If it is not in it, the counter misspelling update by 1. 

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

Because we want to check if any character is a valid one and check every character of the word with the words in dictionnary. 

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

Declared parameters are pointers,'check' and 'load' just read those values and don't need to change these.

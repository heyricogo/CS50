# Questions

## What's `stdint.h`?

The <stdint.h> **header** shall declare sets of **integer types** having *specified widths*, 
and shall define corresponding sets of macros. 
It shall also define macros that **specify limits of integer types** corresponding to types defined in other standard headers.
[REFERENCE](http://pubs.opengroup.org/onlinepubs/009695399/basedefs/stdint.h.html)

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

The typedef name uint N _t designates an unsigned integer type with width N. 
The typedef name int N _t designates a signed integer type with width N, no padding bits, and a two's-complement representation.
Thus : 
* uint8_t denotes an unsigned integer type with a width of exactly 8 bits.
* uint32_t denotes an unsigned integer type with a width of exactly 32 bits.
* int32_t denotes a signed integer type with a width of exactly 32 bits.
* uint16_t denotes an unsigned integer type with a width of exactly 16 bits.
[REFERENCE](http://pubs.opengroup.org/onlinepubs/009695399/basedefs/stdint.h.html)

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

* BYTE is 8 bits = 1 byte
* DWORD is 32 bits = 4 bytes
* LONG is 32 bits = 4 bytes
* WORD is 16 bits = 2 bytes

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

Ox424d 

## What's the difference between `bfSize` and `biSize`?

They are both unsigned integer type of 32 bits (8 bytes), but for 2 differents *struct*.

## What does it mean if `biHeight` is negative?

If biHeight is negative, the bitmap is a top-down DIB and its origin is the upper-left corner.
[REFERENCE](https://msdn.microsoft.com/en-us/library/dd183376(v=vs.85).aspx)

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

WORD biBitCount
[REFERENCE](https://msdn.microsoft.com/en-us/library/dd183376(v=vs.85).aspx)

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If the file we are trying to open doesn't exist. 

## Why is the third argument to `fread` always `1` in our code?

Because, we want to read each element of the file, each one with a size of size bytes

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

padding = 1

## What does `fseek` do?

Sets the position indicator associated with the stream to a new position
[REFERENCE](http://www.cplusplus.com/reference/cstdio/fseek/?kw=fseek)

## What is `SEEK_CUR`?

Current position of the file pointer
[REFERENCE](http://www.cplusplus.com/reference/cstdio/fseek/?kw=fseek)
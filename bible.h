#ifndef BIBLE_H
#define BIBLE_H

typedef struct {
    char* id;
    char* text;
} BibleVerse;

extern BibleVerse bible[];
extern const int bible_length;

#endif /* BIBLE_H */
#pragma once

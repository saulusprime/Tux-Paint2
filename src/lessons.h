/*
  lessons.h

  For Tux Paint
  Drawing lessons for the "Learn" tool: reading them, and drawing their
  steps (see lessons/README.txt for the files)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
  (See COPYING.txt)

  Copyright (c) 2026 by Paolo Pierno
*/

#ifndef LESSONS_H
#define LESSONS_H

#include "SDL.h"

/* Difficulty levels: the lessons' subfolders. "custom" is for the user's
   own pictures and lessons (shown only when there are some): Tux Paint
   doesn't ship any. */
enum
{
  LESSON_EASY,
  LESSON_MEDIUM,
  LESSON_HARD,
  LESSON_CUSTOM,
  NUM_LESSON_LEVELS
};

extern const char *const lesson_level_dirs[NUM_LESSON_LEVELS];

typedef enum
{
  LESSON_STEP_DRAW,		/* lines to draw */
  LESSON_STEP_GUIDE,		/* a light helper shape, erased later */
  LESSON_STEP_COLOR,		/* an area to color */
  LESSON_STEP_ERASE,		/* erase the helper shapes (or the grid) */

  /* A plain picture's steps, to copy it with a grid (see lesson.picture) */
  LESSON_STEP_LOOK,		/* look at the picture */
  LESSON_STEP_GRID,		/* draw a light grid on the paper */
  LESSON_STEP_COPY,		/* copy it one box at a time */
  LESSON_STEP_PAINT		/* color it */
} lesson_step_kind;

typedef struct lesson_step
{
  lesson_step_kind kind;
  char *layer;			/* id of its group in the SVG; NULL for "erase" */
  char *text;			/* the instructions, in the best language found */
  char *lang;			/* that language ("en" when English) */
} lesson_step;

typedef struct lesson
{
  char *name;			/* file name, without its extension */
  char *svg_fname;		/* the drawing; for a picture, maybe a PNG or JPEG */
  int picture;			/* a plain picture (in "custom", with no steps of its own) */
  char *title;
  char *title_lang;
  int level;
  int num_steps;
  lesson_step *steps;
} lesson;

/* Whether lessons can be shown (they need librsvg 2.46 or newer) */
int lessons_supported(void);

/* All the lessons in the levels' subfolders of the folders given (later
   folders win over earlier ones for a lesson of the same level and name),
   sorted by level, number of steps and title. Texts are in the first of
   langs found (e.g. "it_IT", "it"), else in English.
   In "custom" a picture (SVG, PNG, JPEG) with no steps of its own (no
   NAME.txt, or one with just the title) becomes a lesson that copies it
   with a grid; its texts come from gettext(), in ui_lang ("en" when
   untranslated). NULL if none. */
lesson **lessons_find(const char *const *dirs, int num_dirs,
		      const char *const *langs, int num_langs, const char *ui_lang, int *num);
void lessons_free(lesson ** lessons, int num);

/* The finished picture, w x h at most, on white */
SDL_Surface *lesson_thumbnail(const lesson * l, int w, int h);


/* A lesson's steps, drawn in an area of a given size: on top a strip
   with a dot for each step (room for the title on its left), below it the
   picture on a sheet of paper, and beside it the tool to use (pencil,
   crayon of the color, eraser) */
typedef struct lesson_pics lesson_pics;

lesson_pics *lesson_pics_new(const lesson * l, int area_w, int area_h, int top_h);
void lesson_pics_free(lesson_pics * p);

/* Step `step` (0-based) when its animation is at `anim` (0 to 1; at 1 it is
   over). Before the first step (-1) and after the last one (num_steps),
   the finished picture. The surface (area_w x area_h, opaque) belongs to
   p, and changes at the next call. */
SDL_Surface *lesson_pics_frame(lesson_pics * p, int step, float anim);

/* Where the dots start (the title has to end before) */
int lesson_pics_dots_x(const lesson_pics * p);

/* The selector's tab for a level (stars on the left; its name goes from
   *text_x on) and a lesson's card, w x h, on white */
SDL_Surface *lesson_level_tab(int level, int w, int h, int selected, int *text_x);
SDL_Surface *lesson_card(int level, int w, int h, int selected);

#endif

/*
  lesson_frames.c

  Draws the "Learn" tool's pictures with Tux Paint's own src/lessons.c,
  into BMP files: no window, no Tux Paint. See README.md.

  Usage: lesson_frames LESSONS_DIR LANG OUT_DIR [WIDTH HEIGHT]

  For every lesson found: OUT_DIR/LEVEL-NAME-thumb.bmp (the selector's
  thumbnail), -intro.bmp and -final.bmp (before the first step and after
  the last one), -NN.bmp (step NN once its animation is over) and
  -NN-anim.bmp (step NN at 10% of it). Also level-L-S-tab.bmp and
  level-L-S-card.bmp, the selector's tab and card for level L, selected
  (S = 1) or not (S = 0).

  Copyright (c) 2026 by Paolo Pierno; GPL v2 or later, like Tux Paint.
*/

#include <stdio.h>
#include <stdlib.h>
#include "SDL.h"
#include "lessons.h"

static void save(SDL_Surface * s, const char *path, int free_it)
{
  if (s == NULL)
  {
    printf("  can't draw %s\n", path);
    return;
  }
  SDL_SaveBMP(s, path);
  if (free_it)
    SDL_FreeSurface(s);
}

int main(int argc, char *argv[])
{
  const char *dirs[1], *langs[1];
  lesson **lessons;
  lesson *l;
  lesson_pics *pics;
  char path[1024];
  const char *level;
  int num, i, step, w = 608, h = 424, text_x;

  if (argc != 4 && argc != 6)
  {
    fprintf(stderr, "Usage: %s LESSONS_DIR LANG OUT_DIR [WIDTH HEIGHT]\n", argv[0]);
    return 1;
  }
  if (argc == 6)
  {
    w = atoi(argv[4]);
    h = atoi(argv[5]);
  }

  dirs[0] = argv[1];
  langs[0] = argv[2];
  lessons = lessons_find(dirs, 1, langs, 1, langs[0], &num);
  printf("%d lessons\n", num);

  for (i = 0; i < num; i++)
  {
    l = lessons[i];
    level = lesson_level_dirs[l->level];
    printf("%s/%s: \"%s\" (%s), %d steps\n", level, l->name, l->title, l->title_lang,
	   l->num_steps);

    snprintf(path, sizeof(path), "%s/%s-%s-thumb.bmp", argv[3], level, l->name);
    save(lesson_thumbnail(l, 180, 135), path, 1);

    pics = lesson_pics_new(l, w, h, h / 13);
    if (pics == NULL)
    {
      printf("  can't draw it\n");
      continue;
    }

    for (step = -1; step <= l->num_steps; step++)
    {
      if (step < 0 || step == l->num_steps)
      {
	snprintf(path, sizeof(path), "%s/%s-%s-%s.bmp", argv[3], level, l->name,
		 step < 0 ? "intro" : "final");
	save(lesson_pics_frame(pics, step, 1.0), path, 0);
	continue;
      }

      printf("  %d. [%s] %s\n", step + 1, l->steps[step].lang, l->steps[step].text);

      snprintf(path, sizeof(path), "%s/%s-%s-%02d.bmp", argv[3], level, l->name, step + 1);
      save(lesson_pics_frame(pics, step, 1.0), path, 0);

      snprintf(path, sizeof(path), "%s/%s-%s-%02d-anim.bmp", argv[3], level, l->name, step + 1);
      save(lesson_pics_frame(pics, step, 0.1), path, 0);
    }

    lesson_pics_free(pics);
  }

  for (i = 0; i < NUM_LESSON_LEVELS * 2; i++)
  {
    snprintf(path, sizeof(path), "%s/level-%d-%d-tab.bmp", argv[3], i / 2, i % 2);
    save(lesson_level_tab(i / 2, 200, 36, i % 2, &text_x), path, 1);

    snprintf(path, sizeof(path), "%s/level-%d-%d-card.bmp", argv[3], i / 2, i % 2);
    save(lesson_card(i / 2, 200, 150, i % 2), path, 1);
  }

  lessons_free(lessons, num);
  return 0;
}

/*
  lessons.c

  For Tux Paint
  Drawing lessons for the "Learn" tool: see lessons.h, and
  lessons/README.txt for the files

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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <math.h>

#ifdef WIN32
#include "win32_dirent.h"
#else
#include <dirent.h>
#endif

#include "SDL.h"
#include "SDL_image.h"
#include "lessons.h"

#include <libintl.h>
#ifndef gettext_noop
#define gettext_noop(String) String
#endif

#if !defined(NOSVG) && !defined(OLD_SVG)
#include <librsvg/rsvg.h>
#if LIBRSVG_CHECK_VERSION(2, 46, 0)
#define LESSONS_OK
#endif
#endif

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

const char *const lesson_level_dirs[NUM_LESSON_LEVELS] = {
  "easy", "medium", "hard", "custom"
};

/* The steps of a plain picture of the user's (in "custom"), to copy it on
   paper with a grid */
static const struct
{
  lesson_step_kind kind;
  const char *text;
} picture_steps[] = {
  /* Learn dialog: first step to copy a picture of the user's own */
  {LESSON_STEP_LOOK, gettext_noop("Look carefully at the picture: we are going to copy it on paper.")},
  /* Learn dialog: second step to copy a picture (a 3 by 3 grid is shown on it) */
  {LESSON_STEP_GRID, gettext_noop("With a light pencil, divide your paper into nine boxes: draw two lines down and two lines across, like on the picture.")},
  /* Learn dialog: third step to copy a picture */
  {LESSON_STEP_COPY, gettext_noop("Copy the drawing one box at a time: in each box of your paper, draw what you see in the same box of the picture.")},
  /* Learn dialog: fourth step to copy a picture */
  {LESSON_STEP_ERASE, gettext_noop("Now erase the light lines of the grid with the eraser.")},
  /* Learn dialog: last step to copy a picture */
  {LESSON_STEP_PAINT, gettext_noop("Color your drawing: like the picture, or with the colors you like best!")}
};

#define NUM_PICTURE_STEPS (int) (sizeof(picture_steps) / sizeof(picture_steps[0]))

#define LINE_LEN 2048


/* --- Reading a lesson --- */

/* A block of lines (the file's blocks are separated by empty lines) */
typedef struct block
{
  int num;
  char **lines;
} block;

static void free_blocks(block * blocks, int num)
{
  int i, j;

  for (i = 0; i < num; i++)
  {
    for (j = 0; j < blocks[i].num; j++)
      free(blocks[i].lines[j]);
    free(blocks[i].lines);
  }
  free(blocks);
}

/* The file's blocks, without comments; NULL if it can't be read */
static block *read_blocks(const char *fname, int *num)
{
  FILE *fi;
  char buf[LINE_LEN];
  block *blocks = NULL, *bigger;
  char **lines;
  size_t len;
  int in_block = 0, first = 1;
  char *line;

  *num = 0;

  fi = fopen(fname, "r");
  if (fi == NULL)
    return NULL;

  while (fgets(buf, sizeof(buf), fi) != NULL)
  {
    line = buf;

    /* (A UTF-8 byte order mark) */
    if (first && memcmp(line, "\xef\xbb\xbf", 3) == 0)
      line += 3;
    first = 0;

    len = strlen(line);
    while (len > 0 && isspace((unsigned char) line[len - 1]))
      line[--len] = '\0';

    if (line[0] == '#')
      continue;

    if (len == 0)
    {
      in_block = 0;
      continue;
    }

    if (!in_block)
    {
      bigger = realloc(blocks, sizeof(block) * (*num + 1));
      if (bigger == NULL)
	break;
      blocks = bigger;
      blocks[*num].num = 0;
      blocks[*num].lines = NULL;
      (*num)++;
      in_block = 1;
    }

    lines = realloc(blocks[*num - 1].lines, sizeof(char *) * (blocks[*num - 1].num + 1));
    if (lines == NULL)
      break;
    blocks[*num - 1].lines = lines;
    lines[blocks[*num - 1].num] = strdup(line);
    if (lines[blocks[*num - 1].num] == NULL)
      break;
    blocks[*num - 1].num++;
  }

  fclose(fi);
  return blocks;
}

/* If the line is a translation ("it.utf8=Testo", "pt_BR=Texto"), the
   length of its language code; else 0 */
static size_t translation_lang_len(const char *line)
{
  size_t n = 0;

  while (isalnum((unsigned char) line[n]) || line[n] == '_' || line[n] == '@')
    n++;

  if (n == 0)
    return 0;
  if (strncasecmp(line + n, ".utf8=", 6) == 0 || strncasecmp(line + n, ".utf-8=", 7) == 0 ||
      line[n] == '=')
    return n;

  return 0;
}

/* Whether the line is a translation into `want` ("pt_BR"), or, if loose,
   into its language alone ("pt"); an empty one doesn't count */
static int translation_is(const char *line, const char *want, int loose)
{
  size_t n = translation_lang_len(line), want_n = strlen(want);
  const char *cut;

  if (n == 0 || strchr(line, '=')[1] == '\0')
    return 0;

  if (loose)
  {
    cut = strpbrk(want, "_@.");
    if (cut == NULL)
      return 0;			/* (Nothing looser than the exact match) */
    want_n = cut - want;
  }

  return n == want_n && strncasecmp(line, want, n) == 0;
}

/* The block's text (from line `from` on: English first, then the
   translations) in the best of the languages wanted */
static int pick_text(const block * b, int from, const char *const *langs, int num_langs,
		     char **text, char **lang)
{
  int best = -1, i, k, loose;
  size_t n;

  *text = *lang = NULL;
  if (b->num <= from)
    return 0;

  for (loose = 0; loose <= 1 && best < 0; loose++)
    for (k = 0; k < num_langs && best < 0; k++)
      for (i = from + 1; i < b->num && best < 0; i++)
	if (translation_is(b->lines[i], langs[k], loose))
	  best = i;

  if (best < 0)
  {
    *text = strdup(b->lines[from]);
    *lang = strdup("en");
  }
  else
  {
    n = translation_lang_len(b->lines[best]);
    *text = strdup(strchr(b->lines[best], '=') + 1);
    *lang = malloc(n + 1);
    if (*lang != NULL)
    {
      memcpy(*lang, b->lines[best], n);
      (*lang)[n] = '\0';
    }
  }

  if (*text == NULL || *lang == NULL)
  {
    free(*text);
    free(*lang);
    *text = *lang = NULL;
    return 0;
  }

  return 1;
}

static void lesson_free(lesson * l)
{
  int i;

  if (l == NULL)
    return;

  for (i = 0; i < l->num_steps; i++)
  {
    free(l->steps[i].layer);
    free(l->steps[i].text);
    free(l->steps[i].lang);
  }
  free(l->steps);
  free(l->name);
  free(l->svg_fname);
  free(l->title);
  free(l->title_lang);
  free(l);
}

static lesson *lesson_load(const char *txt_fname, const char *svg_fname, const char *name,
			   int level, const char *const *langs, int num_langs)
{
  block *blocks;
  int num_blocks, i;
  lesson *l;
  lesson_step *step;
  char kind[16], layer[128], extra[2];
  int got;

  blocks = read_blocks(txt_fname, &num_blocks);
  if (blocks == NULL)
    return NULL;

  l = calloc(1, sizeof(lesson));
  if (l == NULL || num_blocks < 2 || blocks[0].num == 0)
  {
    /* (In "custom", a title alone is a picture's: see picture_lesson()) */
    if (num_blocks < 2 && level != LESSON_CUSTOM)
      fprintf(stderr, "Lesson %s: no steps\n", txt_fname);
    free(l);
    free_blocks(blocks, num_blocks);
    return NULL;
  }

  l->name = strdup(name);
  l->svg_fname = strdup(svg_fname);
  l->level = level;
  l->steps = calloc(num_blocks - 1, sizeof(lesson_step));
  if (l->name == NULL || l->svg_fname == NULL || l->steps == NULL ||
      !pick_text(&blocks[0], 0, langs, num_langs, &l->title, &l->title_lang))
  {
    lesson_free(l);
    free_blocks(blocks, num_blocks);
    return NULL;
  }

  for (i = 1; i < num_blocks; i++)
  {
    step = &l->steps[l->num_steps];

    /* (Left empty only when memory ran out while reading) */
    if (blocks[i].num == 0)
      continue;

    got = sscanf(blocks[i].lines[0], "%15s %127s %1s", kind, layer, extra);

    if (got == 1 && strcmp(kind, "erase") == 0)
      step->kind = LESSON_STEP_ERASE;
    else if (got == 2 && strcmp(kind, "draw") == 0)
      step->kind = LESSON_STEP_DRAW;
    else if (got == 2 && strcmp(kind, "guide") == 0)
      step->kind = LESSON_STEP_GUIDE;
    else if (got == 2 && strcmp(kind, "color") == 0)
      step->kind = LESSON_STEP_COLOR;
    else
    {
      fprintf(stderr, "Lesson %s: step %d: what is \"%s\"?\n", txt_fname, i,
	      blocks[i].lines[0]);
      continue;
    }

    if (step->kind != LESSON_STEP_ERASE)
    {
      step->layer = strdup(layer);
      if (step->layer == NULL)
	continue;
    }

    if (!pick_text(&blocks[i], 1, langs, num_langs, &step->text, &step->lang))
    {
      fprintf(stderr, "Lesson %s: step %d has no instructions\n", txt_fname, i);
      free(step->layer);
      step->layer = NULL;
      continue;
    }

    l->num_steps++;
  }

  free_blocks(blocks, num_blocks);

  if (l->num_steps == 0)
  {
    lesson_free(l);
    return NULL;
  }

  return l;
}

static int compare_lessons(const void *a, const void *b)
{
  const lesson *la = *(const lesson * const *) a;
  const lesson *lb = *(const lesson * const *) b;

  if (la->level != lb->level)
    return la->level - lb->level;
  if (la->num_steps != lb->num_steps)
    return la->num_steps - lb->num_steps;
  return strcasecmp(la->title, lb->title);
}

/* Add a lesson to the list; one of the same level and name already there
   is replaced (a later folder wins). 0 if out of memory (then l is freed). */
static int add_lesson(lesson *** found, int *num, lesson * l)
{
  lesson **bigger;
  int i;

  for (i = 0; i < *num; i++)
  {
    if ((*found)[i]->level == l->level && strcmp((*found)[i]->name, l->name) == 0)
    {
      lesson_free((*found)[i]);
      (*found)[i] = l;
      return 1;
    }
  }

  bigger = realloc(*found, sizeof(lesson *) * (*num + 1));
  if (bigger == NULL)
  {
    lesson_free(l);
    return 0;
  }
  *found = bigger;
  (*found)[(*num)++] = l;
  return 1;
}

/* How good a picture file is (an SVG is the best); 0 if it isn't one */
static int picture_rank(const char *fname, size_t *ext_len)
{
  static const struct
  {
    const char *ext;
    int rank;
  } exts[] = {
    {".svg", 3}, {".png", 2}, {".jpg", 1}, {".jpeg", 1}
  };
  size_t len = strlen(fname), n;
  unsigned int i;

  for (i = 0; i < sizeof(exts) / sizeof(exts[0]); i++)
  {
    n = strlen(exts[i].ext);
    if (len > n && strcasecmp(fname + len - n, exts[i].ext) == 0)
    {
      *ext_len = n;
      return exts[i].rank;
    }
  }

  return 0;
}

/* A picture of the user's as a lesson that copies it with a grid. The
   title is NAME.txt's, if there is one, else the file's name. */
static lesson *picture_lesson(const char *dir_path, const char *fname, const char *name,
			      const char *const *langs, int num_langs, const char *ui_lang)
{
  lesson *l;
  block *blocks;
  int num_blocks, i;
  char path[1024];
  const char *text;
  size_t n;

  l = calloc(1, sizeof(lesson));
  if (l == NULL)
    return NULL;

  l->picture = 1;
  l->level = LESSON_CUSTOM;
  l->name = strdup(name);
  l->steps = calloc(NUM_PICTURE_STEPS, sizeof(lesson_step));
  if (snprintf(path, sizeof(path), "%s/%s", dir_path, fname) < (int) sizeof(path))
    l->svg_fname = strdup(path);
  if (l->name == NULL || l->steps == NULL || l->svg_fname == NULL)
  {
    lesson_free(l);
    return NULL;
  }

  if (snprintf(path, sizeof(path), "%s/%s.txt", dir_path, name) < (int) sizeof(path))
  {
    blocks = read_blocks(path, &num_blocks);
    if (blocks != NULL)
    {
      if (num_blocks > 0 && blocks[0].num > 0)
	pick_text(&blocks[0], 0, langs, num_langs, &l->title, &l->title_lang);
      free_blocks(blocks, num_blocks);
    }
  }

  if (l->title == NULL)
  {
    /* "my_red-car" -> "My red car" */
    l->title = strdup(name);
    l->title_lang = strdup(ui_lang);
    if (l->title == NULL || l->title_lang == NULL)
    {
      lesson_free(l);
      return NULL;
    }
    for (n = 0; l->title[n] != '\0'; n++)
      if (l->title[n] == '_' || l->title[n] == '-')
	l->title[n] = ' ';
    l->title[0] = toupper((unsigned char) l->title[0]);
  }

  for (i = 0; i < NUM_PICTURE_STEPS; i++)
  {
    text = gettext(picture_steps[i].text);
    l->steps[i].kind = picture_steps[i].kind;
    l->steps[i].text = strdup(text);
    l->steps[i].lang = strdup(strcmp(text, picture_steps[i].text) != 0 ? ui_lang : "en");
    if (l->steps[i].text == NULL || l->steps[i].lang == NULL)
    {
      l->num_steps = i + 1;
      lesson_free(l);
      return NULL;
    }
  }
  l->num_steps = NUM_PICTURE_STEPS;

  return l;
}

lesson **lessons_find(const char *const *dirs, int num_dirs,
		      const char *const *langs, int num_langs, const char *ui_lang, int *num)
{
  lesson **found = NULL, *l;
  int d, level, i, rank, best, here_first;
  DIR *dir;
  struct dirent *ent;
  char path[1024], txt_fname[1024], svg_fname[1024], name[256];
  size_t len, ext_len = 0;
  FILE *fi;

  *num = 0;

  if (!lessons_supported())
    return NULL;

  for (d = 0; d < num_dirs; d++)
  {
    if (dirs[d] == NULL)
      continue;

    for (level = 0; level < NUM_LESSON_LEVELS; level++)
    {
      if (snprintf(path, sizeof(path), "%s/%s", dirs[d], lesson_level_dirs[level]) >=
	  (int) sizeof(path))
	continue;
      dir = opendir(path);
      if (dir == NULL)
	continue;

      /* (Lessons found in this folder start here in the list) */
      here_first = *num;

      /* Lessons: NAME.txt with the steps of NAME.svg */
      while ((ent = readdir(dir)) != NULL)
      {
	len = strlen(ent->d_name);
	if (len <= 4 || len - 4 >= sizeof(name) || strcasecmp(ent->d_name + len - 4, ".txt") != 0 ||
	    strcasecmp(ent->d_name, "README.txt") == 0 || ent->d_name[0] == '.')
	  continue;

	memcpy(name, ent->d_name, len - 4);
	name[len - 4] = '\0';
	if (snprintf(txt_fname, sizeof(txt_fname), "%s/%s", path, ent->d_name) >=
	    (int) sizeof(txt_fname) ||
	    snprintf(svg_fname, sizeof(svg_fname), "%s/%s.svg", path, name) >=
	    (int) sizeof(svg_fname))
	  continue;		/* (too long) */

	fi = fopen(svg_fname, "r");
	if (fi == NULL)
	  continue;
	fclose(fi);

	l = lesson_load(txt_fname, svg_fname, name, level, langs, num_langs);
	if (l != NULL)
	  add_lesson(&found, num, l);
      }

      /* In "custom", also the pictures with no steps of their own: one
         per name, the best kind of file (SVG, then PNG, then JPEG) */
      if (level == LESSON_CUSTOM)
      {
	rewinddir(dir);
	while ((ent = readdir(dir)) != NULL)
	{
	  rank = picture_rank(ent->d_name, &ext_len);
	  len = strlen(ent->d_name);
	  if (rank == 0 || ent->d_name[0] == '.' || len - ext_len >= sizeof(name))
	    continue;
	  memcpy(name, ent->d_name, len - ext_len);
	  name[len - ext_len] = '\0';

	  /* (A lesson, or a better file, of that name in this folder?) */
	  best = 1;
	  for (i = here_first; i < *num && best; i++)
	  {
	    if (found[i]->level != LESSON_CUSTOM || strcmp(found[i]->name, name) != 0)
	      continue;
	    if (!found[i]->picture || picture_rank(found[i]->svg_fname, &ext_len) >= rank)
	      best = 0;
	  }
	  if (!best)
	    continue;

	  l = picture_lesson(path, ent->d_name, name, langs, num_langs, ui_lang);
	  if (l != NULL)
	    add_lesson(&found, num, l);
	}
      }

      closedir(dir);
    }
  }

  if (*num > 0)
    qsort(found, *num, sizeof(lesson *), compare_lessons);

  return found;
}

void lessons_free(lesson ** lessons, int num)
{
  int i;

  for (i = 0; i < num; i++)
    lesson_free(lessons[i]);
  free(lessons);
}


#ifdef LESSONS_OK

/* --- Drawing them --- */

/* New lines, and new guide shapes (as in devtools/content/lesson_preview.py) */
static const double highlight[3] = { 0xff / 255.0, 0x4d / 255.0, 0x2e / 255.0 };
static const double guide_highlight[3] = { 0xff / 255.0, 0x9e / 255.0, 0x80 / 255.0 };

static const double ink[3] = { 0x2b / 255.0, 0x2b / 255.0, 0x2b / 255.0 };
static const double desk[3] = { 0xee / 255.0, 0xf1 / 255.0, 0xf5 / 255.0 };
static const double paper_edge[3] = { 0xc9 / 255.0, 0xce / 255.0, 0xd6 / 255.0 };
static const double paper_shadow[3] = { 0xdc / 255.0, 0xe0 / 255.0, 0xe6 / 255.0 };

struct lesson_pics
{
  const lesson *l;
  int area_w, area_h, top_h;
  double dot_r, dot_step, dots_x;	/* the step dots, in the top strip */
  int pic_x, pic_y, pic_w, pic_h;
  double tool_cx, tool_w;	/* the column for the tool, right of the picture */
  cairo_surface_t **layers;	/* each step's group alone, at the picture's size */
  cairo_surface_t *picture;	/* a plain picture (lesson.picture), at that size */
  double (*colors)[3];		/* each color step's color */
  cairo_surface_t *frame;
  SDL_Surface *frame_sdl;	/* (the frame's pixels) */
};

int lessons_supported(void)
{
  return 1;
}

static RsvgHandle *open_svg(const char *fname)
{
  GError *gerr = NULL;
  RsvgHandle *handle;

  handle = rsvg_handle_new_from_file(fname, &gerr);
  if (handle == NULL)
  {
    fprintf(stderr, "Lesson %s: can't read it (%s)\n", fname,
	    gerr != NULL ? gerr->message : "?");
    if (gerr != NULL)
      g_error_free(gerr);
  }

  return handle;
}

/* The biggest w x h of that aspect that fits in max_w x max_h */
static void fit(double aspect, int max_w, int max_h, int *w, int *h)
{
  if (max_w / aspect <= max_h)
  {
    *w = max_w;
    *h = (int) (max_w / aspect + 0.5);
  }
  else
  {
    *h = max_h;
    *w = (int) (max_h * aspect + 0.5);
  }
  if (*w < 1)
    *w = 1;
  if (*h < 1)
    *h = 1;
}

/* Width / height of the drawing */
static double picture_aspect(RsvgHandle * handle)
{
  gboolean has_w, has_h, has_vb;
  RsvgLength w, h;
  RsvgRectangle vb;

  rsvg_handle_get_intrinsic_dimensions(handle, &has_w, &w, &has_h, &h, &has_vb, &vb);

  if (has_vb && vb.width > 0 && vb.height > 0)
    return vb.width / vb.height;

#if LIBRSVG_CHECK_VERSION(2, 52, 0)
  {
    gdouble pw, ph;

    /* (No viewBox: its size, if in absolute units) */
    if (rsvg_handle_get_intrinsic_size_in_pixels(handle, &pw, &ph) && pw > 0 && ph > 0)
      return pw / ph;
  }
#endif

  return 4.0 / 3.0;
}

/* A plain picture of the user's: an SVG, or an image SDL_image reads */
typedef struct picture_src
{
  RsvgHandle *svg;
  cairo_surface_t *raster;	/* (premultiplied ARGB) */
  double aspect;
} picture_src;

/* The biggest raster kept: bigger photos are scaled down when read */
#define MAX_RASTER 2048

static int picture_open(const char *fname, picture_src * ps)
{
  SDL_Surface *img, *argb;
  cairo_surface_t *full;
  cairo_t *cr;
  unsigned char *data;
  Uint32 *src, a, px;
  int x, y, stride, keep_alpha, w, h;
  size_t len = strlen(fname);

  memset(ps, 0, sizeof(*ps));

  if (len > 4 && strcasecmp(fname + len - 4, ".svg") == 0)
  {
    ps->svg = open_svg(fname);
    if (ps->svg == NULL)
      return 0;
    ps->aspect = picture_aspect(ps->svg);
    return 1;
  }

  img = IMG_Load(fname);
  if (img == NULL)
  {
    fprintf(stderr, "Lesson %s: can't read it (%s)\n", fname, IMG_GetError());
    return 0;
  }

  /* To 32-bit ARGB, then premultiplied for cairo (an image with no alpha
     is opaque) */
  keep_alpha = (img->format->Amask != 0);
  argb = SDL_CreateRGBSurface(SDL_SWSURFACE, img->w, img->h, 32,
			      0x00ff0000, 0x0000ff00, 0x000000ff, 0xff000000);
  if (argb == NULL)
  {
    SDL_FreeSurface(img);
    return 0;
  }
  SDL_SetAlpha(img, 0, 0);
  SDL_BlitSurface(img, NULL, argb, NULL);
  SDL_FreeSurface(img);

  full = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, argb->w, argb->h);
  if (cairo_surface_status(full) != CAIRO_STATUS_SUCCESS)
  {
    cairo_surface_destroy(full);
    SDL_FreeSurface(argb);
    return 0;
  }
  cairo_surface_flush(full);
  data = cairo_image_surface_get_data(full);
  stride = cairo_image_surface_get_stride(full);
  SDL_LockSurface(argb);
  for (y = 0; y < argb->h; y++)
  {
    src = (Uint32 *) ((Uint8 *) argb->pixels + y * argb->pitch);
    for (x = 0; x < argb->w; x++)
    {
      px = src[x];
      a = keep_alpha ? px >> 24 : 255;
      *(Uint32 *) (data + y * stride + x * 4) =
	(a << 24) | ((((px >> 16) & 0xff) * a / 255) << 16) |
	((((px >> 8) & 0xff) * a / 255) << 8) | ((px & 0xff) * a / 255);
    }
  }
  SDL_UnlockSurface(argb);
  cairo_surface_mark_dirty(full);
  ps->aspect = (double) argb->w / argb->h;
  w = argb->w;
  h = argb->h;
  SDL_FreeSurface(argb);

  /* (A big photo, smaller: it's only shown at the screen's size) */
  if (w > MAX_RASTER || h > MAX_RASTER)
  {
    fit(ps->aspect, MAX_RASTER, MAX_RASTER, &x, &y);
    ps->raster = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, x, y);
    cr = cairo_create(ps->raster);
    cairo_scale(cr, (double) x / w, (double) y / h);
    cairo_set_source_surface(cr, full, 0, 0);
    cairo_pattern_set_filter(cairo_get_source(cr), CAIRO_FILTER_GOOD);
    cairo_paint(cr);
    cairo_destroy(cr);
    cairo_surface_destroy(full);
  }
  else
    ps->raster = full;

  return 1;
}

/* The whole picture into x, y, w, h (of its aspect) */
static void picture_draw(picture_src * ps, cairo_t * cr, double x, double y, double w, double h)
{
  RsvgRectangle viewport;

  if (ps->svg != NULL)
  {
    viewport.x = x;
    viewport.y = y;
    viewport.width = w;
    viewport.height = h;
    rsvg_handle_render_document(ps->svg, cr, &viewport, NULL);
  }
  else if (ps->raster != NULL)
  {
    cairo_save(cr);
    cairo_translate(cr, x, y);
    cairo_scale(cr, w / cairo_image_surface_get_width(ps->raster),
		h / cairo_image_surface_get_height(ps->raster));
    cairo_set_source_surface(cr, ps->raster, 0, 0);
    cairo_pattern_set_filter(cairo_get_source(cr), CAIRO_FILTER_GOOD);
    cairo_paint(cr);
    cairo_restore(cr);
  }
}

static void picture_close(picture_src * ps)
{
  if (ps->svg != NULL)
    g_object_unref(ps->svg);
  if (ps->raster != NULL)
    cairo_surface_destroy(ps->raster);
  memset(ps, 0, sizeof(*ps));
}

/* One group of the drawing (all of it if id is NULL) into cr, the whole
   drawing taking x, y, w, h */
static int render_group(RsvgHandle * handle, cairo_t * cr, const char *id,
			double x, double y, double w, double h)
{
  RsvgRectangle viewport;
  GError *gerr = NULL;
  char sub[130];
  int ok;

  viewport.x = x;
  viewport.y = y;
  viewport.width = w;
  viewport.height = h;

  snprintf(sub, sizeof(sub), "#%s", id);
  if (!rsvg_handle_has_sub(handle, sub))
    return 0;

  ok = rsvg_handle_render_layer(handle, cr, sub, &viewport, &gerr);
  if (gerr != NULL)
    g_error_free(gerr);

  return ok;
}

/* The commonest color of a group's opaque pixels; with colorful, only
   among the clearly colored ones (not white, grey or black): 0 if none */
static int main_color(cairo_surface_t * s, double rgb[3], int colorful)
{
  int x, y, w, h, stride, best = 0, *counts;
  unsigned char *data;
  Uint32 p, a, r, g, b;
  double sum[3] = { 0, 0, 0 };
  long n = 0;

  rgb[0] = rgb[1] = rgb[2] = 0.5;

  counts = calloc(32768, sizeof(int));
  if (counts == NULL)
    return 0;

  cairo_surface_flush(s);
  data = cairo_image_surface_get_data(s);
  w = cairo_image_surface_get_width(s);
  h = cairo_image_surface_get_height(s);
  stride = cairo_image_surface_get_stride(s);

  /* (Premultiplied ARGB, in native-endian 32-bit words) */
  for (y = 0; y < h; y++)
    for (x = 0; x < w; x++)
    {
      p = *(Uint32 *) (data + y * stride + x * 4);
      a = p >> 24;
      if (a < 200)
	continue;
      r = ((p >> 16) & 0xff) * 255 / a;
      g = ((p >> 8) & 0xff) * 255 / a;
      b = (p & 0xff) * 255 / a;
      if (colorful)
      {
	Uint32 hi = (r > g ? r : g), lo = (r < g ? r : g);

	hi = (b > hi ? b : hi);
	lo = (b < lo ? b : lo);
	if (hi - lo < 60)
	  continue;
      }
      counts[((r >> 3) << 10) | ((g >> 3) << 5) | (b >> 3)]++;
    }

  for (x = 1; x < 32768; x++)
    if (counts[x] > counts[best])
      best = x;

  if (counts[best] > 0)
  {
    for (y = 0; y < h; y++)
      for (x = 0; x < w; x++)
      {
	p = *(Uint32 *) (data + y * stride + x * 4);
	a = p >> 24;
	if (a < 200)
	  continue;
	r = ((p >> 16) & 0xff) * 255 / a;
	g = ((p >> 8) & 0xff) * 255 / a;
	b = (p & 0xff) * 255 / a;
	if ((int) (((r >> 3) << 10) | ((g >> 3) << 5) | (b >> 3)) != best)
	  continue;
	sum[0] += r;
	sum[1] += g;
	sum[2] += b;
	n++;
      }
    rgb[0] = sum[0] / n / 255;
    rgb[1] = sum[1] / n / 255;
    rgb[2] = sum[2] / n / 255;
  }

  free(counts);
  return n > 0;
}

lesson_pics *lesson_pics_new(const lesson * l, int area_w, int area_h, int top_h)
{
  static const double default_crayon[3] = { 0x3a / 255.0, 0x86 / 255.0, 0xff / 255.0 };
  lesson_pics *p;
  RsvgHandle *handle = NULL;
  picture_src ps;
  double aspect;
  int i, side, pic_area_h;
  cairo_t *cr;

  if (area_w < 16 || area_h - top_h < 16)
    return NULL;

  if (l->picture)
  {
    if (!picture_open(l->svg_fname, &ps))
      return NULL;
    aspect = ps.aspect;
  }
  else
  {
    handle = open_svg(l->svg_fname);
    if (handle == NULL)
      return NULL;
    aspect = picture_aspect(handle);
  }

  p = calloc(1, sizeof(lesson_pics));
  if (p == NULL)
  {
    if (handle != NULL)
      g_object_unref(handle);
    if (l->picture)
      picture_close(&ps);
    return NULL;
  }

  p->l = l;
  p->area_w = area_w;
  p->area_h = area_h;
  p->top_h = top_h;

  /* Room on both sides (the picture stays centered) for the tool */
  pic_area_h = area_h - top_h;
  side = pic_area_h / 6;
  fit(aspect, area_w - side * 2, pic_area_h - pic_area_h / 30, &p->pic_w, &p->pic_h);
  p->pic_x = (area_w - p->pic_w) / 2;
  p->pic_y = top_h + (pic_area_h - p->pic_h) / 2;
  p->tool_w = area_w - (p->pic_x + p->pic_w);
  if (p->tool_w > pic_area_h / 4.0)
    p->tool_w = pic_area_h / 4.0;
  p->tool_cx = p->pic_x + p->pic_w + (area_w - (p->pic_x + p->pic_w)) / 2.0;

  /* The dots, at the right of the strip */
  p->dot_r = top_h * 0.2;
  p->dot_step = top_h * 0.6;
  if (l->num_steps * p->dot_step > area_w * 0.5)
  {
    p->dot_step = area_w * 0.5 / l->num_steps;
    p->dot_r = p->dot_step / 3;
  }
  p->dots_x = p->pic_x + p->pic_w - l->num_steps * p->dot_step;

  p->layers = calloc(l->num_steps, sizeof(cairo_surface_t *));
  p->colors = calloc(l->num_steps, sizeof(double[3]));
  p->frame = cairo_image_surface_create(CAIRO_FORMAT_RGB24, area_w, area_h);
  if (p->layers == NULL || p->colors == NULL ||
      cairo_surface_status(p->frame) != CAIRO_STATUS_SUCCESS)
  {
    if (handle != NULL)
      g_object_unref(handle);
    if (l->picture)
      picture_close(&ps);
    lesson_pics_free(p);
    return NULL;
  }

  /* A plain picture: drawn once; its main color is the crayon's */
  if (l->picture)
  {
    p->picture = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, p->pic_w, p->pic_h);
    cr = cairo_create(p->picture);
    picture_draw(&ps, cr, 0, 0, p->pic_w, p->pic_h);
    cairo_destroy(cr);
    picture_close(&ps);

    for (i = 0; i < l->num_steps; i++)
      if (l->steps[i].kind == LESSON_STEP_PAINT &&
	  !main_color(p->picture, p->colors[i], 1))
	memcpy(p->colors[i], default_crayon, sizeof(default_crayon));
  }

  for (i = 0; i < l->num_steps; i++)
  {
    if (l->steps[i].layer == NULL)
      continue;

    p->layers[i] = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, p->pic_w, p->pic_h);
    cr = cairo_create(p->layers[i]);
    if (!render_group(handle, cr, l->steps[i].layer, 0, 0, p->pic_w, p->pic_h))
    {
      fprintf(stderr, "Lesson %s: no group \"%s\" in %s\n", l->name,
	      l->steps[i].layer, l->svg_fname);
      cairo_destroy(cr);
      cairo_surface_destroy(p->layers[i]);
      p->layers[i] = NULL;
      continue;
    }
    cairo_destroy(cr);

    if (l->steps[i].kind == LESSON_STEP_COLOR)
      main_color(p->layers[i], p->colors[i], 0);
  }

  if (handle != NULL)
    g_object_unref(handle);

  /* (RGB24 is 32-bit xRGB in native-endian words) */
  p->frame_sdl = SDL_CreateRGBSurfaceFrom(cairo_image_surface_get_data(p->frame),
					  area_w, area_h, 32,
					  cairo_image_surface_get_stride(p->frame),
					  0x00ff0000, 0x0000ff00, 0x000000ff, 0);
  if (p->frame_sdl == NULL)
  {
    lesson_pics_free(p);
    return NULL;
  }

  return p;
}

void lesson_pics_free(lesson_pics * p)
{
  int i;

  if (p == NULL)
    return;

  if (p->frame_sdl != NULL)
    SDL_FreeSurface(p->frame_sdl);
  if (p->frame != NULL)
    cairo_surface_destroy(p->frame);
  if (p->picture != NULL)
    cairo_surface_destroy(p->picture);
  if (p->layers != NULL)
  {
    for (i = 0; i < p->l->num_steps; i++)
      if (p->layers[i] != NULL)
	cairo_surface_destroy(p->layers[i]);
    free(p->layers);
  }
  free(p->colors);
  free(p);
}

/* How visible the new step is during its animation: it appears, then
   blinks twice */
static double pulse(float anim)
{
  double t;

  if (anim >= 1)
    return 1;
  if (anim < 0.2)
    return anim / 0.2;

  t = (anim - 0.2) / 0.8;
  return 1.0 - 0.7 * pow(sin(M_PI * 2 * t), 2);
}

static void paint_layer(cairo_t * cr, lesson_pics * p, int i, const double *tint, double alpha)
{
  if (p->layers[i] == NULL || alpha <= 0)
    return;

  if (tint != NULL)
  {
    cairo_set_source_rgba(cr, tint[0], tint[1], tint[2], alpha);
    cairo_mask_surface(cr, p->layers[i], p->pic_x, p->pic_y);
  }
  else
  {
    cairo_set_source_surface(cr, p->layers[i], p->pic_x, p->pic_y);
    cairo_paint_with_alpha(cr, alpha);
  }
}

static void fill_and_outline(cairo_t * cr, const double rgb[3], double line_w)
{
  cairo_set_source_rgb(cr, rgb[0], rgb[1], rgb[2]);
  cairo_fill_preserve(cr);
  cairo_set_source_rgb(cr, ink[0], ink[1], ink[2]);
  cairo_set_line_width(cr, line_w);
  cairo_stroke(cr);
}

/* A pencil or a crayon, point down, centered in (0, 0), w wide, h long */
static void draw_stick(cairo_t * cr, double w, double h, const double body[3],
		       const double band[3], const double cone[3], const double point[3])
{
  double top = -h / 2, body_end = h / 2 - h * 0.27, tip = h / 2;
  double cut = tip - h * 0.08, r = w * 0.25, lw = w * 0.09;

  cairo_set_line_join(cr, CAIRO_LINE_JOIN_ROUND);

  /* Body, round at the top */
  cairo_new_path(cr);
  cairo_move_to(cr, -w / 2, body_end);
  cairo_line_to(cr, -w / 2, top + r);
  cairo_arc(cr, -w / 2 + r, top + r, r, M_PI, M_PI * 1.5);
  cairo_arc(cr, w / 2 - r, top + r, r, M_PI * 1.5, M_PI * 2);
  cairo_line_to(cr, w / 2, body_end);
  cairo_close_path(cr);
  fill_and_outline(cr, body, lw);

  /* The crayon's paper */
  if (band != NULL)
  {
    cairo_rectangle(cr, -w / 2, top + (body_end - top) * 0.3, w, (body_end - top) * 0.4);
    fill_and_outline(cr, band, lw);
  }

  /* Cone and point */
  cairo_move_to(cr, -w / 2, body_end);
  cairo_line_to(cr, w / 2, body_end);
  cairo_line_to(cr, w * 0.14, cut);
  cairo_line_to(cr, -w * 0.14, cut);
  cairo_close_path(cr);
  fill_and_outline(cr, cone, lw);

  cairo_move_to(cr, -w * 0.14, cut);
  cairo_line_to(cr, w * 0.14, cut);
  cairo_line_to(cr, 0, tip);
  cairo_close_path(cr);
  fill_and_outline(cr, point, lw);
}

/* An eraser, centered in (0, 0), w wide */
static void draw_eraser(cairo_t * cr, double w)
{
  static const double rubber[3] = { 0xff / 255.0, 0x8f / 255.0, 0xab / 255.0 };
  static const double sleeve[3] = { 0x3a / 255.0, 0x86 / 255.0, 0xff / 255.0 };
  double h = w * 0.5, r = h * 0.2, lw = w * 0.045;

  cairo_set_line_join(cr, CAIRO_LINE_JOIN_ROUND);

  cairo_new_path(cr);
  cairo_arc(cr, -w / 2 + r, -h / 2 + r, r, M_PI, M_PI * 1.5);
  cairo_arc(cr, w / 2 - r, -h / 2 + r, r, M_PI * 1.5, M_PI * 2);
  cairo_arc(cr, w / 2 - r, h / 2 - r, r, 0, M_PI * 0.5);
  cairo_arc(cr, -w / 2 + r, h / 2 - r, r, M_PI * 0.5, M_PI);
  cairo_close_path(cr);
  fill_and_outline(cr, rubber, lw);

  cairo_rectangle(cr, -w * 0.05, -h / 2, w * 0.4, h);
  fill_and_outline(cr, sleeve, lw);
}

/* What to use for the step, wiggling during its animation */
static void draw_tool(cairo_t * cr, lesson_pics * p, int step, float anim)
{
  static const double pencil_body[3] = { 0xff / 255.0, 0xd9 / 255.0, 0x3b / 255.0 };
  static const double wood[3] = { 0xf2 / 255.0, 0xc5 / 255.0, 0x8f / 255.0 };
  double w = p->tool_w * 0.4, h, wiggle, darker[3];
  int i;

  if (w < 4)
    return;
  h = w * 4.5;
  if (h > (p->area_h - p->top_h) * 0.6)
  {
    h = (p->area_h - p->top_h) * 0.6;
    w = h / 4.5;
  }

  /* (Small enough to stay in its column) */
  wiggle = (anim < 1 ? sin(M_PI * 4 * anim) * (1 - anim) * 0.4 : 0);

  cairo_save(cr);
  cairo_translate(cr, p->tool_cx, p->top_h + (p->area_h - p->top_h) / 2.0);

  switch (p->l->steps[step].kind)
  {
  case LESSON_STEP_LOOK:
    break;			/* (nothing to use yet) */

  case LESSON_STEP_COLOR:
  case LESSON_STEP_PAINT:
    for (i = 0; i < 3; i++)
      darker[i] = p->colors[step][i] * 0.75;
    cairo_rotate(cr, 0.2 + 0.3 * wiggle);
    draw_stick(cr, w, h, p->colors[step], darker, p->colors[step], darker);
    break;

  case LESSON_STEP_GUIDE:
  case LESSON_STEP_GRID:
    /* (Drawn lightly: a paler pencil) */
    cairo_push_group(cr);
    cairo_rotate(cr, 0.2 + 0.3 * wiggle);
    draw_stick(cr, w, h, pencil_body, NULL, wood, ink);
    cairo_pop_group_to_source(cr);
    cairo_paint_with_alpha(cr, 0.5);
    break;

  case LESSON_STEP_ERASE:
    cairo_translate(cr, 0, h * 0.3 * wiggle);
    cairo_rotate(cr, -1.2);
    draw_eraser(cr, p->tool_w * 0.8);
    break;

  default:
    cairo_rotate(cr, 0.2 + 0.3 * wiggle);
    draw_stick(cr, w, h, pencil_body, NULL, wood, ink);
    break;
  }

  cairo_restore(cr);
}

/* A dot for each step: done, current (bigger, in the highlight color), to
   come (hollow) */
static void draw_dots(cairo_t * cr, lesson_pics * p, int step)
{
  int i;
  double x, y = p->top_h / 2.0, r;

  for (i = 0; i < p->l->num_steps; i++)
  {
    x = p->dots_x + (i + 0.5) * p->dot_step;
    r = (i == step ? p->dot_r * 1.35 : p->dot_r);
    cairo_new_path(cr);
    cairo_arc(cr, x, y, r, 0, 2 * M_PI);
    if (i == step)
      cairo_set_source_rgb(cr, highlight[0], highlight[1], highlight[2]);
    else if (i < step)
      cairo_set_source_rgb(cr, ink[0], ink[1], ink[2]);
    else
      cairo_set_source_rgb(cr, 1, 1, 1);
    cairo_fill_preserve(cr);
    cairo_set_source_rgb(cr, ink[0], ink[1], ink[2]);
    cairo_set_line_width(cr, p->dot_r * 0.3);
    cairo_stroke(cr);
  }
}

int lesson_pics_dots_x(const lesson_pics * p)
{
  return (int) p->dots_x;
}

/* The 3 x 3 grid of a picture's steps, over it */
static void draw_grid(cairo_t * cr, lesson_pics * p, const double rgb[3], double alpha)
{
  double lw = p->pic_h / 150.0, dashes[2];
  int i;

  if (alpha <= 0)
    return;
  if (lw < 1.5)
    lw = 1.5;
  dashes[0] = lw * 4;
  dashes[1] = lw * 3;

  cairo_save(cr);
  cairo_new_path(cr);
  for (i = 1; i < 3; i++)
  {
    cairo_move_to(cr, p->pic_x + p->pic_w * i / 3.0, p->pic_y);
    cairo_line_to(cr, p->pic_x + p->pic_w * i / 3.0, p->pic_y + p->pic_h);
    cairo_move_to(cr, p->pic_x, p->pic_y + p->pic_h * i / 3.0);
    cairo_line_to(cr, p->pic_x + p->pic_w, p->pic_y + p->pic_h * i / 3.0);
  }
  cairo_set_source_rgba(cr, rgb[0], rgb[1], rgb[2], alpha);
  cairo_set_line_width(cr, lw);
  cairo_set_dash(cr, dashes, 2, 0);
  cairo_stroke(cr);
  cairo_restore(cr);
}

/* A plain picture, in color or (to copy its lines) pale and grey */
static void paint_picture(cairo_t * cr, lesson_pics * p, int pale, double alpha)
{
  if (alpha <= 0)
    return;

  cairo_push_group(cr);
  cairo_set_source_surface(cr, p->picture, p->pic_x, p->pic_y);
  cairo_paint(cr);
  if (pale)
  {
    cairo_set_operator(cr, CAIRO_OPERATOR_HSL_SATURATION);
    cairo_set_source_rgb(cr, 0.5, 0.5, 0.5);
    cairo_mask_surface(cr, p->picture, p->pic_x, p->pic_y);
    cairo_set_operator(cr, CAIRO_OPERATOR_OVER);
    cairo_set_source_rgba(cr, 1, 1, 1, 0.35);
    cairo_mask_surface(cr, p->picture, p->pic_x, p->pic_y);
  }
  cairo_pop_group_to_source(cr);
  cairo_paint_with_alpha(cr, alpha);
}

/* A plain picture's steps: look, grid, copy, erase the grid, color */
static void picture_frame(cairo_t * cr, lesson_pics * p, int step, float anim)
{
  static const double grid_color[3] = { 0x8a / 255.0, 0x9b / 255.0, 0xb0 / 255.0 };
  lesson_step_kind kind;

  if (step < 0 || step >= p->l->num_steps)
  {
    paint_picture(cr, p, 0, 1);
    return;
  }

  kind = p->l->steps[step].kind;
  switch (kind)
  {
  case LESSON_STEP_GRID:
    paint_picture(cr, p, 1, 1);
    draw_grid(cr, p, guide_highlight, pulse(anim));
    break;
  case LESSON_STEP_COPY:
    paint_picture(cr, p, 1, 1);
    draw_grid(cr, p, grid_color, 1);
    break;
  case LESSON_STEP_ERASE:
    paint_picture(cr, p, 1, 1);
    draw_grid(cr, p, highlight, 1 - anim);	/* (fading away) */
    break;
  case LESSON_STEP_PAINT:
    /* (The colors come back) */
    paint_picture(cr, p, 1, 1);
    paint_picture(cr, p, 0, anim < 0.5 ? anim * 2 : 1);
    break;
  default:
    paint_picture(cr, p, 0, 1);
    break;
  }
}

SDL_Surface *lesson_pics_frame(lesson_pics * p, int step, float anim)
{
  const lesson *l = p->l;
  int finished = (step < 0 || step >= l->num_steps);
  int last = finished ? l->num_steps - 1 : step;
  int i, j, erased_by;
  double edge = p->area_h / 300.0;
  cairo_t *cr;

  cr = cairo_create(p->frame);

  /* A sheet of paper on the desk */
  if (edge < 1)
    edge = 1;
  cairo_set_source_rgb(cr, desk[0], desk[1], desk[2]);
  cairo_paint(cr);
  cairo_rectangle(cr, p->pic_x + edge * 3, p->pic_y + edge * 3, p->pic_w, p->pic_h);
  cairo_set_source_rgb(cr, paper_shadow[0], paper_shadow[1], paper_shadow[2]);
  cairo_fill(cr);
  cairo_rectangle(cr, p->pic_x, p->pic_y, p->pic_w, p->pic_h);
  cairo_set_source_rgb(cr, 1, 1, 1);
  cairo_fill_preserve(cr);
  cairo_set_source_rgb(cr, paper_edge[0], paper_edge[1], paper_edge[2]);
  cairo_set_line_width(cr, edge);
  cairo_stroke(cr);

  if (l->picture)
  {
    picture_frame(cr, p, step, anim);
    last = -1;			/* (no groups) */
  }

  /* Colors under guides under lines; the new step blinks */
  for (i = 0; i <= last; i++)
    if (l->steps[i].kind == LESSON_STEP_COLOR)
      paint_layer(cr, p, i, NULL, i == step ? pulse(anim) : 1);

  for (i = 0; i <= last && !finished; i++)
  {
    if (l->steps[i].kind != LESSON_STEP_GUIDE)
      continue;

    erased_by = -1;
    for (j = i + 1; j <= last && erased_by < 0; j++)
      if (l->steps[j].kind == LESSON_STEP_ERASE)
	erased_by = j;

    if (erased_by < 0)
      paint_layer(cr, p, i, i == step ? guide_highlight : NULL, i == step ? pulse(anim) : 1);
    else if (erased_by == step)
      paint_layer(cr, p, i, highlight, 1 - anim);	/* fading away */
  }

  for (i = 0; i <= last; i++)
    if (l->steps[i].kind == LESSON_STEP_DRAW)
      paint_layer(cr, p, i, i == step ? highlight : NULL, i == step ? pulse(anim) : 1);

  if (!finished)
    draw_tool(cr, p, step, anim);

  if (p->top_h > 0)
    draw_dots(cr, p, step < 0 ? -1 : step);

  cairo_destroy(cr);
  cairo_surface_flush(p->frame);

  return p->frame_sdl;
}

/* Rounded rectangle path */
static void round_rect(cairo_t * cr, double x, double y, double w, double h, double r)
{
  cairo_new_path(cr);
  cairo_arc(cr, x + r, y + r, r, M_PI, M_PI * 1.5);
  cairo_arc(cr, x + w - r, y + r, r, M_PI * 1.5, M_PI * 2);
  cairo_arc(cr, x + w - r, y + h - r, r, 0, M_PI * 0.5);
  cairo_arc(cr, x + r, y + h - r, r, M_PI * 0.5, M_PI);
  cairo_close_path(cr);
}

/* Each level's color: green, yellow, coral */
static const double level_colors[NUM_LESSON_LEVELS][3] = {
  {0x90 / 255.0, 0xd2 / 255.0, 0x6d / 255.0},
  {0xff / 255.0, 0xd9 / 255.0, 0x3b / 255.0},
  {0xff / 255.0, 0x8f / 255.0, 0x6b / 255.0},
  {0x8e / 255.0, 0xca / 255.0, 0xe6 / 255.0}	/* (custom: light blue) */
};

static SDL_Surface *cairo_to_sdl(cairo_surface_t * cs)
{
  SDL_Surface *s;
  int y, w = cairo_image_surface_get_width(cs), h = cairo_image_surface_get_height(cs);

  cairo_surface_flush(cs);
  s = SDL_CreateRGBSurface(SDL_SWSURFACE, w, h, 32, 0x00ff0000, 0x0000ff00, 0x000000ff, 0);
  if (s == NULL)
    return NULL;

  SDL_LockSurface(s);
  for (y = 0; y < h; y++)
    memcpy((Uint8 *) s->pixels + y * s->pitch,
	   cairo_image_surface_get_data(cs) + y * cairo_image_surface_get_stride(cs), w * 4);
  SDL_UnlockSurface(s);

  return s;
}

static void heart(cairo_t * cr, double cx, double cy, double r)
{
  cairo_new_path(cr);
  cairo_move_to(cr, cx, cy + r * 0.9);
  cairo_curve_to(cr, cx - r * 1.4, cy - r * 0.1, cx - r * 0.7, cy - r * 1.2, cx, cy - r * 0.45);
  cairo_curve_to(cr, cx + r * 0.7, cy - r * 1.2, cx + r * 1.4, cy - r * 0.1, cx, cy + r * 0.9);
  cairo_close_path(cr);
}

static void star(cairo_t * cr, double cx, double cy, double r)
{
  int i;
  double a;

  cairo_new_path(cr);
  for (i = 0; i < 10; i++)
  {
    a = -M_PI / 2 + i * M_PI / 5;
    cairo_line_to(cr, cx + cos(a) * (i % 2 ? r * 0.45 : r), cy + sin(a) * (i % 2 ? r * 0.45 : r));
  }
  cairo_close_path(cr);
}

SDL_Surface *lesson_level_tab(int level, int w, int h, int selected, int *text_x)
{
  cairo_surface_t *cs;
  cairo_t *cr;
  SDL_Surface *s;
  const double *c = level_colors[level];
  double pale[3], lw = h / 16.0, r = h * 0.24, x;
  int i;

  if (w < 8 || h < 8)
    return NULL;

  for (i = 0; i < 3; i++)
    pale[i] = 1 - (1 - c[i]) * 0.35;

  cs = cairo_image_surface_create(CAIRO_FORMAT_RGB24, w, h);
  cr = cairo_create(cs);
  cairo_set_source_rgb(cr, 1, 1, 1);
  cairo_paint(cr);

  round_rect(cr, lw, lw, w - lw * 2, h - lw * 2, h * 0.3);
  if (selected)
    cairo_set_source_rgb(cr, c[0], c[1], c[2]);
  else
    cairo_set_source_rgb(cr, pale[0], pale[1], pale[2]);
  cairo_fill_preserve(cr);
  if (selected)
    cairo_set_source_rgb(cr, ink[0], ink[1], ink[2]);
  else
    cairo_set_source_rgb(cr, paper_edge[0], paper_edge[1], paper_edge[2]);
  cairo_set_line_width(cr, selected ? lw * 1.5 : lw);
  cairo_stroke(cr);

  /* One star for each level of difficulty; the user's own, a heart */
  if (r > w * 0.05)
    r = w * 0.05;
  x = h * 0.2;
  for (i = 0; i <= (level == LESSON_CUSTOM ? 0 : level); i++)
  {
    if (level == LESSON_CUSTOM)
      heart(cr, x + r, h / 2.0, r);
    else
      star(cr, x + r, h / 2.0, r);
    cairo_set_source_rgb(cr, 1, 1, 1);
    cairo_fill_preserve(cr);
    cairo_set_source_rgb(cr, ink[0], ink[1], ink[2]);
    cairo_set_line_width(cr, lw * 0.8);
    cairo_set_line_join(cr, CAIRO_LINE_JOIN_ROUND);
    cairo_stroke(cr);
    x += r * 1.9;
  }
  *text_x = (int) (x + h * 0.1);

  cairo_destroy(cr);
  s = cairo_to_sdl(cs);
  cairo_surface_destroy(cs);

  return s;
}

SDL_Surface *lesson_card(int level, int w, int h, int selected)
{
  cairo_surface_t *cs;
  cairo_t *cr;
  SDL_Surface *s;
  const double *c = level_colors[level];
  double lw = (w < h ? w : h) / 60.0;
  int i;
  double pale[3];

  if (w < 8 || h < 8)
    return NULL;
  if (lw < 1)
    lw = 1;

  for (i = 0; i < 3; i++)
    pale[i] = 1 - (1 - c[i]) * 0.3;

  cs = cairo_image_surface_create(CAIRO_FORMAT_RGB24, w, h);
  cr = cairo_create(cs);
  cairo_set_source_rgb(cr, 1, 1, 1);
  cairo_paint(cr);

  round_rect(cr, lw * 2, lw * 2, w - lw * 4, h - lw * 4, (w < h ? w : h) * 0.08);
  if (selected)
    cairo_set_source_rgb(cr, pale[0], pale[1], pale[2]);
  else
    cairo_set_source_rgb(cr, desk[0], desk[1], desk[2]);
  cairo_fill_preserve(cr);
  if (selected)
    cairo_set_source_rgb(cr, c[0] * 0.8, c[1] * 0.8, c[2] * 0.8);
  else
    cairo_set_source_rgb(cr, paper_edge[0], paper_edge[1], paper_edge[2]);
  cairo_set_line_width(cr, selected ? lw * 3 : lw);
  cairo_stroke(cr);

  cairo_destroy(cr);
  s = cairo_to_sdl(cs);
  cairo_surface_destroy(cs);

  return s;
}

SDL_Surface *lesson_thumbnail(const lesson * l, int w, int h)
{
  RsvgHandle *handle;
  cairo_surface_t *cs;
  cairo_t *cr;
  SDL_Surface *s;
  picture_src ps;
  int pw, ph, i, pass;
  lesson_step_kind kinds[2] = { LESSON_STEP_COLOR, LESSON_STEP_DRAW };

  if (l->picture)
  {
    if (!picture_open(l->svg_fname, &ps))
      return NULL;
    fit(ps.aspect, w, h, &pw, &ph);
    cs = cairo_image_surface_create(CAIRO_FORMAT_RGB24, pw, ph);
    cr = cairo_create(cs);
    cairo_set_source_rgb(cr, 1, 1, 1);
    cairo_paint(cr);
    picture_draw(&ps, cr, 0, 0, pw, ph);
    cairo_destroy(cr);
    picture_close(&ps);
    s = cairo_to_sdl(cs);
    cairo_surface_destroy(cs);
    return s;
  }

  handle = open_svg(l->svg_fname);
  if (handle == NULL)
    return NULL;

  fit(picture_aspect(handle), w, h, &pw, &ph);

  cs = cairo_image_surface_create(CAIRO_FORMAT_RGB24, pw, ph);
  cr = cairo_create(cs);
  cairo_set_source_rgb(cr, 1, 1, 1);
  cairo_paint(cr);
  for (pass = 0; pass < 2; pass++)
    for (i = 0; i < l->num_steps; i++)
      if (l->steps[i].kind == kinds[pass])
	render_group(handle, cr, l->steps[i].layer, 0, 0, pw, ph);
  cairo_destroy(cr);
  cairo_surface_flush(cs);
  g_object_unref(handle);

  s = cairo_to_sdl(cs);
  cairo_surface_destroy(cs);

  return s;
}

#else

/* No librsvg, or one older than 2.46 (no rsvg_handle_render_layer()) */

int lessons_supported(void)
{
  return 0;
}

SDL_Surface *lesson_thumbnail(const lesson * l, int w, int h)
{
  (void) l;
  (void) w;
  (void) h;
  return NULL;
}

lesson_pics *lesson_pics_new(const lesson * l, int area_w, int area_h, int top_h)
{
  (void) l;
  (void) area_w;
  (void) area_h;
  (void) top_h;
  return NULL;
}

int lesson_pics_dots_x(const lesson_pics * p)
{
  (void) p;
  return 0;
}

SDL_Surface *lesson_level_tab(int level, int w, int h, int selected, int *text_x)
{
  (void) level;
  (void) w;
  (void) h;
  (void) selected;
  *text_x = 0;
  return NULL;
}

SDL_Surface *lesson_card(int level, int w, int h, int selected)
{
  (void) level;
  (void) w;
  (void) h;
  (void) selected;
  return NULL;
}

void lesson_pics_free(lesson_pics * p)
{
  (void) p;
}

SDL_Surface *lesson_pics_frame(lesson_pics * p, int step, float anim)
{
  (void) p;
  (void) step;
  (void) anim;
  return NULL;
}

#endif

/* crossstitch.c

   Cross Stitch: a "Magic" tool plugin for Tux Paint, made from the example
   plugin (magic/docs/tp_magic_example.c). It turns the picture into
   embroidery on fabric: an "x" of thread in each square of the fabric, the
   color of the picture there. White parts stay bare fabric.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version. (See COPYING.txt)

   Last modified: 2026.11.01
*/


/* Inclusion of header files: */
/* -------------------------- */

#include <stdio.h>
#include <string.h>
#include <libintl.h>

#include "tp_magic_api.h"
#include "SDL_image.h"
#include "SDL_mixer.h"


/* Tool Enumerations: */
/* ------------------ */

enum {
  TOOL_CROSSSTITCH,
  NUM_TOOLS
};


/* Sizes, in pixels of the canvas: */

#define STITCH_SIZE 8   /* A square of the fabric, and its stitch */
#define BRUSH_RADIUS 16

/* Picture colors this light count as white (bare fabric) */
#define WHITE_MIN 235


static const char * crossstitch_snd_filenames[NUM_TOOLS] = {
  "crossstitch.ogg",
};

static const char * crossstitch_icon_filenames[NUM_TOOLS] = {
  "crossstitch.png",
};

static const char * crossstitch_names[NUM_TOOLS] = {
  gettext_noop("Cross Stitch"),
};

/* For painting, and for the entire picture: */
static const char * crossstitch_descs[NUM_TOOLS][2] = {
  {
    gettext_noop("Click and drag the mouse to embroider the picture with cross stitches."),
    gettext_noop("Click to embroider your entire picture with cross stitches."),
  },
};


/* Our global variables: */
/* --------------------- */

static Mix_Chunk * crossstitch_snd_effect[NUM_TOOLS];

/* The fabric, and how it's shaded within a square (darker at the holes
   in its corners and along its weave) */
static const Uint8 crossstitch_fabric[3] = { 239, 233, 218 };
static float crossstitch_fabric_shade[STITCH_SIZE][STITCH_SIZE];

/* The two diagonals of the "x", the lower one first: how much they cover
   each pixel of the square, how they shade the thread there (rounded, a
   bit darker below), and the shine on the upper one */
static float crossstitch_cover[2][STITCH_SIZE][STITCH_SIZE];
static float crossstitch_shade[2][STITCH_SIZE][STITCH_SIZE];
static float crossstitch_shine[STITCH_SIZE][STITCH_SIZE];


/* Our local function prototypes: */
/* ------------------------------ */

Uint32 crossstitch_api_version(void);
int crossstitch_init(magic_api * api);
int crossstitch_get_tool_count(magic_api * api);
SDL_Surface * crossstitch_get_icon(magic_api * api, int which);
char * crossstitch_get_name(magic_api * api, int which);
char * crossstitch_get_description(magic_api * api, int which, int mode);
int crossstitch_requires_colors(magic_api * api, int which);
int crossstitch_modes(magic_api * api, int which);
void crossstitch_shutdown(magic_api * api);
void crossstitch_click(magic_api * api, int which, int mode,
                       SDL_Surface * canvas, SDL_Surface * snapshot,
                       int x, int y, SDL_Rect * update_rect);
void crossstitch_drag(magic_api * api, int which, SDL_Surface * canvas,
                      SDL_Surface * snapshot, int ox, int oy, int x, int y,
                      SDL_Rect * update_rect);
void crossstitch_release(magic_api * api, int which,
                         SDL_Surface * canvas, SDL_Surface * snapshot,
                         int x, int y, SDL_Rect * update_rect);
void crossstitch_set_color(magic_api * api, Uint8 r, Uint8 g, Uint8 b);
void crossstitch_switchin(magic_api * api, int which, int mode, SDL_Surface * canvas);
void crossstitch_switchout(magic_api * api, int which, int mode, SDL_Surface * canvas);


/* Setup Functions: */
/* ---------------- */

Uint32 crossstitch_api_version(void)
{
  return(TP_MAGIC_API_VERSION);
}

int crossstitch_init(magic_api * api)
{
  int i, u, v, diag;
  char fname[1024];
  float half_width, pu, pv, dist, cover, bulge;

  for (i = 0; i < NUM_TOOLS; i++)
  {
    snprintf(fname, sizeof(fname), "%s/sounds/magic/%s",
             api->data_directory, crossstitch_snd_filenames[i]);
    crossstitch_snd_effect[i] = Mix_LoadWAV(fname);
  }

  /* Work out the look of a square once */

  half_width = STITCH_SIZE * 0.2;

  for (v = 0; v < STITCH_SIZE; v++)
  {
    for (u = 0; u < STITCH_SIZE; u++)
    {
      if (u == 0 && v == 0)
        crossstitch_fabric_shade[v][u] = 0.80;  /* A hole */
      else if (u == 0 || v == 0)
        crossstitch_fabric_shade[v][u] = 0.95;
      else
        crossstitch_fabric_shade[v][u] = 1.0;

      /* (Pixel centers; the diagonals go corner to corner) */
      pu = u + 0.5;
      pv = v + 0.5;

      for (diag = 0; diag < 2; diag++)
      {
        if (diag == 0)
          dist = (pu > pv ? pu - pv : pv - pu) * 0.7071;
        else
          dist = (pu + pv > STITCH_SIZE ? pu + pv - STITCH_SIZE : STITCH_SIZE - pu - pv) * 0.7071;

        cover = half_width + 0.5 - dist;
        if (cover < 0.0)
          cover = 0.0;
        else if (cover > 1.0)
          cover = 1.0;

        bulge = 1.0 - (dist / half_width) * (dist / half_width);
        if (bulge < 0.0)
          bulge = 0.0;

        crossstitch_cover[diag][v][u] = cover;
        crossstitch_shade[diag][v][u] = (diag == 0 ? 0.85 : 1.0) * (0.75 + 0.30 * bulge);
        if (diag == 1)
          crossstitch_shine[v][u] = 0.12 * bulge * bulge;
      }
    }
  }

  return(1);
}

int crossstitch_get_tool_count(magic_api * api ATTRIBUTE_UNUSED)
{
  return(NUM_TOOLS);
}

SDL_Surface * crossstitch_get_icon(magic_api * api, int which)
{
  char fname[1024];

  snprintf(fname, sizeof(fname), "%s/images/magic/%s",
           api->data_directory, crossstitch_icon_filenames[which]);

  return(IMG_Load(fname));
}

char * crossstitch_get_name(magic_api * api ATTRIBUTE_UNUSED, int which)
{
  return(strdup(gettext(crossstitch_names[which])));
}

char * crossstitch_get_description(magic_api * api ATTRIBUTE_UNUSED, int which, int mode)
{
  return(strdup(gettext(crossstitch_descs[which][mode == MODE_FULLSCREEN ? 1 : 0])));
}

/* The thread takes the colors of the picture */
int crossstitch_requires_colors(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED)
{
  return 0;
}

int crossstitch_modes(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED)
{
  return(MODE_PAINT | MODE_FULLSCREEN);
}

void crossstitch_shutdown(magic_api * api ATTRIBUTE_UNUSED)
{
  int i;

  for (i = 0; i < NUM_TOOLS; i++)
  {
    if (crossstitch_snd_effect[i] != NULL)
      Mix_FreeChunk(crossstitch_snd_effect[i]);
  }
}


/* The Magic Effect Routines! */
/* -------------------------- */

/* Embroider the square whose top left corner is at sx/sy (a multiple of
   STITCH_SIZE), from the picture in 'snapshot' */
static void crossstitch_square(magic_api * api, SDL_Surface * canvas,
                               SDL_Surface * snapshot, int sx, int sy)
{
  int u, v, i, x, y, count, total, diag;
  Uint8 r, g, b;
  Uint8 thread[3] = { 0, 0, 0 }, out[3];
  float sum[3], color[3], a, k, shine;

  /* The thread is the average color of the picture in the square, leaving
     out what's white; a square that's almost all white stays bare (a
     sixteenth is enough to stitch it: a thin line becomes a row of
     stitches) */

  sum[0] = sum[1] = sum[2] = 0.0;
  count = total = 0;

  for (y = sy; y < sy + STITCH_SIZE && y < canvas->h; y++)
  {
    for (x = sx; x < sx + STITCH_SIZE && x < canvas->w; x++)
    {
      total++;
      SDL_GetRGB(api->getpixel(snapshot, x, y), snapshot->format, &r, &g, &b);
      if (r >= WHITE_MIN && g >= WHITE_MIN && b >= WHITE_MIN)
        continue;

      sum[0] += api->sRGB_to_linear(r);
      sum[1] += api->sRGB_to_linear(g);
      sum[2] += api->sRGB_to_linear(b);
      count++;
    }
  }

  if (count > 0)
  {
    thread[0] = api->linear_to_sRGB(sum[0] / count);
    thread[1] = api->linear_to_sRGB(sum[1] / count);
    thread[2] = api->linear_to_sRGB(sum[2] / count);
  }

  for (v = 0; v < STITCH_SIZE; v++)
  {
    for (u = 0; u < STITCH_SIZE; u++)
    {
      for (i = 0; i < 3; i++)
        color[i] = crossstitch_fabric[i] * crossstitch_fabric_shade[v][u];

      if (count * 16 >= total)
      {
        for (diag = 0; diag < 2; diag++)
        {
          a = crossstitch_cover[diag][v][u];
          if (a <= 0.0)
            continue;

          k = crossstitch_shade[diag][v][u];
          shine = (diag == 1 ? crossstitch_shine[v][u] : 0.0);

          for (i = 0; i < 3; i++)
          {
            float t = thread[i] * k + (255 - thread[i]) * shine;

            if (t > 255.0)
              t = 255.0;
            color[i] = color[i] * (1.0 - a) + t * a;
          }
        }
      }

      for (i = 0; i < 3; i++)
        out[i] = (Uint8) (color[i] + 0.5);

      api->putpixel(canvas, sx + u, sy + v,
                    SDL_MapRGB(canvas->format, out[0], out[1], out[2]));
    }
  }
}

/* Embroider the squares around x/y, the ones not done yet in this stroke */
static void crossstitch_line_callback(void * ptr, int which ATTRIBUTE_UNUSED,
                                      SDL_Surface * canvas, SDL_Surface * snapshot,
                                      int x, int y)
{
  magic_api * api = (magic_api *) ptr;
  int sx, sy, cx, cy;
  int left, top;

  /* (Rounding down, also left of or above the canvas) */
  left = (x - BRUSH_RADIUS + STITCH_SIZE * 1000) / STITCH_SIZE * STITCH_SIZE - STITCH_SIZE * 1000;
  top = (y - BRUSH_RADIUS + STITCH_SIZE * 1000) / STITCH_SIZE * STITCH_SIZE - STITCH_SIZE * 1000;

  for (sy = top; sy <= y + BRUSH_RADIUS; sy += STITCH_SIZE)
  {
    for (sx = left; sx <= x + BRUSH_RADIUS; sx += STITCH_SIZE)
    {
      /* Squares with their center in the brush; touched() marks them done
         (it says "done" for squares off the canvas, too) */
      cx = sx + STITCH_SIZE / 2;
      cy = sy + STITCH_SIZE / 2;

      if (api->in_circle(cx - x, cy - y, BRUSH_RADIUS) && !api->touched(sx, sy))
        crossstitch_square(api, canvas, snapshot, sx, sy);
    }
  }
}


/* Functions that respond to events in Tux Paint: */
/* ---------------------------------------------- */

void crossstitch_click(magic_api * api, int which, int mode,
                       SDL_Surface * canvas, SDL_Surface * snapshot,
                       int x, int y, SDL_Rect * update_rect)
{
  int sx, sy;

  if (mode == MODE_PAINT)
  {
    crossstitch_drag(api, which, canvas, snapshot, x, y, x, y, update_rect);
    return;
  }

  /* The entire picture: */

  for (sy = 0; sy < canvas->h; sy += STITCH_SIZE)
    for (sx = 0; sx < canvas->w; sx += STITCH_SIZE)
      crossstitch_square(api, canvas, snapshot, sx, sy);

  update_rect->x = 0;
  update_rect->y = 0;
  update_rect->w = canvas->w;
  update_rect->h = canvas->h;

  api->playsound(crossstitch_snd_effect[which], 128, 255);
}

void crossstitch_drag(magic_api * api, int which, SDL_Surface * canvas,
                      SDL_Surface * snapshot, int ox, int oy, int x, int y,
                      SDL_Rect * update_rect)
{
  api->line((void *) api, which, canvas, snapshot,
            ox, oy, x, y, 1, crossstitch_line_callback);

  if (ox > x) { int tmp = ox; ox = x; x = tmp; }
  if (oy > y) { int tmp = oy; oy = y; y = tmp; }

  /* (Squares reach a bit past the brush) */
  update_rect->x = ox - BRUSH_RADIUS - STITCH_SIZE;
  update_rect->y = oy - BRUSH_RADIUS - STITCH_SIZE;
  update_rect->w = (x + BRUSH_RADIUS + STITCH_SIZE) - update_rect->x;
  update_rect->h = (y + BRUSH_RADIUS + STITCH_SIZE) - update_rect->y;

  api->playsound(crossstitch_snd_effect[which],
                 (x * 255) / canvas->w, // pan
                 255); // distance
}

void crossstitch_release(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED,
                         SDL_Surface * canvas ATTRIBUTE_UNUSED, SDL_Surface * snapshot ATTRIBUTE_UNUSED,
                         int x ATTRIBUTE_UNUSED, int y ATTRIBUTE_UNUSED,
                         SDL_Rect * update_rect ATTRIBUTE_UNUSED)
{
}

void crossstitch_set_color(magic_api * api ATTRIBUTE_UNUSED, Uint8 r ATTRIBUTE_UNUSED,
                           Uint8 g ATTRIBUTE_UNUSED, Uint8 b ATTRIBUTE_UNUSED)
{
}

void crossstitch_switchin(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED,
                          int mode ATTRIBUTE_UNUSED, SDL_Surface * canvas ATTRIBUTE_UNUSED)
{
}

void crossstitch_switchout(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED,
                           int mode ATTRIBUTE_UNUSED, SDL_Surface * canvas ATTRIBUTE_UNUSED)
{
}

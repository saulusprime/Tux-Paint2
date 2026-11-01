/* halftone.c

   Last modified: 2011.07.17
*/


/* Inclusion of header files: */
/* -------------------------- */

#include <stdio.h>
#include <string.h>
#include <libintl.h>
#include <math.h>

#include "tp_magic_api.h"
#include "SDL_image.h"
#include "SDL_mixer.h"

enum {
  TOOL_HALFTONE,
  NUM_TOOLS
};


const char * snd_filenames[NUM_TOOLS] = {
  "halftone.ogg",
};

const char * icon_filenames[NUM_TOOLS] = {
  "halftone.png",
};

const char * names[NUM_TOOLS] = {
  gettext_noop("Halftone"),
};

const char * descs[NUM_TOOLS] = {
  gettext_noop("Click and drag to turn your drawing into a newspaper."),
};

Mix_Chunk * snd_effect[NUM_TOOLS];

static SDL_Surface * canvas_backup;

/* Distance between the dots of each ink, in pixels */
#define DOT_SPACING 6

/* Function Prototypes: */

void halftone_drag(magic_api * api, int which, SDL_Surface * canvas,
	          SDL_Surface * snapshot, int ox, int oy, int x, int y,
		  SDL_Rect * update_rect);
void halftone_line_callback(void * ptr, int which,
                           SDL_Surface * canvas, SDL_Surface * snapshot,
                           int x, int y);
Uint32 halftone_api_version(void);
int halftone_init(magic_api * api);
int halftone_get_tool_count(magic_api * api);
SDL_Surface * halftone_get_icon(magic_api * api, int which);
char * halftone_get_name(magic_api * api, int which);
char * halftone_get_description(magic_api * api, int which, int mode);
int halftone_requires_colors(magic_api * api, int which);
int halftone_modes(magic_api * api, int which);
void halftone_shutdown(magic_api * api);
void halftone_click(magic_api * api, int which, int mode,
	           SDL_Surface * canvas, SDL_Surface * snapshot,
	           int x, int y, SDL_Rect * update_rect);
void halftone_release(magic_api * api, int which,
	           SDL_Surface * canvas, SDL_Surface * snapshot,
	           int x, int y, SDL_Rect * update_rect);
void halftone_set_color(magic_api * api, Uint8 r, Uint8 g, Uint8 b);
void halftone_switchin(magic_api * api, int which, int mode, SDL_Surface * canvas);
void halftone_switchout(magic_api * api, int which, int mode, SDL_Surface * canvas);
void halftone_rgb2cmyk(Uint8 r, Uint8 g, Uint8 b, float cmyk[]);

Uint32 halftone_api_version(void)
{
  return(TP_MAGIC_API_VERSION);
}

int halftone_init(magic_api * api)
{
  int i;
  char fname[1024];

  canvas_backup = NULL;

  for (i = 0; i < NUM_TOOLS; i++)
  {
    snprintf(fname, sizeof(fname),
             "%s/sounds/magic/%s",
	     api->data_directory, snd_filenames[i]);

    snd_effect[i] = Mix_LoadWAV(fname);
  }


  return(1);
}

int halftone_get_tool_count(magic_api * api ATTRIBUTE_UNUSED)
{
  return(NUM_TOOLS);
}

SDL_Surface * halftone_get_icon(magic_api * api, int which)
{
  char fname[1024];

  snprintf(fname, sizeof(fname), "%s/images/magic/%s",
	     api->data_directory, icon_filenames[which]);

  return(IMG_Load(fname));
}

char * halftone_get_name(magic_api * api ATTRIBUTE_UNUSED, int which)
{
  const char * our_name_english;
  const char * our_name_localized;

  our_name_english = names[which];
  our_name_localized = gettext(our_name_english);

  return(strdup(our_name_localized));
}

char * halftone_get_description(magic_api * api ATTRIBUTE_UNUSED, int which, int mode ATTRIBUTE_UNUSED)
{
  const char * our_desc_english;
  const char * our_desc_localized;

  our_desc_english = descs[which];
  our_desc_localized = gettext(our_desc_english);

  return(strdup(our_desc_localized));
}

int halftone_requires_colors(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED)
{
  return 0;
}

int halftone_modes(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED)
{
  return MODE_PAINT;
}

void halftone_shutdown(magic_api * api ATTRIBUTE_UNUSED)
{
  int i;

  for (i = 0; i < NUM_TOOLS; i++)
    Mix_FreeChunk(snd_effect[i]);

  SDL_FreeSurface(canvas_backup);
}

void halftone_click(magic_api * api, int which, int mode ATTRIBUTE_UNUSED,
	           SDL_Surface * canvas, SDL_Surface * snapshot,
	           int x, int y, SDL_Rect * update_rect)
{
  halftone_drag(api, which, canvas, snapshot, x, y, x, y, update_rect);
}

void halftone_drag(magic_api * api, int which, SDL_Surface * canvas,
	          SDL_Surface * snapshot, int ox, int oy, int x, int y,
		  SDL_Rect * update_rect)
{
  api->line((void *) api, which, canvas, snapshot,
            ox, oy, x, y, 4, halftone_line_callback);

  if (ox > x) { int tmp = ox; ox = x; x = tmp; }
  if (oy > y) { int tmp = oy; oy = y; y = tmp; }

  update_rect->x = ox - 16;
  update_rect->y = oy - 16;
  update_rect->w = (x + 16) - update_rect->x;
  update_rect->h = (y + 16) - update_rect->y;

  api->playsound(snd_effect[which],
                 (x * 255) / canvas->w, // pan
	         255); // distance
}

enum {
  CHAN_CYAN,
  CHAN_MAGENTA,
  CHAN_YELLOW,
  CHAN_BLACK,
  NUM_CHANS
};

Uint8 chan_colors[NUM_CHANS][3] = {
  {   0, 255, 255 },
  { 255,   0, 255 },
  { 255, 255,   0 },
  {   0,   0,   0 }
};

/* The angles of the inks' grids of dots, in degrees: the usual ones in
   printing, which make small rosettes instead of a moire */
int chan_angles[NUM_CHANS] = {
  15,
  75,
  0,
  45
};

void halftone_release(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED,
	           SDL_Surface * canvas ATTRIBUTE_UNUSED, SDL_Surface * snapshot ATTRIBUTE_UNUSED,
	           int x ATTRIBUTE_UNUSED, int y ATTRIBUTE_UNUSED, 
                   SDL_Rect * update_rect ATTRIBUTE_UNUSED)

{
}

void halftone_set_color(magic_api * api ATTRIBUTE_UNUSED, Uint8 r ATTRIBUTE_UNUSED, 
                   Uint8 g ATTRIBUTE_UNUSED, Uint8 b ATTRIBUTE_UNUSED)
{
}

void halftone_line_callback(void * ptr, int which ATTRIBUTE_UNUSED,
                           SDL_Surface * canvas, SDL_Surface * snapshot ATTRIBUTE_UNUSED,
                           int x, int y)
{
  Uint8 r, g, b;
  Uint32 total_r, total_g, total_b;
  int xx, yy, channel, sx, sy;
  float px, py, u, v, cu, cv, cx, cy, du, dv, dot, cover;
  float paper[3], cmyk[4], co[NUM_CHANS], si[NUM_CHANS];
  magic_api * api = (magic_api *) ptr;

  /* Lock to grid, centered around mouse */
  x = ((x / 8) - 1) * 8;
  y = ((y / 8) - 1) * 8;

  if (api->touched(x, y)) { return; }

  for (channel = 0; channel < NUM_CHANS; channel++)
  {
    co[channel] = cos(chan_angles[channel] * M_PI / 180.0);
    si[channel] = sin(chan_angles[channel] * M_PI / 180.0);
  }

  /* Each pixel is worked out from where it is on the canvas, so squares
     drawn over each other match */

  for (yy = y; yy < y + 16; yy++) {
    for (xx = x; xx < x + 16; xx++) {
      paper[0] = paper[1] = paper[2] = 1.0;

      for (channel = 0; channel < NUM_CHANS; channel++) {
        /* The dot of this ink's (rotated) grid that the pixel is in, and
           where its center is on the canvas */
        px = xx + 0.5;
        py = yy + 0.5;
        u = px * co[channel] + py * si[channel];
        v = - px * si[channel] + py * co[channel];
        cu = (floor(u / DOT_SPACING) + 0.5) * DOT_SPACING;
        cv = (floor(v / DOT_SPACING) + 0.5) * DOT_SPACING;
        cx = cu * co[channel] - cv * si[channel];
        cy = cu * si[channel] + cv * co[channel];

        /* How much of this ink there is: from the avg color around the dot */
        total_r = total_g = total_b = 0;
        for (sy = -1; sy <= 1; sy++) {
          for (sx = -1; sx <= 1; sx++) {
            SDL_GetRGB(api->getpixel(canvas_backup,
                                     cx + sx * DOT_SPACING / 3,
                                     cy + sy * DOT_SPACING / 3),
                       canvas_backup->format, &r, &g, &b);
            total_r += r;
            total_g += g;
            total_b += b;
          }
        }
        halftone_rgb2cmyk(total_r / 9, total_g / 9, total_b / 9, cmyk);

        /* A dot covering about that much of its square (dots touch at
           about 80%), with a soft edge */
        dot = DOT_SPACING * 0.58 * sqrt(cmyk[channel]);
        du = u - cu;
        dv = v - cv;
        cover = dot - sqrt(du * du + dv * dv) + 0.5;
        if (cover <= 0.0)
          continue;
        if (cover > 1.0)
          cover = 1.0;
        if (dot < 0.5)
          cover = cover * dot * 2.0;  /* (a tiny dot is a fainter one) */

        /* Inks absorb what they don't reflect, as on paper */
        paper[0] *= 1.0 - cover * (1.0 - chan_colors[channel][0] / 255.0);
        paper[1] *= 1.0 - cover * (1.0 - chan_colors[channel][1] / 255.0);
        paper[2] *= 1.0 - cover * (1.0 - chan_colors[channel][2] / 255.0);
      }

      api->putpixel(canvas, xx, yy,
                    SDL_MapRGB(canvas->format, paper[0] * 255.0 + 0.5,
                               paper[1] * 255.0 + 0.5, paper[2] * 255.0 + 0.5));
    }
  }
}

void halftone_switchin(magic_api * api, int which ATTRIBUTE_UNUSED, 
                 int mode ATTRIBUTE_UNUSED, SDL_Surface * canvas)
{
  /* (Tux Paint's canvas may have been resized since) */
  if (canvas_backup != NULL &&
      (canvas_backup->w != canvas->w || canvas_backup->h != canvas->h))
  {
    SDL_FreeSurface(canvas_backup);
    canvas_backup = NULL;
  }

  if (canvas_backup == NULL)
    canvas_backup = SDL_CreateRGBSurface(SDL_ANYFORMAT, api->canvas_w, api->canvas_h, canvas->format->BitsPerPixel, canvas->format->Rmask, canvas->format->Gmask, canvas->format->Bmask, canvas->format->Amask);

  /* FIXME: What to do if it comes back NULL!? :( */

  SDL_BlitSurface(canvas, NULL, canvas_backup, NULL);
}

void halftone_switchout(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED, 
                  int mode ATTRIBUTE_UNUSED, SDL_Surface * canvas ATTRIBUTE_UNUSED)
{
}

void halftone_rgb2cmyk(Uint8 r, Uint8 g, Uint8 b, float cmyk[])
{
  float mincmy, c, m, y, k;

  /* Simple RGB to CMYK math (not worrying about color profiles, etc.),
     based on math found at http://www.javascripter.net/faq/rgb2cmyk.htm
     by Alexei Kourbatov <alexei@kourbatov.com> */

  if (r == 0 && g == 0 && b == 0)
  {
    /* Black */
    c = 0.0;
    m = 0.0;
    y = 0.0;
    k = 1.0;
  }
  else
  {
    c = 1.0 - (((float) r) / 255.0);
    m = 1.0 - (((float) g) / 255.0);
    y = 1.0 - (((float) b) / 255.0);
   
    mincmy = min(c, min(m, y));
    c = (c - mincmy) / (1.0 - mincmy);
    m = (m - mincmy) / (1.0 - mincmy);
    y = (y - mincmy) / (1.0 - mincmy);
    k = mincmy;
  }

  cmyk[0] = c;
  cmyk[1] = m;
  cmyk[2] = y;
  cmyk[3] = k;
}

/*
  magic_run.c: run a Tux Paint "Magic" plugin outside Tux Paint, on a
  picture, and save the result. For looking at what a tool does, and for
  running plugins under AddressSanitizer, without the interface.

  usage: magic_run PLUGIN.so TOOL paint|full IN.bmp|png OUT.bmp
                   [color=R,G,B] [click=X,Y] [drag=X,Y,X,Y...] [seed=N]

  TOOL is the plugin's tool number (0 for the first). With "full", the
  tool is clicked once in its full-image mode (at the first click=, or in
  the middle). With "paint", each click= is a click and release, each
  drag= a click at its first point, a drag through the others, and a
  release, as Tux Paint does them. The canvas is 32 bits, like Tux Paint's.
  The plugin finds its images and sounds under DATA (environment variable,
  default ~/.local/share/tuxpaint/). There is no sound.

  Build: see devtools/magic-test/README.md.
*/

#include <dlfcn.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "SDL.h"
#include "SDL_image.h"
#include "tp_magic_api.h"
#include "rgblinear.h"

/* The plugin's functions */
static Uint32 (*p_api_version)(void);
static int (*p_init)(magic_api *);
static int (*p_get_tool_count)(magic_api *);
static char * (*p_get_name)(magic_api *, int);
static char * (*p_get_description)(magic_api *, int, int);
static int (*p_requires_colors)(magic_api *, int);
static int (*p_modes)(magic_api *, int);
static void (*p_set_color)(magic_api *, Uint8, Uint8, Uint8);
static void (*p_switchin)(magic_api *, int, int, SDL_Surface *);
static void (*p_switchout)(magic_api *, int, int, SDL_Surface *);
static void (*p_click)(magic_api *, int, int, SDL_Surface *, SDL_Surface *, int, int, SDL_Rect *);
static void (*p_drag)(magic_api *, int, SDL_Surface *, SDL_Surface *, int, int, int, int, SDL_Rect *);
static void (*p_release)(magic_api *, int, SDL_Surface *, SDL_Surface *, int, int, SDL_Rect *);
static void (*p_shutdown)(magic_api *);

static SDL_Surface * canvas;
static Uint8 * touched;
static int button_is_down;


/* The API, as Tux Paint gives it (src/tuxpaint.c, src/pixels.c) */

static void api_update_progress_bar(void)
{
}

static void api_special_notify(int flags)
{
  printf("special_notify(%d)\n", flags);
}

static float api_sRGB_to_linear(Uint8 srgb)
{
  return(sRGB_to_linear_table[srgb]);
}

static Uint8 api_linear_to_sRGB(float lin)
{
  return(linear_to_sRGB(lin));
}

static int api_in_circle(int x, int y, int rad)
{
  return((x * x) + (y * y) - (rad * rad) < 0);
}

static Uint32 api_getpixel(SDL_Surface * surface, int x, int y)
{
  if (x < 0) x = 0;
  if (x >= surface->w) x = surface->w - 1;
  if (y < 0) y = 0;
  if (y >= surface->h) y = surface->h - 1;

  return(*(Uint32 *) ((Uint8 *) surface->pixels + y * surface->pitch + x * 4));
}

static void api_putpixel(SDL_Surface * surface, int x, int y, Uint32 pixel)
{
  if (x < 0 || y < 0 || x >= surface->w || y >= surface->h)
    return;

  *(Uint32 *) ((Uint8 *) surface->pixels + y * surface->pitch + x * 4) = pixel;
}

static void api_playsound(Mix_Chunk * snd, int lr, int ud)
{
  (void) snd;
  (void) lr;
  (void) ud;
}

static void api_stopsound(void)
{
}

/* A copy of magic_line_func() */
static void api_line(void * mapi, int which, SDL_Surface * canvas, SDL_Surface * last,
                     int x1, int y1, int x2, int y2, int step,
                     void (*cb)(void *, int, SDL_Surface *, SDL_Surface *, int, int))
{
  int dx, dy, y;
  float m, b;
  int cnt;

  dx = x2 - x1;
  dy = y2 - y1;
  cnt = step - 1;

  if (dx != 0)
  {
    m = ((float) dy) / ((float) dx);
    b = y1 - m * x1;
    dx = (x2 >= x1) ? 1 : -1;

    while (x1 != x2)
    {
      y1 = m * x1 + b;
      y2 = m * (x1 + dx) + b;

      if (y1 > y2)
      {
        for (y = y1; y >= y2; y--)
        {
          cnt = (cnt + 1) % step;
          if (cnt == 0)
            cb(mapi, which, canvas, last, x1, y);
        }
      }
      else
      {
        for (y = y1; y <= y2; y++)
        {
          cnt = (cnt + 1) % step;
          if (cnt == 0)
            cb(mapi, which, canvas, last, x1, y);
        }
      }
      x1 = x1 + dx;
    }
  }
  else
  {
    if (y1 > y2)
    {
      for (y = y1; y >= y2; y--)
      {
        cnt = (cnt + 1) % step;
        if (cnt == 0)
          cb(mapi, which, canvas, last, x1, y);
      }
    }
    else
    {
      for (y = y1; y <= y2; y++)
      {
        cnt = (cnt + 1) % step;
        if (cnt == 0)
          cb(mapi, which, canvas, last, x1, y);
      }
    }
  }
}

static int api_button_down(void)
{
  return(button_is_down);
}

/* Copies of rgbtohsv() and hsvtorgb() */
static void api_rgbtohsv(Uint8 r8, Uint8 g8, Uint8 b8, float *h, float *s, float *v)
{
  float rgb_min, rgb_max, delta, r, g, b;

  r = (r8 / 255.0);
  g = (g8 / 255.0);
  b = (b8 / 255.0);

  rgb_min = r < g ? (r < b ? r : b) : (g < b ? g : b);
  rgb_max = r > g ? (r > b ? r : b) : (g > b ? g : b);
  *v = rgb_max;
  delta = rgb_max - rgb_min;

  if (rgb_max == 0)
  {
    *s = 0;
    *h = -1;
  }
  else
  {
    *s = delta / rgb_max;
    if (r == rgb_max)
      *h = (g - b) / delta;
    else if (g == rgb_max)
      *h = 2 + (b - r) / delta;
    else
      *h = 4 + (r - g) / delta;
    *h = (*h * 60);
    if (*h < 0)
      *h = (*h + 360);
  }
}

static void api_hsvtorgb(float h, float s, float v, Uint8 * r8, Uint8 * g8, Uint8 * b8)
{
  int i;
  float f, p, q, t, r, g, b;

  if (s == 0)
  {
    r = g = b = v;
  }
  else
  {
    h = h / 60;
    i = floor(h);
    f = h - i;
    p = v * (1 - s);
    q = v * (1 - s * f);
    t = v * (1 - s * (1 - f));

    if (i == 0) { r = v; g = t; b = p; }
    else if (i == 1) { r = q; g = v; b = p; }
    else if (i == 2) { r = p; g = v; b = t; }
    else if (i == 3) { r = p; g = q; b = v; }
    else if (i == 4) { r = t; g = p; b = v; }
    else { r = v; g = p; b = q; }
  }

  *r8 = (Uint8) (r * 255);
  *g8 = (Uint8) (g * 255);
  *b8 = (Uint8) (b * 255);
}

/* Like Tux Paint's thumbnail2() (which also keeps transparency): a box
   filter when reducing, nearest pixel when enlarging; good enough here */
static SDL_Surface * api_scale(SDL_Surface * src, int w, int h, int keep_aspect)
{
  SDL_Surface * src32, * dst;
  int x, y, sx, sy, x0, x1, y0, y1, n;
  Uint32 r, g, b, a, p;
  Uint8 pr, pg, pb, pa;

  if (keep_aspect)
  {
    float k = (float) w / src->w;
    if ((float) h / src->h < k)
      k = (float) h / src->h;
    w = src->w * k;
    h = src->h * k;
  }
  if (w < 1) w = 1;
  if (h < 1) h = 1;

  src32 = SDL_CreateRGBSurface(SDL_SWSURFACE, src->w, src->h, 32,
                               0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000);
  SDL_SetAlpha(src, 0, 0);
  SDL_BlitSurface(src, NULL, src32, NULL);
  dst = SDL_CreateRGBSurface(SDL_SWSURFACE, w, h, 32,
                             0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000);

  for (y = 0; y < h; y++)
  {
    for (x = 0; x < w; x++)
    {
      x0 = x * src->w / w;
      x1 = (x + 1) * src->w / w;
      y0 = y * src->h / h;
      y1 = (y + 1) * src->h / h;
      if (x1 <= x0) x1 = x0 + 1;
      if (y1 <= y0) y1 = y0 + 1;
      r = g = b = a = 0;
      n = 0;
      for (sy = y0; sy < y1; sy++)
        for (sx = x0; sx < x1; sx++)
        {
          p = api_getpixel(src32, sx, sy);
          SDL_GetRGBA(p, src32->format, &pr, &pg, &pb, &pa);
          r += pr * pa;
          g += pg * pa;
          b += pb * pa;
          a += pa;
          n++;
        }
      if (a > 0)
        p = SDL_MapRGBA(dst->format, r / a, g / a, b / a, a / n);
      else
        p = SDL_MapRGBA(dst->format, 0, 0, 0, 0);
      api_putpixel(dst, x, y, p);
    }
  }

  SDL_FreeSurface(src32);
  return(dst);
}

static Uint8 api_touched(int x, int y)
{
  Uint8 res;

  if (x < 0 || x >= canvas->w || y < 0 || y >= canvas->h)
    return(1);

  res = touched[(y * canvas->w) + x];
  touched[(y * canvas->w) + x] = 1;
  return(res);
}


static void * plugin_function(void * handle, const char * prefix, const char * name)
{
  char sym[256];
  void * f;

  snprintf(sym, sizeof(sym), "%s_%s", prefix, name);
  f = dlsym(handle, sym);
  if (f == NULL)
  {
    fprintf(stderr, "Missing %s in the plugin\n", sym);
    exit(1);
  }
  return(f);
}

static int parse_ints(const char * s, int * vals, int max)
{
  int n = 0;
  char * end;

  while (n < max && *s)
  {
    vals[n++] = strtol(s, &end, 10);
    if (end == s)
      break;
    s = end;
    if (*s == ',')
      s++;
  }
  return(n);
}

int main(int argc, char * argv[])
{
  void * handle;
  char prefix[256], * slash, * dot;
  magic_api api;
  SDL_Surface * img, * last;
  SDL_Rect update_rect;
  int which, mode, i, j, n, vals[512];
  char * name, * desc;
  const char * data;
  char datadir[1024];

  if (argc < 6)
  {
    fprintf(stderr, "usage: magic_run PLUGIN.so TOOL paint|full IN OUT [color=R,G,B] [click=X,Y] [drag=X,Y,...] [seed=N]\n");
    return(1);
  }

  /* The plugin, and its functions' prefix (its file name) */

  handle = dlopen(argv[1], RTLD_NOW | RTLD_LOCAL);
  if (handle == NULL)
  {
    fprintf(stderr, "%s\n", dlerror());
    return(1);
  }
  slash = strrchr(argv[1], '/');
  snprintf(prefix, sizeof(prefix), "%s", slash ? slash + 1 : argv[1]);
  dot = strchr(prefix, '.');
  if (dot)
    *dot = '\0';

  p_api_version = plugin_function(handle, prefix, "api_version");
  p_init = plugin_function(handle, prefix, "init");
  p_get_tool_count = plugin_function(handle, prefix, "get_tool_count");
  p_get_name = plugin_function(handle, prefix, "get_name");
  p_get_description = plugin_function(handle, prefix, "get_description");
  p_requires_colors = plugin_function(handle, prefix, "requires_colors");
  p_modes = plugin_function(handle, prefix, "modes");
  p_set_color = plugin_function(handle, prefix, "set_color");
  p_switchin = plugin_function(handle, prefix, "switchin");
  p_switchout = plugin_function(handle, prefix, "switchout");
  p_click = plugin_function(handle, prefix, "click");
  p_drag = plugin_function(handle, prefix, "drag");
  p_release = plugin_function(handle, prefix, "release");
  p_shutdown = plugin_function(handle, prefix, "shutdown");

  if (p_api_version() != TP_MAGIC_API_VERSION)
  {
    fprintf(stderr, "API version 0x%x, not 0x%x\n", p_api_version(), TP_MAGIC_API_VERSION);
    return(1);
  }

  if (SDL_Init(0) < 0)
  {
    fprintf(stderr, "SDL_Init: %s\n", SDL_GetError());
    return(1);
  }

  /* The canvas */

  img = IMG_Load(argv[4]);
  if (img == NULL)
  {
    fprintf(stderr, "Can't load %s: %s\n", argv[4], IMG_GetError());
    return(1);
  }
  canvas = SDL_CreateRGBSurface(SDL_SWSURFACE, img->w, img->h, 32,
                                0x00FF0000, 0x0000FF00, 0x000000FF, 0);
  last = SDL_CreateRGBSurface(SDL_SWSURFACE, img->w, img->h, 32,
                              0x00FF0000, 0x0000FF00, 0x000000FF, 0);
  SDL_BlitSurface(img, NULL, canvas, NULL);
  SDL_FreeSurface(img);
  touched = calloc(canvas->w * canvas->h, 1);

  data = getenv("DATA");
  if (data == NULL)
  {
    snprintf(datadir, sizeof(datadir), "%s/.local/share/tuxpaint/", getenv("HOME"));
    data = datadir;
  }

  memset(&api, 0, sizeof(api));
  api.tp_version = "0.9.22";
  api.data_directory = (char *) data;
  api.update_progress_bar = api_update_progress_bar;
  api.special_notify = api_special_notify;
  api.sRGB_to_linear = api_sRGB_to_linear;
  api.linear_to_sRGB = api_linear_to_sRGB;
  api.in_circle = api_in_circle;
  api.getpixel = api_getpixel;
  api.putpixel = api_putpixel;
  api.playsound = api_playsound;
  api.stopsound = api_stopsound;
  api.line = api_line;
  api.button_down = api_button_down;
  api.rgbtohsv = api_rgbtohsv;
  api.hsvtorgb = api_hsvtorgb;
  api.canvas_w = canvas->w;
  api.canvas_h = canvas->h;
  api.scale = api_scale;
  api.touched = api_touched;
  api.load_icon = IMG_Load;  /* (no SVG version here) */

  srand(1);
  for (i = 6; i < argc; i++)
    if (strncmp(argv[i], "seed=", 5) == 0)
      srand(atoi(argv[i] + 5));

  if (!p_init(&api))
  {
    fprintf(stderr, "init() failed\n");
    return(1);
  }

  which = atoi(argv[2]);
  if (which < 0 || which >= p_get_tool_count(&api))
  {
    fprintf(stderr, "The plugin has %d tools\n", p_get_tool_count(&api));
    return(1);
  }
  mode = (strcmp(argv[3], "full") == 0) ? MODE_FULLSCREEN : MODE_PAINT;
  if (mode == MODE_PAINT && !(p_modes(&api, which) & MODE_PAINT))
    mode = p_modes(&api, which) & ~MODE_FULLSCREEN;
  if (!(p_modes(&api, which) & mode))
  {
    fprintf(stderr, "The tool doesn't have that mode (modes: 0x%x)\n", p_modes(&api, which));
    return(1);
  }

  name = p_get_name(&api, which);
  desc = p_get_description(&api, which, mode);
  printf("%s: %s\n", name, desc ? desc : "(no description)");
  free(name);
  free(desc);

  if (p_requires_colors(&api, which))
    p_set_color(&api, 0, 0, 0);
  for (i = 6; i < argc; i++)
  {
    if (strncmp(argv[i], "color=", 6) == 0 && parse_ints(argv[i] + 6, vals, 3) == 3)
      p_set_color(&api, vals[0], vals[1], vals[2]);
  }

  p_switchin(&api, which, mode, canvas);

  if (mode == MODE_FULLSCREEN)
  {
    int x = canvas->w / 2, y = canvas->h / 2;

    for (i = 6; i < argc; i++)
      if (strncmp(argv[i], "click=", 6) == 0 && parse_ints(argv[i] + 6, vals, 2) == 2)
      {
        x = vals[0];
        y = vals[1];
        break;
      }

    SDL_BlitSurface(canvas, NULL, last, NULL);
    memset(touched, 0, canvas->w * canvas->h);
    button_is_down = 1;
    p_click(&api, which, mode, canvas, last, x, y, &update_rect);
    button_is_down = 0;
    p_release(&api, which, canvas, last, x, y, &update_rect);
  }
  else
  {
    for (i = 6; i < argc; i++)
    {
      int is_click = (strncmp(argv[i], "click=", 6) == 0);

      if (!is_click && strncmp(argv[i], "drag=", 5) != 0)
        continue;

      n = parse_ints(argv[i] + (is_click ? 6 : 5), vals, 512) / 2;
      if (n < 1)
        continue;

      /* As Tux Paint: 'last' is the picture before the stroke */
      SDL_BlitSurface(canvas, NULL, last, NULL);
      memset(touched, 0, canvas->w * canvas->h);
      button_is_down = 1;
      memset(&update_rect, 0, sizeof(update_rect));
      p_click(&api, which, mode, canvas, last, vals[0], vals[1], &update_rect);
      for (j = 1; j < n; j++)
      {
        memset(&update_rect, 0, sizeof(update_rect));
        p_drag(&api, which, canvas, last, vals[j * 2 - 2], vals[j * 2 - 1],
               vals[j * 2], vals[j * 2 + 1], &update_rect);
      }
      button_is_down = 0;
      p_release(&api, which, canvas, last, vals[n * 2 - 2], vals[n * 2 - 1], &update_rect);
    }
  }

  p_switchout(&api, which, mode, canvas);
  p_shutdown(&api);

  if (SDL_SaveBMP(canvas, argv[5]) < 0)
  {
    fprintf(stderr, "Can't save %s: %s\n", argv[5], SDL_GetError());
    return(1);
  }

  SDL_FreeSurface(canvas);
  SDL_FreeSurface(last);
  free(touched);
  dlclose(handle);
  SDL_Quit();
  return(0);
}

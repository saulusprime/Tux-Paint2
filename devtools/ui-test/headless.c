/*
  headless.c

  Drive Tux Paint with no window and no screen: an LD_PRELOAD library that,
  with SDL_VIDEODRIVER=dummy, feeds Tux Paint the events of a script and
  saves the screen to BMP files. Nothing shows on the desktop and the
  user's mouse can't spoil a test (see README.md).

  The script (file named by $TP_SCRIPT), one command per line, run in
  order whenever Tux Paint polls for events:

    wait MS          wait MS milliseconds
    click X Y        left button pressed and released at X, Y
    move X Y         mouse moved to X, Y
    key NAME         a key pressed and released (SDL 1.2 name: "right",
                     "escape", "return", "space", "1", …)
    resize W H       the window manager resized the window to W x H
    shot FILE        save the screen as FILE (BMP)
    exit             end Tux Paint at once (_exit(0), no clean-up)

  Lines starting with "#" and empty lines are skipped. It also logs to
  stderr ("headless: …") every sound played on mixer channel 3, the speech
  channel, with its length.

  Build (see README.md):
    cc -shared -fPIC -o headless.so headless.c $(pkg-config --cflags sdl) -ldl

  Copyright (c) 2026 by Paolo Pierno; GPL v2 or later, like Tux Paint.
*/

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dlfcn.h>

#include "SDL.h"
#include "SDL_mixer.h"

#define MAX_LINES 2048

static char *lines[MAX_LINES];
static int num_lines, cur_line, loaded;
static Uint32 wait_until;

/* Events still to hand out for the current command */
static SDL_Event queue[4];
static int queued, queue_pos;

static void load_script(void)
{
  FILE *fi;
  char buf[1024];
  const char *fname = getenv("TP_SCRIPT");

  loaded = 1;
  if (fname == NULL || (fi = fopen(fname, "r")) == NULL)
  {
    fprintf(stderr, "headless: no script (TP_SCRIPT)\n");
    return;
  }

  while (num_lines < MAX_LINES && fgets(buf, sizeof(buf), fi) != NULL)
  {
    buf[strcspn(buf, "\r\n")] = '\0';
    if (buf[0] == '\0' || buf[0] == '#')
      continue;
    lines[num_lines++] = strdup(buf);
  }
  fclose(fi);
}

static SDLKey key_by_name(const char *name)
{
  int k;

  for (k = SDLK_FIRST; k < SDLK_LAST; k++)
    if (strcmp(SDL_GetKeyName((SDLKey) k), name) == 0)
      return (SDLKey) k;

  fprintf(stderr, "headless: no key \"%s\"\n", name);
  return SDLK_UNKNOWN;
}

static void mouse_event(int type, int x, int y)
{
  SDL_Event *e = &queue[queued++];

  memset(e, 0, sizeof(*e));
  e->type = type;
  if (type == SDL_MOUSEMOTION)
  {
    e->motion.x = x;
    e->motion.y = y;
  }
  else
  {
    e->button.button = SDL_BUTTON_LEFT;
    e->button.state = (type == SDL_MOUSEBUTTONDOWN ? SDL_PRESSED : SDL_RELEASED);
    e->button.x = x;
    e->button.y = y;
  }
}

/* Run the script's commands that are due; 1 if events were queued */
static int run_script(void)
{
  char cmd[32], arg[1000];
  int x, y;
  SDL_Surface *screen;
  SDL_Event *e;

  while (cur_line < num_lines && SDL_GetTicks() >= wait_until && queued == 0)
  {
    arg[0] = '\0';
    sscanf(lines[cur_line], "%31s %999[^\n]", cmd, arg);
    fprintf(stderr, "headless: %s\n", lines[cur_line]);
    cur_line++;

    if (strcmp(cmd, "wait") == 0)
      wait_until = SDL_GetTicks() + atoi(arg);
    else if (strcmp(cmd, "click") == 0 && sscanf(arg, "%d %d", &x, &y) == 2)
    {
      mouse_event(SDL_MOUSEMOTION, x, y);
      mouse_event(SDL_MOUSEBUTTONDOWN, x, y);
      mouse_event(SDL_MOUSEBUTTONUP, x, y);
    }
    else if (strcmp(cmd, "move") == 0 && sscanf(arg, "%d %d", &x, &y) == 2)
      mouse_event(SDL_MOUSEMOTION, x, y);
    else if (strcmp(cmd, "key") == 0)
    {
      e = &queue[queued++];
      memset(e, 0, sizeof(*e));
      e->type = SDL_KEYDOWN;
      e->key.state = SDL_PRESSED;
      e->key.keysym.sym = key_by_name(arg);
      queue[queued] = *e;
      queue[queued].type = SDL_KEYUP;
      queue[queued].key.state = SDL_RELEASED;
      queued++;
    }
    else if (strcmp(cmd, "resize") == 0 && sscanf(arg, "%d %d", &x, &y) == 2)
    {
      e = &queue[queued++];
      memset(e, 0, sizeof(*e));
      e->type = SDL_VIDEORESIZE;
      e->resize.w = x;
      e->resize.h = y;
    }
    else if (strcmp(cmd, "shot") == 0)
    {
      screen = SDL_GetVideoSurface();
      if (screen == NULL || SDL_SaveBMP(screen, arg) != 0)
	fprintf(stderr, "headless: can't save %s\n", arg);
    }
    else if (strcmp(cmd, "exit") == 0)
    {
      fflush(stderr);
      _exit(0);
    }
    else
      fprintf(stderr, "headless: what is \"%s\"?\n", lines[cur_line - 1]);
  }

  return queued > 0;
}

int SDL_PollEvent(SDL_Event * event)
{
  static int (*real) (SDL_Event *) = NULL;

  if (real == NULL)
    real = (int (*)(SDL_Event *)) dlsym(RTLD_NEXT, "SDL_PollEvent");
  if (!loaded)
    load_script();

  if (queued > 0 || run_script())
  {
    if (event != NULL)
    {
      *event = queue[queue_pos++];
      if (queue_pos == queued)
	queued = queue_pos = 0;
    }
    return 1;
  }

  return real(event);
}

int Mix_PlayChannelTimed(int channel, Mix_Chunk * chunk, int loops, int ticks)
{
  static int (*real) (int, Mix_Chunk *, int, int) = NULL;

  if (real == NULL)
    real = (int (*)(int, Mix_Chunk *, int, int)) dlsym(RTLD_NEXT, "Mix_PlayChannelTimed");

  if (channel == 3 && chunk != NULL)
    fprintf(stderr, "headless: speech played, %u bytes\n", chunk->alen);

  return real(channel, chunk, loops, ticks);
}

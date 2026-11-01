/*
  puzzle.c v. 1.2

  puzzle, Puzzle tool
  Tux Paint - A simple drawing program for children.

  Author: Adam 'foo-script' Rakowski ; foo-script@o2.pl

  Copyright (c) 2002-2009 by Bill Kendrick and others; see AUTHORS.txt
  bill@newbreedsoftware.com
  http://www.tuxpaint.org/

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
*/


#include <time.h>	//for time()
#include <stdlib.h>
#include "tp_magic_api.h"
#include "SDL_image.h"
#include "SDL_mixer.h"

#define RATIO 5		//change this value to get bigger puzzle

static Mix_Chunk * puzzle_snd;
static int puzzle_gcd=0;		//length of side of each rectangle; 0 is temporary value.
// static int puzzle_rect_q=4;		//quantity of rectangles when using paint mode. Must be an odd value - but it's even!
static SDL_Surface * piece_backup;	//a piece, while two trade places

Uint32 puzzle_api_version(void) ;
int puzzle_init(magic_api * api);
int puzzle_get_tool_count(magic_api * api);
SDL_Surface * puzzle_get_icon(magic_api * api, int which);
char * puzzle_get_name(magic_api * api, int which);
char * puzzle_get_description(magic_api * api, int which, int mode);
void puzzle_release(magic_api * api, int which,
	           SDL_Surface * canvas, SDL_Surface * last,
	           int x, int y, SDL_Rect * update_rect);
void puzzle_shutdown(magic_api * api);
void puzzle_set_color(magic_api * api, Uint8 r, Uint8 g, Uint8 b);
int puzzle_requires_colors(magic_api * api, int which);
void puzzle_switchin(magic_api * api, int which, int mode, SDL_Surface * canvas);
void puzzle_switchout(magic_api * api, int which, int mode, SDL_Surface * canvas);
int puzzle_modes(magic_api * api, int which);
static void puzzle_draw(void * ptr, int which_tool,
               SDL_Surface * canvas, SDL_Surface * snapshot, int x, int y);
void puzzle_drag(magic_api * api, int which, SDL_Surface * canvas,
	          SDL_Surface * last, int ox, int oy, int x, int y,
		  SDL_Rect * update_rect);

void puzzle_click(magic_api * api, int which, int mode,
	           SDL_Surface * canvas, SDL_Surface * last,
	           int x, int y, SDL_Rect * update_rect);
int gcd(int a, int b);

Uint32 puzzle_api_version(void) { return(TP_MAGIC_API_VERSION); }

int puzzle_init(magic_api * api)
{
  char fname[1024];

  snprintf(fname, sizeof(fname), "%s/sounds/magic/puzzle.ogg",
	    api->data_directory);
  puzzle_snd = Mix_LoadWAV(fname);

  return 1 ;
}

int puzzle_get_tool_count(magic_api * api ATTRIBUTE_UNUSED)
{
  return 1;
}

SDL_Surface * puzzle_get_icon(magic_api * api, int which ATTRIBUTE_UNUSED)
{
  char fname[1024];

  snprintf(fname, sizeof(fname), "%s/images/magic/puzzle.png",
	   api->data_directory);

  return(IMG_Load(fname));
}

char * puzzle_get_name(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED)
{
  return(strdup(gettext_noop("Puzzle")));
}


char * puzzle_get_description(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED, int mode)
{
  if (mode==MODE_PAINT)
	return strdup(gettext_noop("Click the part of your picture where would you like a puzzle."));
  return strdup(gettext_noop("Click to make a puzzle in fullscreen mode."));
}

void puzzle_release(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED,
	           SDL_Surface * canvas ATTRIBUTE_UNUSED, SDL_Surface * last ATTRIBUTE_UNUSED,
	           int x ATTRIBUTE_UNUSED, int y ATTRIBUTE_UNUSED, SDL_Rect * update_rect ATTRIBUTE_UNUSED)
{
  api->playsound(puzzle_snd, 128, 255);
}

void puzzle_shutdown(magic_api * api ATTRIBUTE_UNUSED)
{
  if (puzzle_snd != NULL)
    Mix_FreeChunk(puzzle_snd);
}

void puzzle_set_color(magic_api * api ATTRIBUTE_UNUSED, Uint8 r ATTRIBUTE_UNUSED, Uint8 g ATTRIBUTE_UNUSED, Uint8 b ATTRIBUTE_UNUSED)
{
}

int puzzle_requires_colors(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED)
{
  return 0;
}

int gcd(int a, int b)		//greatest common divisor
{
 if (b==0) return a;
 return gcd(b, a%b);
}

void puzzle_switchin(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED, int mode ATTRIBUTE_UNUSED, SDL_Surface * canvas)
{
	int shorter = (canvas->w < canvas->h ? canvas->w : canvas->h);

	/* Pieces whose side divides both sides of the canvas, if that's not
	   too small or too big for it (the canvas changes size with Tux
	   Paint's window); otherwise about 1/12 of its shorter side */
	puzzle_gcd=RATIO*gcd(canvas->w, canvas->h);
	if (puzzle_gcd < shorter / 20 || puzzle_gcd > shorter / 8)
		puzzle_gcd = shorter / 12;
	if (puzzle_gcd < 8)
		puzzle_gcd = 8;

	if (piece_backup != NULL)
		SDL_FreeSurface(piece_backup);
        piece_backup = SDL_CreateRGBSurface(SDL_ANYFORMAT, puzzle_gcd, puzzle_gcd, canvas->format->BitsPerPixel, canvas->format->Rmask, canvas->format->Gmask, canvas->format->Bmask, canvas->format->Amask);
}

void puzzle_switchout(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED, int mode ATTRIBUTE_UNUSED, SDL_Surface * canvas ATTRIBUTE_UNUSED)
{
  SDL_FreeSurface(piece_backup);
  piece_backup = NULL;
}

int puzzle_modes(magic_api * api ATTRIBUTE_UNUSED, int which ATTRIBUTE_UNUSED)
{
  return(MODE_PAINT | MODE_FULLSCREEN);
}

static void puzzle_draw(void * ptr, int which_tool ATTRIBUTE_UNUSED,
               SDL_Surface * canvas, SDL_Surface * snapshot ATTRIBUTE_UNUSED, int x, int y)
{	
  
  	
  magic_api * api = (magic_api *) ptr;
	
  Uint8 r;		//r - random value
  SDL_Rect rect_this, rect_that, rect_backup;

  x = (x / puzzle_gcd) * puzzle_gcd;
  y = (y / puzzle_gcd) * puzzle_gcd;

  if (!api->touched(x, y))
  {
	  srand(rand());
		
	   r=rand()%4;
	  
	   rect_that.x=x;
	   rect_that.y=y;
	  
	   switch(r)
	   {
		case 0:		//upper
			if (y>=puzzle_gcd) 
				rect_that.y=y-puzzle_gcd;
			
		break;
		case 1:		//right
			if (x<canvas->w-puzzle_gcd) 
				rect_that.x=x+puzzle_gcd;
		
		break;
		case 2:		//lower
			if (y<canvas->h-puzzle_gcd) 
				rect_that.y=y+puzzle_gcd;
		
		break;
		case 3:		//left
			if (x>=puzzle_gcd) 
				rect_that.x=x-puzzle_gcd;
		break;
	   }
	   
	   rect_this.x=x;
	   rect_this.y=y;
	   rect_this.h=rect_this.w=puzzle_gcd;
	   rect_that.h=rect_that.w=puzzle_gcd;

  
  /* (Blitting changes the rectangles: clipped to the surfaces) */
  rect_backup = rect_that;
  SDL_BlitSurface(canvas, &rect_backup, piece_backup, NULL);
  rect_backup = rect_that;
  SDL_BlitSurface(canvas, &rect_this, canvas, &rect_backup);
  SDL_BlitSurface(piece_backup, NULL, canvas, &rect_this);
  }
}

/* The entire picture: all the pieces in a random place. The ones at the
   right and bottom edges may be narrower, if the canvas isn't a multiple
   of the pieces' size; they only trade places with pieces of their size */
static void puzzle_shuffle(SDL_Surface * canvas, SDL_Surface * last)
{
  int cols, rows, n, i, j, k, group;
  SDL_Rect * pieces, src, dest;
  int * members;

  cols = (canvas->w + puzzle_gcd - 1) / puzzle_gcd;
  rows = (canvas->h + puzzle_gcd - 1) / puzzle_gcd;
  n = cols * rows;

  pieces = (SDL_Rect *) malloc(sizeof(SDL_Rect) * n);
  members = (int *) malloc(sizeof(int) * n);
  if (pieces == NULL || members == NULL)
  {
    free(pieces);
    free(members);
    return;
  }

  for (i = 0; i < n; i++)
  {
    pieces[i].x = (i % cols) * puzzle_gcd;
    pieces[i].y = (i / cols) * puzzle_gcd;
    pieces[i].w = (pieces[i].x + puzzle_gcd <= canvas->w ? puzzle_gcd : canvas->w - pieces[i].x);
    pieces[i].h = (pieces[i].y + puzzle_gcd <= canvas->h ? puzzle_gcd : canvas->h - pieces[i].y);
  }

  /* Groups: whole pieces, the right column, the bottom row, the corner */
  for (group = 0; group < 4; group++)
  {
    k = 0;
    for (i = 0; i < n; i++)
    {
      int narrow = (pieces[i].w < puzzle_gcd), short_one = (pieces[i].h < puzzle_gcd);

      if (narrow + short_one * 2 == group)
        members[k++] = i;
    }

    /* Shuffle them (Fisher-Yates), then put each piece of the picture
       where its place in the shuffled list says */
    for (i = k - 1; i > 0; i--)
    {
      int tmp;

      j = rand() % (i + 1);
      tmp = members[i];
      members[i] = members[j];
      members[j] = tmp;
    }

    j = 0;
    for (i = 0; i < n; i++)
    {
      int narrow = (pieces[i].w < puzzle_gcd), short_one = (pieces[i].h < puzzle_gcd);

      if (narrow + short_one * 2 != group)
        continue;

      src = pieces[members[j++]];
      dest = pieces[i];
      SDL_BlitSurface(last, &src, canvas, &dest);
    }
  }

  free(pieces);
  free(members);
}

void puzzle_drag(magic_api * api, int which, SDL_Surface * canvas,
	          SDL_Surface * last, int ox ATTRIBUTE_UNUSED, int oy ATTRIBUTE_UNUSED, int x, int y,
		  SDL_Rect * update_rect)
{
	puzzle_draw(api, which, canvas, last, x-puzzle_gcd/2, y-puzzle_gcd/2);

	puzzle_draw(api, which, canvas, last, x-1.5*puzzle_gcd/2, y-puzzle_gcd/2);
	puzzle_draw(api, which, canvas, last, x+0.5*puzzle_gcd, y-puzzle_gcd/2);
	puzzle_draw(api, which, canvas, last, x-puzzle_gcd/2, y-1.5*puzzle_gcd);
	puzzle_draw(api, which, canvas, last, x-puzzle_gcd/2, y+0.5*puzzle_gcd);
	
	update_rect->x=0;
	update_rect->y=0;
	update_rect->h=canvas->h;
	update_rect->w=canvas->w;
}

void puzzle_click(magic_api * api, int which, int mode,
	           SDL_Surface * canvas, SDL_Surface * last,
	           int x, int y, SDL_Rect * update_rect)
{
	if (mode == MODE_FULLSCREEN)
	{
		puzzle_shuffle(canvas, last);

		update_rect->x=0;
		update_rect->y=0;
		update_rect->h=canvas->h;
		update_rect->w=canvas->w;
		return;
	}

	puzzle_drag(api, which, canvas, last, x, y, x, y, update_rect);
}


/*
  progressbar.h

  For Tux Paint
  Progress bar functions

  Copyright (c) 2002-2006 by Bill Kendrick and others
  bill@newbreedsoftware.com
  http://www.newbreedsoftware.com/tuxpaint/

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

  June 14, 2002 - February 18, 2006
  $Id: progressbar.c,v 1.3 2006/08/27 21:00:55 wkendrick Exp $
*/


#include "progressbar.h"
#include "debug.h"

SDL_Surface *img_progress;
int progress_bar_disabled, prog_bar_ctr;

void show_progress_bar(SDL_Surface * screen)
{
  SDL_Rect dest, src;
  int x, w, h;
  static Uint32 oldtime;
  Uint32 newtime;

  if (progress_bar_disabled || img_progress == NULL)
    return;

  /* The image holds two periods of the pattern (65x24, unless scaled) */
  w = img_progress->w / 2;
  h = img_progress->h;

  newtime = SDL_GetTicks();
  if (newtime > oldtime + 15)	// trying not to eat some serious CPU time!
  {
    for (x = 0; x < screen->w; x = x + w)
    {
      src.x = w - (prog_bar_ctr % w);
      src.y = 0;
      src.w = w;
      src.h = h;

      dest.x = x;
      dest.y = screen->h - h;

      SDL_BlitSurface(img_progress, &src, screen, &dest);
    }

    prog_bar_ctr++;

    SDL_UpdateRect(screen, 0, screen->h - h, screen->w, h);
  }
  oldtime = newtime;


  /* (A FIXME here asked to bring back eat_sdl_events(), off since 2006.
     It stays off: this is called from dialogs and Magic tools too, not only
     at startup, and that function quit at once when the window was closed,
     without offering to save, and threw away clicks and keys meant for
     them.) */
}

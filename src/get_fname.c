/*
  get_fname.c

  Copyright (c) 2009
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

  $Id: get_fname.c,v 1.5 2009/11/23 07:45:25 albert Exp $
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "get_fname.h"
#include "debug.h"
#include "compiler.h"

  /* DIR_SAVE: Where is the user's saved directory?
     This is where their saved files are stored
     and where the "current_id.txt" file is saved.
     
     Windows predefines "savedir" as:
     "C:\Documents and Settings\%USERNAME%\Application Data\TuxPaint"
     though it may get overridden with "--savedir" option

     BeOS similarly predefines "savedir" as "./userdata"...

     Macintosh: It's under ~/Library/Application Support/TuxPaint

     Linux & Unix: It's under ~/.tuxpaint

     DIR_DATA: Where is the user's data directory?
     This is where local fonts, brushes and stamps can be found. */


const char *savedir;
const char *datadir;

/* Returns a newly allocated path, which the caller must free().
   (A FIXME here wished for no allocations, with distinct functions per
   directory and thread.  There are only ~30 callers, at startup, in dialogs
   and when saving or opening, never in a drawing loop, so the cost doesn't
   matter; kept as is.) */

char *get_fname(const char *const name, int kind)
{
  char f[512];
  const char *restrict const dir = (kind==DIR_SAVE) ? savedir : datadir;

  // Some mkdir()'s don't like trailing slashes
  snprintf(f, sizeof(f), "%s%c%s", dir, (*name)?'/':'\0', name);

  return strdup(f);
}

/* Print a plain red picture through Tux Paint's PostScript code (see
   ps_check.sh): ps_check WIDTH HEIGHT OUT [PAPERSIZE]
   OUT is a file, or "|COMMAND" to print through a pipe, as Tux Paint does
   (with errno left nonzero beforehand, as it often is in Tux Paint).
   Exit code: 0 if do_ps_save() reported success. */

#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include "SDL.h"
#include "postscript_print.h"

int main(int argc, char **argv)
{
  SDL_Surface *surf;
  FILE *fi;
  int is_pipe;

  if (argc < 4)
  {
    fprintf(stderr, "usage: %s WIDTH HEIGHT OUT.ps [PAPERSIZE]\n", argv[0]);
    return 2;
  }

  surf = SDL_CreateRGBSurface(SDL_SWSURFACE, atoi(argv[1]), atoi(argv[2]), 32,
                              0xff0000, 0x00ff00, 0x0000ff, 0);
  is_pipe = (argv[3][0] == '|');
  fi = is_pipe ? popen(argv[3] + 1, "w") : fopen(argv[3], "w");
  if (surf == NULL || fi == NULL)
    return 2;

  SDL_FillRect(surf, NULL, SDL_MapRGB(surf->format, 255, 0, 0));

  signal(SIGPIPE, SIG_IGN);	/* (Tux Paint handles it too) */
  errno = ENOENT;
  return !do_ps_save(fi, argv[3], surf, argc > 4 ? argv[4] : NULL, is_pipe);
}

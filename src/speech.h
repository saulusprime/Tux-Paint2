/*
  speech.h

  For Tux Paint
  Reading text aloud (the "Learn" tool's instructions)

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

#ifndef SPEECH_H
#define SPEECH_H

/* The text becomes sound in a thread, played through SDL_mixer on its own
   channel; Tux Paint's mute and "nosound" are up to the caller.

   The voice is, in this order:
   - the command given to speech_init(), if any: it is run with /bin/sh,
     gets the text (UTF-8) on its standard input and must write a sound
     file (e.g. WAV) to its standard output; "%l" in it becomes the
     language code (e.g. "it", "pt-br");
   - eSpeak NG (libespeak-ng.so.1, loaded when first needed: no build
     dependency).
*/

/* Mixer channel used for speech (0-2 are Tux Paint's sounds) */
#define SPEECH_CHANNEL 3

/* Choose the voice; command may be NULL. Doesn't load anything yet. */
void speech_init(const char *command);

/* Whether a voice can be used at all (loads eSpeak NG the first time) */
int speech_available(void);

/* Say text, in language lang ("it", "en", "pt_BR"…), stopping anything
   said before. Returns at once: the sound starts from speech_poll(). */
void speech_say(const char *text, const char *lang);

/* Stop speaking (and drop what is being prepared) */
void speech_stop(void);

/* To call often from event loops: starts the sound once it is ready */
void speech_poll(void);

/* Still preparing or playing something */
int speech_busy(void);

/* At exit */
void speech_quit(void);

#endif

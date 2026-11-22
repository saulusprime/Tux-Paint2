/*
  speech.c

  For Tux Paint
  Reading text aloud (the "Learn" tool's instructions): see speech.h

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
#include <ctype.h>

#include "SDL.h"
#include "speech.h"

#if defined(NOSOUND) || defined(WIN32)

/* No mixer to play it, or no fork() and dlopen(): no voice */

void speech_init(const char *command)
{
  (void) command;
}

int speech_available(void)
{
  return 0;
}

void speech_say(const char *text, const char *lang)
{
  (void) text;
  (void) lang;
}

void speech_stop(void)
{
}

void speech_poll(void)
{
}

int speech_busy(void)
{
  return 0;
}

void speech_quit(void)
{
}

#else

#include <errno.h>
#include <signal.h>
#include <unistd.h>
#include <poll.h>
#include <dlfcn.h>
#include <sys/types.h>
#include <sys/wait.h>

#include "SDL_thread.h"
#include "SDL_mixer.h"

/* A command's sound can't be bigger than this */
#define MAX_COMMAND_OUTPUT (32 * 1024 * 1024)

/* Words per minute: a bit slower than eSpeak NG's 175, for children */
#define ESPEAK_RATE 150


/* --- What the main thread and the worker share (under lock) --- */

static SDL_mutex *lock;

/* Bumped by every speech_say() and speech_stop(): what the worker makes
   for an older one is dropped */
static unsigned int current_id;

/* The next text to make into sound */
static char *pending_text, *pending_lang;
static unsigned int pending_id;

/* Sound made, not yet played */
static Uint8 *ready_data;
static size_t ready_len;
static unsigned int ready_id;

static SDL_Thread *worker;
static int worker_running;


/* --- Main thread only --- */

static char *speech_command;
static Mix_Chunk *playing_chunk;
static int command_warned;


/* --- eSpeak NG, loaded with dlopen() --- */

/* (From espeak-ng/speak_lib.h) */
#define AUDIO_OUTPUT_SYNCHRONOUS 2
#define espeakINITIALIZE_DONT_EXIT 0x8000
#define espeakRATE 1
#define POS_CHARACTER 1
#define espeakCHARS_UTF8 1
#define espeakENDPAUSE 0x1000
#define EE_OK 0

typedef int (*espeak_callback) (short *wav, int numsamples, void *events);

static void *espeak_lib;
static int espeak_loaded;	/* 0: not tried yet, 1: loaded, -1: not there */
static int espeak_rate;		/* samples per second; 0 before espeak_Initialize(), -1 if it failed */

static int (*p_espeak_Initialize) (int output, int buflength, const char *path, int options);
static void (*p_espeak_SetSynthCallback) (espeak_callback cb);
static int (*p_espeak_SetVoiceByName) (const char *name);
static int (*p_espeak_SetParameter) (int parameter, int value, int relative);
static int (*p_espeak_Synth) (const void *text, size_t size, unsigned int position,
			      int position_type, unsigned int end_position,
			      unsigned int flags, unsigned int *unique_identifier,
			      void *user_data);
static int (*p_espeak_Terminate) (void);


/* --- The worker's own --- */

/* Sound being made by eSpeak NG's callback */
static Uint8 *synth_buf;
static size_t synth_len, synth_cap;
static unsigned int synth_id;
static int synth_failed;


static int still_wanted(unsigned int id)
{
  int wanted;

  SDL_mutexP(lock);
  wanted = (id == current_id);
  SDL_mutexV(lock);

  return wanted;
}

static int append(Uint8 ** buf, size_t * len, size_t * cap, const void *data, size_t n)
{
  Uint8 *bigger;
  size_t new_cap;

  if (*len + n > *cap)
  {
    new_cap = (*cap ? *cap * 2 : 65536);
    while (new_cap < *len + n)
      new_cap *= 2;
    bigger = realloc(*buf, new_cap);
    if (bigger == NULL)
      return 0;
    *buf = bigger;
    *cap = new_cap;
  }
  memcpy(*buf + *len, data, n);
  *len += n;

  return 1;
}

/* A language code as eSpeak NG and most commands like it: "pt_BR" -> "pt-br";
   anything odd is dropped (it ends up in a shell command) */
static void normalize_lang(const char *lang, char *out, size_t size)
{
  size_t n = 0;

  for (; lang != NULL && *lang != '\0' && *lang != '.' && *lang != '@' && n + 1 < size; lang++)
  {
    if (isalnum((unsigned char) *lang))
      out[n++] = tolower((unsigned char) *lang);
    else if (*lang == '_' || *lang == '-')
      out[n++] = '-';
  }
  out[n] = '\0';

  if (n == 0)
    snprintf(out, size, "en");
}

static void put_le(Uint8 * p, Uint32 value, int bytes)
{
  int i;

  for (i = 0; i < bytes; i++)
    p[i] = (value >> (8 * i)) & 0xff;
}

/* 16-bit mono PCM as a WAV file in memory */
static Uint8 *make_wav(const Uint8 * pcm, size_t len, int rate, size_t * wav_len)
{
  Uint8 *wav = malloc(44 + len);

  if (wav == NULL)
    return NULL;

  memcpy(wav, "RIFF", 4);
  put_le(wav + 4, 36 + len, 4);
  memcpy(wav + 8, "WAVEfmt ", 8);
  put_le(wav + 16, 16, 4);	/* size of the format */
  put_le(wav + 20, 1, 2);	/* PCM */
  put_le(wav + 22, 1, 2);	/* mono */
  put_le(wav + 24, rate, 4);
  put_le(wav + 28, rate * 2, 4);	/* bytes per second */
  put_le(wav + 32, 2, 2);	/* bytes per sample */
  put_le(wav + 34, 16, 2);	/* bits per sample */
  memcpy(wav + 36, "data", 4);
  put_le(wav + 40, len, 4);
  memcpy(wav + 44, pcm, len);

  *wav_len = 44 + len;
  return wav;
}


/* --- eSpeak NG --- */

static int load_espeak(void)
{
  if (espeak_loaded != 0)
    return espeak_loaded > 0;

  espeak_loaded = -1;

  espeak_lib = dlopen("libespeak-ng.so.1", RTLD_NOW | RTLD_LOCAL);
  if (espeak_lib == NULL)
  {
    fprintf(stderr, "Speech: eSpeak NG is not there (%s)\n", dlerror());
    return 0;
  }

  p_espeak_Initialize = dlsym(espeak_lib, "espeak_Initialize");
  p_espeak_SetSynthCallback = dlsym(espeak_lib, "espeak_SetSynthCallback");
  p_espeak_SetVoiceByName = dlsym(espeak_lib, "espeak_SetVoiceByName");
  p_espeak_SetParameter = dlsym(espeak_lib, "espeak_SetParameter");
  p_espeak_Synth = dlsym(espeak_lib, "espeak_Synth");
  p_espeak_Terminate = dlsym(espeak_lib, "espeak_Terminate");

  if (p_espeak_Initialize == NULL || p_espeak_SetSynthCallback == NULL ||
      p_espeak_SetVoiceByName == NULL || p_espeak_SetParameter == NULL ||
      p_espeak_Synth == NULL || p_espeak_Terminate == NULL)
  {
    fprintf(stderr, "Speech: libespeak-ng.so.1 lacks a function\n");
    dlclose(espeak_lib);
    espeak_lib = NULL;
    return 0;
  }

  espeak_loaded = 1;
  return 1;
}

static int espeak_got_samples(short *wav, int numsamples, void *events)
{
  (void) events;

  /* (Returning 1 stops it: something else is wanted now) */
  if (!still_wanted(synth_id))
    return 1;

  if (wav != NULL && numsamples > 0 &&
      !append(&synth_buf, &synth_len, &synth_cap, wav, (size_t) numsamples * 2))
  {
    synth_failed = 1;
    return 1;
  }

  return 0;
}

/* In the worker */
static Uint8 *synth_espeak(const char *text, const char *lang, unsigned int id, size_t * len)
{
  char voice[32], *dash;
  Uint8 *wav;
  int rate;

  /* (Only the worker writes espeak_rate, under the lock: speech_available()
     reads it) */
  if (espeak_rate == 0)
  {
    rate = p_espeak_Initialize(AUDIO_OUTPUT_SYNCHRONOUS, 0, NULL, espeakINITIALIZE_DONT_EXIT);
    if (rate <= 0)
    {
      fprintf(stderr, "Speech: eSpeak NG couldn't start\n");
      rate = -1;
    }
    else
    {
      p_espeak_SetSynthCallback(espeak_got_samples);
      p_espeak_SetParameter(espeakRATE, ESPEAK_RATE, 0);
    }
    SDL_mutexP(lock);
    espeak_rate = rate;
    SDL_mutexV(lock);
  }
  if (espeak_rate < 0)
    return NULL;

  /* The language's voice, else its main one ("pt-br" -> "pt"), else English */
  normalize_lang(lang, voice, sizeof(voice));
  if (p_espeak_SetVoiceByName(voice) != EE_OK)
  {
    dash = strchr(voice, '-');
    if (dash != NULL)
      *dash = '\0';
    if (dash == NULL || p_espeak_SetVoiceByName(voice) != EE_OK)
      p_espeak_SetVoiceByName("en");
  }

  synth_buf = NULL;
  synth_len = synth_cap = 0;
  synth_id = id;
  synth_failed = 0;

  p_espeak_Synth(text, strlen(text) + 1, 0, POS_CHARACTER, 0,
		 espeakCHARS_UTF8 | espeakENDPAUSE, NULL, NULL);

  wav = NULL;
  if (!synth_failed && synth_len > 0 && still_wanted(id))
    wav = make_wav(synth_buf, synth_len, espeak_rate, len);

  free(synth_buf);
  synth_buf = NULL;

  return wav;
}


/* --- A command --- */

/* The command with "%l" replaced by the language ("%%" is "%") */
static char *expand_command(const char *command, const char *lang)
{
  char code[32], *out;
  size_t n = 0, size;
  const char *p;

  normalize_lang(lang, code, sizeof(code));

  size = strlen(command) + 1;
  for (p = command; *p != '\0'; p++)
    if (p[0] == '%' && p[1] == 'l')
      size += strlen(code);

  out = malloc(size);
  if (out == NULL)
    return NULL;

  for (p = command; *p != '\0'; p++)
  {
    if (p[0] == '%' && p[1] == 'l')
    {
      strcpy(out + n, code);
      n += strlen(code);
      p++;
    }
    else if (p[0] == '%' && p[1] == '%')
    {
      out[n++] = '%';
      p++;
    }
    else
      out[n++] = *p;
  }
  out[n] = '\0';

  return out;
}

/* Stop a command, and whatever it started (its process group) */
static void kill_command(pid_t pid)
{
  if (kill(-pid, SIGKILL) != 0)
    kill(pid, SIGKILL);
}

/* In the worker: the text on the command's input, the sound from its output */
static Uint8 *synth_command(const char *text, const char *lang, unsigned int id, size_t * len)
{
  int to_child[2], from_child[2], status = 0, killed = 0, reaped = 0, ready;
  char *cmd;
  pid_t pid, w;
  Uint8 *buf = NULL, chunk[16384];
  size_t buf_len = 0, buf_cap = 0, done;
  ssize_t got;
  struct pollfd pfd;

  cmd = expand_command(speech_command, lang);
  if (cmd == NULL)
    return NULL;

  if (pipe(to_child) != 0)
  {
    free(cmd);
    return NULL;
  }
  if (pipe(from_child) != 0)
  {
    close(to_child[0]);
    close(to_child[1]);
    free(cmd);
    return NULL;
  }

  pid = fork();
  if (pid == 0)
  {
    /* (Only async-signal-safe calls until exec. A process group of its
       own: stopping it stops a pipeline too.) */
    setpgid(0, 0);
    dup2(to_child[0], 0);
    dup2(from_child[1], 1);
    close(to_child[0]);
    close(to_child[1]);
    close(from_child[0]);
    close(from_child[1]);
    signal(SIGPIPE, SIG_DFL);
    execl("/bin/sh", "sh", "-c", cmd, (char *) NULL);
    _exit(127);
  }

  free(cmd);
  close(to_child[0]);
  close(from_child[1]);

  if (pid < 0)
  {
    close(to_child[1]);
    close(from_child[0]);
    return NULL;
  }
  setpgid(pid, pid);		/* (as the child does: whichever comes first) */

  /* (Writing to a command that doesn't read it all gives EPIPE, not death
     by SIGPIPE: Tux Paint catches it, see signal_handler(), and
     speech_init() ignores it until then) */
  for (done = 0; done < strlen(text);)
  {
    got = write(to_child[1], text + done, strlen(text) - done);
    if (got < 0 && errno == EINTR)
      continue;
    if (got <= 0)
      break;
    done += got;
  }
  if (write(to_child[1], "\n", 1) < 0)
  {
    /* (It didn't want the text) */
  }
  close(to_child[1]);

  pfd.fd = from_child[0];
  pfd.events = POLLIN;
  for (;;)
  {
    if (!still_wanted(id))
    {
      kill_command(pid);
      killed = 1;
      break;
    }

    ready = poll(&pfd, 1, 100);
    if (ready == 0 || (ready < 0 && errno == EINTR))
      continue;
    if (ready < 0)
      break;

    got = read(from_child[0], chunk, sizeof(chunk));
    if (got < 0 && errno == EINTR)
      continue;
    if (got <= 0)
      break;

    if (buf_len + got > MAX_COMMAND_OUTPUT ||
	!append(&buf, &buf_len, &buf_cap, chunk, got))
    {
      kill_command(pid);
      killed = 1;
      break;
    }
  }
  close(from_child[0]);

  /* Its exit status, without waiting for good: a command may close its
     output and still go on (then it's stopped if no longer wanted) */
  while (!reaped)
  {
    w = waitpid(pid, &status, WNOHANG);
    if (w == pid)
      reaped = 1;
    else if (w < 0 && errno != EINTR)
      break;			/* (e.g. SIGCHLD ignored: there is no status) */
    else if (w == 0)
    {
      if (!killed && !still_wanted(id))
      {
	kill_command(pid);
	killed = 1;
      }
      SDL_Delay(20);
    }
  }

  if (killed || buf_len == 0 ||
      (reaped && (!WIFEXITED(status) || WEXITSTATUS(status) != 0)))
  {
    if (!killed)
      fprintf(stderr, "Speech: the speech command gave no sound (exit status %d)\n",
	      reaped && WIFEXITED(status) ? WEXITSTATUS(status) : -1);
    free(buf);
    return NULL;
  }

  *len = buf_len;
  return buf;
}


/* --- The worker --- */

static int worker_main(void *data)
{
  char *text, *lang;
  unsigned int id;
  Uint8 *sound;
  size_t len;

  (void) data;

  for (;;)
  {
    SDL_mutexP(lock);
    if (pending_text == NULL)
    {
      worker_running = 0;
      SDL_mutexV(lock);
      return 0;
    }
    text = pending_text;
    lang = pending_lang;
    id = pending_id;
    pending_text = pending_lang = NULL;
    SDL_mutexV(lock);

    len = 0;
    if (speech_command != NULL)
      sound = synth_command(text, lang, id, &len);
    else
      sound = synth_espeak(text, lang, id, &len);

    free(text);
    free(lang);

    SDL_mutexP(lock);
    if (sound != NULL && id == current_id)
    {
      free(ready_data);
      ready_data = sound;
      ready_len = len;
      ready_id = id;
    }
    else
      free(sound);
    SDL_mutexV(lock);
  }
}


/* --- For Tux Paint --- */

void speech_init(const char *command)
{
  struct sigaction sa;

  if (lock == NULL)
    lock = SDL_CreateMutex();

  free(speech_command);
  speech_command = NULL;

  if (command != NULL && command[0] != '\0')
  {
    speech_command = strdup(command);

    /* Writing to a command that is gone mustn't kill Tux Paint (it gets
       EPIPE instead; Tux Paint later catches SIGPIPE itself); the command
       gets the default back */
    if (sigaction(SIGPIPE, NULL, &sa) == 0 && sa.sa_handler == SIG_DFL)
      signal(SIGPIPE, SIG_IGN);
  }
}

int speech_available(void)
{
  int rate;

  if (lock == NULL)
    return 0;

  if (speech_command != NULL)
    return 1;

  if (!load_espeak())
    return 0;

  SDL_mutexP(lock);
  rate = espeak_rate;
  SDL_mutexV(lock);

  return rate >= 0;
}

void speech_stop(void)
{
  if (lock == NULL)
    return;

  SDL_mutexP(lock);
  current_id++;
  free(pending_text);
  free(pending_lang);
  pending_text = pending_lang = NULL;
  free(ready_data);
  ready_data = NULL;
  SDL_mutexV(lock);

  if (playing_chunk != NULL)
  {
    Mix_HaltChannel(SPEECH_CHANNEL);
    Mix_FreeChunk(playing_chunk);
    playing_chunk = NULL;
  }
}

void speech_say(const char *text, const char *lang)
{
  char *text_copy, *lang_copy;

  if (text == NULL || text[0] == '\0' || !speech_available())
    return;

  speech_stop();

  text_copy = strdup(text);
  lang_copy = strdup(lang != NULL ? lang : "en");
  if (text_copy == NULL || lang_copy == NULL)
  {
    free(text_copy);
    free(lang_copy);
    return;
  }

  SDL_mutexP(lock);

  pending_text = text_copy;
  pending_lang = lang_copy;
  pending_id = current_id;

  if (!worker_running)
  {
    /* (The last one has finished, or is about to: it needs nothing more
       from us) */
    if (worker != NULL)
      SDL_WaitThread(worker, NULL);

    worker_running = 1;
    worker = SDL_CreateThread(worker_main, NULL);
    if (worker == NULL)
    {
      worker_running = 0;
      free(pending_text);
      free(pending_lang);
      pending_text = pending_lang = NULL;
    }
  }

  SDL_mutexV(lock);
}

void speech_poll(void)
{
  Uint8 *data = NULL;
  size_t len = 0;
  int wanted = 0;
  Mix_Chunk *chunk;

  if (lock == NULL)
    return;

  SDL_mutexP(lock);
  if (ready_data != NULL)
  {
    data = ready_data;
    len = ready_len;
    wanted = (ready_id == current_id);
    ready_data = NULL;
  }
  SDL_mutexV(lock);

  if (data != NULL)
  {
    if (wanted)
    {
      chunk = Mix_LoadWAV_RW(SDL_RWFromMem(data, len), 1);
      if (chunk == NULL)
      {
	if (!command_warned)
	  fprintf(stderr, "Speech: can't play the sound (%s)\n", Mix_GetError());
	command_warned = 1;
      }
      else
      {
	if (playing_chunk != NULL)
	{
	  Mix_HaltChannel(SPEECH_CHANNEL);
	  Mix_FreeChunk(playing_chunk);
	}
	playing_chunk = chunk;
	Mix_Volume(SPEECH_CHANNEL, MIX_MAX_VOLUME);
	Mix_PlayChannel(SPEECH_CHANNEL, playing_chunk, 0);
      }
    }
    free(data);
  }

  /* (Finished, or halted by someone else, e.g. muting) */
  if (playing_chunk != NULL && !Mix_Playing(SPEECH_CHANNEL))
  {
    Mix_FreeChunk(playing_chunk);
    playing_chunk = NULL;
  }
}

int speech_busy(void)
{
  int busy;

  if (lock == NULL)
    return 0;

  busy = (playing_chunk != NULL && Mix_Playing(SPEECH_CHANNEL));

  SDL_mutexP(lock);
  busy = busy || pending_text != NULL || ready_data != NULL || worker_running;
  SDL_mutexV(lock);

  return busy;
}

void speech_quit(void)
{
  if (lock == NULL)
    return;

  /* (The worker stops what it was making, and finds nothing more) */
  speech_stop();
  if (worker != NULL)
  {
    SDL_WaitThread(worker, NULL);
    worker = NULL;
  }

  if (espeak_rate > 0)
    p_espeak_Terminate();
  espeak_rate = 0;
  if (espeak_lib != NULL)
    dlclose(espeak_lib);
  espeak_lib = NULL;
  espeak_loaded = 0;

  free(speech_command);
  speech_command = NULL;

  SDL_DestroyMutex(lock);
  lock = NULL;
}

#endif

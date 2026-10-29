/* Print a backtrace on fatal signals, for processes we can't run under gdb.

   gcc -shared -fPIC -o segv_backtrace.so segv_backtrace.c
   LD_PRELOAD=./segv_backtrace.so tuxpaint ...

   Signal handlers survive fork(), so this also covers child processes.
   Translate "binary(+0xOFFSET)" frames with: addr2line -f -e binary 0xOFFSET */

#define _GNU_SOURCE
#include <execinfo.h>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

static void handler(int sig)
{
  void *frames[64];
  char msg[80];
  int n, len;

  n = backtrace(frames, 64);
  len = snprintf(msg, sizeof msg, "\n=== signal %d in pid %d (parent %d) ===\n",
                 sig, (int) getpid(), (int) getppid());
  write(2, msg, len);
  backtrace_symbols_fd(frames, n, 2);

  signal(sig, SIG_DFL);
  raise(sig);
}

__attribute__((constructor)) static void install(void)
{
  signal(SIGSEGV, handler);
  signal(SIGBUS, handler);
  signal(SIGABRT, handler);
  signal(SIGFPE, handler);
}

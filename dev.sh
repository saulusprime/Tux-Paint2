#!/bin/bash
# Build, install and run Tux Paint for local development.
#
# Usage: ./dev.sh {build|install|run|uninstall|clean} [tuxpaint options...]
#
#   build      compile (rebuilds from scratch if PREFIX changed)
#   install    build, then install under PREFIX with a menu launcher
#   run        install, then start Tux Paint in a window
#   uninstall  remove everything installed under PREFIX
#   clean      remove build artifacts
#
# Environment:
#   PREFIX     install prefix (default: $HOME/.local)
#   JOBS       parallel make jobs (default: number of CPUs)
#
# From the VS Code Flatpak sandbox the script re-runs itself on the host,
# where the build dependencies are installed.

set -e

SELF="$(realpath "$0")"

if [ -f /.flatpak-info ]; then
  exec flatpak-spawn --host --env=PREFIX="${PREFIX:-}" --env=JOBS="${JOBS:-}" \
    bash "$SELF" "$@"
fi

cd "$(dirname "$SELF")"

PREFIX="${PREFIX:-$HOME/.local}"
JOBS="${JOBS:-$(nproc)}"

# Install paths are compiled into the binary, but the Makefile doesn't
# rebuild when PREFIX changes: remember the one used for the last build.
STAMP=obj/.build-prefix

# COMPLETIONDIR defaults to /etc; GNOME_PREFIX and KDE_ICON_PREFIX come from
# gnome-config/kde-config, which modern desktops no longer ship.
MAKE_VARS=(
  PREFIX="$PREFIX"
  COMPLETIONDIR="$PREFIX/share/bash-completion/completions"
  GNOME_PREFIX="$PREFIX"
  KDE_ICON_PREFIX="$PREFIX/share/icons"
)

do_build() {
  if [ "$(cat "$STAMP" 2>/dev/null)" != "$PREFIX" ]; then
    echo "PREFIX is now $PREFIX: rebuilding from scratch"
    make clean > /dev/null
  fi
  make -j"$JOBS" "${MAKE_VARS[@]}"
  echo "$PREFIX" > "$STAMP"
}

do_install() {
  do_build
  make "${MAKE_VARS[@]}" install
  # The stock launcher runs "tuxpaint" from $PATH, which may lack $PREFIX/bin
  sed -i "s|^Exec=tuxpaint\$|Exec=$PREFIX/bin/tuxpaint|" \
    "$PREFIX/share/applications/tuxpaint.desktop"
}

case "$1" in
  build)
    do_build
    ;;
  install)
    do_install
    ;;
  run)
    shift
    do_install > /dev/null
    exec "$PREFIX/bin/tuxpaint" --windowed "$@"
    ;;
  uninstall)
    make "${MAKE_VARS[@]}" uninstall
    ;;
  clean)
    make clean
    rm -f "$STAMP"
    ;;
  *)
    sed -n '2,/^$/s/^# \{0,1\}//p' "$SELF"
    exit 1
    ;;
esac

#!/bin/bash
# Build, install and run Tux Paint for local development.
#
# Usage: ./dev.sh {build|install|run|stamps|uninstall|clean} [arguments...]
#
#   build      compile (rebuilds from scratch if PREFIX changed)
#   install    build, then install under PREFIX with a menu launcher
#   run        install, then start Tux Paint in a window; arguments are
#              passed to Tux Paint
#   stamps     add the full stamp collection under PREFIX (the repository
#              only has a few): from a .deb file or a "stamps" folder given
#              as argument, or else from Debian's tuxpaint-stamps-default
#              package, downloaded but not installed
#   uninstall  remove everything installed under PREFIX, stamps included
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

# Paths given as arguments are relative to where the script was started
START_DIR="$PWD"
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
  # The stock launcher (and its "Full screen" action) runs "tuxpaint" from
  # $PATH, which may lack $PREFIX/bin
  sed -i -e "s|^Exec=tuxpaint\$|Exec=$PREFIX/bin/tuxpaint|" \
    -e "s|^Exec=tuxpaint |Exec=$PREFIX/bin/tuxpaint |" \
    "$PREFIX/share/applications/tuxpaint.desktop"
}

# Only data files are copied: nothing from the package or folder is run.
# A folder is accepted if it is named "stamps" or has one inside, as in the
# tuxpaint-stamps source archive.
do_stamps() {
  local src="$1"
  if [ -n "$src" ]; then
    [ "${src#/}" != "$src" ] || src="$START_DIR/$src"
    if [ ! -e "$src" ]; then
      echo "$1: not found" >&2
      exit 1
    fi
  fi
  # Global, not local: the trap runs when the script exits
  STAMPS_TMP="$(mktemp -d)"
  trap 'rm -rf "$STAMPS_TMP"' EXIT
  if [ -z "$src" ]; then
    (cd "$STAMPS_TMP" && apt-get download tuxpaint-stamps-default)
    src="$(echo "$STAMPS_TMP"/*.deb)"
  fi
  if [ -f "$src" ]; then
    dpkg-deb -x "$src" "$STAMPS_TMP/root"
    src="$STAMPS_TMP/root/usr/share/tuxpaint/stamps"
  fi
  [ ! -d "$src/stamps" ] || src="$src/stamps"
  if [ ! -d "$src" ] || [ "$(basename "$src")" != stamps ]; then
    echo "No stamps folder in ${1:-the package}" >&2
    exit 1
  fi
  install -d "$PREFIX/share/tuxpaint/stamps"
  cp -R "$src/." "$PREFIX/share/tuxpaint/stamps/"
  chmod -R a+rX,g-w,o-w "$PREFIX/share/tuxpaint/stamps"
  echo "Stamps installed in $PREFIX/share/tuxpaint/stamps"
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
  stamps)
    do_stamps "${2:-}"
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

#!/bin/bash
# Build Tux Paint where its build dependencies aren't installed, and can't
# be (no root): their Debian/Ubuntu packages are downloaded, not installed,
# and unpacked in a folder of their own.
#
# Usage: devtools/sysroot/sysroot.sh {fetch|make|install|run|env} [arguments...]
#
#   fetch    download the -dev packages (and what they need that the system
#            lacks) into $SYSROOT, unpack them, and make their pkg-config
#            files point there
#   make     run make in the repository with that folder (arguments are
#            passed to make, e.g. "-j4", "PREFIX=...")
#   install  build and install under PREFIX as "dev.sh install" does (menu
#            launcher too), with a copy of the libraries the system lacks in
#            PREFIX/lib/tuxpaint/sysroot-libs: the installed Tux Paint
#            doesn't need this folder any more
#   run      run a built tuxpaint (first argument) with the libraries of
#            that folder (the rest are passed to it)
#   env      print the variables "make" uses, to paste into a shell
#
# Environment:
#   SYSROOT  where (default: ~/.cache/tuxpaint-sysroot)
#   PREFIX   for "make" and "install" (default: ~/.local, as dev.sh)
#
# The binary looks for libraries in PREFIX/lib/tuxpaint/sysroot-libs, then
# in this folder, also for its libraries' own dependencies (e.g. libmikmod:
# an old-style DT_RPATH, which unlike RUNPATH applies to them too).
# When the -dev packages are installed system-wide, use dev.sh instead.

set -e

SYSROOT="${SYSROOT:-$HOME/.cache/tuxpaint-sysroot}"
ROOT="$SYSROOT/root"
LIB="$ROOT/usr/lib/$(gcc -dumpmachine 2>/dev/null || echo x86_64-linux-gnu)"
REPO="$(cd "$(dirname "$(realpath "$0")")/../.." && pwd)"

PACKAGES=(libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev
  libsdl-ttf2.0-dev libsdl-pango-dev librsvg2-dev libcairo2-dev
  libfribidi-dev libpaper-dev libpng-dev zlib1g-dev gperf)

do_fetch() {
  local list debs n=0 f t cand sys

  mkdir -p "$SYSROOT/debs"
  # What apt would install (as a simulation: no root needed), plus the
  # packages already on the system whose pkg-config files are needed
  list=$(apt-get install -s --no-install-recommends "${PACKAGES[@]}" 2>/dev/null |
    awk '/^Inst / { print $2 }' | grep -v '^native-architecture$' || true)
  list="$list zlib1g-dev shared-mime-info"
  (cd "$SYSROOT/debs" && apt-get download $list)

  rm -rf "$ROOT"
  mkdir -p "$ROOT"
  for f in "$SYSROOT"/debs/*.deb; do
    dpkg-deb -x "$f" "$ROOT"
  done

  # Library links whose target is installed on the system, not here
  while read -r f; do
    t=$(readlink "$f")
    case "$t" in /*) cand="$ROOT$t" ;; *) cand="$(dirname "$f")/$t" ;; esac
    [ -e "$cand" ] && continue
    sys=$(ls "/usr/lib/$(basename "$LIB")/$(basename "$t")" 2>/dev/null || true)
    if [ -n "$sys" ]; then
      ln -sf "$sys" "$f"
      n=$((n + 1))
    fi
  done < <(find "$ROOT/usr/lib" -xtype l)
  echo "$n links to the system's libraries"

  # pkg-config files with absolute paths into the folder (not
  # PKG_CONFIG_SYSROOT_DIR: the system's own .pc files must still work)
  for f in "$LIB"/pkgconfig/*.pc "$ROOT"/usr/share/pkgconfig/*.pc; do
    [ -e "$f" ] || continue
    sed -i -e "s|^\([a-z_]*\)=/usr|\1=$ROOT/usr|" \
      -e "s| -I/usr/| -I$ROOT/usr/|g" -e "s| -L/usr/| -L$ROOT/usr/|g" "$f"
  done

  echo "Ready: $ROOT"
}

make_vars() {
  local prefix="${PREFIX:-$HOME/.local}"

  RUNTIME_LIBS="$prefix/lib/tuxpaint/sysroot-libs"
  MAKE_ARGS=(
    PREFIX="$prefix"
    GPERF="$ROOT/usr/bin/gperf"
    CPPFLAGS="-I$ROOT/usr/include"
    LDFLAGS="-L$LIB -Wl,-rpath-link,$LIB -Wl,--disable-new-dtags -Wl,-rpath,$RUNTIME_LIBS:$LIB"
  )
  export PKG_CONFIG_PATH="$LIB/pkgconfig:$ROOT/usr/share/pkgconfig"
}

# As dev.sh's do_install(), then the libraries tuxpaint takes from this
# folder (whatever ldd finds here) copied next to the installation
do_install() {
  local prefix="${PREFIX:-$HOME/.local}" stamp="$REPO/obj/.build-prefix" lib n=0

  make_vars
  cd "$REPO"
  # (Install paths are compiled in: a new PREFIX needs a new build)
  if [ "$(cat "$stamp" 2>/dev/null)" != "$prefix" ]; then
    echo "PREFIX is now $prefix: rebuilding from scratch"
    make clean > /dev/null
  fi
  make -j"$(nproc)" "${MAKE_ARGS[@]}"
  echo "$prefix" > "$stamp"
  make "${MAKE_ARGS[@]}" COMPLETIONDIR="$prefix/share/bash-completion/completions" \
    GNOME_PREFIX="$prefix" KDE_ICON_PREFIX="$prefix/share/icons" install
  sed -i -e "s|^Exec=tuxpaint\$|Exec=$prefix/bin/tuxpaint|" \
    -e "s|^Exec=tuxpaint |Exec=$prefix/bin/tuxpaint |" \
    "$prefix/share/applications/tuxpaint.desktop"

  # (Found here, or in the copies of an earlier install: copied again
  # from here, in case this folder was fetched anew)
  mkdir -p "$RUNTIME_LIBS"
  while read -r lib; do
    [ -e "$LIB/$lib" ] || continue
    # (A new file, then renamed: a running Tux Paint keeps the old one)
    cp -L "$LIB/$lib" "$RUNTIME_LIBS/.$lib.new"
    mv -f "$RUNTIME_LIBS/.$lib.new" "$RUNTIME_LIBS/$lib"
    n=$((n + 1))
  done < <(LD_LIBRARY_PATH="$LIB" ldd "$prefix/bin/tuxpaint" |
    awk -v root="$ROOT" -v copies="$RUNTIME_LIBS" \
      'index($3, root) == 1 || index($3, copies) == 1 { print $1 }')
  echo "$n libraries copied to $RUNTIME_LIBS"

  if LD_LIBRARY_PATH= ldd "$prefix/bin/tuxpaint" | grep -q "not found"; then
    echo "Some libraries are still missing:" >&2
    LD_LIBRARY_PATH= ldd "$prefix/bin/tuxpaint" | grep "not found" >&2
    exit 1
  fi
}

case "$1" in
  fetch)
    do_fetch
    ;;
  make)
    shift
    [ -d "$ROOT" ] || { echo "No $ROOT: run \"$0 fetch\" first" >&2; exit 1; }
    make_vars
    cd "$REPO"
    exec make "${MAKE_ARGS[@]}" "$@"
    ;;
  install)
    [ -d "$ROOT" ] || { echo "No $ROOT: run \"$0 fetch\" first" >&2; exit 1; }
    do_install
    ;;
  run)
    shift
    [ -n "$1" ] || { echo "Usage: $0 run TUXPAINT [ARGS...]" >&2; exit 1; }
    LD_LIBRARY_PATH="$LIB${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" exec "$@"
    ;;
  env)
    make_vars
    echo "export PKG_CONFIG_PATH=\"$PKG_CONFIG_PATH\""
    printf 'make'
    printf ' %q' "${MAKE_ARGS[@]}"
    echo
    ;;
  *)
    sed -n '2,29p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
    ;;
esac

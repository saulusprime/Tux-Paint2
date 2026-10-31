/* LD_PRELOAD: make dlclose() do nothing (to tell plugin memory apart in leak reports) */
int dlclose(void *handle) { (void) handle; return 0; }

cmd="startfluxbox"
if type ck-launch-session >/dev/null 2>&1; then
  cmd="ck-launch-session $cmd"
fi
exec $cmd
#exec startkde
